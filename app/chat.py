from .engine import WTMEngine
from .extraction import WTMExtractionEngine
from .models import WTMConversationInput, WTMFormInput, WTMOutput
from .validation import WTMValidationEngine


class WTMChat:
    """
    Capa conversacional de WTM.

    Conecta la conversación del usuario con los componentes
    estructurales de WTM.

    WTMChat no realiza el diagnóstico de BINAH.
    Su función es conducir el descubrimiento y preparar
    el caso para BINAH.
    """

    def __init__(self) -> None:
        self.engine = WTMEngine()
        self.extraction = WTMExtractionEngine()
        self.validation = WTMValidationEngine()

    def start(
        self,
        form_input: WTMFormInput,
    ) -> WTMOutput:
        """
        Inicia una sesión WTM a partir del formulario inicial.
        """

        output = self.engine.create_initial_output(
            form_input
        )

        return self._refresh(output)

    def receive_message(
        self,
        output: WTMOutput,
        message: str,
        conversation_id: str | None = None,
        turn: int | None = None,
    ) -> WTMOutput:
        """
        Recibe un mensaje del usuario y actualiza el estado WTM.
        """

        conversation_input = WTMConversationInput(
            message=message,
            conversation_id=conversation_id,
            turn=turn,
        )

        output = self.engine.process_message(
            output,
            conversation_input,
        )

        output = self.extraction.extract(
            output,
            conversation_input,
        )

        return self._refresh(output)

    def get_next_question(
        self,
        output: WTMOutput,
    ) -> str | None:
        """
        Devuelve la siguiente pregunta pendiente.

        Si no existen preguntas pendientes, devuelve None.
        """

        if not output.questions:
            return None

        for question in output.questions:
            if question.required and not question.answered:
                return question.text

        return None

    def is_ready_for_binah(
        self,
        output: WTMOutput,
    ) -> bool:
        """
        Indica si el caso está listo para continuar hacia BINAH.
        """

        return output.ready_for_binah

    def _refresh(
        self,
        output: WTMOutput,
    ) -> WTMOutput:
        """
        Actualiza preguntas y valida el estado actual.

        La extracción ocurre antes de esta etapa para que
        las preguntas reflejen la información recién obtenida.
        """

        output = self.engine._update_questions(output)

        output = self.validation.validate(output)

        return output