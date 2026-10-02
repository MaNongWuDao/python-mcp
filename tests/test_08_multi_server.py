from __future__ import annotations

import unittest

from tests._helpers import run_client


class MultiServerExampleTests(unittest.TestCase):
    def test_agent_calls_two_mcp_servers(self) -> None:
        result = run_client("examples/08_multi_server/client.py", timeout=120)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("LangGraphDeprecatedSinceV10", result.stderr)
        self.assertIn("servers=math,text", result.stdout)
        self.assertIn("tools=add,reverse", result.stdout)
        self.assertIn("tool_calls=add,reverse", result.stdout)
        self.assertIn("final=Result: 42 | reversed: CBA", result.stdout)


if __name__ == "__main__":
    unittest.main()
