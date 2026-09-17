from app.models import (
    WTMContradiction,
    WTMEvidence,
    WTMHypothesis,
    WTMObservation,
    WTMQuestion,
    WTMUnknown,
    WTMOutput,
)
from app.traceability import WTMTraceabilityEngine


def test_rebuild_traceability():
    engine = WTMTraceabilityEngine()

    output = WTMOutput(
        business="Empresa de prueba",
    )

    output.evidence.append(
        WTMEvidence(
            id="E_001",
            content="Dato de prueba",
            type="USER_STATEMENT",
        )
    )

    output.observations.append(
        WTMObservation(
            id="O_001",
            statement="Observación de prueba",
        )
    )

    output.hypotheses.append(
        WTMHypothesis(
            id="H_001",
            statement="Hipótesis de prueba",
        )
    )

    output.unknowns.append(
        WTMUnknown(
            id="U_001",
            statement="Información desconocida",
        )
    )

    output.contradictions.append(
        WTMContradiction(
            id="C_001",
            statement_a="A",
            statement_b="B",
        )
    )

    output.questions.append(
        WTMQuestion(
            id="Q_001",
            text="Pregunta de prueba",
            type="CLARIFICATION",
        )
    )

    updated = engine.rebuild(output)

    assert updated.traceability.source_evidence_ids == [
        "E_001"
    ]

    assert updated.traceability.observation_ids == [
        "O_001"
    ]

    assert updated.traceability.hypothesis_ids == [
        "H_001"
    ]

    assert updated.traceability.unknown_ids == [
        "U_001"
    ]

    assert updated.traceability.contradiction_ids == [
        "C_001"
    ]

    assert updated.traceability.question_ids == [
        "Q_001"
    ]