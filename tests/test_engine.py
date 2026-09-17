from app.engine import WTMEngine
from app.models import WTMConversationInput, WTMFormInput


def test_create_initial_output():
    engine = WTMEngine()

    form = WTMFormInput(
        business="Empresa de prueba",
        context="Contexto de prueba",
        objective="Objetivo de prueba",
        description="Situación de prueba",
        evidence=["Dato aportado por el usuario"],
    )

    output = engine.create_initial_output(form)

    assert output.business == "Empresa de prueba"
    assert output.context == "Contexto de prueba"
    assert output.objective == "Objetivo de prueba"
    assert output.situation == "Situación de prueba"

    assert len(output.evidence) == 1
    assert output.evidence[0].id == "E_001"
    assert output.evidence[0].content == "Dato aportado por el usuario"

    assert output.status == "VERIFYING"
    assert output.ready_for_binah is False


def test_create_initial_output_generates_questions():
    engine = WTMEngine()

    form = WTMFormInput(
        business="Empresa de prueba",
    )

    output = engine.create_initial_output(form)

    assert output.status == "CLARIFYING"
    assert output.ready_for_binah is False
    assert len(output.questions) == 3

    question_ids = [
        question.id
        for question in output.questions
    ]

    assert "Q_context" in question_ids
    assert "Q_objective" in question_ids
    assert "Q_situation" in question_ids


def test_process_message_adds_evidence():
    engine = WTMEngine()

    form = WTMFormInput(
        business="Empresa de prueba",
        context="Contexto",
        objective="Objetivo",
        description="Situación",
    )

    output = engine.create_initial_output(form)

    conversation = WTMConversationInput(
        message="El problema ocurre principalmente durante la mañana.",
        conversation_id="conv_001",
        turn=1,
    )

    updated = engine.process_message(
        output,
        conversation,
    )

    assert len(updated.evidence) == 1
    assert updated.evidence[0].id == "E_001"
    assert updated.evidence[0].content == (
        "El problema ocurre principalmente durante la mañana."
    )

    assert updated.evidence[0].source == "conversation:conv_001"
    assert updated.status == "CLARIFYING"
    assert updated.ready_for_binah is False