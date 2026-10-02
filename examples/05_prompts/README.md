# MCP 提示词定义与读取

这是一个可直接运行的最小示例，覆盖 MCP 提示词的：

- 定义：使用 `@server.prompt()` 注册同步和异步提示词。
- 发现：客户端调用 `session.list_prompts()`。
- 读取：客户端调用 `session.get_prompt(name, arguments=...)`。
- 参数：展示必填参数和带默认值的可选参数。
- 消息：展示 `UserMessage` 和 `AssistantMessage`。

## 运行环境

- Python 3.11 至 3.13
- MCP Python SDK `2.2.0`

项目固定使用 SDK 2.x。SDK 2.x 已将旧版 `FastMCP` 改名为 `MCPServer`，因此本示例使用：

```python
from mcp.server.mcpserver import MCPServer
```

如果课程或旧项目仍使用 SDK 1.x，对应导入通常是：

```python
from mcp.server.fastmcp import FastMCP
```

## 运行

先安装依赖：

```powershell
uv sync
```

启动客户端。客户端会自动以子进程方式启动 `server.py`：

```powershell
uv run examples/05_prompts/client.py
```

也可以直接使用已创建的虚拟环境：

```powershell
.\.venv\Scripts\python.exe examples\05_prompts\client.py
```

预期输出包含已注册的两个提示词、它们的参数，以及使用示例参数渲染后的消息内容。
