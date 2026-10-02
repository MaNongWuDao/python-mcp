# 03 Structured Output：结构化输出

## 学习目标

- 使用 Pydantic 模型声明工具的输出 Schema。
- 使用嵌套模型表达结构化字段。
- 从 `CallToolResult.structured_content`（协议字段 `structuredContent`）读取结构化内容。
- 验证文本内容与结构化输出一致。

## 运行

```powershell
uv run python examples/03_structured_output/client.py
```

## 关键 API

- `@server.tool(structured_output=True)`：声明工具返回结构化输出。
- `session.list_tools()`：发现服务端提供的工具。
- `session.call_tool()`：调用工具并接收结果。
- `CallToolResult.structured_content`（协议字段 `structuredContent`）：读取按输出 Schema 校验的结构化内容。

## 预期输出

输出应包含：

```text
title=Quarterly Report
score=97.5
tags=python,mcp
owner=Ada
content_matches_structured=true
```
