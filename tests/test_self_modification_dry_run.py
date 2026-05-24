from __future__ import annotations

import subprocess
import sys
from dataclasses import replace

from chanta_core.self_modification_safety import (
    APPLICABILITY_CHECK_SKILL_ID,
    DIFF_PREVIEW_SKILL_ID,
    DRY_RUN_SKILL_ID,
    PATCH_CANDIDATE_CREATE_SKILL_ID,
    PATCH_DRAFT_CREATE_SKILL_ID,
    REQUEST_CREATE_SKILL_ID,
    SELF_MODIFICATION_OCEL_EVENT_TYPES,
    SELF_MODIFICATION_OCEL_OBJECT_TYPES,
    SELF_MODIFICATION_OCEL_RELATION_TYPES,
    STATIC_SAFETY_CHECK_SKILL_ID,
    STATIC_SAFETY_REPORT_SKILL_ID,
    PatchAnchorApplicabilityService,
    PatchDraftCreateRequest,
    PatchDraftSourceService,
    PatchDryRunCheckRequest,
    PatchDryRunEnginePolicy,
    PatchDryRunReport,
    PatchDryRunReportService,
    PatchDryRunSourceService,
    PatchInMemoryApplicabilityEngine,
    PatchStaticSafetyCheckRequest,
    PatchStaticSafetyReport,
    PatchStaticSafetyReportService,
    PatchStaticSafetySourceService,
    SelfModificationDiffPreviewService,
    SelfModificationDryRunService,
    SelfModificationRegistryService,
    SelfModificationRequestCandidateService,
    SelfModificationRequestCreateRequest,
    SelfModificationStaticSafetyService,
)


def _bundle(**hint_overrides):
    candidate_result = SelfModificationRequestCandidateService().create_request_and_candidate(
        SelfModificationRequestCreateRequest(goal_text="docs cleanup", target_paths=["README.md"])
    )
    assert candidate_result.patch_candidate is not None
    candidate = candidate_result.patch_candidate
    hint = {
        "relative_path": "README.md",
        "operation_type": "comment_only_change",
        "anchor_type": "eof",
        "provided_context": "sanitized context only",
        "new_text_preview": "# preview-only candidate change",
    }
    hint.update(hint_overrides)
    draft_result = SelfModificationDiffPreviewService(
        source_service=PatchDraftSourceService({candidate.candidate_id: candidate})
    ).create_patch_draft_and_preview(
        PatchDraftCreateRequest(patch_candidate_id=candidate.candidate_id, operation_hints=[hint])
    )
    assert draft_result.draft is not None
    assert draft_result.diff_preview is not None
    draft = draft_result.draft
    context = replace(draft.target_context_refs[0], truncated=False, redacted=False)
    draft = replace(draft, target_context_refs=[context])
    preview = replace(draft_result.diff_preview, target_refs=[context.to_dict()], truncated=False, redacted=False)
    static_report = SelfModificationStaticSafetyService(
        report_service=PatchStaticSafetyReportService(
            source_service=PatchStaticSafetySourceService(
                patch_candidates={candidate.candidate_id: candidate},
                patch_drafts={draft.draft_id: draft},
                diff_previews={preview.preview_id: preview},
            )
        )
    ).check_static_safety(
        PatchStaticSafetyCheckRequest(
            patch_candidate_id=candidate.candidate_id,
            draft_id=draft.draft_id,
            preview_id=preview.preview_id,
        )
    ).report
    return candidate, draft, preview, static_report


def _service(candidate, draft, preview, static_report):
    return SelfModificationDryRunService(
        report_service=PatchDryRunReportService(
            source_service=PatchDryRunSourceService(
                patch_candidates={candidate.candidate_id: candidate},
                patch_drafts={draft.draft_id: draft},
                diff_previews={preview.preview_id: preview},
                static_safety_reports={static_report.report_id: static_report},
            )
        )
    )


