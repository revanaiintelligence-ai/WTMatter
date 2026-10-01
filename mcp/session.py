from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

from app.chat import WTMChat
from app.models import WTMOutput


@dataclass
class WTMSession:
    """
    Estado de una conversación WTM.

    Una sesión mantiene el WTMOutput completo para que cada
    nuevo mensaje continúe sobre el mismo caso.
    """

    conversation_id: str
    output: WTMOutput


class WTMSessionManager:
    """
    Gestor simple de sesiones WTM.

    Esta primera implementación mantiene las sesiones en memoria.
    No introduce todavía una base de datos ni almacenamiento externo.

    Para producción, el almacenamiento podrá sustituirse sin
    modificar la interfaz de las herramientas MCP.
    """

    def __init__(self) -> None:
        self._sessions: Dict[str, WTMSession] = {}
        self._chat = WTMChat()

    def start(
        self,
        conversation_id: str,
        message: str,
        business: str = "Por determinar",
    ) -> WTMSession:
        """
        Crea una nueva sesión WTM a partir del primer mensaje.
        """

        output = self._chat.start_conversation(
            message=message,
            business=business,
            conversation_id=conversation_id,
            turn=1,
        )

        session = WTMSession(
            conversation_id=conversation_id,
            output=output,
        )

        self._sessions[conversation_id] = session

        return session

    def get(
        self,
        conversation_id: str,
    ) -> Optional[WTMSession]:
        """
        Recupera una sesión existente.
        """

        return self._sessions.get(conversation_id)

    def receive(
        self,
        conversation_id: str,
        message: str,
    ) -> WTMSession:
        """
        Incorpora un nuevo mensaje a una sesión existente.
        """

        session = self._sessions.get(conversation_id)

        if session is None:
            raise ValueError(
                f"WTM session not found: {conversation_id}"
            )

        current_turn = len(session.output.evidence) + 1

        session.output = self._chat.receive_message(
            output=session.output,
            message=message,
            conversation_id=conversation_id,
            turn=current_turn,
        )

        return session

    def delete(
        self,
        conversation_id: str,
    ) -> bool:
        """
        Elimina una sesión existente.

        Devuelve True si existía y fue eliminada.
        """

        return self._sessions.pop(
            conversation_id,
            None,
        ) is not None