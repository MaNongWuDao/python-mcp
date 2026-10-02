from __future__ import annotations

import asyncio
import sys
from pathlib import Path

from langchain.agents import create_agent
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from examples._shared.console import configure_console, print_heading
from examples._shared.fake_model import FakeToolCallingModel
from examples._shared.langchain_tools import MCPToolkit, StdioConnection


ROOT = Path(__file__).parent


def build_fake_model() -> FakeToolCallingModel:
    return FakeToolCallingModel(
        messages=iter(
            [
                AIMessage(
                    content="",
                    tool_calls=[
                        {
                            "name": "add",
                            "args": {"a": 40, "b": 2},
                            "id": "call_add",
                            "type": "tool_call",
                        }
                    ],
                ),
                AIMessage(
                    content="",
                    tool_calls=[
                        {
                            "name": "reverse",
                            "args": {"text": "ABC"},
                            "id": "call_reverse",
                            "type": "tool_call",
                        }
                    ],
                ),
                AIMessage(content="Result: 42 | reversed: CBA"),
            ]
        )
    )


async def run_demo() -> None:
    connections = {
        "math": StdioConnection(
            command=sys.executable,
            args=[str(ROOT / "math_server.py")],
            cwd=str(ROOT),
        ),
        "text": StdioConnection(
            command=sys.executable,
            args=[str(ROOT / "text_server.py")],
            cwd=str(ROOT),
        ),
    }

    tools = await MCPToolkit(connections).get_tools()
    agent = create_agent(model=build_fake_model(), tools=tools)
    result = await agent.ainvoke(
        {"messages": [HumanMessage(content="Add 40 and 2, then reverse ABC.")]}
    )

    messages = result["messages"]
    called_names = [
        call["name"]
        for message in messages
        if isinstance(message, AIMessage)
        for call in message.tool_calls
    ]
    tool_messages = [message for message in messages if isinstance(message, ToolMessage)]

    print_heading("LangChain / LangGraph 多 Server 调用")
    print(f"servers={','.join(sorted(connections))}")
    print(f"tools={','.join(sorted(tool.name for tool in tools))}")
    print(f"tool_calls={','.join(called_names)}")
    print(f"tool_results={'; '.join(str(message.content) for message in tool_messages)}")
    print(f"final={messages[-1].content}")


if __name__ == "__main__":
    configure_console()
    asyncio.run(run_demo())
