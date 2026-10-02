from __future__ import annotations

import asyncio
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from examples._shared.console import configure_console, print_heading
from examples._shared.stdio import open_stdio_session


SERVER_PATH = Path(__file__).with_name("server.py")


async def run_demo() -> None:
    async with open_stdio_session(SERVER_PATH) as session:
        first = (await session.call_tool("remember", {"value": "alpha"})).structured_content
        second = (await session.call_tool("remember", {"value": "beta"})).structured_content

        if first is None or second is None:
            raise RuntimeError("remember must return structured_content")

        print_heading("生命周期")
        print(f"started={str(first['started']).lower()}")
        print(f"first_count={first['count']}")
        print(f"second_count={second['count']}")
        print(f"values={','.join(second['values'])}")


if __name__ == "__main__":
    configure_console()
    asyncio.run(run_demo())
