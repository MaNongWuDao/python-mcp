# MCP 代码实践

Python MCP SDK `2.2.0` 示例集，覆盖 Server/Client、工具、结构化输出、资源、提示词、生命周期、LangChain/LangGraph 和传输模式。

## 快速开始

```powershell
uv sync
uv run python scripts/run_all.py
```

## 示例

| 目录 | 学习重点 | 运行 |
| --- | --- | --- |
| `examples/01_server_client` | 初始化、能力、ping | `uv run python examples/01_server_client/client.py` |
| `examples/02_tools` | 工具发现、参数、进度、错误 | `uv run python examples/02_tools/client.py` |
| `examples/03_structured_output` | Pydantic 与 structuredContent | `uv run python examples/03_structured_output/client.py` |
| `examples/04_resources` | 静态资源和 URI 模板 | `uv run python examples/04_resources/client.py` |
| `examples/05_prompts` | 提示词发现与参数渲染 | `uv run python examples/05_prompts/client.py` |
| `examples/06_lifespan` | 启动、共享状态和关闭 | `uv run python examples/06_lifespan/client.py` |
| `examples/07_langchain_tools` | LangChain/LangGraph 单 Server | `uv run python examples/07_langchain_tools/client.py` |
| `examples/08_multi_server` | LangGraph 多 Server 调用 | `uv run python examples/08_multi_server/client.py` |
| `examples/09_transport_modes` | stdio、SSE、Streamable HTTP | `uv run python examples/09_transport_modes/client.py` |

## OpenAI 可选路径

默认 LangChain 示例使用 Fake Model，不需要外部网络或 API Key。要使用真实模型：

```powershell
$env:OPENAI_API_KEY="..."
uv run python examples/07_langchain_tools/client.py --real
```

## 测试

```powershell
uv run python -m unittest discover -s tests -v
```
