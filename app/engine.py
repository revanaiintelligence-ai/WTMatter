"""
WTMatter Conversation Engine.

Este módulo contiene el motor central de conversación de WTM.

Principios:
- WTM organiza y estructura la información.
- La conversación no está limitada por un cuestionario rígido.
- Las preguntas pendientes son información auxiliar, no una secuencia obligatoria.
- La inteligencia que utiliza WTM puede decidir qué preguntar, cuándo profundizar,
  cuándo explorar hipótesis y cuándo considerar suficiente el caso.
- WTM separa evidencia, observaciones, hipótesis, desconocidos y contradicciones.
- La decisión de utilizar IA, automatización u otra solución corresponde a BINAH
  y a las capas posteriores del sistema.
"""

from __future__ import annotations

from typing import Optional

from .models import (
    WTMConversationInput,
    WTMEvidence,
    WTMEvidenceType,
    WTMFormInput,
    WTMOutput,
)
from .questions import WTMQuestionManager


class WTMEngine:
    """
    Motor principal de WTMatter.

    El engine mantiene la estructura del caso y procesa la información
    recibida durante la conversación.

    No intenta sustituir a la inteligencia conversacional externa.
    """

    def __init__(self) -> None:
        self.question_manager = WTMQuestionManager()

    def create_initial_output(
        self,
        form_input: WTMFormInput,
    ) -> WTMOutput:
        """
        Crea el estado inicial de WTM a partir de una entrada inicial.

        Se conserva la compatibilidad con el flujo anterior basado en
        formulario.
        """

        output = WTMOutput(
            business=form_input.business,
            context=form_input.context,
            objective=form_input.objective,
            situation=form_input.description,
            status="OBSERVING",
            ready_for_binah=False,
        )

        # La información proporcionada inicialmente por el usuario
        # constituye evidencia declarada, pero todavía provisional.
        if form_input.description:
            output.evidence.append(
                WTMEvidence(
                    type=WTMEvidenceType.USER_STATEMENT,
                    content=form_input.description,
                    source="form",
                    status="PROVISIONAL",
                )
            )

        # Conservar evidencia adicional enviada en el formulario.
        if form_input.evidence:
            output.evidence.extend(form_input.evidence)

        self._update_questions(output)

        return output

    def process_message(
        self,
        output: WTMOutput,
        conversation_input: WTMConversationInput,
    ) -> WTMOutput:
        """
        Procesa un nuevo mensaje de conversación.

        El mensaje se incorpora como evidencia declarada por el usuario.
        La interpretación estructurada puede realizarse posteriormente
        por la capa de extracción o por la inteligencia que utilice WTM.
        """

        message = conversation_input.message.strip()

        if not message:
            return output

        conversation_id = conversation_input.conversation_id

        if conversation_id:
            source = f"conversation:{conversation_id}"
        else:
            source = "conversation"

        output.evidence.append(
            WTMEvidence(
                type=WTMEvidenceType.USER_STATEMENT,
                content=message,
                source=source,
                status="PROVISIONAL",
            )
        )

        # La conversación continúa mientras exista nueva información
        # que pueda ser estructurada o verificada.
        output.status = "CLARIFYING"

        # No se fuerza automáticamente ready_for_binah=True aquí.
        # La suficiencia del caso depende de la información estructurada,
        # la validación y la inteligencia conversacional.
        output.ready_for_binah = False

        self._update_questions(output)

        return output

    def _update_questions(
        self,
        output: WTMOutput,
    ) -> WTMOutput:
        """
        Actualiza las preguntas pendientes de WTM.

        Las preguntas son una representación estructural de información
        que podría faltar. No constituyen un cuestionario obligatorio.

        La IA que utilice WTM puede decidir libremente:

        - qué preguntar,
        - cuándo preguntar,
        - cuándo profundizar,
        - cuándo explorar una hipótesis,
        - cuándo contrastar una contradicción,
        - cuándo proponer una posible solución para consideración humana,
        - y cuándo considerar suficiente la información.

        Por tanto, las preguntas generadas aquí NO deben interpretarse
        como una secuencia obligatoria de conversación.
        """

        pending_questions = self.question_manager.build_basic_questions(
            context=bool(output.context),
            objective=bool(output.objective),
            situation=bool(output.situation),
        )

        output.questions = pending_questions

        # Las preguntas pendientes son información auxiliar.
        #
        # No se utilizan para imponer un bloqueo artificial de la
        # conversación. El sistema puede continuar conversando,
        # explorar hipótesis o profundizar aunque existan preguntas.
        #
        # La decisión real de suficiencia debe provenir de la combinación
        # entre información estructurada, evidencia, validación y la
        # inteligencia que esté utilizando WTM.

        if pending_questions:
            output.status = "CLARIFYING"
        else:
            output.status = "VERIFYING"

        # No convertir automáticamente las preguntas en bloqueos.
        output.blocking_reasons = []

        return output

    def get_pending_questions(
        self,
        output: WTMOutput,
    ) -> list:
        """
        Devuelve las preguntas actualmente pendientes.

        Este método es auxiliar para interfaces, MCP u otras capas
        externas. No significa que todas deban formularse al usuario.
        """

        return list(output.questions)

    def has_pending_questions(
        self,
        output: WTMOutput,
    ) -> bool:
        """
        Indica si existen preguntas estructurales pendientes.

        No implica que WTM esté bloqueado.
        """

        return bool(output.questions)

    def mark_ready_for_binah(
        self,
        output: WTMOutput,
    ) -> WTMOutput:
        """
        Marca explícitamente un caso como preparado para BINAH.

        Este método existe para que una capa superior, después de realizar
        la evaluación correspondiente, pueda efectuar el handoff.

        El engine no decide por sí mismo que un caso está listo únicamente
        porque existan o no preguntas.
        """

        output.status = "READY_FOR_BINAH"
        output.ready_for_binah = True
        output.blocking_reasons = []

        return output

    def mark_not_ready_for_binah(
        self,
        output: WTMOutput,
        reasons: Optional[list[str]] = None,
    ) -> WTMOutput:
        """
        Marca explícitamente que el caso todavía no está preparado
        para BINAH.

        Las razones son informativas y deben representar impedimentos
        reales, no simplemente preguntas pendientes.
        """

        output.ready_for_binah = False

        if output.status == "READY_FOR_BINAH":
            output.status = "VERIFYING"

        output.blocking_reasons = list(reasons or [])

        return output