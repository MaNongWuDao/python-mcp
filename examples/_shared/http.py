from __future__ import annotations

import asyncio
import socket
import sys
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

def find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


async def wait_for_server(host: str, port: int, timeout: float = 10.0) -> None:
    loop = asyncio.get_running_loop()
    deadline = loop.time() + timeout
    last_error: OSError | None = None

    while loop.time() < deadline:
        try:
            reader, writer = await asyncio.open_connection(host, port)
            del reader
            writer.close()
            await writer.wait_closed()
            return
        except OSError as exc:
            last_error = exc
            await asyncio.sleep(0.05)

    raise TimeoutError(f"Server did not listen on {host}:{port} within {timeout}s") from last_error


@asynccontextmanager
async def run_http_server(
    server_path: Path,
    transport: str,
    port: int,
) -> AsyncIterator[asyncio.subprocess.Process]:
    process = await asyncio.create_subprocess_exec(
        sys.executable,
        str(server_path),
        "--transport",
        transport,
        "--port",
        str(port),
        cwd=str(server_path.parent),
        stdout=asyncio.subprocess.DEVNULL,
        stderr=None,
    )
    try:
        await wait_for_server("127.0.0.1", port)
        yield process
    finally:
        if process.returncode is None:
            process.terminate()
            try:
                await asyncio.wait_for(process.wait(), timeout=5.0)
            except TimeoutError:
                process.kill()
                await process.wait()
