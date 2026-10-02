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
        initialized = session.initialize_result
        if initialized is None:
            raise RuntimeError("ClientSession was not initialized")

        print_heading("初始化结果")
        print(f"server_info={initialized.server_info.name}")
        print(f"server_version={initialized.server_info.version}")
        print(f"protocol_version={initialized.protocol_version}")
        print(f"instructions={session.instructions}")

        await session.send_ping()
        print("ping=ok")


if __name__ == "__main__":
    configure_console()
    asyncio.run(run_demo())
