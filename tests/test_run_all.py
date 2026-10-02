from __future__ import annotations

import io
import subprocess
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest import mock

from tests._helpers import ROOT, load_module


run_all = load_module("scripts/run_all.py", "scripts_run_all")


class RunAllTests(unittest.TestCase):
    def test_list_contains_every_example(self) -> None:
        result = subprocess.run(
            [sys.executable, "scripts/run_all.py", "--list"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=30,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            result.stdout.strip().splitlines(),
            [
                "examples/01_server_client/client.py",
                "examples/02_tools/client.py",
                "examples/03_structured_output/client.py",
                "examples/04_resources/client.py",
                "examples/05_prompts/client.py",
                "examples/06_lifespan/client.py",
                "examples/07_langchain_tools/client.py",
                "examples/08_multi_server/client.py",
                "examples/09_transport_modes/client.py",
            ],
        )

    def test_failing_client_prints_fail_and_returns_one(self) -> None:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with mock.patch.object(run_all, "CLIENTS", ["tests/fixtures/failing_client.py"]):
            with mock.patch.object(sys, "argv", ["run_all.py"]):
                with redirect_stdout(stdout), redirect_stderr(stderr):
                    exit_code = run_all.main()

        self.assertEqual(exit_code, 1)
        self.assertIn("FAIL tests/fixtures/failing_client.py", stderr.getvalue())
        self.assertIn("intentional failure", stderr.getvalue())
        self.assertEqual(stdout.getvalue(), "")

    def test_timeout_prints_fail_with_timeout(self) -> None:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with mock.patch.object(run_all, "DEFAULT_TIMEOUT", 1):
            with mock.patch.object(
                run_all,
                "CLIENTS",
                ["tests/fixtures/sleeping_client.py"],
            ):
                with mock.patch.object(sys, "argv", ["run_all.py"]):
                    with redirect_stdout(stdout), redirect_stderr(stderr):
                        exit_code = run_all.main()

        self.assertEqual(exit_code, 1)
        self.assertIn(
            "FAIL tests/fixtures/sleeping_client.py timeout=1s",
            stderr.getvalue(),
        )
        self.assertEqual(stdout.getvalue(), "")


if __name__ == "__main__":
    unittest.main()
