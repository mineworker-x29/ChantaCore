from __future__ import annotations

from pathlib import Path

from chanta_core.internal_dominion import DominionStaticSafetyCheckRequest, DominionStaticSafetyService


def test_static_safety_performs_no_forbidden_later_stage_effects() -> None:
    report = DominionStaticSafetyService().check_static_safety(DominionStaticSafetyCheckRequest())

    assert report.safe_to_dispatch is False
    assert report.preflight_required is True
    assert report.human_gate_required is True
    assert report.authorization_required is True
    assert report.status_tracking_required is True
    assert report.outcome_record_required is True
    assert report.runtime_touched is False
    assert report.provider_api_call_performed is False
    assert report.dispatch_enabled is False
    assert report.dispatched is False
    assert report.credential_exposed is False
    assert report.raw_secret_output is False
    assert report.llm_judge_used is False


def test_static_safety_source_has_no_forbidden_runtime_tokens() -> None:
    text = Path("src/chanta_core/internal_dominion/static_safety.py").read_text(encoding="utf-8")
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
        "openai",
        "anthropic",
        "completion",
        "chat.completions",
        "exec(",
        "eval(",
    ]
    for token in forbidden:
        assert token not in text
    assert "llm_judge_used: bool = False" in text


def test_vendor_names_are_not_static_safety_core_logic() -> None:
    text = Path("src/chanta_core/internal_dominion/static_safety.py").read_text(encoding="utf-8")
    for token in ["A360", "Automation Anywhere", "Brity", "UiPath", "Power Automate"]:
        assert token not in text


def test_static_safety_does_not_introduce_private_persona_material() -> None:
    private_persona_token = "Ve" + "ra"
    private_root_token = "ChantaResearchGroup" + "_Members"
    changed_public_files = [
        Path("src/chanta_core/internal_dominion/static_safety.py"),
        Path("docs/versions/v0.23/v0.23.5_dominion_static_safety_check.md"),
        Path("tests/test_dominion_static_safety.py"),
        Path("tests/test_dominion_static_safety_boundaries.py"),
    ]
    for path in changed_public_files:
        text = path.read_text(encoding="utf-8")
        assert private_persona_token not in text
        assert private_root_token not in text
