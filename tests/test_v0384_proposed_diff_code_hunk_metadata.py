from dataclasses import fields
import inspect

import pytest

from chanta_core.agent_runtime import (
    ProposedChangeEvidenceMap,
    ProposedChangeOperationKind,
    ProposedChangeRationale,
    ProposedCodeHunk,
    ProposedCodeHunkKind,
    ProposedDiffFormatKind,
    ProposedDiffMetadata,
    ProposedFileChange,
    ProposedPatchArtifactKind,
    ProposedPatchConfidenceLevel,
    ProposedPatchDisposition,
    ProposedPatchDoNothingComparison,
    ProposedPatchDoNothingComparisonKind,
    ProposedPatchEnvelope,
    ProposedPatchEvidenceKind,
    ProposedPatchReviewRequirement,
    ProposedPatchReviewRequirementKind,
    RepairPatchMetadataDecision,
    RepairPatchMetadataDecisionKind,
    RepairPatchMetadataFlagSet,
    RepairPatchMetadataInput,
    RepairPatchMetadataMode,
    RepairPatchMetadataNoApplyGuarantee,
    RepairPatchMetadataPolicy,
    RepairPatchMetadataReadinessLevel,
    RepairPatchMetadataReport,
    RepairPatchMetadataRiskKind,
    RepairPatchMetadataRunPreview,
    RepairPatchMetadataSourceKind,
    RepairPatchMetadataSourceRef,
    RepairPatchMetadataStatus,
    RepairPatchMetadataValidationFinding,
    RepairPatchMetadataValidationReport,
    RepairSourceContextSufficiencyKind,
    V0384ReadinessReport,
    build_proposed_change_evidence_map,
    build_proposed_change_rationale,
    build_proposed_code_hunk,
    build_proposed_diff_metadata,
    build_proposed_file_change,
    build_proposed_patch_do_nothing_comparison,
    build_proposed_patch_envelope,
    build_proposed_patch_review_requirement,
    build_repair_change_intent,
    build_repair_patch_metadata_decision,
    build_repair_patch_metadata_flags,
    build_repair_patch_metadata_input,
    build_repair_patch_metadata_input_from_scope_plan,
    build_repair_patch_metadata_no_apply_guarantee,
    build_repair_patch_metadata_policy,
    build_repair_patch_metadata_report,
    build_repair_patch_metadata_run_preview,
    build_repair_patch_metadata_source_ref,
    build_repair_patch_metadata_validation_finding,
    build_repair_patch_metadata_validation_report,
    build_repair_scope_plan,
    build_repair_source_context_assessment,
    build_repair_source_context_snapshot,
    build_repair_source_excerpt,
    build_repair_source_file_snapshot,
    build_repair_symbol_context_hint,
    build_v0384_readiness_report,
    compare_proposed_patch_to_do_nothing,
    create_proposed_change_evidence_map_from_scope,
    create_proposed_change_rationale_from_intent,
    create_proposed_code_hunks_from_scope_context,
    create_proposed_diff_metadata_from_hunks,
    create_proposed_file_changes,
    create_proposed_patch_envelope,
    create_proposed_patch_review_requirement,
    decide_repair_patch_metadata,
    default_repair_patch_metadata_policy,
    proposed_code_hunk_is_not_edit,
    proposed_diff_metadata_is_not_applied_diff,
    proposed_patch_envelope_is_not_patch_application,
    repair_patch_metadata_decision_is_not_apply_permission,
    repair_patch_metadata_flags_preserve_no_apply,
    repair_patch_metadata_policy_blocks_apply_and_repair,
    v0384_readiness_report_is_not_execution_ready,
    validate_proposed_patch_envelope,
)


SAFE_FLAG_NAMES = {
    "ready_for_v0385_repair_proposal_safety_validation",
    "ready_for_v0386_human_review_packet",
    "ready_for_repair_patch_metadata_generation",
    "ready_for_proposed_diff_metadata_generation",
    "ready_for_proposed_code_hunk_metadata_generation",
    "ready_for_proposed_patch_envelope_metadata_generation",
    "ready_for_proposed_file_change_metadata",
    "ready_for_change_rationale_metadata",
    "ready_for_patch_evidence_map",
    "ready_for_patch_do_nothing_comparison",
    "ready_for_patch_review_requirement",
    "ready_for_future_repair_proposal_safety_validation_input",
    "ready_for_future_human_review_packet_input",
}


