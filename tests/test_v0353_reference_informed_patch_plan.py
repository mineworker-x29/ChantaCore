import inspect

import pytest

from chanta_core.agent_runtime import (
    PatchChangeKind,
    PatchChangeNodeStatus,
    PatchChangeSetGraphStatus,
    PatchDependencyKind,
    PatchPlanDecisionKind,
    PatchPlanMode,
    PatchPlanReadinessLevel,
    PatchPlanRiskKind,
    PatchPlanSourceKind,
    PatchPlanStatus,
    PatchTargetKind,
    ReferencePatternDisposition,
    build_patch_change_node,
    build_patch_change_set_graph,
    build_patch_change_set_graph_from_intent_context,
    build_patch_dependency_edge,
    build_patch_documentation_plan,
    build_patch_plan,
    build_patch_plan_flags,
    build_patch_plan_no_diff_no_apply_guarantee,
    build_patch_plan_report,
    build_patch_plan_run_preview,
    build_patch_plan_source_ref,
    build_patch_planning_input,
    build_patch_planning_input_from_context_snapshot,
    build_patch_planning_policy,
    build_patch_target_file_plan,
    build_patch_test_plan,
    build_reference_harness_pattern,
    build_reference_informed_patch_pattern_use,
    build_reference_informed_patch_pattern_uses_from_digest_and_context,
    build_reference_pattern_digest,
    build_v0353_readiness_report,
    build_patch_intent_scope_bundle,
    build_patch_context_snapshot,
    build_patch_context_reference_summary,
    default_patch_planning_policy,
    patch_change_set_graph_is_not_diff_proposal,
    patch_plan_flags_preserve_no_diff_no_apply,
    patch_plan_is_not_patch_proposal,
    patch_planning_policy_blocks_diff_apply,
    validate_patch_change_set_graph,
    validate_patch_plan,
    v0353_readiness_report_is_not_execution_ready,
)
from chanta_core.agent_runtime import patch_plan as plan_module


def test_v0353_taxonomies_have_required_values() -> None:
    assert PatchPlanMode.COMBINED_CONTEXT_AND_REFERENCE_INFORMED.value == "combined_context_and_reference_informed"
    assert PatchPlanMode.UNKNOWN.value == "unknown"
    assert PatchPlanSourceKind.V0352_PATCH_CONTEXT_SNAPSHOT.value == "v0352_patch_context_snapshot"
    assert PatchPlanStatus.CHANGE_SET_GRAPH_CREATED.value == "change_set_graph_created"
    assert PatchPlanReadinessLevel.DESIGN_HANDOFF_READY_FOR_V0354.value == "design_handoff_ready_for_v0354"
    assert PatchPlanDecisionKind.ALLOW_CHANGE_SET_GRAPH_METADATA.value == "allow_change_set_graph_metadata"
    assert PatchPlanRiskKind.PATCH_DIFF_GENERATION_RISK.value == "patch_diff_generation_risk"
    assert PatchChangeKind.ADD_CONTRACT_MODEL.value == "add_contract_model"
    assert PatchChangeNodeStatus.PLANNED.value == "planned"
    assert PatchDependencyKind.REQUIRES_PLAN_BEFORE_DIFF.value == "requires_plan_before_diff"
    assert PatchChangeSetGraphStatus.GRAPH_CREATED.value == "graph_created"


