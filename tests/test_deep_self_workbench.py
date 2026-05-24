from __future__ import annotations

import subprocess
import sys

from chanta_core.deep_self_introspection import (
    DeepSelfCoverageService,
    DeepSelfSafetyBoundaryStatus,
    DeepSelfSubjectStatusView,
    DeepSelfWorkbenchRequest,
    DeepSelfWorkbenchService,
    SelfCapabilityRegistryAwarenessService,
)


def test_deep_self_workbench_snapshot_builds() -> None:
    snapshot = DeepSelfWorkbenchService().build_snapshot()

    assert snapshot.read_only is True
    assert snapshot.mutation_performed is False
    assert snapshot.coverage
    assert snapshot.subject_statuses
    assert snapshot.safety_boundary.status == "ok"
    assert snapshot.findings_view.total_findings >= 1
    assert snapshot.contradiction_view.open_count == 0
    assert snapshot.ocel_coverage.ocel_coverage_status == "complete"
    assert snapshot.pig_ocpx_status.projection_status == "complete"
    assert snapshot.limitations


def test_coverage_includes_v0210_through_v0217_subjects() -> None:
    coverage = DeepSelfWorkbenchService().build_snapshot().coverage
    by_subject = {row.subject: row for row in coverage}

    for subject in [
        "deep_self_contract",
        "capability_truth",
        "runtime_boundary",
        "policy_gate",
        "trace_integrity",
        "context_projection",
        "candidate_memory_boundary",
        "claim_consistency",
    ]:
        assert subject in by_subject
        row = by_subject[subject]
        assert row.has_model is True
        assert row.has_service is True
        assert row.has_cli is True
        assert row.has_tests is True
        assert row.has_ocel_mapping is True
        assert row.has_pig_projection is True
        assert row.has_ocpx_projection is True
        assert row.has_workbench_visibility is True


def test_subject_status_view_includes_all_deep_self_subjects() -> None:
    statuses = DeepSelfWorkbenchService().build_snapshot().subject_statuses
    by_subject = {item.subject_id: item for item in statuses}

    for subject in [
        "capability_truth",
        "runtime_boundary",
        "policy_gate",
        "trace_integrity",
        "context_projection",
        "candidate_memory_boundary",
        "claim_consistency",
    ]:
        assert subject in by_subject
        assert by_subject[subject].latest_report_id is not None
        assert by_subject[subject].open_finding_count >= 0
        assert by_subject[subject].critical_finding_count >= 0


def test_findings_and_contradiction_views_count_findings() -> None:
    snapshot = DeepSelfWorkbenchService().build_snapshot()

    assert snapshot.findings_view.total_findings == len(snapshot.findings)
    assert snapshot.findings_view.open_findings == len(snapshot.findings)
    assert snapshot.findings_view.critical_count >= 0
    assert snapshot.findings_view.error_count >= 0
    assert snapshot.findings_view.warning_count >= 0
    assert snapshot.findings_view.info_count >= 0
    assert isinstance(snapshot.findings_view.by_subject, dict)
    assert snapshot.contradiction_view.contradiction_status in {"none", "open", "warning", "failed"}


def test_safety_boundary_counts_are_visible_and_safe_by_default() -> None:
    safety = DeepSelfWorkbenchService().build_snapshot().safety_boundary

    assert safety.mutation_enabled_count == 0
    assert safety.permission_grant_enabled_count == 0
    assert safety.policy_mutation_enabled_count == 0
    assert safety.registry_mutation_enabled_count == 0
    assert safety.trace_repair_enabled_count == 0
    assert safety.context_injection_enabled_count == 0
    assert safety.memory_promotion_enabled_count == 0
    assert safety.candidate_promotion_enabled_count == 0
    assert safety.materialization_enabled_count == 0
    assert safety.shell_enabled_count == 0
    assert safety.network_enabled_count == 0
    assert safety.mcp_enabled_count == 0
    assert safety.plugin_enabled_count == 0
    assert safety.external_harness_enabled_count == 0
    assert safety.llm_judge_enabled_count == 0
    assert safety.dangerous_capability_count == 0
    assert safety.status == "ok"


def test_ocel_pig_ocpx_coverage_views_are_complete() -> None:
    snapshot = DeepSelfWorkbenchService().build_snapshot()

    assert snapshot.ocel_coverage.object_type_count > 0
    assert snapshot.ocel_coverage.event_type_count > 0
    assert snapshot.ocel_coverage.relation_type_count > 0
    assert snapshot.ocel_coverage.missing_object_types == []
    assert snapshot.ocel_coverage.missing_event_types == []
    assert snapshot.ocel_coverage.missing_relation_types == []
    assert snapshot.pig_ocpx_status.pig_available is True
    assert snapshot.pig_ocpx_status.pig_missing_subjects == []
    assert snapshot.pig_ocpx_status.ocpx_available is True
    assert snapshot.pig_ocpx_status.ocpx_missing_read_models == []


class _WarningSubjectStatusService:
    def build_subject_statuses(self):
        return [
            DeepSelfSubjectStatusView(
                subject_id="capability_truth",
                subject_name="Capability Truth",
                status="warning",
                latest_report_id="report:warning",
                passed_count=0,
                warning_count=1,
                failed_count=0,
                blocked_count=0,
                open_finding_count=1,
                critical_finding_count=0,
                stale=True,
                limitations=["stale test"],
            )
        ]


