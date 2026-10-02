from __future__ import annotations

import asyncio
import sys
from pathlib import Path

from mcp import ClientSession
from mcp.client.sse import sse_client
from mcp.client.streamable_http import streamable_http_client

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from examples._shared.console import configure_console, print_heading
from examples._shared.http import find_free_port, run_http_server
from examples._shared.stdio import open_stdio_session


SERVER_PATH = Path(__file__).with_name("server.py")


def first_text(result) -> str:
    return "".join(
        item.text for item in result.content if getattr(item, "type", None) == "text"
    )


async def call_stdio() -> str:
    async with open_stdio_session(SERVER_PATH) as session:
        result = await session.call_tool("echo", {"text": "stdio:hello"})
        return first_text(result)


async def call_sse(port: int) -> str:
    async with run_http_server(SERVER_PATH, "sse", port):
        async with sse_client(f"http://127.0.0.1:{port}/sse") as streams:
            async with ClientSession(*streams) as session:
                await session.initialize()
                result = await session.call_tool("echo", {"text": "sse:hello"})
                return first_text(result)


async def call_streamable_http(port: int) -> str:
    async with run_http_server(SERVER_PATH, "streamable-http", port):
        async with streamable_http_client(
            f"http://127.0.0.1:{port}/mcp"
        ) as streams:
            async with ClientSession(*streams) as session:
                await session.initialize()
                result = await session.call_tool(
                    "echo",
                    {"text": "streamable-http:hello"},
                )
                return first_text(result)


async def run_demo() -> None:
    print_heading("传输模式")
    print(f"[stdio] echo={await call_stdio()}")
    print(f"[sse] echo={await call_sse(find_free_port())}")
    print(
        "[streamable-http] "
        f"echo={await call_streamable_http(find_free_port())}"
    )


if __name__ == "__main__":
    configure_console()
    asyncio.run(run_demo())
