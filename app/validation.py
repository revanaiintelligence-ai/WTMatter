from .models import WTMOutput

class WTMValidationEngine:
"""
Motor de validación de WTM.

Comprueba si el caso tiene la información estructural
mínima para continuar hacia BINAH.

No realiza diagnóstico empresarial.
No determina soluciones.
No convierte información provisional en verificada.

La suficiencia analítica del caso corresponde a la
evaluación posterior de BINAH y a la inteligencia
que utilice el sistema.
"""

def validate(
    self,
    output: WTMOutput,
) -> WTMOutput:
    """
    Valida la estructura y los bloqueos explícitos del caso.

    La presencia de campos no demuestra que su contenido
    sea verdadero ni que el análisis esté completo.
    READY_FOR_BINAH significa únicamente que WTM no detecta
    bloqueos estructurales definidos en este contrato.
    """

    blocking_reasons = []

    business = (output.business or "").strip()
    context = (output.context or "").strip()
    objective = (output.objective or "").strip()
    situation = (output.situation or "").strip()

    if not business or business.casefold() == "por determinar":
        blocking_reasons.append(
            "El negocio o entidad todavía no está identificado."
        )

    if not context:
        blocking_reasons.append(
            "Falta información sobre el contexto."
        )

    if not objective:
        blocking_reasons.append(
            "Falta información sobre el objetivo."
        )

    if not situation:
        blocking_reasons.append(
            "Falta información sobre la situación actual."
        )

    unresolved_contradictions = [
        contradiction
        for contradiction in output.contradictions
        if not contradiction.resolved
    ]

    if unresolved_contradictions:
        blocking_reasons.append(
            "Existen contradicciones no resueltas."
        )

    critical_unknowns = [
        unknown
        for unknown in output.unknowns
        if unknown.importance == "CRITICAL"
        and unknown.blocks_binah
    ]

    if critical_unknowns:
        blocking_reasons.append(
            "Existe información crítica faltante que bloquea el avance hacia BINAH."
        )

    output.blocking_reasons = blocking_reasons

    if blocking_reasons:
        output.status = "INSUFFICIENT_INFORMATION"
        output.ready_for_binah = False
    else:
        output.status = "READY_FOR_BINAH"
        output.ready_for_binah = True

    return output