def test_patch_plan_flags_allow_plan_graph_handoff_and_block_unsafe_readiness() -> None:
    flags = build_patch_plan_flags()
    assert flags.patch_plan_layer_constructed is True
    assert flags.change_set_graph_defined is True
    assert flags.target_file_plan_defined is True
    assert flags.test_plan_defined is True
    assert flags.documentation_plan_defined is True
    assert flags.reference_informed_planning_available is True
    assert flags.ready_for_v0354_diff_proposal_envelope is True
    assert flags.ready_for_v0355_patch_risk_conformance_scanner is True
    assert flags.ready_for_patch_plan is True
    assert flags.ready_for_change_set_graph is True
    assert flags.ready_for_reference_informed_patch_plan is True
    assert flags.ready_for_execution is False
    assert flags.ready_for_diff_proposal is False
    assert flags.ready_for_patch_proposal is False
    assert flags.ready_for_patch_hunk_generation is False
    assert flags.ready_for_patch_application is False
    assert flags.ready_for_workspace_write is False
    assert flags.ready_for_code_edit is False
    assert flags.ready_for_apply_patch is False
    assert flags.ready_for_git_apply is False
    assert flags.ready_for_test_execution is False
    assert flags.ready_for_shell_execution is False
    assert flags.ready_for_reference_execution is False
    assert flags.ready_for_reference_import is False
    assert flags.production_certified is False
    assert patch_plan_flags_preserve_no_diff_no_apply(flags)


@pytest.mark.parametrize(
    "unsafe_flag",
    [
        "ready_for_execution",
        "ready_for_diff_proposal",
        "ready_for_patch_proposal",
        "ready_for_patch_hunk_generation",
        "ready_for_patch_application",
        "ready_for_workspace_write",
        "ready_for_code_edit",
        "ready_for_apply_patch",
        "ready_for_git_apply",
        "ready_for_test_execution",
        "ready_for_shell_execution",
        "ready_for_subprocess_execution",
        "ready_for_command_execution",
        "ready_for_dependency_install",
        "ready_for_reference_execution",
        "ready_for_reference_import",
        "ready_for_provider_invocation",
        "ready_for_direct_network_access",
        "ready_for_credential_access",
        "ready_for_secret_read",
    ],
)
def test_patch_plan_flags_reject_unsafe_readiness(unsafe_flag: str) -> None:
    with pytest.raises(ValueError):
        build_patch_plan_flags(**{unsafe_flag: True})


def test_source_ref_pattern_use_policy_and_input_are_metadata_only() -> None:
    source_ref = build_patch_plan_source_ref()
    assert source_ref.source_kind == PatchPlanSourceKind.V0352_PATCH_CONTEXT_SNAPSHOT

    adapted = build_reference_informed_patch_pattern_use()
    assert adapted.rejected is False
    assert adapted.future_track is False
    assert adapted.applied_to_change_node_ids

    rejected = build_reference_informed_patch_pattern_use(
        pattern_use_id="pattern_use:rejected",
        rejected=True,
        rejection_reason="Reference runtime behavior is rejected.",
        applied_to_change_node_ids=[],
    )
    assert rejected.rejected is True

    future = build_reference_informed_patch_pattern_use(
        pattern_use_id="pattern_use:future",
        future_track=True,
    )
    assert future.future_track is True

    with pytest.raises(ValueError):
        build_reference_informed_patch_pattern_use(rejected=True)

    policy = default_patch_planning_policy()
    assert policy.require_context_snapshot is True
    assert policy.require_intent_scope_bundle is True
    assert policy.require_non_goal_register is True
    assert policy.allow_reference_informed_patterns is True
    assert policy.allow_future_diff_handoff is True
    assert policy.allow_diff_text is False
    assert policy.allow_patch_hunks is False
    assert policy.allow_patch_apply is False
    assert policy.allow_workspace_write is False
    assert policy.allow_code_edit is False
    assert policy.allow_test_execution is False
    assert policy.allow_dependency_install is False
    assert policy.allow_shell is False
    assert patch_planning_policy_blocks_diff_apply(policy)

    for field in ["allow_diff_text", "allow_patch_hunks", "allow_patch_apply", "allow_workspace_write", "allow_code_edit", "allow_test_execution", "allow_dependency_install", "allow_shell"]:
        with pytest.raises(ValueError):
            build_patch_planning_policy(**{field: True})

    planning_input = build_patch_planning_input()
    assert "diff_proposal_generation" in planning_input.prohibited_runtime_actions
    assert "patch_application" in planning_input.prohibited_runtime_actions
    assert "reference_execution" in planning_input.prohibited_runtime_actions


