from __future__ import annotations

import unittest

from tests._helpers import run_client


class TransportExampleTests(unittest.TestCase):
    def test_all_three_transports_execute_the_same_tool(self) -> None:
        result = run_client("examples/09_transport_modes/client.py", timeout=120)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("[stdio] echo=stdio:hello", result.stdout)
        self.assertIn("[sse] echo=sse:hello", result.stdout)
        self.assertIn("[streamable-http] echo=streamable-http:hello", result.stdout)


if __name__ == "__main__":
    unittest.main()