def _unsafe_flag_names(cls):
    return [
        field.name
        for field in fields(cls)
        if (field.name.startswith("ready_for_") and field.name not in SAFE_FLAG_NAMES)
        or field.name == "production_certified"
    ]


def _source_context_snapshot(summary="assertion mismatch points at target function"):
    file_snapshot = build_repair_source_file_snapshot(
        file_snapshot_id="fs:module",
        normalized_relative_path="pkg/module.py",
        bounded_content_preview="def target_function():\n    return 1\n",
    )
    excerpt = build_repair_source_excerpt(
        source_excerpt_id="excerpt:module",
        file_snapshot_id=file_snapshot.file_snapshot_id,
        normalized_relative_path="pkg/module.py",
        excerpt_text="def target_function():\n    return 1\n",
        excerpt_summary=summary,
    )
    hint = build_repair_symbol_context_hint(
        symbol_context_hint_id="hint:target_function",
        source_excerpt_id=excerpt.source_excerpt_id,
        normalized_relative_path="pkg/module.py",
        symbol_name="target_function",
        hint_summary="target function appears in supplied metadata",
    )
    assessment = build_repair_source_context_assessment(
        context_assessment_id="assessment:source-context",
        sufficiency_kind=RepairSourceContextSufficiencyKind.SUFFICIENT_FOR_FUTURE_PATCH_METADATA,
        source_snapshot_ids=[file_snapshot.file_snapshot_id],
        excerpt_ids=[excerpt.source_excerpt_id],
        symbol_hint_ids=[hint.symbol_context_hint_id],
        sufficient_for_future_scope_planning=True,
        sufficient_for_future_patch_metadata=True,
    )
    return build_repair_source_context_snapshot(
        source_context_snapshot_id="snapshot:source-context",
        file_snapshots=[file_snapshot],
        source_excerpts=[excerpt],
        symbol_context_hints=[hint],
        context_assessment=assessment,
        snapshot_summary=summary,
    )


def _scope_plan(summary="scope plan supports future patch metadata"):
    intent = build_repair_change_intent(rationale=summary)
    return build_repair_scope_plan(change_intents=[intent], plan_summary=summary)


def test_taxonomies_have_required_values():
    assert {item.value for item in RepairPatchMetadataMode} == {
        "proposed_diff_metadata",
        "proposed_code_hunk_metadata",
        "proposed_file_change_metadata",
        "proposed_patch_envelope_metadata",
        "change_rationale_metadata",
        "patch_evidence_map",
        "do_nothing_patch_comparison",
        "future_safety_validation_input",
        "future_human_review_packet_input",
        "blocked",
        "no_op",
        "unknown",
    }
    assert "v0383_repair_scope_plan" in {item.value for item in RepairPatchMetadataSourceKind}
    assert "patch_envelope_created" in {item.value for item in RepairPatchMetadataStatus}
    assert "future_safety_validation_input_ready" in {item.value for item in RepairPatchMetadataReadinessLevel}
    assert "allow_proposed_code_hunk_metadata" in {item.value for item in RepairPatchMetadataDecisionKind}
    assert "dependency_install_risk" in {item.value for item in RepairPatchMetadataRiskKind}
    assert "proposed_patch_envelope" in {item.value for item in ProposedPatchArtifactKind}
    assert "unified_diff_like_metadata" in {item.value for item in ProposedDiffFormatKind}
    assert "import_path_adjustment" in {item.value for item in ProposedCodeHunkKind}
    assert "propose_replace" in {item.value for item in ProposedChangeOperationKind}
    assert "unsafe_operation_blocked" in {item.value for item in ProposedPatchDisposition}
    assert "inconclusive" in {item.value for item in ProposedPatchConfidenceLevel}
    assert "human_review_required_before_any_apply" in {item.value for item in ProposedPatchReviewRequirementKind}
    assert "do_nothing_required_due_to_high_risk" in {item.value for item in ProposedPatchDoNothingComparisonKind}
    assert "scope_plan_ref" in {item.value for item in ProposedPatchEvidenceKind}


