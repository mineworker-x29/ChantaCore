from __future__ import annotations

import subprocess
import sys
from dataclasses import replace

from chanta_core.self_modification_safety import (
    APPLY_GATE_SKILL_ID,
    APPLICABILITY_CHECK_SKILL_ID,
    DIFF_PREVIEW_SKILL_ID,
    DRY_RUN_SKILL_ID,
    PATCH_CANDIDATE_CREATE_SKILL_ID,
    PATCH_DRAFT_CREATE_SKILL_ID,
    REQUEST_CREATE_SKILL_ID,
    REVIEW_GATE_SKILL_ID,
    ROLLBACK_PLAN_SKILL_ID,
    SELF_MODIFICATION_EFFECT_TYPES,
    SELF_MODIFICATION_OCEL_EVENT_TYPES,
    SELF_MODIFICATION_OCEL_OBJECT_TYPES,
    SELF_MODIFICATION_OCEL_RELATION_TYPES,
    STATIC_SAFETY_CHECK_SKILL_ID,
    STATIC_SAFETY_REPORT_SKILL_ID,
    HumanReviewDecision,
    HumanReviewRequest,
    HumanReviewSourceService,
    PatchDraftCreateRequest,
    PatchDraftSourceService,
    PatchDryRunCheckRequest,
    PatchDryRunReport,
    PatchDryRunReportService,
    PatchDryRunSourceService,
    PatchStaticSafetyCheckRequest,
    PatchStaticSafetyReport,
    PatchStaticSafetyReportService,
    PatchStaticSafetySourceService,
    RollbackPlanDescriptor,
    SelfModificationDiffPreviewService,
    SelfModificationDryRunService,
    SelfModificationRegistryService,
    SelfModificationRequestCandidateService,
    SelfModificationRequestCreateRequest,
    SelfModificationReviewGateService,
    SelfModificationStaticSafetyService,
)


def _bundle():
    candidate_result = SelfModificationRequestCandidateService().create_request_and_candidate(
        SelfModificationRequestCreateRequest(goal_text="docs cleanup", target_paths=["README.md"])
    )
    assert candidate_result.patch_candidate is not None
    candidate = candidate_result.patch_candidate
    draft_result = SelfModificationDiffPreviewService(
        source_service=PatchDraftSourceService({candidate.candidate_id: candidate})
    ).create_patch_draft_and_preview(
        PatchDraftCreateRequest(
            patch_candidate_id=candidate.candidate_id,
            operation_hints=[
                {
                    "relative_path": "README.md",
                    "operation_type": "comment_only_change",
                    "anchor_type": "eof",
                    "provided_context": "sanitized context only",
                    "new_text_preview": "# preview-only candidate change",
                }
            ],
        )
    )
    assert draft_result.draft is not None
    assert draft_result.diff_preview is not None
    draft = draft_result.draft
    preview = draft_result.diff_preview
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
    dry_report = SelfModificationDryRunService(
        report_service=PatchDryRunReportService(
            source_service=PatchDryRunSourceService(
                patch_candidates={candidate.candidate_id: candidate},
                patch_drafts={draft.draft_id: draft},
                diff_previews={preview.preview_id: preview},
                static_safety_reports={static_report.report_id: static_report},
            )
        )
    ).check_applicability(
        PatchDryRunCheckRequest(
            patch_candidate_id=candidate.candidate_id,
            draft_id=draft.draft_id,
            preview_id=preview.preview_id,
            static_safety_report_id=static_report.report_id,
        )
    ).report
    source = HumanReviewSourceService(
        patch_candidates={candidate.candidate_id: candidate},
        patch_drafts={draft.draft_id: draft},
        diff_previews={preview.preview_id: preview},
        static_safety_reports={static_report.report_id: static_report},
        dry_run_reports={dry_report.report_id: dry_report},
    )
    service = SelfModificationReviewGateService(source_service=source)
    request = service.request_review(
        patch_candidate_id=candidate.candidate_id,
        draft_id=draft.draft_id,
        preview_id=preview.preview_id,
        static_safety_report_id=static_report.report_id,
        dry_run_report_id=dry_report.report_id,
    )
    return candidate, draft, preview, static_report, dry_report, service, request


def test_human_review_request_can_be_created() -> None:
    candidate, draft, preview, static_report, dry_report, _, request = _bundle()

    assert isinstance(request, HumanReviewRequest)
    assert request.review_request_id.startswith("human_review_request:")
    assert request.patch_candidate_id == candidate.candidate_id
    assert request.draft_id == draft.draft_id
    assert request.preview_id == preview.preview_id
    assert request.static_safety_report_id == static_report.report_id
    assert request.dry_run_report_id == dry_report.report_id
    assert request.raw_patch_content_included is False
    assert request.raw_file_content_included is False
    assert request.summary_refs and request.risk_refs and request.evidence_refs


