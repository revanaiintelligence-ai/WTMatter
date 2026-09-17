from app.models import WTMContradiction, WTMOutput
from app.validation import WTMValidationEngine


def test_validation_blocks_incomplete_output():
    engine = WTMValidationEngine()

    output = WTMOutput(
        business="Empresa de prueba",
    )

    updated = engine.validate(output)

    assert updated.ready_for_binah is False
    assert updated.status == "INSUFFICIENT_INFORMATION"

    assert "Falta información sobre el contexto." in (
        updated.blocking_reasons
    )

    assert "Falta información sobre el objetivo." in (
        updated.blocking_reasons
    )

    assert "Falta información sobre la situación actual." in (
        updated.blocking_reasons
    )


def test_validation_allows_complete_output():
    engine = WTMValidationEngine()

    output = WTMOutput(
        business="Empresa de prueba",
        context="Contexto de prueba",
        objective="Objetivo de prueba",
        situation="Situación de prueba",
    )

    updated = engine.validate(output)

    assert updated.ready_for_binah is True
    assert updated.status == "READY_FOR_BINAH"
    assert updated.blocking_reasons == []


def test_validation_blocks_unresolved_contradiction():
    engine = WTMValidationEngine()

    output = WTMOutput(
        business="Empresa de prueba",
        context="Contexto de prueba",
        objective="Objetivo de prueba",
        situation="Situación de prueba",
    )

    output.contradictions.append(
        WTMContradiction(
            id="C_001",
            statement_a="La respuesta es rápida.",
            statement_b="La respuesta es lenta.",
            source_ids=[],
            resolved=False,
        )
    )

    updated = engine.validate(output)

    assert updated.ready_for_binah is False
    assert updated.status == "INSUFFICIENT_INFORMATION"
    assert (
        "Existen contradicciones no resueltas."
        in updated.blocking_reasons
    )