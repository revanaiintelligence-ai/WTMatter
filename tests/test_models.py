from app.models import (
    WTMFormInput,
    WTMOutput,
)


def test_wtm_form_input():
    data = WTMFormInput(
        business="Empresa de prueba",
        context="Contexto de prueba",
        objective="Objetivo de prueba",
        description="Situación de prueba",
    )

    assert data.business == "Empresa de prueba"
    assert data.context == "Contexto de prueba"
    assert data.objective == "Objetivo de prueba"
    assert data.description == "Situación de prueba"


def test_wtm_output():
    output = WTMOutput(
        business="Empresa de prueba",
    )

    assert output.methodology == "WTM"
    assert output.version == "0.1"
    assert output.business == "Empresa de prueba"
    assert output.ready_for_binah is False