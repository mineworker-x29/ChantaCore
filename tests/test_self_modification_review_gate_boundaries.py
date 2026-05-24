from __future__ import annotations

from pathlib import Path

from chanta_core.self_modification_safety import (
    SELF_MODIFICATION_EFFECT_TYPES,
    SELF_MODIFICATION_OCEL_EVENT_TYPES,
    SELF_MODIFICATION_OCEL_OBJECT_TYPES,
    SELF_MODIFICATION_OCEL_RELATION_TYPES,
    HumanReviewSourceService,
    SelfModificationReviewGateService,
)


DOC_FILE = Path("docs/versions/v0.22/v0.22.5_human_review_apply_gate.md")


def test_v0_22_5_restore_grade_doc_exists_and_states_boundaries() -> None:
    text = DOC_FILE.read_text(encoding="utf-8")
    assert "Human Review & Apply Gate" in text
    assert "인간 검토·적용 게이트" in text
    assert "Review decision is not execution." in text
    assert "Review approval is not file mutation." in text
    assert "Apply gate is not patch apply." in text
    assert "Apply gate requires dry-run pass." in text
    assert "Apply gate requires rollback plan." in text
    assert "Apply gate requires explicit operator approval." in text
    assert "v0.22.6 Bounded Patch Apply" in text
    assert "Restore procedure" in text
    assert "Withdrawal Conditions" in text
    assert "Validity Horizon" in text


def test_review_gate_boundary_flags_are_disabled_even_when_gate_opens() -> None:
    service = SelfModificationReviewGateService(source_service=HumanReviewSourceService(allow_synthetic=True))
    request = service.request_review()
    decision = service.record_review_decision(review_request_id=request.review_request_id, decision="approve")
    report = service.evaluate_apply_gate(review_request=request, review_decision=decision).report
    state = report.apply_gate_state

    assert state.apply_gate_opened is True
    assert state.eligible_for_bounded_apply is True
    assert state.safe_to_apply is False
    assert state.patch_applied is False
    assert state.file_write_performed is False
    assert state.workspace_file_changed_emitted is False
    assert state.shell_executed is False
    assert state.test_lint_executed is False
    assert decision.approved_for_direct_apply is False
    assert report.rollback_plan is not None
    assert report.rollback_plan.rollback_execution_enabled is False
    assert report.rollback_plan.rollback_executed is False


def test_review_gate_ocel_mapping_has_gate_state_but_no_workspace_change_effect() -> None:
    for object_type in [
        "human_review_request",
        "human_review_decision",
        "apply_gate_precondition_check",
        "rollback_plan_descriptor",
        "apply_gate_finding",
        "apply_gate_authorization",
        "apply_gate_state",
        "human_review_apply_gate_report",
        "apply_gate_no_action_candidate",
        "apply_gate_needs_more_input_candidate",
        "patch_dry_run_report",
        "patch_static_safety_report",
        "patch_draft",
        "diff_preview",
        "patch_candidate",
        "modification_request",
        "execution_envelope",
        "pig_report",
        "ocpx_projection",
    ]:
        assert object_type in SELF_MODIFICATION_OCEL_OBJECT_TYPES
    for event_type in [
        "self_modification_human_review_requested",
        "self_modification_human_review_decision_recorded",
        "self_modification_rollback_plan_created",
        "self_modification_apply_gate_preconditions_checked",
        "self_modification_apply_gate_opened",
        "self_modification_apply_gate_blocked",
        "self_modification_apply_gate_rejected",
        "self_modification_apply_gate_needs_more_input_created",
        "self_modification_apply_gate_no_action_created",
        "self_modification_human_review_apply_gate_report_created",
    ]:
        assert event_type in SELF_MODIFICATION_OCEL_EVENT_TYPES
    for relation_type in [
        "requests_human_review",
        "records_review_decision",
        "approves_for_apply_gate",
        "rejects_patch_candidate",
        "requires_revision",
        "supports_no_action",
        "requires_more_input",
        "uses_static_safety_report",
        "uses_dry_run_report",
        "uses_patch_draft",
        "uses_diff_preview",
        "uses_patch_candidate",
        "requires_rollback_plan",
        "creates_rollback_plan",
        "checks_apply_gate_preconditions",
        "opens_apply_gate",
        "blocks_apply_gate",
        "authorizes_bounded_apply_stage",
        "not_applied_to_workspace",
        "not_safe_to_apply",
        "requires_bounded_apply",
        "requires_post_apply_verification",
        "visible_in_workbench",
        "recorded_in_envelope",
        "derived_from_dry_run_report",
        "derived_from_static_safety_report",
        "derived_from_patch_draft",
        "derived_from_diff_preview",
        "derived_from_patch_candidate",
    ]:
        assert relation_type in SELF_MODIFICATION_OCEL_RELATION_TYPES
    assert {"read_only_observation", "state_candidate_created", "gate_state_created"} <= set(SELF_MODIFICATION_EFFECT_TYPES)
    assert "workspace_file_changed" in SELF_MODIFICATION_EFFECT_TYPES


def test_review_gate_runtime_source_contains_no_forbidden_execution_imports() -> None:
    text = Path("src/chanta_core/self_modification_safety/review_gate.py").read_text(encoding="utf-8")
    forbidden = [
        "subprocess",
        "os.system",
        "requests",
        "httpx",
        "mcp.connect",
        "plugin.load",
        "Path.write_text",
        "Path.write_bytes",
        "shutil.move",
        "os.remove",
        "chmod",
        "safe_to_apply=True",
        "approved_for_direct_apply=True",
        "rollback_executed=True",
        "file_write_performed=True",
        "workspace_file_changed_emitted=True",
        "shell_executed=True",
        "test_lint_executed=True",
        "llm_approve",
        "auto_approve",
    ]
    for token in forbidden:
        assert token not in text
