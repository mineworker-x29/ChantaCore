
from __future__ import annotations

from chanta_core.runtime.agent_runtime import AgentRuntime


class ChatService:
    def __init__(self, runtime: AgentRuntime | None = None) -> None:
        self.runtime = runtime or AgentRuntime()

    def chat(self, user_input: str, session_id: str | None = None) -> str:
        return self.runtime.run(user_input, session_id=session_id).response_text

    def run(self, user_input: str) -> str:
        return self.chat(user_input)
