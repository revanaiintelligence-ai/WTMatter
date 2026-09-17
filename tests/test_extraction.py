from app.extraction import WTMExtractionEngine
from app.models import WTMConversationInput, WTMOutput


def test_extract_context():
    engine = WTMExtractionEngine()

    output = WTMOutput(
        business="Empresa de prueba",
    )

    conversation = WTMConversationInput(
        message="contexto: tenemos retrasos en la atención al cliente."
    )

    updated = engine.extract(
        output,
        conversation,
    )

    assert updated.context == (
        "tenemos retrasos en la atención al cliente."
    )


def test_extract_objective():
    engine = WTMExtractionEngine()

    output = WTMOutput(
        business="Empresa de prueba",
    )

    conversation = WTMConversationInput(
        message="objetivo: reducir el tiempo de respuesta."
    )

    updated = engine.extract(
        output,
        conversation,
    )

    assert updated.objective == (
        "reducir el tiempo de respuesta."
    )


def test_extract_situation():
    engine = WTMExtractionEngine()

    output = WTMOutput(
        business="Empresa de prueba",
    )

    conversation = WTMConversationInput(
        message="situación: los clientes esperan demasiado."
    )

    updated = engine.extract(
        output,
        conversation,
    )

    assert updated.situation == (
        "los clientes esperan demasiado."
    )


def test_extract_does_not_invent_information():
    engine = WTMExtractionEngine()

    output = WTMOutput(
        business="Empresa de prueba",
    )

    conversation = WTMConversationInput(
        message="Tenemos algunos problemas con el proceso."
    )

    updated = engine.extract(
        output,
        conversation,
    )

    assert updated.context is None
    assert updated.objective is None
    assert updated.situation is None