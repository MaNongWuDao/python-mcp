from __future__ import annotations

import unittest

from tests._helpers import load_module, run_client


class LifespanExampleTests(unittest.TestCase):
    def test_integration_uses_one_state_per_session(self) -> None:
        result = run_client("examples/06_lifespan/client.py")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("started=true", result.stdout)
        self.assertIn("first_count=1", result.stdout)
        self.assertIn("second_count=2", result.stdout)
        self.assertIn("values=alpha,beta", result.stdout)

    def test_lifespan_closes_state(self) -> None:
        module = load_module("examples/06_lifespan/server.py", "lifespan_server_test")

        async def exercise() -> None:
            async with module.lifespan(module.server) as state:
                self.assertTrue(state.started)
                self.assertFalse(state.closed)
            self.assertTrue(state.closed)

        import asyncio

        asyncio.run(exercise())


if __name__ == "__main__":
    unittest.main()
