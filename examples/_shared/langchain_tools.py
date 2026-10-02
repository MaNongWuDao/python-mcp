from __future__ import annotations

import json
from collections.abc import AsyncIterator, Mapping
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Literal

from langchain_core.tools import StructuredTool, ToolException
from mcp import ClientSession, StdioServerParameters, stdio_client
from mcp.types import Tool as MCPTool


@dataclass(frozen=True)
class StdioConnection:
    command: str
    args: list[str]
    cwd: str | None = None
    env: dict[str, str] | None = None
    transport: Literal["stdio"] = "stdio"


class MCPToolkit:
    """Convert MCP tools into LangChain tools without the incompatible adapter."""

    def __init__(
        self,
        connections: Mapping[str, StdioConnection],
        *,
        tool_name_prefix: bool = False,
    ) -> None:
        self.connections = dict(connections)
        self.tool_name_prefix = tool_name_prefix

    @asynccontextmanager
    async def _open(self, connection: StdioConnection) -> AsyncIterator[ClientSession]:
        if connection.transport != "stdio":
            raise ValueError(f"Unsupported transport: {connection.transport}")
        params = StdioServerParameters(
            command=connection.command,
            args=connection.args,
            cwd=connection.cwd,
            env=connection.env,
        )
        async with stdio_client(params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                yield session

    @staticmethod
    def _result_text(result: object) -> str:
        content = getattr(result, "content", [])
        text = "\n".join(
            item.text
            for item in content
            if getattr(item, "type", None) == "text"
        )
        if text:
            return text
        structured = getattr(result, "structured_content", None)
        if structured is not None:
            return json.dumps(structured, ensure_ascii=False)
        return ""

    def _convert(
        self,
        server_name: str,
        connection: StdioConnection,
        mcp_tool: MCPTool,
    ) -> StructuredTool:
        async def call_tool(**arguments: object) -> str:
            async with self._open(connection) as session:
                result = await session.call_tool(mcp_tool.name, arguments)
            if result.is_error:
                raise ToolException(self._result_text(result))
            return self._result_text(result)

        name = mcp_tool.name
        if self.tool_name_prefix:
            name = f"{server_name}_{name}"
        return StructuredTool.from_function(
            coroutine=call_tool,
            name=name,
            description=mcp_tool.description or "",
            args_schema=mcp_tool.input_schema,
        )

    async def get_tools(self) -> list[StructuredTool]:
        tools: list[StructuredTool] = []
        for server_name, connection in self.connections.items():
            async with self._open(connection) as session:
                result = await session.list_tools()
            tools.extend(
                self._convert(server_name, connection, mcp_tool)
                for mcp_tool in result.tools
            )
        return tools
