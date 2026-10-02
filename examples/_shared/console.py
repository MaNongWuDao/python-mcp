from __future__ import annotations

import sys


def configure_console() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")


def print_heading(title: str) -> None:
    print(f"\n{'=' * 60}\n{title}\n{'=' * 60}")
