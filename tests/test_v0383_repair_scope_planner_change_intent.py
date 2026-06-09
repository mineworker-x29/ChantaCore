from dataclasses import fields
import inspect

import pytest

from chanta_core.agent_runtime import (
    RepairAffectedArtifactKind,
    RepairAffectedFileCandidate,
    RepairAffectedSymbolCandidate,
    RepairChangeIntent,
    RepairChangeIntentKind,
    RepairScopeConfidenceLevel,
    RepairScopeDisposition,
    RepairScopeDoNothingComparison,
    RepairScopeDoNothingComparisonKind,
    RepairScopeEvidenceKind,
    RepairScopeEvidenceMap,
    RepairScopeKind,
    RepairScopePlan,
    RepairScopePlanningDecision,
    RepairScopePlanningDecisionKind,
    RepairScopePlanningFlagSet,
    RepairScopePlanningInput,
    RepairScopePlanningMode,
    RepairScopePlanningNoGenerationGuarantee,
    RepairScopePlanningPolicy,
    RepairScopePlanningReadinessLevel,
    RepairScopePlanningReport,
    RepairScopePlanningRiskKind,
    RepairScopePlanningRunPreview,
    RepairScopePlanningSourceKind,
    RepairScopePlanningSourceRef,
    RepairScopePlanningStatus,
    RepairScopePlanningValidationFinding,
    RepairScopePlanningValidationReport,
    RepairScopeRiskAssessment,
    RepairSourceContextSufficiencyKind,
    V0383ReadinessReport,
    assess_repair_scope_risk,
    build_repair_affected_file_candidate,
    build_repair_affected_symbol_candidate,
    build_repair_change_intent,
    build_repair_scope_do_nothing_comparison,
    build_repair_scope_evidence_map,
    build_repair_scope_plan,
    build_repair_scope_planning_decision,
    build_repair_scope_planning_flags,
    build_repair_scope_planning_input,
    build_repair_scope_planning_input_from_source_context,
    build_repair_scope_planning_no_generation_guarantee,
    build_repair_scope_planning_policy,
    build_repair_scope_planning_report,
    build_repair_scope_planning_run_preview,
    build_repair_scope_planning_source_ref,
    build_repair_scope_planning_validation_finding,
    build_repair_scope_planning_validation_report,
    build_repair_scope_risk_assessment,
    build_repair_source_context_assessment,
    build_repair_source_context_snapshot,
    build_repair_source_excerpt,
    build_repair_source_file_snapshot,
    build_repair_symbol_context_hint,
    build_scope_evidence_map_from_context_and_evidence,
    build_v0383_readiness_report,
    compare_scope_plan_to_do_nothing,
    create_repair_scope_plan,
    decide_repair_scope_planning,
    default_repair_scope_planning_policy,
    derive_affected_file_candidates_from_source_context,
    derive_affected_symbol_candidates_from_source_context,
    derive_repair_change_intents,
    repair_change_intent_is_not_code_modification,
    repair_scope_decision_is_not_generation_permission,
    repair_scope_plan_is_not_proposal,
    repair_scope_planning_flags_preserve_no_generation,
    repair_scope_policy_blocks_generation_and_execution,
    v0383_readiness_report_is_not_execution_ready,
    validate_repair_scope_plan,
)


SAFE_FLAG_NAMES = {
    "ready_for_v0384_proposed_diff_code_hunk_metadata",
    "ready_for_v0385_repair_proposal_safety_validation",
    "ready_for_repair_scope_planner",
    "ready_for_change_intent_model",
    "ready_for_affected_file_candidates",
    "ready_for_affected_symbol_candidates",
    "ready_for_scope_evidence_map",
    "ready_for_scope_risk_assessment",
    "ready_for_do_nothing_scope_comparison",
    "ready_for_future_proposed_diff_metadata_input",
    "ready_for_future_proposed_code_hunk_metadata_input",
}


def _unsafe_flag_names(cls):
    return [
        field.name
        for field in fields(cls)
        if (field.name.startswith("ready_for_") and field.name not in SAFE_FLAG_NAMES)
        or field.name == "production_certified"
    ]


def _source_context_snapshot(task_summary="assertion mismatch points at target function"):
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
        excerpt_summary=task_summary,
    )
    hint = build_repair_symbol_context_hint(
        symbol_context_hint_id="hint:target_function",
        source_excerpt_id=excerpt.source_excerpt_id,
        normalized_relative_path="pkg/module.py",
        symbol_name="target_function",
        hint_summary="target function appears in supplied v0.38.2 excerpt metadata",
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
        snapshot_summary=task_summary,
    )


