from __future__ import annotations

import unittest

from tests._helpers import run_client


class ToolExampleTests(unittest.TestCase):
    def test_tools_are_listed_called_and_report_progress(self) -> None:
        result = run_client("examples/02_tools/client.py")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("tools=add,divide,slow_echo", result.stdout)
        self.assertIn("add=42", result.stdout)
        self.assertIn("progress=1/2", result.stdout)
        self.assertIn("progress=2/2", result.stdout)
        self.assertIn("slow_echo=HELLO MCP", result.stdout)
        self.assertIn("divide_error=division by zero", result.stdout)


if __name__ == "__main__":
    unittest.main()
