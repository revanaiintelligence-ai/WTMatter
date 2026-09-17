from app.engine import WTMEngine
from app.extraction import WTMExtractionEngine
from app.traceability import WTMTraceabilityEngine
from app.validation import WTMValidationEngine
from app.models import (
    WTMConversationInput,
    WTMFormInput,
)


def test_wtm_full_flow_to_binah():
    engine = WTMEngine()
    extraction = WTMExtractionEngine()
    validation = WTMValidationEngine()
    traceability = WTMTraceabilityEngine()

    form = WTMFormInput(
        business="Empresa de prueba",
        evidence=[
            "Los clientes esperan demasiado.",
        ],
    )

    output = engine.create_initial_output(form)

    assert output.status == "CLARIFYING"
    assert output.ready_for_binah is False

    messages = [
        WTMConversationInput(
            message=(
                "contexto: el equipo recibe muchas solicitudes "
                "durante el día."
            ),
            conversation_id="conv_001",
            turn=1,
        ),
        WTMConversationInput(
            message=(
                "objetivo: reducir el tiempo de respuesta "
                "a los clientes."
            ),
            conversation_id="conv_001",
            turn=2,
        ),
        WTMConversationInput(
            message=(
                "situación: los clientes esperan demasiado "
                "para recibir una respuesta."
            ),
            conversation_id="conv_001",
            turn=3,
        ),
    ]

    for message in messages:
        output = engine.process_message(
            output,
            message,
        )

        output = extraction.extract(
            output,
            message,
        )

    output = traceability.rebuild(output)
    output = validation.validate(output)

    assert output.context == (
        "el equipo recibe muchas solicitudes "
        "durante el día."
    )

    assert output.objective == (
        "reducir el tiempo de respuesta "
        "a los clientes."
    )

    assert output.situation == (
        "los clientes esperan demasiado "
        "para recibir una respuesta."
    )

    assert output.ready_for_binah is True
    assert output.status == "READY_FOR_BINAH"

    assert output.blocking_reasons == []

    assert output.traceability.source_evidence_ids == [
        "E_001",
        "E_002",
        "E_003",
        "E_004",
    ]

    assert output.traceability.question_ids == []