# 08: LangChain / LangGraph 多 Server 调用

## 学习目标

- 建立多个 MCP stdio 连接。
- 使用 `MCPToolkit` 聚合多个 Server 的工具。
- 用 LangChain 的 `create_agent()` 跨 Server 依次调用工具并生成最终回答。
- 默认使用确定性的 Fake Chat Model，不读取 API Key、不访问网络。

## 运行命令

```powershell
uv run python examples/08_multi_server/client.py
```

## 关键 API

- `MCPToolkit(connections)`：接收多个 `StdioConnection` 并聚合工具。
- `MCPToolkit.get_tools()`：连接所有 MCP Server 并返回 LangChain 工具。
- `create_agent()`：把模型和工具组装成 LangChain Agent。

## 预期输出

```text
servers=math,text
tools=add,reverse
tool_calls=add,reverse
tool_results=42; CBA
final=Result: 42 | reversed: CBA
```

本目录有意包含两个 Server 文件（`math_server.py` 与 `text_server.py`），用于演示一个 Agent 在多个 MCP Server 之间依次调用工具。
