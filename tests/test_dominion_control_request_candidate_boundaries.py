from __future__ import annotations

from pathlib import Path

from chanta_core.internal_dominion import (
    DOMINION_EFFECT_TYPES,
    DominionControlRequestCandidateService,
    DominionControlRequestCreateRequest,
)


def test_control_request_candidate_performs_no_forbidden_later_stage_effects() -> None:
    report = DominionControlRequestCandidateService().create_request_and_candidate(
        DominionControlRequestCreateRequest(goal_text="observe status", requested_action_verb="observe")
    )
    candidate = report.action_candidate

    assert report.control_plan_created is False
    assert report.preflight_checked is False
    assert report.human_gate_opened is False
    assert report.authorization_created is False
    assert report.dispatched is False
    assert report.external_runtime_touched is False
    assert report.provider_api_call_performed is False
    assert report.credential_exposed is False
    assert report.request.control_plan_created is False
    assert report.request.preflight_checked is False
    assert report.request.human_gate_opened is False
    assert report.request.authorization_created is False
    assert report.request.dispatched is False
    assert report.request.external_runtime_touched is False
    assert report.request.provider_api_call_performed is False
    assert candidate is not None
    assert candidate.control_plan_created is False
    assert candidate.target_bound is False
    assert candidate.preflight_checked is False
    assert candidate.human_gate_opened is False
    assert candidate.authorization_created is False
    assert candidate.dispatch_enabled is False
    assert candidate.dispatched is False
    assert candidate.external_runtime_touched is False
    assert candidate.provider_api_call_performed is False


def test_control_request_effects_remain_candidate_only_ocel_effects() -> None:
    assert {"read_only_observation", "state_candidate_created"} <= set(DOMINION_EFFECT_TYPES)
    assert "external_runtime_touched" not in DOMINION_EFFECT_TYPES
    assert "external_control_dispatched" not in DOMINION_EFFECT_TYPES


def test_control_runtime_source_has_no_forbidden_positive_tokens() -> None:
    text = Path("src/chanta_core/internal_dominion/control.py").read_text(encoding="utf-8")
    forbidden = [
        "requests.",
        "httpx",
        "urllib",
        "aiohttp",
        "mcp.connect",
        "plugin.load",
        "subprocess",
        "os.system",
        "shell=True",
        "external_control_dispatched",
        "external_runtime_touched=True",
        "provider_api_call_performed=True",
        "dispatch_enabled=True",
        "dispatched=True",
        "control_plan_created=True",
        "target_bound=True",
        "preflight_checked=True",
        "human_gate_opened=True",
        "authorization_created=True",
        "credential_value_stored=True",
        "credential_value_output=True",
        "credential_exposed=True",
        "raw_secret_output=True",
        "network_enabled=True",
        "mcp_enabled=True",
        "plugin_enabled=True",
        "shell_enabled=True",
        "local_command_enabled=True",
        "growthkernel_dependency_required=True",
        "llm_judge",
        "openai",
        "anthropic",
        "completion",
        "chat.completions",
        "exec(",
        "eval(",
    ]
    for token in forbidden:
        assert token not in text


def test_vendor_names_are_not_control_core_logic() -> None:
    text = Path("src/chanta_core/internal_dominion/control.py").read_text(encoding="utf-8")
    for token in ["A360", "Automation Anywhere", "Brity", "UiPath", "Power Automate"]:
        assert token not in text
