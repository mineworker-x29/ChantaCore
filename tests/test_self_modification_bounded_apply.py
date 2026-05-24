from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import subprocess
import sys

from chanta_core.self_modification_safety import (
    ApplyGateAuthorization,
    ApplyGatePreconditionCheck,
    ApplyGateState,
    BoundedPatchApplyReportService,
    BoundedPatchApplyRequest,
    BoundedPatchApplySourceService,
    BoundedWorkspaceWriter,
    DiffPreviewArtifact,
    PatchAnchorRef,
    PatchDraft,
    PatchDryRunCheckRequest,
    PatchDryRunEnginePolicy,
    PatchDryRunOperationResult,
    PatchDryRunReport,
    PatchDryRunTargetSnapshot,
    PatchOperationDraft,
    PatchTargetContextRef,
    RollbackPlanDescriptor,
    SelfModificationBoundedApplyService,
    SelfModificationRegistryService,
)
from chanta_core.self_modification_safety.bounded_apply import CONFIRMATION_PHRASE


def _hash_text(text: str) -> str:
    import hashlib

    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _bundle(tmp_path: Path, *, content: str = "alpha\n") -> tuple[BoundedPatchApplySourceService, BoundedPatchApplyRequest, Path]:
    target = tmp_path / "target.txt"
    target.write_text(content, encoding="utf-8", newline="")
    before_hash = _hash_text(content)
    target_id = "target:workspace_file"
    patch_candidate_id = "patch_candidate:test"
    draft_id = "patch_draft:test"
    preview_id = "diff_preview:test"
    dry_run_id = "patch_dry_run_report:test"
    static_id = "patch_static_safety_report:test"
    rollback_id = "rollback_plan_descriptor:test"
    gate_id = "apply_gate_state:test"
    auth_id = "apply_gate_authorization:test"
    context = PatchTargetContextRef(
        context_id="patch_target_context_ref:test",
        target_id=target_id,
        target_type="workspace_file",
        relative_path="target.txt",
        content_available=True,
        content_source="bounded_text_read",
        line_range_start=1,
        line_range_end=1,
        truncated=False,
        redacted=False,
        private_boundary_risk=False,
        evidence_refs=[],
    )
    anchor = PatchAnchorRef(
        anchor_id="patch_anchor_ref:test",
        target_id=target_id,
        relative_path="target.txt",
        anchor_type="eof",
        anchor_text_preview=None,
        line_start=1,
        line_end=1,
        confidence="high",
        ambiguous=False,
        evidence_refs=[],
    )
    operation = PatchOperationDraft(
        operation_id="patch_operation_draft:test",
        operation_type="append_block",
        target_ref={"target_id": target_id, "relative_path": "target.txt"},
        anchor_ref=anchor,
        old_text_preview=None,
        new_text_preview="beta",
        rationale="test append",
        added_line_count=1,
        removed_line_count=0,
        operation_status="drafted",
    )
    draft = PatchDraft(
        draft_id=draft_id,
        patch_candidate_id=patch_candidate_id,
        request_id="self_modification_request:test",
        created_at="2026-05-16T00:00:00Z",
        target_context_refs=[context],
        anchors=[anchor],
        operations=[operation],
        findings=[],
    )
    preview = DiffPreviewArtifact(
        preview_id=preview_id,
        draft_id=draft_id,
        patch_candidate_id=patch_candidate_id,
        created_at="2026-05-16T00:00:00Z",
        preview_format="summary",
        target_refs=[{"target_id": target_id, "relative_path": "target.txt"}],
        hunk_previews=[],
        findings=[],
        preview_text_sanitized="append one sanitized line",
        truncated=False,
        redacted=False,
    )
    snapshot = PatchDryRunTargetSnapshot(
        snapshot_id="patch_dry_run_target_snapshot:test",
        target_id=target_id,
        relative_path="target.txt",
        content_available=True,
        snapshot_source="safe_workspace_read",
        content_hash_before=before_hash,
        byte_count=len(content.encode("utf-8")),
        line_count=1,
        encoding="utf-8",
        line_ending="\n",
        truncated=False,
        redacted=False,
        private_boundary_risk=False,
        secret_risk=False,
        generated_file_risk=False,
    )
    dry_run = PatchDryRunReport(
        report_id=dry_run_id,
        created_at="2026-05-16T00:00:00Z",
        request=PatchDryRunCheckRequest(patch_candidate_id=patch_candidate_id, draft_id=draft_id, preview_id=preview_id),
        patch_candidate_id=patch_candidate_id,
        draft_id=draft_id,
        preview_id=preview_id,
        static_safety_report_id=static_id,
        engine_policy=PatchDryRunEnginePolicy(),
        target_snapshots=[snapshot],
        operation_results=[
            PatchDryRunOperationResult(
                result_id="patch_dry_run_operation_result:test",
                operation_id=operation.operation_id,
                target_id=target_id,
                operation_type=operation.operation_type,
                anchor_check=None,
                would_apply_in_memory=True,
                applied_in_memory=True,
                conflict_count=0,
                conflicts=[],
                resulting_content_hash=_hash_text("alpha\nbeta"),
                resulting_line_count=2,
                result_status="passed",
            )
        ],
        findings=[],
        checked_operation_count=1,
        passed_operation_count=1,
        warning_operation_count=0,
        failed_operation_count=0,
        blocked_operation_count=0,
        conflict_count=0,
        dry_run_status="passed",
        eligible_for_review=True,
    )
    rollback = RollbackPlanDescriptor(
        rollback_plan_id=rollback_id,
        patch_candidate_id=patch_candidate_id,
        draft_id=draft_id,
        preview_id=preview_id,
        plan_type="reverse_patch",
        rollback_possible=True,
        rollback_scope="same_file",
        before_snapshot_refs=[{"target_id": target_id}],
        reverse_operation_refs=[{"operation_id": operation.operation_id}],
        limitations=[],
    )
    precondition = ApplyGatePreconditionCheck(
        check_id="apply_gate_precondition_check:test",
        patch_candidate_id=patch_candidate_id,
        draft_id=draft_id,
        preview_id=preview_id,
        static_safety_report_id=static_id,
        dry_run_report_id=dry_run_id,
        review_decision_id="human_review_decision:test",
        static_safety_passed=True,
        dry_run_passed=True,
        eligible_for_review=True,
        review_approved=True,
        rollback_plan_available=True,
        private_boundary_clear=True,
        secret_boundary_clear=True,
        target_still_within_scope=True,
        apply_gate_allowed=True,
        failed_preconditions=[],
        warning_preconditions=[],
        evidence_refs=[],
    )
    authorization = ApplyGateAuthorization(
        authorization_id=auth_id,
        apply_gate_id=gate_id,
        patch_candidate_id=patch_candidate_id,
        draft_id=draft_id,
        preview_id=preview_id,
        dry_run_report_id=dry_run_id,
        review_decision_id="human_review_decision:test",
        rollback_plan_id=rollback_id,
    )
    gate = ApplyGateState(
        apply_gate_id=gate_id,
        created_at="2026-05-16T00:00:00Z",
        patch_candidate_id=patch_candidate_id,
        draft_id=draft_id,
        preview_id=preview_id,
        static_safety_report_id=static_id,
        dry_run_report_id=dry_run_id,
        review_decision_id="human_review_decision:test",
        rollback_plan_id=rollback_id,
        precondition_check=precondition,
        authorization=authorization,
        gate_status="open",
        review_approved=True,
        apply_gate_opened=True,
        eligible_for_bounded_apply=True,
    )
    source = BoundedPatchApplySourceService(
        workspace_root=tmp_path,
        apply_gates={gate_id: gate},
        authorizations={auth_id: authorization},
        patch_drafts={draft_id: draft},
        diff_previews={preview_id: preview},
        dry_run_reports={dry_run_id: dry_run},
        rollback_plans={rollback_id: rollback},
    )
    request = BoundedPatchApplyRequest(
        apply_gate_id=gate_id,
        authorization_id=auth_id,
        patch_candidate_id=patch_candidate_id,
        draft_id=draft_id,
        preview_id=preview_id,
        dry_run_report_id=dry_run_id,
        static_safety_report_id=static_id,
        rollback_plan_id=rollback_id,
        operator_confirmation=True,
        confirmation_phrase=CONFIRMATION_PHRASE,
        expected_target_hashes={target_id: before_hash},
    )
    return source, request, target


