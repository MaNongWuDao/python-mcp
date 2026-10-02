"""最小 MCP Server：只演示初始化元数据和连接存活。"""

from mcp.server.mcpserver import MCPServer


server = MCPServer(
    name="server-client-demo",
    title="MCP Server 与 Client 调用",
    description="演示初始化握手、能力协商和安全关闭。",
    instructions="演示初始化握手、能力协商和 ping",
    version="1.0.0",
)


if __name__ == "__main__":
    server.run(transport="stdio")
