from app.chat import WTMChat
from app.models import WTMFormInput


def test_chat_start_creates_initial_state():
    chat = WTMChat()

    form = WTMFormInput(
        business="Empresa de prueba",
    )

    output = chat.start(form)

    assert output.business == "Empresa de prueba"
    assert output.ready_for_binah is False
    assert output.status == "INSUFFICIENT_INFORMATION"


def test_chat_returns_next_question():
    chat = WTMChat()

    form = WTMFormInput(
        business="Empresa de prueba",
    )

    output = chat.start(form)

    question = chat.get_next_question(output)

    assert question is not None
    assert question == (
        "¿En qué contexto ocurre la situación que quieres analizar?"
    )


def test_chat_processes_conversation_until_ready():
    chat = WTMChat()

    form = WTMFormInput(
        business="Empresa de prueba",
    )

    output = chat.start(form)

    output = chat.receive_message(
        output,
        "contexto: el equipo recibe muchas solicitudes durante el día.",
        conversation_id="conv_001",
        turn=1,
    )

    output = chat.receive_message(
        output,
        "objetivo: reducir el tiempo de respuesta a los clientes.",
        conversation_id="conv_001",
        turn=2,
    )

    output = chat.receive_message(
        output,
        "situación: los clientes esperan demasiado para recibir una respuesta.",
        conversation_id="conv_001",
        turn=3,
    )

    assert output.context == (
        "el equipo recibe muchas solicitudes durante el día."
    )

    assert output.objective == (
        "reducir el tiempo de respuesta a los clientes."
    )

    assert output.situation == (
        "los clientes esperan demasiado para recibir una respuesta."
    )

    assert chat.is_ready_for_binah(output) is True
    assert output.status == "READY_FOR_BINAH"
    assert output.blocking_reasons == []
    assert chat.get_next_question(output) is None


def test_chat_preserves_conversation_evidence():
    chat = WTMChat()

    form = WTMFormInput(
        business="Empresa de prueba",
    )

    output = chat.start(form)

    output = chat.receive_message(
        output,
        "Los clientes esperan demasiado.",
        conversation_id="conv_001",
        turn=1,
    )

    assert len(output.evidence) == 1
    assert output.evidence[0].content == (
        "Los clientes esperan demasiado."
    )
    assert output.evidence[0].source == "conversation:conv_001"
    assert output.ready_for_binah is False