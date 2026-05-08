from chanta_core.agents.default_agent import load_default_agent_profile
from chanta_core.runtime.capability_contract import RuntimeCapabilityIntrospectionService


def test_capability_profile_contains_identity_limitations_and_soul_boundary() -> None:
    capability_profile = (
        RuntimeCapabilityIntrospectionService().build_default_agent_profile()
    )
    prompt_block = capability_profile.to_prompt_block()

    assert capability_profile.profile_id.startswith("agent_capability_profile:")
    assert "trace-aware local LLM chat endpoint" in capability_profile.identity_statement
    assert "skill:llm_chat" in capability_profile.current_capability_statement
    assert "does not directly read files" in capability_profile.limitation_statement
    assert "not yet an active Soul or workspace agent" in (
        capability_profile.soul_boundary_statement
    )
    assert "available_now:" in prompt_block
    assert "not_implemented:" in prompt_block
    assert "Do not claim capabilities" in prompt_block


def test_default_agent_prompt_includes_runtime_derived_capability_contract() -> None:
    profile = load_default_agent_profile()

    assert "Runtime capability contract:" in profile.system_prompt
    assert "available_now:" in profile.system_prompt
    assert "metadata_only:" in profile.system_prompt
    assert "disabled_candidates:" in profile.system_prompt
    assert "requires_review:" in profile.system_prompt
    assert "requires_permission:" in profile.system_prompt
    assert "not_implemented:" in profile.system_prompt
    assert "When asked what you can do" in profile.system_prompt


def test_default_agent_prompt_does_not_claim_unavailable_capabilities() -> None:
    profile = load_default_agent_profile()

    assert "do not have direct filesystem" in profile.system_prompt
    assert "MCP connection" in profile.system_prompt
    assert "plugin loading" in profile.system_prompt
    assert "workspace file read" in profile.system_prompt
    assert "active runtime registry updates" in profile.system_prompt
    assert "not yet an active Soul" in profile.system_prompt
    assert "I can read files" not in profile.system_prompt
    assert "I can execute shell" not in profile.system_prompt
    assert "I can connect MCP" not in profile.system_prompt
    assert "I can load plugins" not in profile.system_prompt
