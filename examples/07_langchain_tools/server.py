from __future__ import annotations

from mcp.server.mcpserver import MCPServer


server = MCPServer(name="calculator-server", version="1.0.0")


@server.tool()
def add(a: int, b: int) -> int:
    """返回两个整数之和。"""
    return a + b


@server.tool()
def multiply(a: int, b: int) -> int:
    """返回两个整数之积。"""
    return a * b


if __name__ == "__main__":
    server.run(transport="stdio")