class _FailedSubjectStatusService:
    def build_subject_statuses(self):
        return [
            DeepSelfSubjectStatusView(
                subject_id="claim_consistency",
                subject_name="Claim Consistency",
                status="failed",
                latest_report_id="report:failed",
                passed_count=0,
                warning_count=0,
                failed_count=1,
                blocked_count=0,
                open_finding_count=1,
                critical_finding_count=0,
                stale=False,
                limitations=[],
            )
        ]


class _UnsafeSafetyService:
    def inspect_safety_boundary(self):
        return DeepSelfSafetyBoundaryStatus(
            mutation_enabled_count=1,
            permission_grant_enabled_count=0,
            policy_mutation_enabled_count=0,
            registry_mutation_enabled_count=0,
            trace_repair_enabled_count=0,
            context_injection_enabled_count=0,
            memory_promotion_enabled_count=0,
            candidate_promotion_enabled_count=0,
            materialization_enabled_count=0,
            shell_enabled_count=0,
            network_enabled_count=0,
            mcp_enabled_count=0,
            plugin_enabled_count=0,
            external_harness_enabled_count=0,
            llm_judge_enabled_count=0,
            dangerous_capability_count=0,
            status="violation",
        )


def test_workbench_warning_and_stale_subject_generate_findings() -> None:
    snapshot = DeepSelfWorkbenchService(subject_status_service=_WarningSubjectStatusService()).build_snapshot()
    findings = {item.finding_type for item in snapshot.findings}

    assert "subject_stale" in findings
    assert snapshot.findings_view.warning_count >= 1


def test_workbench_violation_for_safety_count_and_failed_claims() -> None:
    unsafe = DeepSelfWorkbenchService(safety_service=_UnsafeSafetyService()).build_snapshot()
    failed = DeepSelfWorkbenchService(subject_status_service=_FailedSubjectStatusService()).build_snapshot()

    assert "safety_boundary_violation" in {item.finding_type for item in unsafe.findings}
    assert "subject_failed" in {item.finding_type for item in failed.findings}


def test_pig_and_ocpx_projection_build_for_workbench() -> None:
    service = DeepSelfWorkbenchService()
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    assert pig["version"] == "v0.21.8"
    assert pig["subject"] == "deep_self_workbench"
    assert "workbench is not correction" in pig["principles"]
    assert "workbench is not approval" in pig["principles"]
    assert "workbench is not promotion" in pig["principles"]
    assert "workbench is not execution" in pig["principles"]
    assert pig["read_only"] is True
    assert pig["mutation_performed"] is False
    assert pig["correction_enabled"] is False
    assert pig["promotion_enabled"] is False
    assert pig["execution_enabled"] is False
    assert pig["shows_subject_status"] is True
    assert pig["shows_findings"] is True
    assert pig["shows_contradictions"] is True
    assert pig["shows_safety_boundary"] is True
    assert ocpx["state"] == "deep_self_introspection_workbench"
    for model in [
        "DeepSelfWorkbenchState",
        "DeepSelfSubjectStatusState",
        "DeepSelfFindingsState",
        "DeepSelfSafetyBoundaryState",
        "DeepSelfCoverageState",
    ]:
        assert model in ocpx["target_read_models"]


def test_workbench_optional_skills_are_read_only_and_previous_skills_remain_implemented() -> None:
    records = {record.skill_id: record for record in SelfCapabilityRegistryAwarenessService().view_registry().records if record.skill_id}

    for skill_id in [
        "skill:deep_self_claim_consistency_check",
        "skill:deep_self_contradiction_register",
        "skill:deep_self_workbench_view",
        "skill:deep_self_audit_view",
        "skill:deep_self_findings_view",
    ]:
        assert records[skill_id].status == "implemented"
        assert records[skill_id].read_only is True
        assert records[skill_id].execution_enabled is False
        assert records[skill_id].canonical_promotion_enabled is False


def test_cli_workbench_sections_work() -> None:
    commands = [
        ["deep-self", "workbench"],
        ["deep-self", "workbench", "--section", "overview"],
        ["deep-self", "workbench", "--section", "capability"],
        ["deep-self", "workbench", "--section", "runtime"],
        ["deep-self", "workbench", "--section", "policy"],
        ["deep-self", "workbench", "--section", "trace"],
        ["deep-self", "workbench", "--section", "context"],
        ["deep-self", "workbench", "--section", "boundary"],
        ["deep-self", "workbench", "--section", "claims"],
        ["deep-self", "workbench", "--section", "contradictions"],
        ["deep-self", "workbench", "--section", "safety"],
        ["deep-self", "workbench", "--section", "coverage"],
    ]
    for command in commands:
        result = subprocess.run(
            [sys.executable, "-m", "chanta_core.cli", *command],
            check=False,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "Deep Self-Introspection Workbench" in result.stdout
        assert "subject_statuses=" in result.stdout
        assert "critical_count=" in result.stdout
        assert "contradiction_open_count=" in result.stdout
        assert "mutation_enabled_count=" in result.stdout
        assert "ocel_coverage_status=" in result.stdout
        assert "v0.21.9_readiness_hint=" in result.stdout
        assert "read_only=true" in result.stdout
        assert "mutation_performed=false" in result.stdout
        assert "raw_prompt_body_printed=False" in result.stdout
        assert "raw_transcript_printed=False" in result.stdout
