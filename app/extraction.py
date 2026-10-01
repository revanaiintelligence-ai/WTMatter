import re

from app.models import WTMConversationInput, WTMOutput

class WTMExtractionEngine:
"""
Motor de extracción de información de WTM.

Responsabilidades:
- Reconocer campos explícitos.
- Aprovechar declaraciones naturales inequívocas.
- Conservar la información original como evidencia.
- Evitar convertir hipótesis o suposiciones en hechos.

Este componente no realiza el diagnóstico empresarial
ni decide qué solución necesita el usuario.

La interpretación avanzada puede delegarse a la IA
que utilice el sistema.
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

OBJECTIVE_PHRASES = (
    "quiero",
    "busco",
    "necesito lograr",
    "mi meta es",
    "nuestro objetivo es",
    "me gustaría",
)

def extract(
    self,
    output: WTMOutput,
    conversation: WTMConversationInput,
) -> WTMOutput:
    """
    Extrae información del mensaje actual.

    Primero utiliza marcadores explícitos.
    Después aplica reconocimientos naturales limitados,
    sin inferir información que no esté declarada.
    """

    message = conversation.message.strip()

    if not message:
        return output

    context = self._extract_context(message)
    objective = self._extract_objective(message)
    situation = self._extract_situation(message)

    if context is None:
        context = self._natural_context(message)

    if objective is None:
        objective = self._natural_objective(message)

    if situation is None:
        situation = self._natural_situation(message)

    if context is not None:
        output.context = self._merge(
            output.context,
            context,
        )

    if objective is not None:
        output.objective = self._merge(
            output.objective,
            objective,
        )

    if situation is not None:
        output.situation = self._merge(
            output.situation,
            situation,
        )

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
def _natural_context(
    message: str,
) -> str | None:
    """
    Reconoce contextos declarados directamente.

    No intenta deducir el sector o tipo de negocio
    a partir de síntomas aislados.
    """

    patterns = (
        r"\b(?:en|dentro de)\s+(mi|nuestro)\s+"
        r"(negocio|empresa|equipo|organización|proyecto)\b",
        r"\b(?:mi|nuestro)\s+"
        r"(negocio|empresa|equipo|organización|proyecto)\b",
    )

    for pattern in patterns:
        match = re.search(
            pattern,
            message,
            flags=re.IGNORECASE,
        )

        if match:
            return match.group(0).strip()

    return None

def _natural_objective(
    self,
    message: str,
) -> str | None:
    """
    Reconoce objetivos cuando el usuario expresa
    directamente una intención.
    """

    lowered = message.lower()

    for phrase in self.OBJECTIVE_PHRASES:
        pattern = (
            rf"(?<!\w){re.escape(phrase)}(?!\w)"
        )

        match = re.search(
            pattern,
            lowered,
        )

        if match is None:
            continue

        value = message[match.start():].strip()

        if value:
            return value

    return None

@staticmethod
def _natural_situation(
    message: str,
) -> str | None:
    """
    Utiliza el mensaje como situación cuando contiene
    una descripción concreta y no parece ser únicamente
    una pregunta o una intención.

    No determina si lo descrito es verdadero:
    conserva la declaración como provisional.
    """

    text = message.strip()

    if not text:
        return None

    if text.endswith("?"):
        return None

    lowered = text.lower()

    objective_starters = (
        "quiero ",
        "busco ",
        "me gustaría ",
        "mi objetivo es ",
        "nuestro objetivo es ",
    )

    if lowered.startswith(objective_starters):
        return None

    if len(text.split()) < 4:
        return None

    return text

@staticmethod
def _find_after_marker(
    message: str,
    markers: tuple[str, ...],
) -> str | None:
    """
    Busca un marcador independiente y extrae el texto
    que aparece después de él.

    Ejemplo:
        "situación: los clientes esperan demasiado"
    """

    for marker in markers:
        pattern = (
            rf"(?<!\w){re.escape(marker)}(?!\w)\s*:?"
        )

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

@staticmethod
def _merge(
    current: str | None,
    new_value: str,
) -> str:
    """
    Conserva el dato anterior y agrega información nueva
    sin duplicar exactamente el mismo texto.
    """

    value = new_value.strip()

    if not current:
        return value

    previous = current.strip()

    if value.casefold() in previous.casefold():
        return previous

    if previous.casefold() in value.casefold():
        return value

    return f"{previous}\n{value}"