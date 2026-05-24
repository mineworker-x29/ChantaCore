from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace
import subprocess
import sys

from chanta_core.self_modification_safety import (
    SelfModificationWorkbenchRequest,
    SelfModificationWorkbenchService,
    SelfModificationWorkbenchSourceService,
)
from chanta_core.self_modification_safety.bounded_apply import BoundedPatchApplyReportService
from chanta_core.self_modification_safety.post_apply import (
    PostApplyVerificationReportService,
    PostApplyVerificationRequest,
    PostApplyVerificationSourceService,
    SelfModificationPostApplyVerificationService,
)
from chanta_core.self_modification_safety import SelfModificationBoundedApplyService

from tests.test_self_modification_bounded_apply import _bundle


def _workbench_service(tmp_path: Path, *, include_post_apply: bool = True) -> SelfModificationWorkbenchService:
    source, request, _ = _bundle(tmp_path)
    apply_report = SelfModificationBoundedApplyService(
        report_service=BoundedPatchApplyReportService(source_service=source)
    ).apply_bounded_patch(request).report
    assert apply_report.transaction is not None
    change = apply_report.transaction.file_changes[0]
    post_result = None
    if include_post_apply:
        post_source = PostApplyVerificationSourceService(
            workspace_root=tmp_path,
            apply_reports={apply_report.report_id: apply_report},
            authorizations={request.authorization_id: source.authorizations[request.authorization_id]},
            rollback_plans={request.rollback_plan_id: source.rollback_plans[request.rollback_plan_id]},
        )
        post_result = SelfModificationPostApplyVerificationService(
            report_service=PostApplyVerificationReportService(source_service=post_source)
        ).verify_and_record_outcome(PostApplyVerificationRequest(apply_report_id=apply_report.report_id))
    workbench_source = SelfModificationWorkbenchSourceService(
        requests=[SimpleNamespace(request_id="self_modification_request:test", created_at="2026-05-16T00:00:00Z")],
        patch_candidates=[
            SimpleNamespace(
                patch_candidate_id=request.patch_candidate_id,
                request_id="self_modification_request:test",
                created_at="2026-05-16T00:00:01Z",
            )
        ],
        patch_drafts=list(source.patch_drafts.values()),
        diff_previews=list(source.diff_previews.values()),
        dry_run_reports=list(source.dry_run_reports.values()),
        review_decisions=[
            SimpleNamespace(
                decision_id="human_review_decision:test",
                decision="approve",
                decided_at="2026-05-16T00:00:05Z",
            )
        ],
        apply_gates=list(source.apply_gates.values()),
        authorizations=[source.authorizations[request.authorization_id]],
        rollback_plans=list(source.rollback_plans.values()),
        bounded_apply_reports=[apply_report],
        post_apply_reports=[post_result.verification_report] if post_result else [],
        outcomes=[post_result.outcome_record] if post_result and post_result.outcome_record else [],
        events=[
            {
                "event_id": change.workspace_file_changed_event_id,
                "event_type": "workspace_file_changed",
                "transaction_id": apply_report.transaction.transaction_id,
                "change_id": change.change_id,
                "target_id": change.target_id,
            }
        ],
    )
    return SelfModificationWorkbenchService(source_service=workbench_source)


def test_self_modification_workbench_snapshot_builds_full_pipeline(tmp_path: Path) -> None:
    snapshot = _workbench_service(tmp_path).build_snapshot(SelfModificationWorkbenchRequest())

    assert snapshot.read_only is True
    assert snapshot.mutation_performed is False
    assert snapshot.pipeline_items
    item = snapshot.pipeline_items[0]
    assert item.request_id == "self_modification_request:test"
    assert item.patch_candidate_id == "patch_candidate:test"
    assert item.draft_id == "patch_draft:test"
    assert item.preview_id == "diff_preview:test"
    assert item.dry_run_report_id == "patch_dry_run_report:test"
    assert item.apply_gate_id == "apply_gate_state:test"
    assert item.bounded_apply_report_id is not None
    assert item.transaction_id is not None
    assert item.post_apply_verification_report_id is not None
    assert item.outcome_id is not None
    assert item.current_stage == "outcome"
    assert item.current_status == "completed"
    assert item.next_required_action == "Ready for v0.22.9 consolidation review."


def test_subject_statuses_include_all_self_modification_stages(tmp_path: Path) -> None:
    snapshot = _workbench_service(tmp_path).build_snapshot()
    subject_ids = {item.subject_id for item in snapshot.subject_statuses}

    for subject_id in [
        "subject:modification_request",
        "subject:patch_candidate",
        "subject:diff_preview",
        "subject:patch_static_safety",
        "subject:patch_dry_run",
        "subject:modification_review_gate",
        "subject:patch_apply_gate",
        "subject:bounded_patch_apply",
        "subject:post_apply_verification",
        "subject:modification_outcome",
        "subject:self_modification_workbench",
    ]:
        assert subject_id in subject_ids
    versions = {item.version_introduced for item in snapshot.subject_statuses}
    assert "v0.22.0" in versions
    assert "v0.22.8" in versions


def test_authorization_and_change_views_are_sanitized(tmp_path: Path) -> None:
    snapshot = _workbench_service(tmp_path).build_snapshot()

    assert snapshot.authorizations
    auth = snapshot.authorizations[0]
    assert auth.authorization_status == "consumed"
    assert auth.consumed is True
    assert auth.consumed_by_transaction_id is not None
    assert snapshot.changes
    change = snapshot.changes[0]
    assert change.relative_path == "target.txt"
    assert change.before_hash
    assert change.after_hash
    assert change.workspace_file_changed_event_id
    assert change.post_apply_verification_report_id is not None
    assert change.outcome_id is not None
    assert change.verification_status == "passed"
    assert change.outcome_status == "applied_verified"
    assert change.raw_content_emitted is False


