"""MCP Prompt Server 示例。

本文件只负责定义提示词。客户端通过 stdio 启动该进程后，可以：
1. 使用 prompts/list 查看所有提示词及其参数。
2. 使用 prompts/get 传入参数并取得渲染后的消息列表。
"""

from __future__ import annotations

from typing import Annotated

from mcp.server.mcpserver import AssistantMessage, MCPServer, UserMessage
from pydantic import Field


# `name` 和 `description` 会出现在 prompts/list 的返回结果中。
server = MCPServer(
    name="prompt-demo",
    title="MCP 提示词示例服务",
    description="演示如何定义、发现和读取 MCP 提示词。",
    version="0.1.0",
)


@server.prompt(
    name="explain_code",
    title="解释代码",
    description="根据编程语言和源码生成一段代码解释任务的提示词。",
)
def explain_code(
    language: Annotated[str, Field(description="编程语言，例如 Python、TypeScript")],
    code: Annotated[str, Field(description="需要解释的源代码")],
) -> list[UserMessage]:
    """返回单个 user 消息，形成一个可发送给模型的代码解释提示词。"""
    return [
        UserMessage(
            content=(
                f"请解释下面这段 {language} 代码。\n"
                "要求：先概括用途，再按执行流程说明关键逻辑，最后指出边界条件。\n\n"
                f"```{language.lower()}\n{code}\n```"
            )
        )
    ]


@server.prompt(
    name="review_code",
    title="审查代码",
    description="生成代码审查提示词，并附带 assistant 输出格式前缀。",
)
async def review_code(
    language: Annotated[str, Field(description="编程语言，例如 Python、TypeScript")],
    code: Annotated[str, Field(description="需要审查的源代码")],
    focus: Annotated[
        str,
        Field(description="本次审查重点关注的内容"),
    ] = "正确性、可读性和边界条件",
) -> list[UserMessage | AssistantMessage]:
    """异步提示词可以读取数据库或文件；这里保持无副作用，便于直接运行。

    返回 user + assistant 两条消息，assistant 消息可作为模型输出的起始前缀。
    """
    return [
        UserMessage(
            content=(
                f"请审查下面的 {language} 代码，重点关注：{focus}。\n"
                "每个问题都要说明风险、触发条件和修复建议。\n\n"
                f"```{language.lower()}\n{code}\n```"
            )
        ),
        AssistantMessage(content="## 问题清单\n"),
    ]


if __name__ == "__main__":
    # 客户端会通过标准输入/输出与当前进程通信。
    # 不要把调试信息 print 到 stdout，否则会破坏 MCP 的 JSON-RPC 数据流。
    server.run(transport="stdio")
