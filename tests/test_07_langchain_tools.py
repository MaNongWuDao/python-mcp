from __future__ import annotations

import unittest

from tests._helpers import run_client


class LangChainToolExampleTests(unittest.TestCase):
    def test_fake_model_executes_mcp_tool(self) -> None:
        result = run_client("examples/07_langchain_tools/client.py", timeout=120)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("LangGraphDeprecatedSinceV10", result.stderr)
        self.assertIn("tools=add,multiply", result.stdout)
        self.assertIn("tool_calls=multiply", result.stdout)
        self.assertIn("tool_result=42", result.stdout)
        self.assertIn("final=6 * 7 = 42", result.stdout)


if __name__ == "__main__":
    unittest.main()
