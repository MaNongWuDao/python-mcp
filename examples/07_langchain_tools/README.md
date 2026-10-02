# 07: LangChain / LangGraph 工具集成

## 学习目标

- 使用仓库内的 `MCPToolkit` 把 MCP 工具转换为 LangChain `StructuredTool`。
- 用 LangChain 的 `create_agent()` 执行 MCP 工具并生成最终回答。
- 默认使用确定性的 Fake Chat Model，不读取 API Key、不访问网络。
- 可选通过 `ChatOpenAI` 使用真实模型。

## 离线运行

```powershell
uv run python examples/07_langchain_tools/client.py
```

## 真实模型运行

```powershell
$env:OPENAI_API_KEY="..."; uv run python examples/07_langchain_tools/client.py --real
```

## 关键 API

- `MCPToolkit.get_tools()`：连接 MCP Server 并返回 LangChain 工具。
- `create_agent()`：把模型和工具组装成 LangChain Agent。
- `ainvoke()`：异步运行 Agent 并返回消息历史。
- `GenericFakeChatModel`：离线测试用的确定性模型。

## 预期离线输出

```text
tools=add,multiply
tool_calls=multiply
tool_result=42
final=6 * 7 = 42
```