def test_bounded_apply_applies_approved_workspace_file_and_records_change(tmp_path: Path) -> None:
    source, request, target = _bundle(tmp_path)
    service = SelfModificationBoundedApplyService(
        report_service=BoundedPatchApplyReportService(
            source_service=source,
            engine=None,
        )
    )

    result = service.apply_bounded_patch(request)
    report = result.report

    assert target.read_text(encoding="utf-8") == "alpha\nbeta"
    assert report.apply_status == "applied"
    assert report.changed_file_count == 1
    assert report.applied_operation_count == 1
    assert report.workspace_file_changed_emitted is True
    assert report.authorization_consumed is True
    assert report.rollback_plan_available is True
    assert report.post_apply_verification_required is True
    assert report.post_apply_verified is False
    assert report.outcome_recorded is False
    assert report.shell_executed is False
    assert report.test_lint_executed is False
    assert report.raw_content_emitted is False
    assert report.transaction is not None
    change = report.transaction.file_changes[0]
    assert change.before_hash != change.after_hash
    assert change.workspace_file_changed_event_id.startswith("workspace_file_changed:")
    assert change.raw_content_emitted is False
    assert source.authorizations[request.authorization_id].consumed is True


def test_bounded_apply_blocks_without_apply_gate(tmp_path: Path) -> None:
    source, request, target = _bundle(tmp_path)
    source.apply_gates.clear()
    report = SelfModificationBoundedApplyService(
        report_service=BoundedPatchApplyReportService(source_service=source)
    ).apply_bounded_patch(request).report

    assert report.apply_status == "blocked"
    assert target.read_text(encoding="utf-8") == "alpha\n"
    assert "missing_apply_gate" in [item.finding_type for item in report.findings]


