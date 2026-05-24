from __future__ import annotations

from pathlib import Path

from chanta_core.internal_dominion import (
    APPROVAL_PHRASE,
    DominionHumanReviewGateService,
    DominionHumanReviewRequestCreateRequest,
)


SOURCE = Path("src/chanta_core/internal_dominion/human_review_gate.py")
DOC = Path("docs/versions/v0.23.7_human_review_dominion_gate.md")


def _report(**kwargs):
    request = DominionHumanReviewRequestCreateRequest(
        preflight_report_id=kwargs.pop("preflight_report_id", "dominion_runtime_preflight_report:v0.23.6"),
        requested_review_decision=kwargs.pop("decision", "approve"),
        approval_phrase=kwargs.pop("phrase", APPROVAL_PHRASE),
        decision_rationale=kwargs.pop("rationale", "operator reviewed declared readiness"),
        strictness=kwargs.pop("strictness", "standard"),
    )
    return DominionHumanReviewGateService().review_and_gate(request)


def test_gate_report_keeps_all_execution_boundaries_disabled() -> None:
    report = _report()
    authorization = report.authorization

    assert report.safe_to_dispatch is False
    assert report.bounded_dispatch_allowed_now is False
    assert report.authorization_consumed is False
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
    assert authorization is not None
    assert authorization.single_use is True
    assert authorization.consumed is False
    assert authorization.dispatch_performed is False
    assert authorization.external_runtime_touched is False
    assert authorization.provider_api_call_performed is False
    assert authorization.credential_exposed is False


def test_gate_detects_migration_and_premature_track_markers() -> None:
    report = _report(
        strictness=(
            "self_execution; GrowthKernel dependency; vendor hardcoding; "
            "authorization consumed; local runtime provider attempted; "
            "general agent usability attempted; schumpeter split attempted"
        )
    )
    finding_types = {item.finding_type for item in report.findings}

    assert "self_execution_legacy_detected" in finding_types
    assert "growthkernel_dependency_detected" in finding_types
    assert "vendor_hardcoding_detected" in finding_types
    assert "authorization_consumed_too_early" in finding_types
    assert "premature_local_runtime_provider_detected" in finding_types
    assert "premature_general_agent_usability_detected" in finding_types
    assert "schumpeter_split_detected" in finding_types


def test_gate_source_has_no_live_execution_imports_or_calls() -> None:
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


def test_gate_source_has_no_positive_execution_boundary_flags() -> None:
    text = SOURCE.read_text(encoding="utf-8")
    forbidden = [
        "external_runtime_touched=True",
        "runtime_touched=True",
        "provider_api_call_performed=True",
        "live_preflight_performed=True",
        "dispatch_allowed=True",
        "dispatch_enabled=True",
        "dispatched=True",
        "bounded_dispatch_allowed_now=True",
        "safe_to_dispatch=True",
        "authorization_consumed=True",
        "run_status_tracking_started=True",
        "output_fetch_started=True",
        "outcome_recorded=True",
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


def test_gate_keeps_vendor_names_out_of_core_implementation() -> None:
    text = SOURCE.read_text(encoding="utf-8")

    for vendor in ["A360", "Automation Anywhere", "Brity", "UiPath", "Power Automate"]:
        assert vendor not in text


def test_gate_public_artifacts_do_not_include_private_vera_material() -> None:
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
