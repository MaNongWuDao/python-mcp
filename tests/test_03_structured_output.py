from __future__ import annotations

import unittest

from tests._helpers import run_client


class StructuredOutputExampleTests(unittest.TestCase):
    def test_tool_returns_structured_content(self) -> None:
        result = run_client("examples/03_structured_output/client.py")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("title=Quarterly Report", result.stdout)
        self.assertIn("score=97.5", result.stdout)
        self.assertIn("tags=python,mcp", result.stdout)
        self.assertIn("owner=Ada", result.stdout)
        self.assertIn("content_matches_structured=true", result.stdout)


if __name__ == "__main__":
    unittest.main()
