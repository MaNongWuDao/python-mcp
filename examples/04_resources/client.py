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


def read_json_text(result) -> dict[str, object]:
    for content in result.contents:
        text = getattr(content, "text", None)
        if text is not None:
            return json.loads(text)
    raise RuntimeError("No text resource content returned")


async def run_demo() -> None:
    async with open_stdio_session(SERVER_PATH) as session:
        resources = await session.list_resources()
        templates = await session.list_resource_templates()

        print_heading("资源")
        print(f"resources={','.join(str(item.uri) for item in resources.resources)}")
        print(
            "templates="
            + ",".join(
                str(item.uri_template)
                for item in templates.resource_templates
            )
        )

        config = read_json_text(await session.read_resource("demo://config"))
        print(f"config_server={config['server']}")

        profile = read_json_text(await session.read_resource("demo://users/1"))
        print(f"user_name={profile['name']}")
        print(f"user_role={profile['role']}")


if __name__ == "__main__":
    configure_console()
    asyncio.run(run_demo())
