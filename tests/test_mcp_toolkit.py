from __future__ import annotations

import sys
import unittest

from langchain_core.tools import ToolException

from tests._helpers import ROOT, load_module


langchain_tools = load_module(
    "examples/_shared/langchain_tools.py",
    "examples_shared_langchain_tools",
)


class MCPToolkitErrorTests(unittest.IsolatedAsyncioTestCase):
    async def test_tool_error_becomes_tool_exception(self) -> None:
        toolkit = langchain_tools.MCPToolkit(
            {
                "tools": langchain_tools.StdioConnection(
                    command=sys.executable,
                    args=[str(ROOT / "examples/02_tools/server.py")],
                    cwd=str(ROOT / "examples/02_tools"),
                )
            }
        )

        tools = await toolkit.get_tools()
        divide = next(tool for tool in tools if tool.name == "divide")

        with self.assertRaises(ToolException) as caught:
            await divide.ainvoke({"a": 10, "b": 0})

        self.assertIn("division by zero", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
