from .models import WTMOutput


class WTMTraceabilityEngine:
    """
    Motor de trazabilidad de WTM.

    Su función es mantener y reconstruir las relaciones
    entre la información recopilada durante el proceso WTM.

    No realiza diagnóstico de BINAH.
    No determina soluciones.
    """

    def rebuild(
        self,
        output: WTMOutput,
    ) -> WTMOutput:
        """
        Reconstruye la trazabilidad del estado actual de WTM.
        """

        output.traceability.source_evidence_ids = [
            evidence.id
            for evidence in output.evidence
        ]

        output.traceability.observation_ids = [
            observation.id
            for observation in output.observations
        ]

        output.traceability.hypothesis_ids = [
            hypothesis.id
            for hypothesis in output.hypotheses
        ]

        output.traceability.unknown_ids = [
            unknown.id
            for unknown in output.unknowns
        ]

        output.traceability.contradiction_ids = [
            contradiction.id
            for contradiction in output.contradictions
        ]

        output.traceability.question_ids = [
            question.id
            for question in output.questions
        ]

        return output