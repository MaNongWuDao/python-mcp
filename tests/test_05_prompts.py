from __future__ import annotations

import unittest

from tests._helpers import run_client


class PromptExampleTests(unittest.TestCase):
    def test_prompt_demo_lists_and_reads_both_prompts(self) -> None:
        result = run_client("examples/05_prompts/client.py")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("可用提示词: 2 个", result.stdout)
        self.assertIn("读取提示词: explain_code", result.stdout)
        self.assertIn("读取提示词: review_code", result.stdout)


if __name__ == "__main__":
    unittest.main()