def test_required_models_are_exported():
    for model in (
        RepairPatchMetadataFlagSet,
        RepairPatchMetadataSourceRef,
        RepairPatchMetadataPolicy,
        RepairPatchMetadataInput,
        ProposedChangeEvidenceMap,
        ProposedChangeRationale,
        ProposedCodeHunk,
        ProposedDiffMetadata,
        ProposedFileChange,
        ProposedPatchReviewRequirement,
        ProposedPatchDoNothingComparison,
        ProposedPatchEnvelope,
        RepairPatchMetadataDecision,
        RepairPatchMetadataValidationFinding,
        RepairPatchMetadataValidationReport,
        RepairPatchMetadataReport,
        RepairPatchMetadataRunPreview,
        RepairPatchMetadataNoApplyGuarantee,
        V0384ReadinessReport,
    ):
        assert model is not None


def test_flags_allow_patch_metadata_readiness_and_preserve_no_apply():
    flags = build_repair_patch_metadata_flags()
    assert flags.repair_patch_metadata_layer_constructed
    assert flags.proposed_diff_metadata_available
    assert flags.proposed_code_hunk_metadata_available
    assert flags.proposed_file_change_metadata_available
    assert flags.proposed_patch_envelope_metadata_available
    assert flags.proposed_change_rationale_available
    assert flags.proposed_change_evidence_map_available
    assert flags.proposed_patch_do_nothing_comparison_available
    assert flags.proposed_patch_review_requirement_available
    for name in SAFE_FLAG_NAMES:
        assert getattr(flags, name) is True
    assert repair_patch_metadata_flags_preserve_no_apply(flags)
    for name in _unsafe_flag_names(RepairPatchMetadataFlagSet):
        assert getattr(flags, name) is False


@pytest.mark.parametrize("field_name", _unsafe_flag_names(RepairPatchMetadataFlagSet))
def test_flags_reject_unsafe_true(field_name):
    with pytest.raises(ValueError):
        build_repair_patch_metadata_flags(**{field_name: True})


def test_policy_allows_proposed_metadata_and_blocks_apply_repair():
    policy = default_repair_patch_metadata_policy()
    assert policy.allow_proposed_diff_metadata
    assert policy.allow_proposed_code_hunk_metadata
    assert policy.allow_proposed_file_change_metadata
    assert policy.allow_proposed_patch_envelope_metadata
    assert policy.allow_change_rationale_metadata
    assert policy.allow_patch_evidence_map
    assert policy.allow_future_safety_validation_input
    assert policy.allow_future_human_review_packet_input
    assert repair_patch_metadata_policy_blocks_apply_and_repair(policy)
    for name in (
        "allow_source_file_read",
        "allow_sandbox_source_read",
        "allow_live_workspace_read",
        "allow_source_file_write",
        "allow_sandbox_source_write",
        "allow_patch_file_write",
        "allow_file_edit",
        "allow_patch_application",
        "allow_apply_patch",
        "allow_git_apply",
        "allow_repair_execution",
        "allow_automatic_repair",
        "allow_test_execution",
        "allow_subprocess",
        "allow_shell",
        "allow_dependency_install",
        "allow_network_access",
        "allow_model_provider_invocation",
        "allow_external_agent_execution",
        "allow_dominion_runtime",
    ):
        assert getattr(policy, name) is False
        with pytest.raises(ValueError):
            build_repair_patch_metadata_policy(**{name: True})


def test_input_is_patch_metadata_request_not_apply_request():
    source_ref = build_repair_patch_metadata_source_ref()
    patch_input = build_repair_patch_metadata_input(source_refs=[source_ref])
    assert patch_input.requested_mode == RepairPatchMetadataMode.PROPOSED_PATCH_ENVELOPE_METADATA
    assert "patch_file_write" in patch_input.prohibited_runtime_actions
    assert "apply_patch" in patch_input.prohibited_runtime_actions
    assert "git_apply" in patch_input.prohibited_runtime_actions
    assert "dominion" in patch_input.prohibited_runtime_actions
    with pytest.raises(ValueError):
        build_repair_patch_metadata_input(prohibited_runtime_actions=["source_read"])