def _report(candidate, draft, preview, static_report) -> PatchDryRunReport:
    result = _service(candidate, draft, preview, static_report).check_applicability(
        PatchDryRunCheckRequest(
            patch_candidate_id=candidate.candidate_id,
            draft_id=draft.draft_id,
            preview_id=preview.preview_id,
            static_safety_report_id=static_report.report_id,
        )
    )
    return result.report


def test_dry_run_report_builds_from_valid_static_report_draft_preview() -> None:
    candidate, draft, preview, static_report = _bundle()
    report = _report(candidate, draft, preview, static_report)

    assert report.report_id.startswith("patch_dry_run_report:")
    assert report.patch_candidate_id == candidate.candidate_id
    assert report.draft_id == draft.draft_id
    assert report.preview_id == preview.preview_id
    assert report.static_safety_report_id == static_report.report_id
    assert report.dry_run_status == "passed"
    assert report.eligible_for_review is True
    assert report.safe_to_apply is False
    assert report.checked_operation_count == 1
    assert report.passed_operation_count == 1
    assert report.conflict_count == 0
    assert isinstance(report, PatchDryRunReport)


def test_engine_policy_and_target_snapshot_are_read_only() -> None:
    candidate, draft, preview, static_report = _bundle()
    report = _report(candidate, draft, preview, static_report)
    snapshot = report.target_snapshots[0]
    policy = report.engine_policy

    assert isinstance(policy, PatchDryRunEnginePolicy)
    assert policy.in_memory_only is True
    assert policy.external_patch_tool_allowed is False
    assert policy.shell_execution_allowed is False
    assert policy.file_write_allowed is False
    assert policy.apply_patch_allowed is False
    assert policy.workspace_file_changed_allowed is False
    assert policy.test_lint_execution_allowed is False
    assert policy.allow_full_content_output is False
    assert snapshot.content_hash_before
    assert snapshot.byte_count is not None
    assert snapshot.line_count is not None
    assert snapshot.encoding == "utf-8"
    assert snapshot.line_ending in {"lf", "crlf"}
    assert snapshot.raw_content_emitted is False
    assert "_content_for_simulation" not in snapshot.to_dict()


def test_anchor_applicability_and_in_memory_operation_simulation_pass() -> None:
    candidate, draft, preview, static_report = _bundle(
        operation_type="text_replace",
        anchor_type="exact_text",
        anchor_text_preview="old line",
        old_text_preview="old line",
        new_text_preview="new line",
    )
    report = _report(candidate, draft, preview, static_report)
    result = report.operation_results[0]
    assert isinstance(result.anchor_check, object)
    assert result.anchor_check is not None
    assert result.anchor_check.anchor_status == "matched"
    assert result.anchor_check.match_count == 1
    assert result.would_apply_in_memory is True
    assert result.applied_in_memory is True
    assert result.file_write_performed is False
    assert result.workspace_file_changed_emitted is False
    assert result.resulting_content_hash
    assert result.resulting_line_count is not None


def test_missing_static_report_and_failed_static_report_block() -> None:
    candidate, draft, preview, static_report = _bundle()
    missing = SelfModificationDryRunService(
        report_service=PatchDryRunReportService(
            source_service=PatchDryRunSourceService(
                patch_candidates={candidate.candidate_id: candidate},
                patch_drafts={draft.draft_id: draft},
                diff_previews={preview.preview_id: preview},
            )
        )
    ).check_applicability(PatchDryRunCheckRequest(draft_id=draft.draft_id, preview_id=preview.preview_id))
    failed_static = replace(static_report, static_safety_status="failed")
    failed = _report(candidate, draft, preview, failed_static)

    assert missing.report.dry_run_status == "blocked"
    assert missing.no_action_candidate is not None
    assert any(finding.finding_type == "missing_static_safety_report" for finding in missing.report.findings)
    assert failed.dry_run_status == "blocked"
    assert any(finding.finding_type == "static_safety_not_passed" for finding in failed.findings)


