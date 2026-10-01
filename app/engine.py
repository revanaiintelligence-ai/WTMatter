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
- Crear el estado inicial.
- Registrar mensajes conversacionales como evidencia.
- Mantener la trazabilidad de la conversación.
- Actualizar el estado de clarificación.
- Coordinar las preguntas pendientes.

WTM no realiza el diagnóstico empresarial final.
Su función es preparar y estructurar información para BINAH.

La interpretación avanzada del contenido puede ser realizada
por la IA que utilice el sistema. Este motor no impone una
lógica rígida de diagnóstico.
"""

def __init__(self):
    self.question_manager = WTMQuestionManager()

def create_initial_output(
    self,
    form_input: WTMFormInput,
) -> WTMOutput:
    """
    Crea el estado inicial de WTM.

    Se mantiene compatible con el flujo basado en formulario.
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

        output.traceability.source_evidence_ids.append(
            evidence_id
        )

    self._update_questions(output)

    return output

def process_message(
    self,
    output: WTMOutput,
    conversation: WTMConversationInput,
) -> WTMOutput:
    """
    Incorpora un nuevo mensaje a la conversación WTM.

    El mensaje se conserva como evidencia de usuario.
    No se fuerza una interpretación ni un diagnóstico.

    La estructuración posterior puede utilizar la información
    extraída por WTM y, cuando exista, la inteligencia de la
    IA que consuma este estado.
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

    output.traceability.source_evidence_ids.append(
        evidence_id
    )

    output.status = "CLARIFYING"
    output.ready_for_binah = False

    return output

def _update_questions(
    self,
    output: WTMOutput,
) -> WTMOutput:
    """
    Actualiza las preguntas pendientes según el estado actual.

    Las preguntas sirven para identificar información que falta.
    No representan un diagnóstico.

    Si existen elementos pendientes, WTM continúa aclarando.
    Si la información básica está presente, pasa a verificación.
    La validación posterior determina si puede continuar hacia BINAH.
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