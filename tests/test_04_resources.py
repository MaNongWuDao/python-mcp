from __future__ import annotations

import unittest

from tests._helpers import run_client


class ResourceExampleTests(unittest.TestCase):
    def test_resources_are_listed_and_read(self) -> None:
        result = run_client("examples/04_resources/client.py")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("resources=demo://config", result.stdout)
        self.assertIn("templates=demo://users/{user_id}", result.stdout)
        self.assertIn("config_server=examples", result.stdout)
        self.assertIn("user_name=Ada Lovelace", result.stdout)
        self.assertIn("user_role=admin", result.stdout)


if __name__ == "__main__":
    unittest.main()
