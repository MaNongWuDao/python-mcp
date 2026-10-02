from __future__ import annotations

import asyncio
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from examples._shared.console import configure_console, print_heading
from examples._shared.stdio import open_stdio_session


SERVER_PATH = Path(__file__).with_name("server.py")


def first_text(result) -> str:
    return "".join(
        item.text for item in result.content if getattr(item, "type", None) == "text"
    )


async def run_demo() -> None:
    async with open_stdio_session(SERVER_PATH) as session:
        tools = await session.list_tools()
        print_heading("工具调用")
        print(f"tools={','.join(sorted(tool.name for tool in tools.tools))}")

        add_result = await session.call_tool("add", {"a": 20, "b": 22})
        print(f"add={first_text(add_result)}")

        async def on_progress(progress: float, total: float | None, message: str | None) -> None:
            total_text = str(int(total)) if total is not None else "?"
            print(f"progress={int(progress)}/{total_text} message={message}")

        echo_result = await session.call_tool(
            "slow_echo",
            {"text": "hello mcp"},
            progress_callback=on_progress,
        )
        print(f"slow_echo={first_text(echo_result)}")

        divide_result = await session.call_tool("divide", {"a": 10, "b": 0})
        divide_message = first_text(divide_result).removeprefix(
            "Error executing tool divide: "
        )
        print(f"divide_error={divide_message}")


if __name__ == "__main__":
    configure_console()
    asyncio.run(run_demo())
