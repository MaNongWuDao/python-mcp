from __future__ import annotations

from pydantic import BaseModel

from mcp.server.mcpserver import MCPServer


class UserProfile(BaseModel):
    user_id: str
    name: str
    role: str


server = MCPServer(name="resources-demo", version="1.0.0")


@server.resource(
    "demo://config",
    name="config",
    description="服务配置",
    mime_type="application/json",
)
def config_resource() -> dict[str, object]:
    return {
        "server": "examples",
        "resource_type": "static",
        "features": ["tools", "resources", "prompts"],
    }


@server.resource(
    "demo://users/{user_id}",
    name="user_profile",
    description="按用户编号读取资料",
    mime_type="application/json",
)
def user_profile(user_id: str) -> UserProfile:
    names = {
        "1": "Ada Lovelace",
        "2": "Grace Hopper",
    }
    return UserProfile(
        user_id=user_id,
        name=names.get(user_id, f"User {user_id}"),
        role="admin" if user_id == "1" else "developer",
    )


if __name__ == "__main__":
    server.run(transport="stdio")