def test_taxonomies_have_required_values():
    assert {item.value for item in RepairScopePlanningMode} == {
        "repair_scope_plan",
        "change_intent_model",
        "affected_file_candidates",
        "affected_symbol_candidates",
        "scope_evidence_map",
        "scope_risk_assessment",
        "do_nothing_scope_comparison",
        "future_patch_metadata_input",
        "blocked",
        "no_op",
        "unknown",
    }
    assert "v0382_source_context_snapshot" in {item.value for item in RepairScopePlanningSourceKind}
    assert "ready_for_future_patch_metadata" in {item.value for item in RepairScopePlanningStatus}
    assert "design_handoff_ready_for_v0384" in {item.value for item in RepairScopePlanningReadinessLevel}
    assert "allow_change_intent_model" in {item.value for item in RepairScopePlanningDecisionKind}
    assert "dependency_install_confusion_risk" in {item.value for item in RepairScopePlanningRiskKind}
    assert "dependency_inspection_scope" in {item.value for item in RepairScopeKind}
    assert "inspect_timeout_without_retry" in {item.value for item in RepairChangeIntentKind}
    assert "function_symbol" in {item.value for item in RepairAffectedArtifactKind}
    assert "selected_primary_scope" in {item.value for item in RepairScopeDisposition}
    assert "inconclusive" in {item.value for item in RepairScopeConfidenceLevel}
    assert "source_context_snapshot_ref" in {item.value for item in RepairScopeEvidenceKind}
    assert "do_nothing_preferred_due_to_high_scope_risk" in {item.value for item in RepairScopeDoNothingComparisonKind}


def test_required_models_are_exported():
    for model in (
        RepairScopePlanningFlagSet,
        RepairScopePlanningSourceRef,
        RepairScopePlanningPolicy,
        RepairScopePlanningInput,
        RepairAffectedFileCandidate,
        RepairAffectedSymbolCandidate,
        RepairScopeEvidenceMap,
        RepairScopeRiskAssessment,
        RepairChangeIntent,
        RepairScopeDoNothingComparison,
        RepairScopePlan,
        RepairScopePlanningDecision,
        RepairScopePlanningValidationFinding,
        RepairScopePlanningValidationReport,
        RepairScopePlanningReport,
        RepairScopePlanningRunPreview,
        RepairScopePlanningNoGenerationGuarantee,
        V0383ReadinessReport,
    ):
        assert model is not None


def test_flags_allow_scope_readiness_and_preserve_no_generation():
    flags = build_repair_scope_planning_flags()
    assert flags.repair_scope_planning_layer_constructed
    assert flags.repair_scope_planner_available
    assert flags.change_intent_model_available
    assert flags.affected_file_candidates_available
    assert flags.affected_symbol_candidates_available
    assert flags.scope_evidence_map_available
    assert flags.scope_risk_assessment_available
    assert flags.do_nothing_scope_comparison_available
    for name in SAFE_FLAG_NAMES:
        assert getattr(flags, name) is True
    assert repair_scope_planning_flags_preserve_no_generation(flags)
    for name in _unsafe_flag_names(RepairScopePlanningFlagSet):
        assert getattr(flags, name) is False


@pytest.mark.parametrize("field_name", _unsafe_flag_names(RepairScopePlanningFlagSet))
def test_flags_reject_unsafe_true(field_name):
    with pytest.raises(ValueError):
        build_repair_scope_planning_flags(**{field_name: True})


