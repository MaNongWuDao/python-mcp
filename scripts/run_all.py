from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TIMEOUT = 120
CLIENTS = [
    "examples/01_server_client/client.py",
    "examples/02_tools/client.py",
    "examples/03_structured_output/client.py",
    "examples/04_resources/client.py",
    "examples/05_prompts/client.py",
    "examples/06_lifespan/client.py",
    "examples/07_langchain_tools/client.py",
    "examples/08_multi_server/client.py",
    "examples/09_transport_modes/client.py",
]


def run_client(
    client: str,
    env: dict[str, str],
    timeout: float | None = None,
) -> bool:
    if timeout is None:
        timeout = DEFAULT_TIMEOUT

    try:
        result = subprocess.run(
            [sys.executable, str(ROOT / client)],
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired:
        print(f"FAIL {client} timeout={timeout}s", file=sys.stderr)
        return False

    if result.returncode != 0:
        print(f"FAIL {client}", file=sys.stderr)
        print(result.stdout, file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        return False

    print(f"PASS {client}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--list", action="store_true")
    args = parser.parse_args()

    if args.list:
        print("\n".join(CLIENTS))
        return 0

    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"

    for client in CLIENTS:
        if not run_client(client, env):
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
