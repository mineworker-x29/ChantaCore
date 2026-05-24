from __future__ import annotations

from pathlib import Path

from chanta_core.internal_dominion import (
    DOMINION_EFFECT_TYPES,
    CapabilityObservationDigestReportService,
    DominionCapabilityObservationRequest,
)


def test_capability_observation_performs_no_forbidden_effects() -> None:
    report = CapabilityObservationDigestReportService().build_report(DominionCapabilityObservationRequest())
    snapshot = report.snapshot

    assert snapshot.dispatch_enabled is False
    assert snapshot.external_runtime_touched is False
    assert snapshot.provider_api_call_performed is False
    assert snapshot.credential_exposed is False
    assert snapshot.raw_secret_output is False
    assert all(descriptor.dispatch_enabled_v0_23_2 is False for descriptor in snapshot.descriptors)
    assert all(descriptor.provider_api_call_performed is False for descriptor in snapshot.descriptors)
    assert all(descriptor.external_runtime_touched is False for descriptor in snapshot.descriptors)
    assert all(candidate.control_request_created is False for candidate in snapshot.candidates)
    assert all(candidate.control_plan_created is False for candidate in snapshot.candidates)
    assert all(candidate.preflight_checked is False for candidate in snapshot.candidates)
    assert all(candidate.human_gate_opened is False for candidate in snapshot.candidates)
    assert all(candidate.dispatch_enabled is False for candidate in snapshot.candidates)
    assert all(candidate.dispatched is False for candidate in snapshot.candidates)


def test_capability_effects_remain_candidate_only_ocel_effects() -> None:
    assert {"read_only_observation", "state_candidate_created"} <= set(DOMINION_EFFECT_TYPES)
    assert "external_runtime_touched" not in DOMINION_EFFECT_TYPES
    assert "external_control_dispatched" not in DOMINION_EFFECT_TYPES


def test_capability_runtime_source_has_no_forbidden_positive_tokens() -> None:
    text = Path("src/chanta_core/internal_dominion/capability.py").read_text(encoding="utf-8")
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
        "dispatch_enabled_v0_23_2=True",
        "dispatched=True",
        "control_request_created=True",
        "control_plan_created=True",
        "preflight_checked=True",
        "human_gate_opened=True",
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


def test_vendor_names_are_not_capability_core_logic() -> None:
    text = Path("src/chanta_core/internal_dominion/capability.py").read_text(encoding="utf-8")
    for token in ["A360", "Automation Anywhere", "Brity", "UiPath", "Power Automate"]:
        assert token not in text
