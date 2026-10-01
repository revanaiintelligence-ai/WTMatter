from __future__ import annotations

from typing import Any, Dict

from .session import WTMSessionManager


class WTMTools:
    """
    Herramientas MCP de WTMatter.

    Esta capa no contiene la lógica de diagnóstico de WTM.
    Solamente adapta las operaciones de WTM a una interfaz
    que pueda ser expuesta mediante MCP.
    """

    def __init__(self) -> None:
        self.sessions = WTMSessionManager()

    def start(
        self,
        conversation_id: str,
        message: str,
        business: str = "Por determinar",
    ) -> Dict[str, Any]:
        """
        Inicia una conversación WTM.
        """

        session = self.sessions.start(
            conversation_id=conversation_id,
            message=message,
            business=business,
        )

        return self._serialize_session(session)

    def chat(
        self,
        conversation_id: str,
        message: str,
    ) -> Dict[str, Any]:
        """
        Envía un nuevo mensaje a una conversación WTM existente.
        """

        session = self.sessions.receive(
            conversation_id=conversation_id,
            message=message,
        )

        return self._serialize_session(session)

    def get_case(
        self,
        conversation_id: str,
    ) -> Dict[str, Any]:
        """
        Recupera el estado estructurado actual del caso WTM.
        """

        session = self.sessions.get(
            conversation_id,
        )

        if session is None:
            raise ValueError(
                f"WTM session not found: {conversation_id}"
            )

        return self._serialize_session(session)

    def handoff(
        self,
        conversation_id: str,
    ) -> Dict[str, Any]:
        """
        Prepara el caso estructurado para una futura conexión
        con REVA.N / BINAH.

        Esta versión no realiza todavía la llamada a BINAH.
        """

        session = self.sessions.get(
            conversation_id,
        )

        if session is None:
            raise ValueError(
                f"WTM session not found: {conversation_id}"
            )

        output = session.output

        return {
            "conversation_id": conversation_id,
            "ready_for_binah": output.ready_for_binah,
            "wtm_output": output.model_dump(),
        }

    @staticmethod
    def _serialize_session(session) -> Dict[str, Any]:
        """
        Convierte el estado WTM en una respuesta JSON-compatible.
        """

        output = session.output

        return {
            "conversation_id": session.conversation_id,
            "status": output.status,
            "ready_for_binah": output.ready_for_binah,
            "business": output.business,
            "context": output.context,
            "objective": output.objective,
            "situation": output.situation,
            "observations": [
                item.model_dump()
                for item in output.observations
            ],
            "hypotheses": [
                item.model_dump()
                for item in output.hypotheses
            ],
            "unknowns": [
                item.model_dump()
                for item in output.unknowns
            ],
            "contradictions": [
                item.model_dump()
                for item in output.contradictions
            ],
            "evidence": [
                item.model_dump()
                for item in output.evidence
            ],
            "questions": [
                item.model_dump()
                for item in output.questions
            ],
            "need_candidate": (
                output.need_candidate.model_dump()
                if output.need_candidate
                else None
            ),
            "conversation_summary": output.conversation_summary,
            "blocking_reasons": output.blocking_reasons,
            "traceability": output.traceability.model_dump(),
        }