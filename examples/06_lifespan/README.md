# 06 Lifespan：服务生命周期

## 学习目标

- 在 MCP 服务启动时初始化 lifespan 状态。
- 在同一条连接的多个请求之间复用 lifespan 状态。
- 使用 `Context.request_context.lifespan_context` 访问请求级上下文中的共享状态。
- 在服务关闭时执行清理逻辑。

## 运行

```powershell
uv run python examples/06_lifespan/client.py
```

## 关键 API

- `MCPServer(..., lifespan=...)`：注册服务启动和关闭时执行的生命周期管理器。
- `Context.request_context.lifespan_context`：在工具处理函数中读取当前会话的 lifespan 状态。
- `session.call_tool()`：连续调用 `remember`，验证状态在同一个会话内持续存在。

## 预期输出

输出应包含：

```text
started=true
first_count=1
second_count=2
values=alpha,beta
```