def test_evidence_map_and_rationale_are_metadata_only():
    evidence_map = build_proposed_change_evidence_map(
        contradictory_evidence_refs=["contradiction"],
        missing_evidence_items=["source excerpt"],
        confidence=ProposedPatchConfidenceLevel.LOW,
    )
    assert evidence_map.supporting_evidence_refs
    assert evidence_map.contradictory_evidence_refs
    assert evidence_map.missing_evidence_items
    with pytest.raises(ValueError):
        build_proposed_change_evidence_map(missing_evidence_items=["source excerpt"], confidence=ProposedPatchConfidenceLevel.HIGH)

    rationale = build_proposed_change_rationale(evidence_map_id=evidence_map.change_evidence_map_id)
    assert rationale.human_review_required
    assert "not proof" in rationale.rationale_summary


def test_proposed_code_hunk_is_bounded_and_not_edit():
    hunk = build_proposed_code_hunk()
    assert hunk.bounded
    assert hunk.generated_from_source_context
    assert proposed_code_hunk_is_not_edit(hunk)
    for name in ("source_read_performed_by_v0384", "write_performed", "edit_applied", "patch_applied", "repair_executed"):
        assert getattr(hunk, name) is False
        with pytest.raises(ValueError):
            build_proposed_code_hunk(**{name: True})
    with pytest.raises(ValueError):
        build_proposed_code_hunk(bounded=False)


def test_proposed_diff_metadata_is_in_memory_and_not_applied():
    diff = build_proposed_diff_metadata()
    assert diff.in_memory_only
    assert diff.bounded
    assert proposed_diff_metadata_is_not_applied_diff(diff)
    for name in ("written_to_file", "applied", "repair_executed"):
        assert getattr(diff, name) is False
        with pytest.raises(ValueError):
            build_proposed_diff_metadata(**{name: True})
    with pytest.raises(ValueError):
        build_proposed_diff_metadata(in_memory_only=False)


def test_proposed_file_change_is_not_file_modification():
    change = build_proposed_file_change()
    assert change.proposed_hunks
    assert change.proposed_diff is not None
    for name in ("creates_new_file", "deletes_file", "renames_file", "changes_permissions", "writes_file", "applies_patch", "repair_executed"):
        assert getattr(change, name) is False
        with pytest.raises(ValueError):
            build_proposed_file_change(**{name: True})


def test_review_requirement_is_not_approval_and_do_nothing_is_represented():
    requirement = build_proposed_patch_review_requirement()
    assert requirement.required_before_any_apply
    assert requirement.human_approval_present is False
    with pytest.raises(ValueError):
        build_proposed_patch_review_requirement(human_approval_present=True)

    comparison = build_proposed_patch_do_nothing_comparison()
    assert comparison.do_nothing_remains_valid
    preferred = build_proposed_patch_do_nothing_comparison(
        comparison_kind=ProposedPatchDoNothingComparisonKind.DO_NOTHING_PREFERRED,
        do_nothing_preferred=True,
        patch_metadata_outperforms_do_nothing=False,
    )
    assert preferred.do_nothing_preferred
    with pytest.raises(ValueError):
        build_proposed_patch_do_nothing_comparison(do_nothing_preferred=True, patch_metadata_outperforms_do_nothing=True)


def test_patch_envelope_is_not_application_or_execution():
    envelope = build_proposed_patch_envelope()
    assert envelope.ready_for_future_safety_validation_input
    assert envelope.ready_for_future_human_review_packet_input
    assert proposed_patch_envelope_is_not_patch_application(envelope)
    for name in (
        "source_read_performed_by_v0384",
        "file_write_performed",
        "patch_file_written",
        "file_edit_performed",
        "patch_applied",
        "apply_patch_called",
        "git_apply_called",
        "tests_run",
        "repair_executed",
        "production_certified",
        "ready_for_execution",
    ):
        assert getattr(envelope, name) is False
        with pytest.raises(ValueError):
            build_proposed_patch_envelope(**{name: True})


def test_do_nothing_preferred_review_gates_envelope():
    comparison = build_proposed_patch_do_nothing_comparison(
        do_nothing_preferred=True,
        patch_metadata_outperforms_do_nothing=False,
    )
    envelope = build_proposed_patch_envelope(
        do_nothing_comparison=comparison,
        disposition=ProposedPatchDisposition.REVIEW_REQUIRED,
        ready_for_future_safety_validation_input=False,
        ready_for_future_human_review_packet_input=False,
    )
    assert envelope.disposition == ProposedPatchDisposition.REVIEW_REQUIRED
    assert not envelope.ready_for_future_safety_validation_input
    with pytest.raises(ValueError):
        build_proposed_patch_envelope(do_nothing_comparison=comparison, disposition=ProposedPatchDisposition.PROPOSED)


