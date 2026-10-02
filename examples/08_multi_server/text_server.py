from __future__ import annotations

from mcp.server.mcpserver import MCPServer


server = MCPServer(name="text-server", version="1.0.0")


@server.tool()
def reverse(text: str) -> str:
    """反转输入文本。"""
    return text[::-1]


if __name__ == "__main__":
    server.run(transport="stdio")
