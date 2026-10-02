from __future__ import annotations

import os
import sys
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from mcp import ClientSession, StdioServerParameters, stdio_client


@asynccontextmanager
async def open_stdio_session(
    server_path: Path,
    logging_callback: Any | None = None,
) -> AsyncIterator[ClientSession]:
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    params = StdioServerParameters(
        command=sys.executable,
        args=[str(server_path)],
        cwd=str(server_path.parent),
        env=env,
    )
    async with stdio_client(params) as (read_stream, write_stream):
        async with ClientSession(
            read_stream,
            write_stream,
            logging_callback=logging_callback,
        ) as session:
            await session.initialize()
            yield session
