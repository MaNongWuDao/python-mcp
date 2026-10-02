from __future__ import annotations

import unittest

from tests._helpers import run_client


class ServerClientExampleTests(unittest.TestCase):
    def test_initialize_and_ping(self) -> None:
        result = run_client("examples/01_server_client/client.py")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("server_info=server-client-demo", result.stdout)
        self.assertIn("protocol_version=", result.stdout)
        self.assertIn("instructions=演示初始化握手、能力协商和 ping", result.stdout)
        self.assertIn("ping=ok", result.stdout)


if __name__ == "__main__":
    unittest.main()
