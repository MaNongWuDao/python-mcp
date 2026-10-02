from __future__ import annotations

import asyncio

from mcp.server.mcpserver import Context, MCPServer
from mcp.server.mcpserver.exceptions import ToolError


server = MCPServer(
    name="tools-demo",
    title="MCP 工具调用",
    version="1.0.0",
)


@server.tool()
def add(a: int, b: int) -> int:
    """返回两个整数之和。"""
    return a + b


@server.tool()
async def slow_echo(text: str, ctx: Context, delay: float = 0.05) -> str:
    """异步工具：报告进度，等待，然后返回大写文本。"""
    await ctx.report_progress(1, 2, "开始")
    await asyncio.sleep(delay)
    await ctx.report_progress(2, 2, "完成")
    return text.upper()


@server.tool()
def divide(a: float, b: float) -> float:
    """演示预期业务错误。"""
    if b == 0:
        raise ToolError("division by zero")
    return a / b


if __name__ == "__main__":
    server.run(transport="stdio")