def test_patch_metadata_decision_does_not_allow_runtime_now():
    decision = build_repair_patch_metadata_decision()
    assert decision.ready_for_future_safety_validation_input
    assert decision.ready_for_future_human_review_packet_input
    assert repair_patch_metadata_decision_is_not_apply_permission(decision)
    for name in (
        "source_read_allowed_now",
        "write_allowed_now",
        "patch_file_write_allowed_now",
        "edit_allowed_now",
        "apply_allowed_now",
        "apply_patch_allowed_now",
        "git_apply_allowed_now",
        "repair_execution_allowed_now",
        "test_execution_allowed_now",
        "model_provider_invocation_allowed_now",
        "external_agent_allowed_now",
    ):
        assert getattr(decision, name) is False
        with pytest.raises(ValueError):
            build_repair_patch_metadata_decision(**{name: True})


def test_create_patch_metadata_from_scope_and_source_context():
    scope_plan = _scope_plan()
    snapshot = _source_context_snapshot()
    patch_input = build_repair_patch_metadata_input_from_scope_plan(scope_plan, snapshot)
    envelope = create_proposed_patch_envelope(patch_input, scope_plan, snapshot)
    assert envelope.proposed_hunks
    assert envelope.proposed_diffs
    assert envelope.file_changes
    assert envelope.proposed_hunks[0].source_read_performed_by_v0384 is False
    assert envelope.proposed_diffs[0].in_memory_only
    assert envelope.ready_for_future_safety_validation_input
    assert proposed_patch_envelope_is_not_patch_application(envelope)


def test_missing_scope_or_source_context_blocks():
    patch_input = build_repair_patch_metadata_input()
    envelope_missing_scope = create_proposed_patch_envelope(patch_input, None, _source_context_snapshot())
    assert envelope_missing_scope.disposition == ProposedPatchDisposition.INSUFFICIENT_CONTEXT
    assert not envelope_missing_scope.ready_for_future_safety_validation_input

    envelope_missing_context = create_proposed_patch_envelope(patch_input, _scope_plan(), None)
    assert envelope_missing_context.disposition == ProposedPatchDisposition.INSUFFICIENT_CONTEXT
    assert not envelope_missing_context.ready_for_future_human_review_packet_input


def test_missing_dependency_and_timeout_do_not_create_install_or_retry_patch():
    dependency_plan = _scope_plan("inspect missing dependency without install")
    dependency_input = build_repair_patch_metadata_input_from_scope_plan(dependency_plan, _source_context_snapshot("missing dependency"))
    dependency_envelope = create_proposed_patch_envelope(dependency_input, dependency_plan, _source_context_snapshot("missing dependency"))
    assert dependency_envelope.disposition == ProposedPatchDisposition.UNSAFE_OPERATION_BLOCKED
    assert not dependency_envelope.proposed_hunks
    assert dependency_envelope.do_nothing_comparison.do_nothing_required

    timeout_plan = _scope_plan("inspect timeout without retry loop")
    timeout_input = build_repair_patch_metadata_input_from_scope_plan(timeout_plan, _source_context_snapshot("timeout"))
    timeout_envelope = create_proposed_patch_envelope(timeout_input, timeout_plan, _source_context_snapshot("timeout"))
    assert timeout_envelope.disposition == ProposedPatchDisposition.UNSAFE_OPERATION_BLOCKED
    assert not timeout_envelope.proposed_diffs


@pytest.mark.parametrize(
    "summary",
    [
        "add network call",
        "add subprocess shell command",
        "invoke model provider",
        "call external agent",
        "enable dominion",
        "read secret token",
        "delete file",
        "rename file",
        "chmod permission",
    ],
)
def test_unsafe_operations_block(summary):
    scope_plan = _scope_plan(summary)
    snapshot = _source_context_snapshot(summary)
    patch_input = build_repair_patch_metadata_input_from_scope_plan(scope_plan, snapshot, task_summary=summary)
    envelope = create_proposed_patch_envelope(patch_input, scope_plan, snapshot)
    assert envelope.disposition == ProposedPatchDisposition.UNSAFE_OPERATION_BLOCKED
    assert not envelope.ready_for_future_safety_validation_input


