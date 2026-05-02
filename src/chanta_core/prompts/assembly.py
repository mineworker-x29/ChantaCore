from __future__ import annotations

from chanta_core.agents.profile import AgentProfile
from chanta_core.llm.types import ChatMessage
from chanta_core.runtime.execution_context import ExecutionContext


class PromptAssemblyService:
    def assemble(
        self,
        context: ExecutionContext,
        profile: AgentProfile,
    ) -> list[ChatMessage]:
        return [
            {"role": "system", "content": profile.system_prompt},
            {"role": "user", "content": context.user_input},
        ]
