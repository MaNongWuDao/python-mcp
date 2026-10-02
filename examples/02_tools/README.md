# 02 Tools：工具调用

## 学习目标

- 使用 `@server.tool()` 注册可自动发现的工具。
- 调用同步工具和异步工具，并传入类型化参数。
- 使用 `Context.report_progress()` 报告工具执行进度。
- 使用 `ToolError` 返回可预期的业务错误。

## 运行

```powershell
uv run python examples/02_tools/client.py
```

## 关键 API

- `@server.tool()`：声明工具及其参数模型。
- `session.list_tools()`：发现服务端提供的工具。
- `session.call_tool()`：调用工具并接收结果或错误。
- `Context.report_progress()`：向客户端报告异步任务进度。
- `ToolError`：将预期业务错误作为工具错误返回。

## 预期输出

输出应包含：

```text
tools=add,divide,slow_echo
add=42
progress=1/2
progress=2/2
slow_echo=HELLO MCP
divide_error=division by zero
```
