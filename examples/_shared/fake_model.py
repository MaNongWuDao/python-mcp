from __future__ import annotations

from langchain_core.language_models.fake_chat_models import GenericFakeChatModel


class FakeToolCallingModel(GenericFakeChatModel):
    """Fake model that returns pre-scripted tool calls without binding tools."""

    def bind_tools(
        self,
        tools,
        *,
        tool_choice=None,
        **kwargs,
    ):
        del tools, tool_choice, kwargs
        return self
