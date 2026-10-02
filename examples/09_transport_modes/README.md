# 传输模式

## 学习目标

- 使用 `stdio`、SSE 和 Streamable HTTP 三种传输方式运行同一个 MCP Server。
- 掌握不同传输对应的客户端 API：stdio 使用共享的 `open_stdio_session()` 辅助函数，HTTP 使用 `sse_client`、`streamable_http_client`。
- 通过 `MCPServer.run(transport=...)` 切换服务端传输模式。
- 验证 HTTP 服务进程在退出后能够被正确清理。

## 运行命令

```powershell
uv run python examples/09_transport_modes/client.py
```

## 关键 API

- `open_stdio_session()`（共享辅助，内部使用 `stdio_client`）
- `sse_client`
- `streamable_http_client`
- `MCPServer.run(transport=...)`

## 预期输出

```text
[stdio] echo=stdio:hello
[sse] echo=sse:hello
[streamable-http] echo=streamable-http:hello
```

## 使用建议

- 本地子进程优先使用 `stdio`，简单且无网络端口占用。
- 新的 HTTP 集成优先使用 Streamable HTTP。
- SSE 保留用于兼容旧版 HTTP 客户端。
