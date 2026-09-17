from typing import List, Optional

from .models import (
    WTMConversationInput,
    WTMFormInput,
    WTMOutput,
    WTMQuestion,
    WTMQuestionType,
    WTMTraceability,
)


class WTMEngine:
    """
    Motor principal de WTM.

    WTM tiene como función:
    1. Recibir información inicial.
    2. Organizar la información disponible.
    3. Detectar información faltante.
    4. Generar preguntas de aclaración.
    5. Preparar un resultado estructurado para BINAH.

    WTM no realiza el diagnóstico final de BINAH.
    """

    def create_initial_output(
        self,
        form_input: WTMFormInput,
    ) -> WTMOutput:
        """
        Crea el estado inicial de WTM a partir del formulario.
        """

        situation = (
            form_input.description
            or form_input.context
            or None
        )

        output = WTMOutput(
            methodology="WTM",
            version="0.1",
            status="COLLECTING",
            business=form_input.business,
            context=form_input.context,
            objective=form_input.objective,
            situation=situation,
        )

        return self._update_questions(output)

    def process_message(
        self,
        output: WTMOutput,
        conversation_input: WTMConversationInput,
    ) -> WTMOutput:
        """
        Incorpora un mensaje de conversación al proceso WTM.

        En esta primera versión el motor no interpreta semánticamente
        el mensaje mediante un modelo de IA. Conserva el mensaje como
        evidencia y actualiza el estado del proceso.
        """

        message = conversation_input.message.strip()

        if not message:
            return output

        evidence_id = self._next_id(
            "E",
            len(output.evidence) + 1,
        )

        output.evidence.append(
            {
                "id": evidence_id,
                "content": message,
                "type": "USER_STATEMENT",
                "source": (
                    f"conversation:"
                    f"{conversation_input.conversation_id}"
                    if conversation_input.conversation_id
                    else "conversation"
                ),
                "status": "PROVISIONAL",
                "supports": [],
                "contradicts": [],
            }
        )

        output.traceability.source_evidence_ids.append(
            evidence_id
        )

        output.status = "CLARIFYING"

        return self._update_questions(output)

    def _update_questions(
        self,
        output: WTMOutput,
    ) -> WTMOutput:
        """
        Determina las preguntas básicas que todavía pueden bloquear
        la preparación del caso para BINAH.
        """

        questions: List[WTMQuestion] = []

        if not output.context:
            questions.append(
                self._question(
                    "context",
                    "¿En qué contexto ocurre la situación que quieres analizar?",
                    "MISSING_INFORMATION",
                    "context",
                )
            )

        if not output.objective:
            questions.append(
                self._question(
                    "objective",
                    "¿Qué quieres lograr o cambiar con respecto a esta situación?",
                    "OBJECTIVE",
                    "objective",
                )
            )

        if not output.situation:
            questions.append(
                self._question(
                    "situation",
                    "¿Qué está ocurriendo actualmente y por qué consideras que necesita atención?",
                    "CLARIFICATION",
                    "situation",
                )
            )

        output.questions = questions

        output.traceability.question_ids = [
            question.id for question in questions
        ]

        if questions:
            output.status = "CLARIFYING"
            output.ready_for_binah = False
            output.blocking_reasons = [
                question.text
                for question in questions
                if question.required
            ]
        else:
            output.status = "READY_FOR_BINAH"
            output.ready_for_binah = True
            output.blocking_reasons = []

        return output

    def _question(
        self,
        question_id: str,
        text: str,
        question_type: str,
        target: str,
    ) -> WTMQuestion:
        """
        Construye una pregunta WTM normalizada.
        """

        return WTMQuestion(
            id=f"Q_{question_id}",
            text=text,
            type=question_type,
            target=target,
            required=True,
            answered=False,
        )

    @staticmethod
    def _next_id(
        prefix: str,
        number: int,
    ) -> str:
        """
        Genera identificadores simples y trazables.
        """

        return f"{prefix}_{number:03d}"