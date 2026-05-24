from contextlib import redirect_stdout
from io import StringIO

from chanta_core.internal_dominion import InternalDominionConsolidationService, InternalDominionRegistryService
from chanta_core.cli.main import main


def test_workbench_and_consolidation_skills_are_read_only_implemented():
    contracts = InternalDominionRegistryService().list_skill_contracts()
    by_id = {item["skill_id"]: item for item in contracts}

    assert by_id["skill:dominion_workbench_view"]["stub"] is False
    assert by_id["skill:dominion_workbench_view"]["consolidation_only"] is True
    assert by_id["skill:dominion_workbench_view"]["workbench_snapshot_only"] is True
    assert by_id["skill:dominion_workbench_view"]["read_only"] is True
    assert by_id["skill:dominion_consolidation_view"]["stub"] is False
    assert by_id["skill:dominion_consolidation_view"]["consolidation_only"] is True
    assert by_id["skill:dominion_consolidation_view"]["release_readiness_only"] is True
    assert by_id["skill:dominion_consolidation_view"]["read_only"] is True

    for skill_id in [
        "skill:dominion_contract_view",
        "skill:dominion_runtime_inventory",
        "skill:dominion_capability_observe",
        "skill:dominion_capability_digest",
        "skill:dominion_control_request_create",
        "skill:dominion_action_candidate_create",
        "skill:dominion_control_plan_create",
        "skill:dominion_target_binding",
        "skill:dominion_static_safety_check",
        "skill:dominion_runtime_preflight",
        "skill:dominion_review_gate",
        "skill:dominion_authorization_create",
        "skill:dominion_bounded_dispatch",
        "skill:dominion_run_status_track",
        "skill:dominion_run_output_fetch",
        "skill:dominion_outcome_record",
    ]:
        assert by_id[skill_id]["stub"] is False
        assert by_id[skill_id]["non_dispatching"] is True
        assert by_id[skill_id]["provider_api_call_enabled"] is False
        assert by_id[skill_id]["external_runtime_touch_enabled"] is False
        assert by_id[skill_id]["local_runtime_provider_enabled"] is False
        assert by_id[skill_id]["general_agent_usability_enabled"] is False


def test_no_goal_drift_flags_remain_false():
    report = InternalDominionConsolidationService().consolidate()

    assert report.safe_to_dispatch is False
    assert report.provider_api_call_performed is False
    assert report.external_runtime_touched is False
    assert report.dispatch_performed is False
    assert report.authorization_consumed is False
    assert report.live_status_tracking_started is False
    assert report.live_output_fetch_started is False
    assert report.real_external_outcome_recorded is False
    assert report.local_runtime_provider_implemented is False
    assert report.general_agent_usability_implemented is False
    assert report.workspace_agent_workbench_implemented is False
    assert report.memory_candidate_continuity_implemented is False
    assert report.external_provider_adapter_implemented is False
    assert report.schumpeter_split_introduced is False
    assert report.credential_exposed is False
    assert report.raw_secret_output is False
    assert report.llm_judge_used is False


def test_finding_types_cover_migration_continuity_markers():
    service = InternalDominionConsolidationService()
    marker_to_finding = {
        "growthkernel_dependency": "growthkernel_dependency_detected",
        "vendor_hardcoding": "vendor_hardcoding_detected",
        "premature_local_runtime_provider": "local_runtime_provider_premature",
        "premature_general_agent_usability": "general_agent_usability_premature",
        "premature_external_provider_adapter": "external_provider_adapter_premature",
        "premature_schumpeter_split": "schumpeter_split_premature",
    }

    for marker, finding_type in marker_to_finding.items():
        report = service.build_report({"markers": [marker]})
        assert report.release_status == "blocked"
        assert any(item.finding_type == finding_type for item in report.findings)


def test_cli_consolidation_views_are_sanitized():
    commands = [
        ["dominion", "consolidate"],
        ["dominion", "release-manifest"],
        ["dominion", "readiness"],
        ["dominion", "safety-boundary"],
        ["dominion", "roadmap-boundary"],
        ["dominion", "gaps"],
        ["dominion", "workbench"],
    ]

    for command in commands:
        buffer = StringIO()
        with redirect_stdout(buffer):
            exit_code = main(command)
        assert exit_code == 0
        output = buffer.getvalue()
        assert "OCEL-native Internal Dominion Foundation v1" in output or "release_status=" in output
        assert "ready_for_v0_25=False" in output or command[-1] not in {"consolidate", "readiness"}
        assert "safe_to_dispatch=False" in output or command[-1] not in {"consolidate", "readiness"}
        assert "credential_value" not in output
        assert "raw_secret" not in output
        assert "D:\\" not in output


def test_cli_summary_contains_required_release_readiness_flags():
    buffer = StringIO()
    with redirect_stdout(buffer):
        exit_code = main(["dominion", "consolidate"])

    assert exit_code == 0
    output = buffer.getvalue()
    assert "release_name=OCEL-native Internal Dominion Foundation v1" in output
    assert "release_status=releasable" in output
    assert "readiness_status=ready" in output
    assert "ready_for_v0_24=True" in output
    assert "ready_for_v0_25=False" in output
    assert "safe_to_dispatch=False" in output
    assert "provider_api_call_performed=False" in output
    assert "external_runtime_touched=False" in output
    assert "dispatch_performed=False" in output
    assert "authorization_consumed=False" in output
    assert "live_status_tracking_started=False" in output
    assert "live_output_fetch_started=False" in output
    assert "real_external_outcome_recorded=False" in output
    assert "local_runtime_provider_implemented=False" in output
    assert "general_agent_usability_implemented=False" in output
    assert "external_provider_adapter_implemented=False" in output
    assert "schumpeter_split_introduced=False" in output
    assert "next_track_recommendation=v0.24.x Internal Provider / Local Runtime Provider" in output