def test_policy_allows_scope_metadata_and_blocks_generation_execution():
    policy = default_repair_scope_planning_policy()
    assert policy.allow_scope_planning
    assert policy.allow_affected_file_candidates
    assert policy.allow_affected_symbol_candidates
    assert policy.allow_scope_evidence_map
    assert policy.allow_change_intent_model
    assert policy.allow_scope_risk_assessment
    assert policy.allow_do_nothing_scope_comparison
    assert policy.allow_future_patch_metadata_input
    assert repair_scope_policy_blocks_generation_and_execution(policy)
    for name in (
        "allow_source_file_read",
        "allow_sandbox_source_read",
        "allow_live_workspace_read",
        "allow_source_file_write",
        "allow_repair_proposal_generation",
        "allow_proposed_diff_generation",
        "allow_proposed_code_hunk_generation",
        "allow_proposed_patch_envelope_generation",
        "allow_repair_patch_proposal",
        "allow_repair_execution",
        "allow_patch_application",
        "allow_apply_patch",
        "allow_git_apply",
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
            build_repair_scope_planning_policy(**{name: True})


def test_scope_input_is_scope_request_not_generation_request():
    source_ref = build_repair_scope_planning_source_ref()
    scope_input = build_repair_scope_planning_input(source_refs=[source_ref])
    assert scope_input.requested_mode == RepairScopePlanningMode.REPAIR_SCOPE_PLAN
    assert "proposal_generation" in scope_input.prohibited_runtime_actions
    assert "diff_generation" in scope_input.prohibited_runtime_actions
    assert "dominion" in scope_input.prohibited_runtime_actions
    with pytest.raises(ValueError):
        build_repair_scope_planning_input(prohibited_runtime_actions=["source_read"])


def test_candidates_are_metadata_only():
    file_candidate = build_repair_affected_file_candidate()
    assert file_candidate.source_read_performed_by_v0383 is False
    for name in ("edit_allowed", "proposal_generation_allowed", "diff_generation_allowed", "hunk_generation_allowed", "repair_execution_allowed"):
        assert getattr(file_candidate, name) is False
        with pytest.raises(ValueError):
            build_repair_affected_file_candidate(**{name: True})

    symbol_candidate = build_repair_affected_symbol_candidate(symbol_name="Worker")
    assert symbol_candidate.imported_or_executed_source is False
    assert symbol_candidate.artifact_kind == RepairAffectedArtifactKind.CLASS_SYMBOL
    for name in ("edit_allowed", "proposal_generation_allowed", "diff_generation_allowed", "hunk_generation_allowed", "repair_execution_allowed"):
        assert getattr(symbol_candidate, name) is False
    with pytest.raises(ValueError):
        build_repair_affected_symbol_candidate(imported_or_executed_source=True)


def test_evidence_map_and_risk_assessment_conservative_behavior():
    evidence_map = build_repair_scope_evidence_map(
        contradictory_evidence_refs=["contradictory:test"],
        missing_evidence_items=["source context"],
        confidence=RepairScopeConfidenceLevel.LOW,
    )
    assert evidence_map.contradictory_evidence_refs
    assert evidence_map.missing_evidence_items
    with pytest.raises(ValueError):
        build_repair_scope_evidence_map(missing_evidence_items=["source context"], confidence=RepairScopeConfidenceLevel.HIGH)

    risk = build_repair_scope_risk_assessment(
        severity="high",
        requires_human_review=True,
        blocks_future_patch_metadata=True,
    )
    assert risk.requires_human_review
    assert risk.blocks_future_patch_metadata
    with pytest.raises(ValueError):
        build_repair_scope_risk_assessment(severity="high", requires_human_review=False, blocks_future_patch_metadata=False)


def test_change_intent_future_gate_and_no_now_permissions():
    intent = build_repair_change_intent()
    assert intent.future_patch_metadata_input_eligible
    assert repair_change_intent_is_not_code_modification(intent)
    for name in (
        "source_read_allowed_now",
        "edit_allowed_now",
        "proposal_generation_allowed_now",
        "diff_generation_allowed_now",
        "hunk_generation_allowed_now",
        "patch_envelope_generation_allowed_now",
        "repair_execution_allowed_now",
    ):
        assert getattr(intent, name) is False
        with pytest.raises(ValueError):
            build_repair_change_intent(**{name: True})
    with pytest.raises(ValueError):
        build_repair_change_intent(
            intent_kind=RepairChangeIntentKind.DO_NOTHING,
            future_patch_metadata_input_eligible=True,
        )


def test_do_nothing_comparison_is_mandatory_and_can_block_future_patch_metadata():
    comparison = build_repair_scope_do_nothing_comparison()
    assert comparison.do_nothing_remains_valid
    preferred = build_repair_scope_do_nothing_comparison(
        comparison_kind=RepairScopeDoNothingComparisonKind.DO_NOTHING_PREFERRED_DUE_TO_INSUFFICIENT_CONTEXT,
        do_nothing_preferred=True,
        scope_plan_outperforms_do_nothing=False,
    )
    assert preferred.do_nothing_preferred
    with pytest.raises(ValueError):
        build_repair_scope_do_nothing_comparison(do_nothing_preferred=True, scope_plan_outperforms_do_nothing=True)


def test_scope_plan_readiness_requires_supported_intent_risk_and_do_nothing():
    plan = build_repair_scope_plan()
    assert plan.ready_for_future_patch_metadata_input
    assert plan.ready_for_future_proposed_diff_metadata_input
    assert plan.ready_for_future_proposed_code_hunk_metadata_input
    assert repair_scope_plan_is_not_proposal(plan)
    for name in (
        "source_read_performed_by_v0383",
        "proposal_generated",
        "diff_generated",
        "hunk_generated",
        "patch_envelope_generated",
        "file_edit_performed",
        "repair_executed",
        "production_certified",
        "ready_for_execution",
    ):
        assert getattr(plan, name) is False
        with pytest.raises(ValueError):
            build_repair_scope_plan(**{name: True})

    blocked_risk = build_repair_scope_risk_assessment(
        severity="high",
        blocks_future_patch_metadata=True,
        requires_human_review=True,
    )
    with pytest.raises(ValueError):
        build_repair_scope_plan(risk_assessment=blocked_risk, ready_for_future_patch_metadata_input=True)


def test_scope_decision_does_not_allow_generation_now():
    decision = build_repair_scope_planning_decision()
    assert decision.ready_for_future_patch_metadata_input
    assert repair_scope_decision_is_not_generation_permission(decision)
    for name in (
        "source_read_allowed_now",
        "proposal_generation_allowed_now",
        "diff_generation_allowed_now",
        "hunk_generation_allowed_now",
        "patch_envelope_generation_allowed_now",
        "repair_execution_allowed_now",
    ):
        assert getattr(decision, name) is False
        with pytest.raises(ValueError):
            build_repair_scope_planning_decision(**{name: True})


def test_create_scope_plan_consumes_source_context_metadata_without_reads():
    snapshot = _source_context_snapshot()
    scope_input = build_repair_scope_planning_input_from_source_context(snapshot, task_summary="assertion mismatch")
    plan = create_repair_scope_plan(scope_input, snapshot)
    assert plan.affected_file_candidates[0].normalized_relative_path == "pkg/module.py"
    assert plan.affected_file_candidates[0].source_read_performed_by_v0383 is False
    assert plan.affected_symbol_candidates[0].imported_or_executed_source is False
    assert plan.change_intents[0].intent_kind in (
        RepairChangeIntentKind.REVIEW_TEST_EXPECTATION_FUTURE_GATE,
        RepairChangeIntentKind.ALIGN_IMPLEMENTATION_WITH_TEST,
    )
    assert plan.ready_for_future_patch_metadata_input
    assert repair_scope_plan_is_not_proposal(plan)


def test_behavioral_scope_mappings_without_install_or_retry():
    dependency_snapshot = _source_context_snapshot("module not found missing dependency")
    dependency_input = build_repair_scope_planning_input_from_source_context(
        dependency_snapshot,
        task_summary="ModuleNotFoundError missing dependency",
    )
    dependency_plan = create_repair_scope_plan(dependency_input, dependency_snapshot)
    assert dependency_plan.change_intents[0].scope_kind == RepairScopeKind.DEPENDENCY_INSPECTION_SCOPE
    assert dependency_plan.change_intents[0].intent_kind == RepairChangeIntentKind.INSPECT_MISSING_DEPENDENCY_WITHOUT_INSTALL
    assert dependency_plan.change_intents[0].edit_allowed_now is False

    timeout_snapshot = _source_context_snapshot("timeout in sandbox test")
    timeout_input = build_repair_scope_planning_input_from_source_context(timeout_snapshot, task_summary="timeout performance failure")
    timeout_plan = create_repair_scope_plan(timeout_input, timeout_snapshot)
    assert timeout_plan.change_intents[0].scope_kind == RepairScopeKind.PERFORMANCE_INVESTIGATION_SCOPE
    assert timeout_plan.change_intents[0].intent_kind == RepairChangeIntentKind.INSPECT_TIMEOUT_WITHOUT_RETRY
    assert timeout_plan.change_intents[0].repair_execution_allowed_now is False

    import_snapshot = _source_context_snapshot("import path failure")
    import_input = build_repair_scope_planning_input_from_source_context(import_snapshot, task_summary="import path failure")
    import_plan = create_repair_scope_plan(import_input, import_snapshot)
    assert import_plan.change_intents[0].scope_kind == RepairScopeKind.IMPORT_PATH_SCOPE
    assert import_plan.change_intents[0].intent_kind == RepairChangeIntentKind.ADJUST_IMPORT_PATH_FUTURE_GATE


def test_no_repair_and_insufficient_context_choose_do_nothing_or_review():
    snapshot = build_repair_source_context_snapshot(
        file_snapshots=[],
        source_excerpts=[],
        symbol_context_hints=[],
        context_assessment=build_repair_source_context_assessment(
            sufficiency_kind=RepairSourceContextSufficiencyKind.INSUFFICIENT_MISSING_SOURCE,
            source_snapshot_ids=[],
            excerpt_ids=[],
            symbol_hint_ids=[],
            missing_context_items=["source context"],
            sufficient_for_future_scope_planning=False,
            sufficient_for_future_patch_metadata=False,
        ),
        ready_for_future_scope_planning_input=False,
        ready_for_future_patch_metadata_input=False,
        snapshot_summary="no repair needed or insufficient context",
    )
    scope_input = build_repair_scope_planning_input_from_source_context(snapshot, task_summary="no repair needed")
    plan = create_repair_scope_plan(scope_input, snapshot)
    decision = decide_repair_scope_planning(plan)
    assert plan.do_nothing_comparison.do_nothing_preferred
    assert not plan.ready_for_future_patch_metadata_input
    assert decision.decision_kind in (
        RepairScopePlanningDecisionKind.CHOOSE_DO_NOTHING,
        RepairScopePlanningDecisionKind.REQUIRE_REVIEW,
    )


def test_validation_report_report_run_preview_guarantee_and_readiness():
    plan = build_repair_scope_plan()
    validation = validate_repair_scope_plan(plan)
    assert validation.metadata_only_scope_planning_confirmed
    assert validation.no_source_read_confirmed
    assert validation.no_proposal_generation_confirmed
    assert validation.no_diff_generation_confirmed
    assert validation.no_hunk_generation_confirmed
    assert validation.no_patch_envelope_generation_confirmed
    assert validation.no_edit_confirmed
    assert validation.no_repair_execution_confirmed

    decision = decide_repair_scope_planning(plan)
    report = build_repair_scope_planning_report(plan=plan, decision=decision, validation_report=validation)
    assert report.ready_for_future_patch_metadata_input
    assert report.ready_for_execution is False
    assert report.production_certified is False

    preview = build_repair_scope_planning_run_preview()
    for field in fields(preview):
        if field.name.startswith("will_"):
            assert getattr(preview, field.name) is False

    guarantee = build_repair_scope_planning_no_generation_guarantee()
    for field in fields(guarantee):
        if field.name.startswith("no_"):
            assert getattr(guarantee, field.name) is True
    with pytest.raises(ValueError):
        build_repair_scope_planning_no_generation_guarantee(no_proposed_diff_generation=False)

    readiness = build_v0383_readiness_report(scope_plan_id=plan.scope_plan_id)
    assert readiness.ready_for_v0384_proposed_diff_code_hunk_metadata
    assert readiness.ready_for_v0385_repair_proposal_safety_validation
    assert readiness.ready_for_repair_scope_planner
    assert readiness.ready_for_change_intent_model
    assert readiness.ready_for_future_proposed_diff_metadata_input
    assert readiness.ready_for_future_proposed_code_hunk_metadata_input
    assert v0383_readiness_report_is_not_execution_ready(readiness)
    for name in _unsafe_flag_names(V0383ReadinessReport):
        assert getattr(readiness, name) is False
        with pytest.raises(ValueError):
            build_v0383_readiness_report(**{name: True})


def test_builder_helpers_exist_and_are_pure_metadata_helpers():
    snapshot = _source_context_snapshot()
    files = derive_affected_file_candidates_from_source_context(snapshot)
    symbols = derive_affected_symbol_candidates_from_source_context(snapshot)
    evidence_map = build_scope_evidence_map_from_context_and_evidence(files, symbols, snapshot)
    risk = assess_repair_scope_risk(evidence_map, "assertion mismatch")
    scope_input = build_repair_scope_planning_input_from_source_context(snapshot)
    intents = derive_repair_change_intents(scope_input, files, symbols, evidence_map, risk)
    comparison = compare_scope_plan_to_do_nothing(risk, intents)
    assert files
    assert symbols
    assert evidence_map.supporting_evidence_refs
    assert risk.requires_human_review
    assert intents
    assert comparison.do_nothing_remains_valid


def test_helpers_do_not_contain_forbidden_runtime_patterns():
    import chanta_core.agent_runtime.repair_scope_planning as module

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
        "apply_patch(",
    ]
    for pattern in forbidden:
        assert pattern not in source