def test_target_snapshot_private_secret_and_unavailable_blocks() -> None:
    candidate, draft, preview, static_report = _bundle()
    no_snapshot = _service(candidate, draft, preview, static_report).check_applicability(
        PatchDryRunCheckRequest(
            draft_id=draft.draft_id,
            preview_id=preview.preview_id,
            static_safety_report_id=static_report.report_id,
            include_target_snapshot=False,
            strictness="strict",
        )
    )
    assert no_snapshot.report.dry_run_status == "blocked"

    context = draft.target_context_refs[0]
    private_context = replace(context, private_boundary_risk=True)
    private_draft = replace(draft, target_context_refs=[private_context])
    assert _report(candidate, private_draft, preview, static_report).dry_run_status == "blocked"

    secret_context = replace(context, relative_path=".env")
    secret_draft = replace(draft, target_context_refs=[secret_context])
    secret_report = _report(candidate, secret_draft, preview, static_report)
    assert secret_report.dry_run_status == "blocked"
    assert any(finding.finding_type == "secret_boundary_block" for finding in secret_report.findings)


def test_anchor_missing_ambiguous_old_text_mismatch_and_context_mismatch_fail() -> None:
    candidate, draft, preview, static_report = _bundle(
        operation_type="insert_after",
        anchor_type="exact_text",
        anchor_text_preview="missing anchor",
        new_text_preview="new line",
    )
    missing = _report(candidate, draft, preview, static_report)
    assert missing.dry_run_status == "failed"
    assert any(finding.finding_type == "anchor_missing" for finding in missing.findings)

    candidate, draft, preview, static_report = _bundle()
    ambiguous_anchor = replace(draft.anchors[0], ambiguous=True)
    ambiguous_operation = replace(draft.operations[0], anchor_ref=ambiguous_anchor)
    draft = replace(draft, anchors=[ambiguous_anchor], operations=[ambiguous_operation])
    ambiguous = _report(candidate, draft, preview, static_report)
    assert ambiguous.dry_run_status == "failed"
    assert any(finding.finding_type == "anchor_ambiguous" for finding in ambiguous.findings)

    candidate, draft, preview, static_report = _bundle(
        operation_type="text_replace",
        anchor_type="exact_text",
        anchor_text_preview="old line",
        old_text_preview="old line",
        new_text_preview="new line",
    )
    operation = replace(draft.operations[0], old_text_preview="absent")
    mismatch_draft = replace(draft, operations=[operation])
    mismatch = _report(candidate, mismatch_draft, preview, static_report)
    assert mismatch.dry_run_status == "failed"
    assert any(finding.finding_type == "old_text_mismatch" for finding in mismatch.findings)


def test_operation_conflict_and_overlapping_hunks_are_detected() -> None:
    candidate, draft, preview, static_report = _bundle(
        operation_type="append_block",
        anchor_type="eof",
        new_text_preview="first",
    )
    operation = draft.operations[0]
    second = replace(operation, operation_id=operation.operation_id + ":2", new_text_preview="second")
    conflict_draft = replace(draft, operations=[operation, second])
    report = _report(candidate, conflict_draft, preview, static_report)

    assert report.dry_run_status in {"failed", "warning"}
    assert report.conflict_count >= 1
    assert any(finding.finding_type == "overlapping_hunks" for finding in report.findings)


def test_truncated_redacted_context_warns_and_report_flags_never_apply() -> None:
    candidate, draft, preview, static_report = _bundle()
    context = replace(draft.target_context_refs[0], truncated=True, redacted=True)
    changed_draft = replace(draft, target_context_refs=[context])
    report = _report(candidate, changed_draft, preview, static_report)

    assert report.dry_run_status == "warning"
    assert report.eligible_for_review is True
    assert any(finding.finding_type == "truncated_context_unreliable" for finding in report.findings)
    assert any(finding.finding_type == "redacted_context_unreliable" for finding in report.findings)
    assert report.safe_to_apply is False
    assert report.human_review_required is True
    assert report.apply_gate_required is True
    assert report.rollback_plan_required is True
    assert report.post_apply_verification_required is True
    assert report.review_status == "report_only"
    assert report.file_write_enabled is False
    assert report.apply_patch_enabled is False
    assert report.file_write_performed is False
    assert report.patch_applied is False
    assert report.workspace_file_changed_emitted is False
    assert report.shell_executed is False
    assert report.test_lint_executed is False


