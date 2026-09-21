import re

from app.models import WTMConversationInput, WTMOutput


class WTMExtractionEngine:
    """
    Motor de extracción conservadora de WTM.

    Solo extrae información cuando el usuario utiliza
    explícitamente un marcador reconocido.

    WTM no inventa, interpreta ni diagnostica información.
    """

    CONTEXT_MARKERS = (
        "contexto",
        "context",
    )

    OBJECTIVE_MARKERS = (
        "objetivo",
        "objective",
        "quiero lograr",
    )

    SITUATION_MARKERS = (
        "situación",
        "situacion",
        "situation",
    )

    def extract(
        self,
        output: WTMOutput,
        conversation: WTMConversationInput,
    ) -> WTMOutput:
        """
        Extrae únicamente información declarada mediante
        marcadores explícitos.
        """

        message = conversation.message.strip()

        context = self._extract_context(message)
        objective = self._extract_objective(message)
        situation = self._extract_situation(message)

        if context is not None:
            output.context = context

        if objective is not None:
            output.objective = objective

        if situation is not None:
            output.situation = situation

        return output

    def _extract_context(
        self,
        message: str,
    ) -> str | None:
        return self._find_after_marker(
            message,
            self.CONTEXT_MARKERS,
        )

    def _extract_objective(
        self,
        message: str,
    ) -> str | None:
        return self._find_after_marker(
            message,
            self.OBJECTIVE_MARKERS,
        )

    def _extract_situation(
        self,
        message: str,
    ) -> str | None:
        return self._find_after_marker(
            message,
            self.SITUATION_MARKERS,
        )

    @staticmethod
    def _find_after_marker(
        message: str,
        markers: tuple[str, ...],
    ) -> str | None:
        """
        Busca un marcador solamente cuando aparece como
        una expresión independiente y no como parte de otra
        palabra.

        Ejemplo válido:
            "situación: los clientes esperan demasiado"

        Ejemplo no válido:
            "Tenemos algunos problemas con el proceso."
        """

        for marker in markers:
            pattern = rf"(?<!\w){re.escape(marker)}(?!\w)\s*:?"

            match = re.search(
                pattern,
                message,
                flags=re.IGNORECASE,
            )

            if match is None:
                continue

            value = message[match.end():].strip()

            if value:
                return value

        return None