def test_human_review_decisions_are_recorded_without_direct_apply() -> None:
    _, _, _, _, _, service, request = _bundle()

    for decision_name in ["approve", "reject", "revise", "no_action", "needs_more_input"]:
        decision = service.record_review_decision(review_request_id=request.review_request_id, decision=decision_name)
        assert isinstance(decision, HumanReviewDecision)
        assert decision.decision == decision_name
        assert decision.approved_for_apply_gate is (decision_name == "approve")
        assert decision.approved_for_direct_apply is False
        assert decision.decision_id.startswith("human_review_decision:")


def test_rollback_plan_descriptor_is_created_without_execution() -> None:
    _, draft, _, _, _, service, request = _bundle()
    plan = service.rollback_service.build_rollback_plan(
        patch_candidate_id=request.patch_candidate_id,
        draft_id=request.draft_id,
        preview_id=request.preview_id,
        draft=draft,
    )

    assert isinstance(plan, RollbackPlanDescriptor)
    assert plan.rollback_plan_id.startswith("rollback_plan_descriptor:")
    assert plan.rollback_possible is True
    assert plan.plan_type == "reverse_patch"
    assert plan.before_snapshot_refs
    assert plan.reverse_operation_refs
    assert plan.rollback_execution_enabled is False
    assert plan.rollback_executed is False


def test_apply_gate_opens_when_all_preconditions_pass() -> None:
    _, _, _, _, _, service, request = _bundle()
    decision = service.record_review_decision(review_request_id=request.review_request_id, decision="approve")
    result = service.evaluate_apply_gate(review_request=request, review_decision=decision)
    report = result.report
    state = report.apply_gate_state

    assert report.report_status == "passed"
    assert report.review_status == "approved"
    assert report.gate_status == "open"
    assert state.precondition_check.apply_gate_allowed is True
    assert state.apply_gate_opened is True
    assert state.eligible_for_bounded_apply is True
    assert state.safe_to_apply is False
    assert state.patch_applied is False
    assert state.file_write_performed is False
    assert state.workspace_file_changed_emitted is False
    assert state.shell_executed is False
    assert state.test_lint_executed is False
    assert state.authorization is not None
    assert state.authorization.authorized_for_stage == "bounded_patch_apply"
    assert state.authorization.authorized_next_version == "v0.22.6"
    assert state.authorization.single_use is True
    assert state.authorization.consumed is False
    assert state.authorization.patch_applied is False
    assert state.authorization.file_write_performed is False
    assert state.authorization.workspace_file_changed_emitted is False


def test_apply_gate_decision_statuses_reject_revise_and_needs_more_input() -> None:
    _, _, _, _, _, service, request = _bundle()

    rejected = service.evaluate_apply_gate(
        review_request=request,
        review_decision=service.record_review_decision(review_request_id=request.review_request_id, decision="reject"),
    )
    revised = service.evaluate_apply_gate(
        review_request=request,
        review_decision=service.record_review_decision(review_request_id=request.review_request_id, decision="revise"),
    )
    needs = service.evaluate_apply_gate(
        review_request=request,
        review_decision=service.record_review_decision(review_request_id=request.review_request_id, decision="needs_more_input"),
    )

    assert rejected.report.gate_status == "rejected"
    assert revised.report.gate_status == "revise_required"
    assert needs.report.gate_status == "needs_more_input"
    assert needs.needs_more_input_candidate is not None


def test_apply_gate_blocks_missing_or_failed_preconditions() -> None:
    _, _, _, static_report, dry_report, service, request = _bundle()
    approved = service.record_review_decision(review_request_id=request.review_request_id, decision="approve")

    missing_review = service.evaluate_apply_gate(review_request=request, review_decision=None)
    assert missing_review.report.gate_status == "needs_more_input"
    assert "review_approval_required" in missing_review.report.apply_gate_state.precondition_check.failed_preconditions

    failed_static = replace(static_report, static_safety_status="failed")
    source = HumanReviewSourceService(
        static_safety_reports={failed_static.report_id: failed_static},
        dry_run_reports={dry_report.report_id: dry_report},
        allow_synthetic=True,
    )
    failed_service = SelfModificationReviewGateService(source_service=source)
    failed_static_result = failed_service.evaluate_apply_gate(review_request=request, review_decision=approved)
    assert failed_static_result.report.gate_status == "blocked"
    assert "static_safety_report_required_or_not_passed" in failed_static_result.report.apply_gate_state.precondition_check.failed_preconditions

    failed_dry = replace(dry_report, dry_run_status="failed", eligible_for_review=False)
    source = HumanReviewSourceService(
        static_safety_reports={static_report.report_id: static_report},
        dry_run_reports={failed_dry.report_id: failed_dry},
        allow_synthetic=True,
    )
    failed_service = SelfModificationReviewGateService(source_service=source)
    failed_dry_result = failed_service.evaluate_apply_gate(review_request=request, review_decision=approved)
    assert failed_dry_result.report.gate_status == "blocked"
    assert "dry_run_report_required_or_not_passed" in failed_dry_result.report.apply_gate_state.precondition_check.failed_preconditions

    impossible_plan = replace(
        service.rollback_service.build_rollback_plan(
            patch_candidate_id=request.patch_candidate_id,
            draft_id=request.draft_id,
            preview_id=request.preview_id,
        ),
        rollback_possible=False,
    )
    rollback_result = service.evaluate_apply_gate(review_request=request, review_decision=approved, rollback_plan=impossible_plan)
    assert rollback_result.report.gate_status == "blocked"
    assert "rollback_plan_required" in rollback_result.report.apply_gate_state.precondition_check.failed_preconditions


