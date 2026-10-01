"""
WTMatter MCP Server.

Punto de entrada para exponer WTMatter mediante Model Context
Protocol.

La lógica de negocio permanece en app/.
Esta capa solamente adapta WTMatter a MCP.
"""

from .tools import WTMTools


def create_wtm_tools() -> WTMTools:
    """
    Crea la instancia principal de herramientas WTM.

    El servidor MCP definitivo utilizará esta instancia para
    registrar las herramientas expuestas a ChatGPT.
    """

    return WTMTools()


def main() -> None:
    """
    Punto de entrada del servidor.

    La implementación del transporte MCP se añadirá después
    de fijar la versión y dependencia MCP que utilizará
    el despliegue de WTMatter.
    """

    tools = create_wtm_tools()

    # Punto de integración del servidor MCP.
    #
    # Las herramientas previstas son:
    #
    # - wtm_start
    # - wtm_chat
    # - wtm_get_case
    # - wtm_handoff
    #
    # No se inicia todavía un transporte concreto aquí para
    # evitar acoplar WTMatter a una implementación MCP no
    # verificada.

    _ = tools

    raise RuntimeError(
        "WTMatter MCP transport is not configured yet."
    )


if __name__ == "__main__":
    main()