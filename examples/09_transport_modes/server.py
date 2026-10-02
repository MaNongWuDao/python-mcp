from __future__ import annotations

import argparse

from mcp.server.mcpserver import MCPServer


server = MCPServer(name="transport-demo", version="1.0.0")


@server.tool()
def echo(text: str) -> str:
    """返回输入文本。"""
    return text


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--transport",
        choices=("stdio", "sse", "streamable-http"),
        default="stdio",
    )
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    if args.transport == "stdio":
        server.run(transport="stdio")
    else:
        server.run(
            transport=args.transport,
            host="127.0.0.1",
            port=args.port,
        )
