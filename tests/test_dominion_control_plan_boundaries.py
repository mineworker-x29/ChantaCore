from __future__ import annotations

from pathlib import Path

from chanta_core.internal_dominion import DominionControlPlanCreateRequest, DominionControlPlanService


def test_control_plan_performs_no_forbidden_later_stage_effects() -> None:
    report = DominionControlPlanService().create_control_plan(DominionControlPlanCreateRequest())
    plan = report.plan

    assert report.static_safety_checked is False
    assert report.preflight_checked is False
    assert report.human_gate_opened is False
    assert report.authorization_created is False
    assert report.dispatch_enabled is False
    assert report.dispatched is False
    assert report.external_runtime_touched is False
    assert report.provider_api_call_performed is False
    assert report.credential_exposed is False
    assert plan is not None
    assert plan.static_safety_checked is False
    assert plan.preflight_checked is False
    assert plan.human_gate_opened is False
    assert plan.authorization_created is False
    assert plan.dispatch_enabled is False
    assert plan.dispatched is False
    assert plan.external_runtime_touched is False
    assert plan.provider_api_call_performed is False
    assert plan.credential_exposed is False
    assert plan.raw_secret_output is False
    assert plan.provider_binding.provider_api_call_performed is False
    assert plan.runtime_binding.runtime_touched is False
    assert plan.capability_binding.dispatch_enabled is False
    assert plan.control_surface_binding is not None
    assert plan.control_surface_binding.dispatch_enabled is False
    assert plan.control_surface_binding.provider_api_call_performed is False


def test_control_plan_source_has_no_forbidden_positive_tokens() -> None:
    text = Path("src/chanta_core/internal_dominion/control_plan.py").read_text(encoding="utf-8")
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
        "runtime_touched=True",
        "provider_api_call_performed=True",
        "dispatch_enabled=True",
        "dispatched=True",
        "static_safety_checked=True",
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


def test_vendor_names_are_not_control_plan_core_logic() -> None:
    text = Path("src/chanta_core/internal_dominion/control_plan.py").read_text(encoding="utf-8")
    for token in ["A360", "Automation Anywhere", "Brity", "UiPath", "Power Automate"]:
        assert token not in text


def test_control_plan_does_not_introduce_private_vera_material() -> None:
    private_persona_token = "Ve" + "ra"
    private_root_token = "ChantaResearchGroup" + "_Members"
    changed_public_files = [
        Path("src/chanta_core/internal_dominion/control_plan.py"),
        Path("docs/versions/v0.23.4_control_plan_target_binding.md"),
        Path("tests/test_dominion_control_plan.py"),
        Path("tests/test_dominion_control_plan_boundaries.py"),
    ]
    for path in changed_public_files:
        text = path.read_text(encoding="utf-8")
        assert private_persona_token not in text
        assert private_root_token not in text
