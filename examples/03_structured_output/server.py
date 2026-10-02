from __future__ import annotations

from pydantic import BaseModel, Field

from mcp.server.mcpserver import MCPServer


class ReportDetails(BaseModel):
    owner: str
    reviewed: bool
    notes: list[str] = Field(default_factory=list)


class Report(BaseModel):
    title: str
    score: float
    tags: list[str]
    details: ReportDetails


server = MCPServer(name="structured-output-demo", version="1.0.0")


@server.tool(structured_output=True)
def build_report(topic: str, score: float) -> Report:
    """返回可由客户端按输出 Schema 校验的 Pydantic 对象。"""
    return Report(
        title=f"{topic} Report",
        score=score,
        tags=["python", "mcp"],
        details=ReportDetails(
            owner="Ada",
            reviewed=True,
            notes=["schema validated", "nested object"],
        ),
    )


if __name__ == "__main__":
    server.run(transport="stdio")