def test_validation_report_report_run_preview_guarantee_and_readiness():
    envelope = build_proposed_patch_envelope()
    validation = validate_proposed_patch_envelope(envelope)
    assert validation.metadata_only_proposal_confirmed
    assert validation.bounded_diff_text_confirmed
    assert validation.no_file_write_confirmed
    assert validation.no_patch_file_write_confirmed
    assert validation.no_edit_confirmed
    assert validation.no_apply_confirmed
    assert validation.no_repair_confirmed
    assert validation.no_tests_confirmed
    assert validation.do_nothing_comparison_confirmed

    decision = decide_repair_patch_metadata(envelope)
    report = build_repair_patch_metadata_report(envelope=envelope, decision=decision, validation_report=validation)
    assert report.ready_for_future_safety_validation_input
    assert report.ready_for_future_human_review_packet_input
    assert report.ready_for_execution is False
    assert report.production_certified is False

    preview = build_repair_patch_metadata_run_preview()
    for field in fields(preview):
        if field.name.startswith("will_"):
            assert getattr(preview, field.name) is False

    guarantee = build_repair_patch_metadata_no_apply_guarantee()
    for field in fields(guarantee):
        if field.name.startswith("no_"):
            assert getattr(guarantee, field.name) is True
    with pytest.raises(ValueError):
        build_repair_patch_metadata_no_apply_guarantee(no_apply=False)

    readiness = build_v0384_readiness_report(proposed_patch_envelope_id=envelope.proposed_patch_envelope_id)
    assert readiness.ready_for_v0385_repair_proposal_safety_validation
    assert readiness.ready_for_v0386_human_review_packet
    assert readiness.ready_for_repair_patch_metadata_generation
    assert readiness.ready_for_proposed_diff_metadata_generation
    assert readiness.ready_for_proposed_code_hunk_metadata_generation
    assert readiness.ready_for_proposed_patch_envelope_metadata_generation
    assert readiness.ready_for_future_repair_proposal_safety_validation_input
    assert readiness.ready_for_future_human_review_packet_input
    assert v0384_readiness_report_is_not_execution_ready(readiness)
    for name in _unsafe_flag_names(V0384ReadinessReport):
        assert getattr(readiness, name) is False
        with pytest.raises(ValueError):
            build_v0384_readiness_report(**{name: True})


def test_helper_functions_create_bounded_in_memory_metadata_only():
    scope_plan = _scope_plan()
    snapshot = _source_context_snapshot()
    evidence_map = create_proposed_change_evidence_map_from_scope(scope_plan, snapshot)
    rationale = create_proposed_change_rationale_from_intent(scope_plan.change_intents[0], evidence_map)
    hunks = create_proposed_code_hunks_from_scope_context(scope_plan, snapshot)
    diffs = create_proposed_diff_metadata_from_hunks(hunks, evidence_map)
    changes = create_proposed_file_changes(hunks, diffs, evidence_map, rationale)
    comparison = compare_proposed_patch_to_do_nothing(evidence_map)
    requirement = create_proposed_patch_review_requirement()
    assert evidence_map.supporting_evidence_refs
    assert rationale.human_review_required
    assert hunks and proposed_code_hunk_is_not_edit(hunks[0])
    assert diffs and proposed_diff_metadata_is_not_applied_diff(diffs[0])
    assert changes and changes[0].writes_file is False
    assert comparison.do_nothing_remains_valid
    assert requirement.human_approval_present is False


def test_helpers_do_not_contain_forbidden_runtime_patterns():
    import chanta_core.agent_runtime.repair_patch_metadata as module

    source = inspect.getsource(module)
    forbidden = [
        "Path.read_text",
        "Path.read_bytes",
        "open(",
        "write_text",
        "write_bytes",
        "import subprocess",
        "subprocess.",
        "os.system",
        "shell=True",
        "import requests",
        "import httpx",
        "import urllib",
        "import aiohttp",
        "import socket",
        "eval(",
        "exec(",
    ]
    for pattern in forbidden:
        assert pattern not in source
