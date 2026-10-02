"""MCP Prompt Client 示例。

客户端会启动同目录下的 server.py，随后完成以下操作：
1. 初始化 MCP 会话。
2. 调用 prompts/list 获取提示词定义。
3. 调用 prompts/get，用具体参数渲染两个提示词。
"""

from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path
from typing import Any

from mcp import ClientSession, StdioServerParameters, stdio_client
from mcp.types import TextContent


SERVER_PATH = Path(__file__).with_name("server.py")

# Windows 终端默认可能使用 GBK；统一输出编码，避免中文在控制台显示为乱码。
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# 演示两种读取方式：一个使用最少的必填参数，另一个使用全部可选参数。
PROMPT_CALLS: list[tuple[str, dict[str, str]]] = [
    (
        "explain_code",
        {
            "language": "Python",
            "code": "def divide(a, b):\n    return a / b",
        },
    ),
    (
        "review_code",
        {
            "language": "Python",
            "code": "def divide(a, b):\n    return a / b",
            "focus": "除零错误、参数类型和文档",
        },
    ),
]


def content_to_text(content: Any) -> str:
    """把文本内容转成字符串，并对非文本内容给出可读占位说明。"""
    if isinstance(content, TextContent):
        return content.text
    return f"<非文本内容: {getattr(content, 'type', type(content).__name__)}>"


async def main() -> None:
    server_env = os.environ.copy()
    server_env["PYTHONUTF8"] = "1"

    # sys.executable 保证客户端使用当前虚拟环境中的 Python 启动服务端。
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(SERVER_PATH)],
        cwd=str(SERVER_PATH.parent),
        env=server_env,
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            init_result = await session.initialize()
            print(f"已连接服务: {init_result.server_info.name}")

            # prompts/list：只读取提示词声明，不会执行提示词函数。
            prompts_result = await session.list_prompts()
            print(f"\n可用提示词: {len(prompts_result.prompts)} 个")
            for prompt in prompts_result.prompts:
                print(f"- {prompt.name}: {prompt.description}")
                for argument in prompt.arguments or []:
                    required = "必填" if argument.required else "可选"
                    print(f"  - {argument.name} ({required}): {argument.description}")

            # prompts/get：传入 arguments 后，服务端调用对应函数并返回消息列表。
            for prompt_name, arguments in PROMPT_CALLS:
                prompt_result = await session.get_prompt(
                    prompt_name,
                    arguments=arguments,
                )
                print(f"\n{'=' * 60}")
                print(f"读取提示词: {prompt_name}")
                print(f"说明: {prompt_result.description}")

                for index, message in enumerate(prompt_result.messages, start=1):
                    print(f"\n[{index}] role={message.role}")
                    print(content_to_text(message.content))


if __name__ == "__main__":
    asyncio.run(main())
