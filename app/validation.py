from .models import WTMOutput


class WTMValidationEngine:
    """
    Motor de validación de WTM.

    Su función es comprobar si la información recopilada
    por WTM presenta las condiciones mínimas para continuar.

    No realiza diagnóstico de BINAH.
    No determina soluciones.
    """

    def validate(
        self,
        output: WTMOutput,
    ) -> WTMOutput:
        """
        Valida el estado actual del caso WTM.
        """

        blocking_reasons = []

        if not output.business.strip():
            blocking_reasons.append(
                "El negocio no está identificado."
            )

        if not output.context:
            blocking_reasons.append(
                "Falta información sobre el contexto."
            )

        if not output.objective:
            blocking_reasons.append(
                "Falta información sobre el objetivo."
            )

        if not output.situation:
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