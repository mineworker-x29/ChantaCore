from __future__ import annotations

from pathlib import Path

from chanta_core.internal_dominion import DominionRuntimePreflightRequest, DominionRuntimePreflightService


SOURCE = Path("src/chanta_core/internal_dominion/runtime_preflight.py")
DOC = Path("docs/versions/v0.23/v0.23.6_runtime_preflight_reachability_check.md")


def _report(plan_id: str = "dominion_control_plan:v0.23.4"):
    return DominionRuntimePreflightService().check_preflight(DominionRuntimePreflightRequest(plan_id=plan_id))


def test_runtime_preflight_report_keeps_all_execution_boundaries_disabled() -> None:
    report = _report()
    policy = report.preflight_mode_policy

    assert report.safe_to_dispatch is False
    assert report.live_preflight_performed is False
    assert report.provider_api_call_performed is False
    assert report.external_runtime_touched is False
    assert report.dispatch_enabled is False
    assert report.dispatched is False
    assert report.credential_exposed is False
    assert report.raw_secret_output is False
    assert report.llm_judge_used is False
    assert report.local_runtime_provider_implemented is False
    assert report.general_agent_usability_implemented is False
    assert report.workspace_agent_workbench_implemented is False
    assert report.memory_candidate_continuity_implemented is False
    assert report.external_provider_adapter_implemented is False
    assert report.schumpeter_split_introduced is False
    assert policy.live_provider_api_allowed is False
    assert policy.external_runtime_touch_allowed is False
    assert policy.network_allowed is False
    assert policy.credential_materialization_allowed is False
    assert policy.dispatch_allowed is False
    assert policy.run_creation_allowed is False
    assert policy.shell_allowed is False
    assert policy.local_command_allowed is False
    assert policy.local_runtime_provider_enabled is False
    assert policy.general_agent_usability_enabled is False
    assert policy.llm_judge_allowed is False


def test_runtime_preflight_blocks_premature_execution_and_future_track_markers() -> None:
    request = DominionRuntimePreflightRequest(
        plan_id="dominion_control_plan:v0.23.4",
        strictness=(
            "provider api call performed; external runtime touched; dispatch attempted; live preflight attempted; "
            "local runtime provider attempted; general agent usability attempted; schumpeter split attempted"
        ),
    )
    report = DominionRuntimePreflightService().check_preflight(request)
    finding_types = {item.finding_type for item in report.findings}

    assert report.preflight_status == "blocked"
    assert "provider_api_call_performed" in finding_types
    assert "external_runtime_touched" in finding_types
    assert "dispatch_attempted" in finding_types
    assert "live_preflight_attempted_too_early" in finding_types
    assert "local_runtime_provider_attempted_too_early" in finding_types
    assert "general_agent_usability_attempted_too_early" in finding_types
    assert "schumpeter_split_attempted_too_early" in finding_types


def test_runtime_preflight_detects_migration_continuity_markers() -> None:
    request = DominionRuntimePreflightRequest(
        plan_id="dominion_control_plan:v0.23.4",
        strictness="self_execution; GrowthKernel dependency; vendor hardcoding",
    )
    report = DominionRuntimePreflightService().check_preflight(request)
    finding_types = {item.finding_type for item in report.findings}

    assert "self_execution_legacy_detected" in finding_types
    assert "growthkernel_dependency_detected" in finding_types
    assert "vendor_hardcoding_detected" in finding_types


def test_runtime_preflight_source_has_no_live_execution_imports_or_calls() -> None:
    text = SOURCE.read_text(encoding="utf-8")
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
        "openai",
        "anthropic",
        "completion",
        "chat.completions",
        "exec(",
        "eval(",
    ]

    for token in forbidden:
        assert token not in text


def test_runtime_preflight_source_has_no_positive_execution_boundary_flags() -> None:
    text = SOURCE.read_text(encoding="utf-8")
    forbidden = [
        "external_runtime_touched=True",
        "runtime_touched=True",
        "provider_api_call_performed=True",
        "live_preflight_performed=True",
        "live_provider_api_allowed=True",
        "external_runtime_touch_allowed=True",
        "dispatch_allowed=True",
        "dispatch_enabled=True",
        "dispatched=True",
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
        "local_runtime_provider_enabled=True",
        "local_runtime_provider_implemented=True",
        "general_agent_usability_enabled=True",
        "general_agent_usability_implemented=True",
        "workspace_agent_workbench_implemented=True",
        "memory_candidate_continuity_implemented=True",
        "external_provider_adapter_implemented=True",
        "schumpeter_split_introduced=True",
        "growthkernel_dependency_required=True",
    ]

    for token in forbidden:
        assert token not in text


def test_runtime_preflight_keeps_vendor_names_out_of_core_implementation() -> None:
    text = SOURCE.read_text(encoding="utf-8")

    for vendor in ["A360", "Automation Anywhere", "Brity", "UiPath", "Power Automate"]:
        assert vendor not in text


def test_runtime_preflight_public_artifacts_do_not_include_private_vera_material() -> None:
    source_text = SOURCE.read_text(encoding="utf-8")
    doc_text = DOC.read_text(encoding="utf-8")

    forbidden_tokens = [
        "ChantaResearchGroup" + "_Members",
        "private " + "Ve" + "ra material",
        "vera" + "_chantacore_mode",
    ]
    for token in forbidden_tokens:
        assert token not in source_text
        assert token not in doc_text
