from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from examples._shared.console import configure_console, print_heading
from examples._shared.stdio import open_stdio_session


SERVER_PATH = Path(__file__).with_name("server.py")


async def run_demo() -> None:
    async with open_stdio_session(SERVER_PATH) as session:
        await session.list_tools()
        result = await session.call_tool(
            "build_report",
            {"topic": "Quarterly", "score": 97.5},
        )
        data = result.structured_content
        if data is None:
            raise RuntimeError("Server did not return structuredContent")

        print_heading("结构化输出")
        print(f"title={data['title']}")
        print(f"score={data['score']}")
        print(f"tags={','.join(data['tags'])}")
        print(f"owner={data['details']['owner']}")

        text = "".join(
            item.text
            for item in result.content
            if getattr(item, "type", None) == "text"
        )
        content_data = json.loads(text)
        print(f"content_matches_structured={str(content_data == data).lower()}")


if __name__ == "__main__":
    configure_console()
    asyncio.run(run_demo())
