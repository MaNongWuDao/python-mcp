# MCP 资源定义与读取

这是一个可直接运行的最小示例，覆盖 MCP 资源的：

- 静态资源：使用 `demo://config` 暴露服务配置。
- URI 模板：使用 `demo://users/{user_id}` 按参数读取用户资料。
- MIME 类型：为 JSON 内容声明 `application/json`。
- 发现与读取：客户端调用 `list_resources()`、`list_resource_templates()` 和 `read_resource()`。

## 运行

先在项目根目录安装依赖：

```powershell
uv sync
```

运行客户端。客户端会自动以子进程方式启动 `server.py`：

```powershell
uv run python examples/04_resources/client.py
```

预期输出包含：

```text
resources=demo://config
templates=demo://users/{user_id}
config_server=examples
user_name=Ada Lovelace
user_role=admin
```

## 关键 API

- `@server.resource()`：注册静态资源或 URI 模板资源。
- `session.list_resources()`：列出静态资源。
- `session.list_resource_templates()`：列出 URI 模板。
- `session.read_resource(uri)`：按 URI 读取资源内容。