def test_change_node_dependency_target_test_and_doc_plans_do_not_mutate() -> None:
    node = build_patch_change_node()
    assert node.status == PatchChangeNodeStatus.PLANNED
    assert node.target_file_refs
    with pytest.raises(ValueError):
        build_patch_change_node(status=PatchChangeNodeStatus.BLOCKED)

    blocked = build_patch_change_node(
        change_node_id="change_node:blocked",
        status=PatchChangeNodeStatus.BLOCKED,
        blocked_reason="Missing context.",
    )
    assert blocked.blocked_reason

    edge = build_patch_dependency_edge()
    assert edge.blocking is True

    target_plan = build_patch_target_file_plan()
    assert target_plan.allowed_for_future_diff is True
    assert target_plan.allowed_for_write is False
    assert target_plan.allowed_for_apply is False
    with pytest.raises(ValueError):
        build_patch_target_file_plan(allowed_for_write=True)
    with pytest.raises(ValueError):
        build_patch_target_file_plan(allowed_for_apply=True)

    test_plan = build_patch_test_plan()
    assert test_plan.ready_for_test_execution is False
    with pytest.raises(ValueError):
        build_patch_test_plan(ready_for_test_execution=True)

    doc_plan = build_patch_documentation_plan()
    assert doc_plan.ready_for_doc_write is False
    with pytest.raises(ValueError):
        build_patch_documentation_plan(ready_for_doc_write=True)


def test_change_set_graph_patch_plan_reports_and_guarantees_are_not_diff_or_apply() -> None:
    graph = build_patch_change_set_graph()
    assert patch_change_set_graph_is_not_diff_proposal(graph)
    assert graph.ready_for_v0354_diff_proposal_envelope is True
    assert graph.ready_for_diff_proposal is False
    assert graph.ready_for_patch_proposal is False
    assert graph.ready_for_execution is False
    for field in ["ready_for_diff_proposal", "ready_for_patch_proposal", "ready_for_execution"]:
        with pytest.raises(ValueError):
            build_patch_change_set_graph(**{field: True})

    plan = build_patch_plan(change_set_graph=graph)
    assert patch_plan_is_not_patch_proposal(plan)
    assert plan.ready_for_v0354_diff_proposal_envelope is True
    assert plan.ready_for_v0355_patch_risk_conformance_scanner is True
    assert plan.ready_for_diff_proposal is False
    assert plan.ready_for_patch_proposal is False
    assert plan.ready_for_patch_application is False
    assert plan.ready_for_execution is False
    for field in ["ready_for_diff_proposal", "ready_for_patch_proposal", "ready_for_patch_application", "ready_for_execution"]:
        with pytest.raises(ValueError):
            build_patch_plan(**{field: True})

    graph_report = validate_patch_change_set_graph(graph)
    assert graph_report.valid is True
    assert graph_report.ready_for_execution is False
    assert graph_report.ready_for_diff_proposal is False

    plan_report = validate_patch_plan(plan)
    assert plan_report.valid is True
    assert plan_report.ready_for_execution is False
    assert plan_report.ready_for_diff_proposal is False
    assert plan_report.ready_for_patch_proposal is False

    report = build_patch_plan_report()
    assert report.plan_ready is True
    assert report.change_set_graph_ready is True
    assert report.reference_informed_plan_ready is True
    assert report.ready_for_diff_proposal is False
    assert report.ready_for_patch_proposal is False
    assert report.ready_for_patch_application is False
    assert report.ready_for_execution is False

    preview = build_patch_plan_run_preview()
    for name in preview.__dataclass_fields__:
        if name.startswith("no_"):
            assert getattr(preview, name) is True

    guarantee = build_patch_plan_no_diff_no_apply_guarantee()
    for name in guarantee.__dataclass_fields__:
        if name.startswith("no_"):
            assert getattr(guarantee, name) is True

    readiness = build_v0353_readiness_report()
    assert readiness.ready_for_v0354_diff_proposal_envelope is True
    assert readiness.ready_for_v0355_patch_risk_conformance_scanner is True
    assert readiness.ready_for_patch_plan is True
    assert readiness.ready_for_change_set_graph is True
    assert readiness.ready_for_reference_informed_patch_plan is True
    assert readiness.ready_for_execution is False
    assert readiness.ready_for_diff_proposal is False
    assert readiness.ready_for_patch_proposal is False
    assert readiness.ready_for_patch_hunk_generation is False
    assert readiness.ready_for_patch_application is False
    assert readiness.ready_for_workspace_write is False
    assert readiness.ready_for_code_edit is False
    assert readiness.ready_for_apply_patch is False
    assert readiness.ready_for_git_apply is False
    assert readiness.ready_for_test_execution is False
    assert readiness.ready_for_shell_execution is False
    assert readiness.ready_for_dependency_install is False
    assert readiness.ready_for_reference_execution is False
    assert readiness.ready_for_reference_import is False
    assert readiness.production_certified is False
    assert v0353_readiness_report_is_not_execution_ready(readiness)