def test_dry_run_ocel_pig_ocpx_and_skill_statuses() -> None:
    contracts = {item["skill_id"]: item for item in SelfModificationRegistryService().list_skill_contracts()}
    service = SelfModificationDryRunService()
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    for skill_id in [
        REQUEST_CREATE_SKILL_ID,
        PATCH_CANDIDATE_CREATE_SKILL_ID,
        PATCH_DRAFT_CREATE_SKILL_ID,
        DIFF_PREVIEW_SKILL_ID,
        STATIC_SAFETY_CHECK_SKILL_ID,
        STATIC_SAFETY_REPORT_SKILL_ID,
        DRY_RUN_SKILL_ID,
        APPLICABILITY_CHECK_SKILL_ID,
    ]:
        assert contracts[skill_id]["status"] == "implemented"
        assert contracts[skill_id]["non_executable"] is True
        assert contracts[skill_id]["file_write_enabled"] is False
        assert contracts[skill_id]["apply_patch_enabled"] is False
    assert contracts["skill:self_modification_review_gate"]["status"] == "implemented"
    assert contracts["skill:self_modification_apply_gate"]["status"] == "implemented"
    assert contracts["skill:self_modification_rollback_plan"]["status"] == "implemented"
    assert "patch_dry_run_report" in SELF_MODIFICATION_OCEL_OBJECT_TYPES
    assert "patch_anchor_applicability_check" in SELF_MODIFICATION_OCEL_OBJECT_TYPES
    assert "self_modification_dry_run_report_created" in SELF_MODIFICATION_OCEL_EVENT_TYPES
    assert "checks_patch_applicability" in SELF_MODIFICATION_OCEL_RELATION_TYPES
    assert "eligible_for_human_review" in SELF_MODIFICATION_OCEL_RELATION_TYPES
    assert pig["version"] == "v0.22.4"
    assert pig["subject"] == "patch_dry_run_applicability_check"
    assert pig["in_memory_only"] is True
    assert pig["file_write_performed"] is False
    assert pig["patch_applied"] is False
    assert pig["workspace_file_changed_emitted"] is False
    assert pig["shell_executed"] is False
    assert pig["test_lint_executed"] is False
    assert pig["safe_to_apply"] is False
    assert pig["llm_judge_enabled"] is False
    assert ocpx["state"] == "self_modification_patch_dry_run_applicability_checked"
    assert "PatchDryRunState" in ocpx["target_read_models"]
    assert "PatchApplicabilityState" in ocpx["target_read_models"]
    assert "PatchDryRunConflictState" in ocpx["target_read_models"]
    assert "PatchReviewEligibilityState" in ocpx["target_read_models"]


def test_dry_run_cli_commands() -> None:
    commands = [
        ["dry-run", "check", "--preview-id", "diff_preview:test", "--static-report-id", "patch_static_safety_report:test"],
        ["dry-run", "check", "--draft-id", "patch_draft:test"],
        ["dry-run", "summary", "--preview-id", "diff_preview:test"],
        ["dry-run", "report", "--report-id", "patch_dry_run_report:test"],
        ["dry-run", "conflicts", "--report-id", "patch_dry_run_report:test"],
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
        assert completed.returncode == 0
        assert "layer=self_modification_safety" in completed.stdout
        assert "safe_to_apply=false" in completed.stdout
        assert "No file mutation occurred." in completed.stdout
        assert "raw_secrets_printed=False" in completed.stdout
        assert "D:\\" not in completed.stdout