def test_safety_boundary_and_readiness_ready_when_no_blockers(tmp_path: Path) -> None:
    snapshot = _workbench_service(tmp_path).build_snapshot()

    assert snapshot.safety_boundary.file_write_count == 1
    assert snapshot.safety_boundary.bounded_writer_write_count == 1
    assert snapshot.safety_boundary.unauthorized_write_count == 0
    assert snapshot.safety_boundary.apply_without_gate_count == 0
    assert snapshot.safety_boundary.consumed_authorization_reuse_count == 0
    assert snapshot.safety_boundary.rollback_executed_count == 0
    assert snapshot.safety_boundary.shell_executed_count == 0
    assert snapshot.safety_boundary.test_lint_executed_count == 0
    assert snapshot.safety_boundary.llm_judge_count == 0
    assert snapshot.safety_boundary.safety_status == "ok"
    assert snapshot.ocel_coverage.workspace_file_changed_trace_complete is True
    assert snapshot.readiness.readiness_status == "ready"
    assert snapshot.readiness.ready_for_consolidation is True


def test_readiness_warning_when_pending_candidate_exists() -> None:
    service = SelfModificationWorkbenchService(
        source_service=SelfModificationWorkbenchSourceService(
            patch_candidates=[SimpleNamespace(patch_candidate_id="patch_candidate:pending")]
        )
    )

    snapshot = service.build_snapshot()

    assert snapshot.pipeline_items[0].current_stage == "candidate"
    assert snapshot.readiness.readiness_status == "warning"
    assert snapshot.readiness.incomplete_pipeline_count == 1


def test_readiness_blocked_when_unverified_apply_exists(tmp_path: Path) -> None:
    snapshot = _workbench_service(tmp_path, include_post_apply=False).build_snapshot()

    assert snapshot.pipeline_items[0].current_stage == "bounded_apply"
    assert snapshot.readiness.readiness_status == "blocked"
    assert snapshot.readiness.unverified_apply_count == 1


def test_safety_boundary_detects_workspace_change_without_transaction_and_authorization_reuse(tmp_path: Path) -> None:
    source, request, _ = _bundle(tmp_path)
    auth = source.authorizations[request.authorization_id]
    workbench = SelfModificationWorkbenchService(
        source_service=SelfModificationWorkbenchSourceService(
            authorizations=[replace(auth, consumed=True)],
            events=[{"event_id": "workspace_file_changed:test", "event_type": "workspace_file_changed"}],
        )
    )

    snapshot = workbench.build_snapshot()

    assert snapshot.safety_boundary.workspace_file_changed_without_transaction_count == 1
    assert snapshot.safety_boundary.consumed_authorization_reuse_count == 1
    assert snapshot.safety_boundary.safety_status == "violation"
    assert snapshot.readiness.readiness_status == "blocked"


def test_findings_timeline_and_ocel_coverage_build(tmp_path: Path) -> None:
    snapshot = _workbench_service(tmp_path).build_snapshot(SelfModificationWorkbenchRequest(max_recent_items=10))

    assert snapshot.findings_view.total_findings >= 1
    assert "post_apply" in snapshot.findings_view.by_stage
    assert snapshot.timeline
    assert [item.to_dict() for item in snapshot.timeline] == [item.to_dict() for item in snapshot.timeline]
    assert snapshot.ocel_coverage.coverage_status == "complete"
    assert not snapshot.ocel_coverage.required_object_types_missing
    assert not snapshot.ocel_coverage.required_event_types_missing
    assert not snapshot.ocel_coverage.required_relation_types_missing


def test_workbench_pig_ocpx_reports() -> None:
    service = SelfModificationWorkbenchService()
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    assert pig["version"] == "v0.22.8"
    assert pig["subject"] == "self_modification_workbench"
    assert pig["read_only"] is True
    assert pig["mutation_performed"] is False
    assert pig["file_write_performed"] is False
    assert pig["workspace_file_changed_emitted"] is False
    assert pig["rollback_executed"] is False
    assert pig["shell_executed"] is False
    assert pig["test_lint_executed"] is False
    assert pig["llm_judge_enabled"] is False
    assert ocpx["state"] == "self_modification_workbench_snapshot_created"
    assert ocpx["effect_types"] == ["read_only_observation"]
    assert "SelfModificationWorkbenchState" in ocpx["target_read_models"]
    assert "SelfModificationReadinessState" in ocpx["target_read_models"]


def test_workbench_cli_sections_are_visible() -> None:
    for command in [
        ["workbench"],
        ["workbench", "--section", "overview"],
        ["workbench", "--section", "pipeline"],
        ["workbench", "--section", "safety"],
        ["workbench", "--section", "readiness"],
    ]:
        completed = subprocess.run(
            [sys.executable, "-m", "chanta_core.cli", "self-modification", *command],
            check=False,
            capture_output=True,
            text=True,
        )
        assert completed.returncode == 0
        assert "layer=self_modification_safety" in completed.stdout
        assert "pipeline_status=" in completed.stdout
        assert "current_stage=" in completed.stdout
        assert "next_required_action=" in completed.stdout
        assert "safety_status=" in completed.stdout
        assert "workspace_file_changed_trace_complete=" in completed.stdout
        assert "ready_for_v0.22.9=" in completed.stdout
        assert "read_only=true" in completed.stdout
        assert "mutation_performed=false" in completed.stdout
        assert "raw_secrets_printed=False" in completed.stdout
