# MCP Server 与 MCP Client 调用

学习目标：初始化握手、Server 元数据、能力协商、`ping` 和连接关闭。

## 运行

```powershell
uv run python examples/01_server_client/client.py
```

## 关键 API

- `MCPServer`
- `ClientSession.initialize()`
- `ClientSession.send_ping()`

## 预期输出

```text
server_info=server-client-demo
protocol_version=<协商后的协议版本>
instructions=演示初始化握手、能力协商和 ping
ping=ok
```
