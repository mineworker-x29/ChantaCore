from __future__ import annotations

from chanta_core.agents.profile import AgentProfile


def load_default_agent_profile() -> AgentProfile:
    return AgentProfile(
        agent_id="chanta_core_default",
        name="ChantaCore Default Agent",
        role="trace-aware local runtime agent",
        system_prompt=(
            "You are ChantaCore, a trace-aware runtime agent running through a "
            "local LLM provider. Answer clearly and keep responses concise."
        ),
        default_temperature=0.7,
        max_tokens=384,
    )
