from app.models import (
    WTMConversationInput,
    WTMEvidence,
    WTMFormInput,
    WTMOutput,
)
from app.questions import WTMQuestionManager


class WTMEngine:
    """
    Motor principal de WTM.

    Responsabilidades:
    - Crear el estado inicial desde el formulario.
    - Registrar mensajes de conversación como evidencia.
    - Mantener el estado de clarificación.
    - Actualizar las preguntas pendientes.

    WTM no diagnostica ni resuelve el caso.
    Su función es preparar información estructurada para BINAH.
    """

    def __init__(self):
        self.question_manager = WTMQuestionManager()

    def create_initial_output(
        self,
        form_input: WTMFormInput,
    ) -> WTMOutput:
        """
        Crea el WTMOutput inicial a partir del formulario.
        """

        output = WTMOutput(
            business=form_input.business,
            context=form_input.context,
            objective=form_input.objective,
            situation=form_input.description,
        )

        for index, evidence in enumerate(form_input.evidence, start=1):
            evidence_id = self._next_id("E", index)

            output.evidence.append(
                WTMEvidence(
                    id=evidence_id,
                    content=evidence,
                    type="USER_STATEMENT",
                    source="form",
                    status="PROVISIONAL",
                )
            )

            output.traceability.source_evidence_ids.append(evidence_id)

        self._update_questions(output)

        return output

    def process_message(
        self,
        output: WTMOutput,
        conversation: WTMConversationInput,
    ) -> WTMOutput:
        """
        Registra un mensaje de conversación como evidencia.

        La recepción de un nuevo mensaje mantiene el caso
        en estado CLARIFYING. La actualización posterior de
        preguntas y la validación determinan el estado final.
        """

        evidence_id = self._next_id(
            "E",
            len(output.evidence) + 1,
        )

        source = "conversation"

        if conversation.conversation_id:
            source = f"conversation:{conversation.conversation_id}"

        output.evidence.append(
            WTMEvidence(
                id=evidence_id,
                content=conversation.message,
                type="USER_STATEMENT",
                source=source,
                status="PROVISIONAL",
            )
        )

        output.traceability.source_evidence_ids.append(evidence_id)

        output.status = "CLARIFYING"

        return output

    def _update_questions(
        self,
        output: WTMOutput,
    ) -> WTMOutput:
        """
        Actualiza las preguntas básicas pendientes.

        Si faltan elementos fundamentales, el caso permanece
        en CLARIFYING.

        Si ya están presentes, pasa a VERIFYING.
        La validación posterior determina READY_FOR_BINAH.
        """

        questions = self.question_manager.build_basic_questions(
            context=bool(output.context),
            objective=bool(output.objective),
            situation=bool(output.situation),
        )

        output.questions = questions

        if questions:
            output.status = "CLARIFYING"
            output.ready_for_binah = False
            output.blocking_reasons = [
                question.text
                for question in questions
                if question.required
            ]
        else:
            output.status = "VERIFYING"
            output.ready_for_binah = False
            output.blocking_reasons = [
                "El caso requiere verificación antes de ser enviado a BINAH."
            ]

        return output

    @staticmethod
    def _next_id(
        prefix: str,
        number: int,
    ) -> str:
        """
        Genera identificadores secuenciales.
        """

        return f"{prefix}_{number:03d}"