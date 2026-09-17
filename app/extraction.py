from typing import List, Optional

from .models import (
    WTMConversationInput,
    WTMOutput,
)


class WTMExtractionEngine:
    """
    Motor de extracción de información de WTM.

    Su función es identificar información explícita
    proporcionada por el usuario y actualizar el estado
    estructurado de WTM.

    No realiza diagnóstico de BINAH.
    No determina la solución del problema.
    """

    def extract(
        self,
        output: WTMOutput,
        conversation_input: WTMConversationInput,
    ) -> WTMOutput:
        """
        Procesa un mensaje y actualiza información explícita
        cuando puede asignarse de forma segura a un campo WTM.
        """

        message = conversation_input.message.strip()

        if not message:
            return output

        self._extract_context(output, message)
        self._extract_objective(output, message)
        self._extract_situation(output, message)

        return output

    @staticmethod
    def _extract_context(
        output: WTMOutput,
        message: str,
    ) -> None:
        """
        Extrae contexto solamente cuando WTM ya dispone
        de una indicación explícita.
        """

        if output.context:
            return

        context = WTMExtractionEngine._find_after_marker(
            message,
            [
                "contexto:",
                "contexto",
            ],
        )

        if context:
            output.context = context

    @staticmethod
    def _extract_objective(
        output: WTMOutput,
        message: str,
    ) -> None:
        """
        Extrae el objetivo cuando aparece explícitamente.
        """

        if output.objective:
            return

        objective = WTMExtractionEngine._find_after_marker(
            message,
            [
                "objetivo:",
                "objetivo",
                "quiero lograr:",
                "quiero lograr",
            ],
        )

        if objective:
            output.objective = objective

    @staticmethod
    def _extract_situation(
        output: WTMOutput,
        message: str,
    ) -> None:
        """
        Extrae la situación cuando aparece explícitamente.
        """

        if output.situation:
            return

        situation = WTMExtractionEngine._find_after_marker(
            message,
            [
                "situación:",
                "situación",
                "problema:",
                "problema",
            ],
        )

        if situation:
            output.situation = situation

    @staticmethod
    def _find_after_marker(
        message: str,
        markers: List[str],
    ) -> Optional[str]:
        """
        Busca una expresión explícita y devuelve el contenido
        posterior a ella.

        La extracción es deliberadamente conservadora:
        si no existe un marcador claro, no inventa información.
        """

        normalized_message = message.strip()
        message_lower = normalized_message.lower()

        for marker in markers:
            marker_lower = marker.lower()

            position = message_lower.find(marker_lower)

            if position == -1:
                continue

            value = normalized_message[
                position + len(marker_lower):
            ].strip()

            if value.startswith(":"):
                value = value[1:].strip()

            if value:
                return value

        return None