def test_fake_intent_context_and_digest_metadata_can_create_plan() -> None:
    intent_bundle = build_patch_intent_scope_bundle()
    context_snapshot = build_patch_context_snapshot(
        reference_summaries=[build_patch_context_reference_summary(summary="Reference context summary metadata only.")]
    )
    digest = build_reference_pattern_digest(
        patterns=[
            build_reference_harness_pattern(pattern_id="pattern:observed", disposition=ReferencePatternDisposition.OBSERVED),
            build_reference_harness_pattern(
                pattern_id="pattern:rejected",
                disposition=ReferencePatternDisposition.REJECTED_FOR_SAFETY,
                rejection_reason="Runtime reference execution rejected.",
            ),
            build_reference_harness_pattern(
                pattern_id="pattern:future",
                disposition=ReferencePatternDisposition.FUTURE_TRACK,
                future_track_note="Diff envelope is later-stage.",
            ),
        ]
    )
    uses = build_reference_informed_patch_pattern_uses_from_digest_and_context(digest, context_snapshot)
    assert len(uses) == 4
    assert any(item.rejected for item in uses)
    assert any(item.future_track for item in uses)

    planning_input = build_patch_planning_input_from_context_snapshot(context_snapshot)
    assert planning_input.patch_context_snapshot_id == context_snapshot.context_snapshot_id
    graph = build_patch_change_set_graph_from_intent_context(intent_bundle, context_snapshot)
    plan = build_patch_plan(change_set_graph=graph, reference_pattern_uses=uses, planning_input_id=planning_input.planning_input_id)
    assert patch_plan_is_not_patch_proposal(plan)
    assert plan.reference_pattern_uses
    assert plan.change_set_graph.change_nodes


def test_missing_context_snapshot_produces_blocked_graph_gap_instead_of_unsafe_expansion() -> None:
    graph = build_patch_change_set_graph_from_intent_context(intent_scope_bundle=None, context_snapshot=None)
    assert graph.status == PatchChangeSetGraphStatus.BLOCKED
    assert len(graph.change_nodes) == 1
    assert graph.change_nodes[0].status == PatchChangeNodeStatus.BLOCKED
    assert graph.change_nodes[0].blocked_reason
    assert graph.ready_for_diff_proposal is False
    assert graph.ready_for_patch_proposal is False
    assert graph.ready_for_execution is False


def test_module_source_has_no_runtime_read_write_shell_diff_or_patch_generation_calls() -> None:
    source = inspect.getsource(plan_module)
    forbidden_patterns = [
        "from pathlib",
        "Path(",
        "read_text(",
        "import subprocess",
        "subprocess.",
        "os.system",
        "shell=True",
        "apply_patch(",
        "write_text(",
        "write_bytes(",
        "open(",
        "unlink(",
        ".rename(",
        ".chmod(",
        ".chown(",
        "requests.",
        "httpx.",
        "urllib.",
        "aiohttp.",
        "socket.",
        "os.environ",
        "eval(",
        "exec(",
        "importlib",
        "logging.",
    ]
    for pattern in forbidden_patterns:
        assert pattern not in source