def test_bounded_apply_blocks_consumed_expired_or_mismatched_authorization(tmp_path: Path) -> None:
    source, request, target = _bundle(tmp_path)
    auth = source.authorizations[request.authorization_id]
    source.authorizations[request.authorization_id] = replace(auth, consumed=True)
    report = SelfModificationBoundedApplyService(
        report_service=BoundedPatchApplyReportService(source_service=source)
    ).apply_bounded_patch(request).report

    assert report.apply_status == "blocked"
    assert target.read_text(encoding="utf-8") == "alpha\n"
    assert "authorization_consumed" in [item.finding_type for item in report.findings]


def test_bounded_apply_blocks_without_operator_confirmation(tmp_path: Path) -> None:
    source, request, target = _bundle(tmp_path)
    blocked = replace(request, operator_confirmation=False, confirmation_phrase=None)
    report = SelfModificationBoundedApplyService(
        report_service=BoundedPatchApplyReportService(source_service=source)
    ).apply_bounded_patch(blocked).report

    assert report.apply_status == "blocked"
    assert target.read_text(encoding="utf-8") == "alpha\n"
    assert "operator_confirmation_missing" in [item.finding_type for item in report.findings]


def test_bounded_apply_blocks_target_hash_drift(tmp_path: Path) -> None:
    source, request, target = _bundle(tmp_path)
    target.write_text("drifted\n", encoding="utf-8", newline="")
    report = SelfModificationBoundedApplyService(
        report_service=BoundedPatchApplyReportService(source_service=source)
    ).apply_bounded_patch(request).report

    assert report.apply_status == "blocked"
    assert target.read_text(encoding="utf-8") == "drifted\n"
    assert "target_hash_drift" in [item.finding_type for item in report.findings]


def test_bounded_writer_checks_expected_before_hash(tmp_path: Path) -> None:
    target = tmp_path / "target.txt"
    target.write_text("alpha\n", encoding="utf-8", newline="")
    writer = BoundedWorkspaceWriter(workspace_root=tmp_path)

    try:
        writer.write_text_atomically("target.txt", "beta\n", "wrong-hash")
    except ValueError as error:
        assert "hash" in str(error)
    else:
        raise AssertionError("writer accepted a mismatched before hash")

    assert target.read_text(encoding="utf-8") == "alpha\n"


def test_bounded_apply_pig_and_ocpx_projection() -> None:
    service = SelfModificationBoundedApplyService()
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    assert pig["version"] == "v0.22.6"
    assert pig["subject"] == "bounded_patch_apply"
    assert pig["bounded_file_write_enabled"] is True
    assert pig["external_patch_tool_allowed"] is False
    assert pig["shell_executed"] is False
    assert pig["test_lint_executed"] is False
    assert pig["post_apply_verified"] is False
    assert pig["llm_judge_enabled"] is False
    assert ocpx["state"] == "self_modification_bounded_patch_applied"
    assert "BoundedPatchApplyState" in ocpx["target_read_models"]
    assert "workspace_file_changed" in ocpx["effect_types"]


def test_bounded_apply_skill_contract_is_implemented() -> None:
    contracts = {item["skill_id"]: item for item in SelfModificationRegistryService().list_skill_contracts()}

    bounded = contracts["skill:self_modification_bounded_patch_apply"]
    assert bounded["status"] == "implemented"
    assert bounded["bounded_file_write_enabled"] is True
    assert bounded["file_write_enabled"] is True
    assert bounded["apply_patch_enabled"] is False
    assert contracts["skill:self_modification_post_apply_verify"]["status"] == "implemented"
    assert contracts["skill:self_modification_outcome_record"]["status"] == "implemented"


def test_bounded_apply_cli_commands_are_visible() -> None:
    commands = [
        [
            "apply",
            "bounded",
            "--apply-gate-id",
            "apply_gate_state:test",
            "--authorization-id",
            "apply_gate_authorization:test",
            "--confirm",
            CONFIRMATION_PHRASE,
        ],
        ["apply", "report", "--report-id", "bounded_patch_apply_report:test"],
        ["apply", "transaction", "--transaction-id", "bounded_patch_apply_transaction:test"],
        ["apply", "changes", "--report-id", "bounded_patch_apply_report:test"],
        ["pig-report"],
        ["ocpx-projection"],
    ]
    for command in commands:
        completed = subprocess.run(
            [sys.executable, "-m", "chanta_core.cli", "self-modification", *command],
            check=False,
            capture_output=True,
            text=True,
        )
        assert "layer=self_modification_safety" in completed.stdout
        assert "post_apply_verification_required=true" in completed.stdout or command in [["pig-report"], ["ocpx-projection"]]
        assert "post_apply_verified=false" in completed.stdout or command == ["ocpx-projection"]
        assert "raw_secrets_printed=False" in completed.stdout
        if command[:2] == ["apply", "bounded"]:
            assert completed.returncode == 1
            assert "apply_status=blocked" in completed.stdout
        else:
            assert completed.returncode == 0
