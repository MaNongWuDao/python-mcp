from __future__ import annotations

import argparse
import asyncio
import os
import sys
from pathlib import Path

from langchain.agents import create_agent
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from examples._shared.console import configure_console, print_heading
from examples._shared.fake_model import FakeToolCallingModel
from examples._shared.langchain_tools import MCPToolkit, StdioConnection


SERVER_PATH = Path(__file__).with_name("server.py")


def build_model(use_openai: bool) -> BaseChatModel:
    if use_openai:
        from langchain_openai import ChatOpenAI

        if not os.getenv("OPENAI_API_KEY"):
            raise SystemExit("OPENAI_API_KEY is required when --real is used")
        return ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
            temperature=0,
        )

    return FakeToolCallingModel(
        messages=iter(
            [
                AIMessage(
                    content="",
                    tool_calls=[
                        {
                            "name": "multiply",
                            "args": {"a": 6, "b": 7},
                            "id": "call_multiply",
                            "type": "tool_call",
                        }
                    ],
                ),
                AIMessage(content="6 * 7 = 42"),
            ]
        )
    )


async def run_demo(use_openai: bool) -> None:
    toolkit = MCPToolkit(
        {
            "calculator": StdioConnection(
                command=sys.executable,
                args=[str(SERVER_PATH)],
                cwd=str(SERVER_PATH.parent),
            )
        }
    )
    tools = await toolkit.get_tools()
    model = build_model(use_openai)
    agent = create_agent(model=model, tools=tools)
    result = await agent.ainvoke(
        {"messages": [HumanMessage(content="Use multiply to calculate 6 * 7.")]}
    )

    messages = result["messages"]
    tool_names = ",".join(sorted(tool.name for tool in tools))
    called_names = [
        call["name"]
        for message in messages
        if isinstance(message, AIMessage)
        for call in message.tool_calls
    ]
    tool_messages = [message for message in messages if isinstance(message, ToolMessage)]

    print_heading("LangChain / LangGraph 工具集成")
    print(f"tools={tool_names}")
    print(f"tool_calls={','.join(called_names)}")
    print(f"tool_result={tool_messages[-1].content}")
    print(f"final={messages[-1].content}")


if __name__ == "__main__":
    configure_console()
    parser = argparse.ArgumentParser()
    parser.add_argument("--real", action="store_true")
    args = parser.parse_args()
    asyncio.run(run_demo(args.real))
