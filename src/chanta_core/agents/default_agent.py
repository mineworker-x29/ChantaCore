from __future__ import annotations

from chanta_core.agents.profile import AgentProfile
from chanta_core.runtime.capability_contract import build_default_agent_capability_prompt_block


def load_default_agent_profile() -> AgentProfile:
    capability_prompt_block = build_default_agent_capability_prompt_block()
    return AgentProfile(
        agent_id="chanta_core_default",
        name="ChantaCore Default Agent",
        role="trace-aware local runtime agent",
        system_prompt=(
            "You are ChantaCore, a trace-aware runtime agent running through a "
            "local LLM provider. Answer clearly and keep responses concise. "
            "Always provide a non-empty response. In the default chat path, you "
            "can answer from the prompt and assembled OCEL/PIG context, but you "
            "do not have direct filesystem, shell, network, MCP, plugin, or "
            "runtime tool access unless an explicit ChantaCore skill provides it. "
            "If a requested action is unavailable, state that limitation plainly "
            "instead of implying that the action was performed.\n\n"
            f"{capability_prompt_block}"
        ),
        default_temperature=0.7,
        max_tokens=1024,
    )
