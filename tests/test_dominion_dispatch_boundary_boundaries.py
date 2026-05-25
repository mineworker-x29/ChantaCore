from __future__ import annotations

from pathlib import Path

from chanta_core.internal_dominion import DominionDispatchBoundaryRequest, DominionDispatchBoundaryService


SOURCE = Path("src/chanta_core/internal_dominion/dispatch_boundary.py")
DOC = Path("docs/versions/v0.23/v0.23.8_authorization_bounded_dispatch_status_outcome_boundary.md")


def test_docs_define_v0_23_8_identity_and_boundaries():
    text = DOC.read_text(encoding="utf-8")

    assert "Authorization / Bounded Dispatch / Status / Outcome Boundary" in text
    assert "권한·제한 Dispatch·상태·결과 경계" in text
    assert "Track: Internal Dominion Foundation" in text
    assert "Authorization boundary is not authorization consumption." in text
    assert "Bounded dispatch boundary is not dispatch." in text
    assert "Status boundary is not live status tracking." in text
    assert "Output boundary is not output fetch." in text
    assert "Outcome boundary is not real external outcome record." in text
    assert "v0.23.9 Internal Dominion Consolidation / Release Readiness" in text
    assert "v0.24.x = Internal Provider / Local Runtime Provider" in text
    assert "v0.25.x = General Agent Usability & Tool Routing" in text
    assert "v0.29.x+ = External Skill / External Provider Adapter Development" in text


def test_dispatch_boundary_source_contains_no_live_runtime_or_provider_calls():
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
        "external_control_dispatched",
        "external_runtime_touched=True",
        "runtime_touched=True",
        "provider_api_call_performed=True",
        "actual_dispatch_performed=True",
        "simulated_dispatch_performed=True",
        "external_run_started=True",
        "authorization_consumed=True",
        "consumption_allowed_in_v0_23_8=True",
        "bounded_dispatch_allowed_now=True",
        "safe_to_dispatch=True",
        "live_status_tracking_started=True",
        "live_output_fetch_started=True",
        "real_external_outcome_recorded=True",
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
        "openai",
        "anthropic",
        "chat.completions",
        "exec(",
        "eval(",
    ]

    for token in forbidden:
        assert token not in text


def test_vendor_names_are_not_runtime_logic_in_dispatch_boundary_source():
    text = SOURCE.read_text(encoding="utf-8")

    for token in ["A360", "Automation Anywhere", "Brity", "UiPath", "Power Automate"]:
        assert token not in text


def test_no_private_material_is_added_to_dispatch_boundary_source_or_docs():
    combined = SOURCE.read_text(encoding="utf-8") + DOC.read_text(encoding="utf-8")
    private_persona_token = "Ve" + "ra material"
    private_path_token = "ChantaResearchGroup" + "_Members"

    assert private_persona_token not in combined
    assert private_path_token not in combined
    assert "raw secrets" in combined


def test_forbidden_effects_block_without_mutating_authorization_or_dispatching():
    report = DominionDispatchBoundaryService().create_boundary(
        DominionDispatchBoundaryRequest(requested_dispatch_note="actual-dispatch external-run authorization-consumption real-outcome")
    )

    assert report.report_status == "blocked"
    assert report.authorization_consumed is False
    assert report.actual_dispatch_performed is False
    assert report.external_run_started is False
    assert report.live_status_tracking_started is False
    assert report.live_output_fetch_started is False
    assert report.real_external_outcome_recorded is False
    assert {item.finding_type for item in report.findings} >= {
        "actual_dispatch_attempted",
        "external_run_started",
        "authorization_consumption_attempted",
        "real_external_outcome_recorded",
    }
