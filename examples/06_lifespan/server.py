from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from typing import Any

from mcp.server.mcpserver import Context, MCPServer


@dataclass
class AppState:
    values: list[str] = field(default_factory=list)
    started: bool = False
    closed: bool = False


@asynccontextmanager
async def lifespan(server: MCPServer[AppState]) -> AsyncIterator[AppState]:
    del server
    state = AppState(started=True)
    try:
        yield state
    finally:
        state.closed = True


server = MCPServer(
    name="lifespan-demo",
    version="1.0.0",
    lifespan=lifespan,
)


@server.tool()
async def remember(
    value: str,
    ctx: Context[AppState, Any],
) -> dict[str, object]:
    """把值写入 lifespan 状态，同一条连接内状态持续存在。"""
    state = ctx.request_context.lifespan_context
    state.values.append(value)
    return {
        "started": state.started,
        "count": len(state.values),
        "values": list(state.values),
    }


if __name__ == "__main__":
    server.run(transport="stdio")