def test_apply_gate_report_has_required_safety_flags_and_horizon() -> None:
    _, _, _, _, _, service, request = _bundle()
    decision = service.record_review_decision(review_request_id=request.review_request_id, decision="approve")
    report = service.evaluate_apply_gate(review_request=request, review_decision=decision).report

    assert report.safe_to_apply is False
    assert report.patch_applied is False
    assert report.file_write_performed is False
    assert report.workspace_file_changed_emitted is False
    assert report.shell_executed is False
    assert report.test_lint_executed is False
    assert report.withdrawal_conditions
    assert report.validity_horizon
    assert any(finding.finding_type == "apply_gate_opened" for finding in report.findings)


def test_review_gate_ocel_pig_ocpx_and_skill_statuses() -> None:
    contracts = {item["skill_id"]: item for item in SelfModificationRegistryService().list_skill_contracts()}
    service = SelfModificationReviewGateService()
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
        REVIEW_GATE_SKILL_ID,
        APPLY_GATE_SKILL_ID,
        ROLLBACK_PLAN_SKILL_ID,
    ]:
        assert contracts[skill_id]["status"] == "implemented"
        assert contracts[skill_id]["non_executable"] is True
        assert contracts[skill_id]["file_write_enabled"] is False
        assert contracts[skill_id]["apply_patch_enabled"] is False
    assert contracts["skill:self_modification_post_apply_verify"]["status"] == "implemented"
    assert contracts["skill:self_modification_outcome_record"]["status"] == "implemented"
    assert "human_review_request" in SELF_MODIFICATION_OCEL_OBJECT_TYPES
    assert "apply_gate_state" in SELF_MODIFICATION_OCEL_OBJECT_TYPES
    assert "self_modification_apply_gate_opened" in SELF_MODIFICATION_OCEL_EVENT_TYPES
    assert "opens_apply_gate" in SELF_MODIFICATION_OCEL_RELATION_TYPES
    assert "authorizes_bounded_apply_stage" in SELF_MODIFICATION_OCEL_RELATION_TYPES
    assert {"read_only_observation", "state_candidate_created", "gate_state_created"} <= set(SELF_MODIFICATION_EFFECT_TYPES)
    assert "workspace_file_changed" in SELF_MODIFICATION_EFFECT_TYPES
    assert pig["version"] == "v0.22.5"
    assert pig["subject"] == "human_review_apply_gate"
    assert pig["review_decision_allowed"] is True
    assert pig["apply_gate_state_allowed"] is True
    assert pig["patch_applied"] is False
    assert pig["file_write_performed"] is False
    assert pig["workspace_file_changed_emitted"] is False
    assert pig["safe_to_apply"] is False
    assert pig["shell_executed"] is False
    assert pig["test_lint_executed"] is False
    assert pig["llm_judge_enabled"] is False
    assert ocpx["state"] == "self_modification_human_review_apply_gate_checked"
    assert "HumanReviewState" in ocpx["target_read_models"]
    assert "ApplyGateState" in ocpx["target_read_models"]
    assert "RollbackPlanState" in ocpx["target_read_models"]
    assert "BoundedApplyEligibilityState" in ocpx["target_read_models"]


def test_review_gate_cli_commands() -> None:
    commands = [
        ["review", "request", "--preview-id", "diff_preview:test", "--dry-run-report-id", "patch_dry_run_report:test"],
        ["review", "decide", "--review-request-id", "human_review_request:test", "--decision", "approve"],
        ["review", "decide", "--review-request-id", "human_review_request:test", "--decision", "reject"],
        ["review", "decide", "--review-request-id", "human_review_request:test", "--decision", "revise"],
        ["review", "decide", "--review-request-id", "human_review_request:test", "--decision", "no_action"],
        ["review", "decide", "--review-request-id", "human_review_request:test", "--decision", "needs_more_input"],
        ["apply-gate", "evaluate", "--review-decision-id", "human_review_decision:test"],
        ["apply-gate", "view", "--apply-gate-id", "apply_gate_state:test"],
        ["rollback-plan", "view", "--rollback-plan-id", "rollback_plan_descriptor:test"],
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
