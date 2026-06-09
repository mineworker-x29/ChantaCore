import inspect

import pytest

import chanta_core.agent_runtime.patch_apply_boundary as boundary_module
from chanta_core.agent_runtime.patch_apply_boundary import (
    AgenticTaskBoundaryPolicy,
    AgenticTaskExecutionPosture,
    AgenticTaskRuntimeKind,
    HumanApprovalBoundaryPolicy,
    HumanApprovalPosture,
    PatchApplyExecutionPosture,
    PatchApplySandboxAllowedSurface,
    PatchApplySandboxBoundary,
    PatchApplySandboxCapabilityKind,
    PatchApplySandboxDecisionKind,
    PatchApplySandboxFlagSet,
    PatchApplySandboxNoLiveWriteGuarantee,
    PatchApplySandboxPermissionDecision,
    PatchApplySandboxPolicy,
    PatchApplySandboxProhibitedSurface,
    PatchApplySandboxReadinessLevel,
    PatchApplySandboxRiskKind,
    PatchApplySandboxRiskRegister,
    PatchApplySandboxSourceRef,
    PatchApplySandboxStatus,
    PatchApplySandboxSurfaceKind,
    PatchApplySandboxTrackKind,
    PatchApplyWritePosture,
    V0360ReadinessReport,
    V036RoadmapOverview,
    agentic_task_boundary_blocks_autonomous_runtime,
    build_agentic_task_boundary_policy,
    build_human_approval_boundary_policy,
    build_patch_apply_sandbox_allowed_surface,
    build_patch_apply_sandbox_boundary,
    build_patch_apply_sandbox_denied_action,
    build_patch_apply_sandbox_flags,
    build_patch_apply_sandbox_gate_evaluation,
    build_patch_apply_sandbox_no_live_write_guarantee,
    build_patch_apply_sandbox_permission_decision,
    build_patch_apply_sandbox_permission_request,
    build_patch_apply_sandbox_policy,
    build_patch_apply_sandbox_prohibited_surface,
    build_patch_apply_sandbox_risk_register,
    build_patch_apply_sandbox_source_ref,
    build_v0360_readiness_report,
    build_v036_roadmap_overview,
    human_approval_boundary_rejects_model_approval,
    patch_apply_sandbox_boundary_is_not_apply,
    patch_apply_sandbox_decision_is_not_apply_permission,
    patch_apply_sandbox_flags_preserve_no_apply,
    patch_apply_sandbox_policy_blocks_live_write,
    v0360_readiness_report_is_not_execution_ready,
)


def test_taxonomies_are_complete():
    assert {item.value for item in PatchApplySandboxTrackKind} == {
        "boundary_foundation",
        "apply_candidate_human_approval_contract",
        "dry_run_patch_apply_simulation",
        "sandbox_workspace_overlay_policy",
        "sandbox_patch_apply_engine",
        "sandbox_post_apply_validation",
        "bounded_agentic_task_operation_cycle",
        "patch_apply_sandbox_ocel_trace_packet",
        "cli_sandbox_apply_agentic_surface",
        "consolidation",
        "unknown",
    }
    assert {item.value for item in PatchApplySandboxSurfaceKind} == {
        "apply_candidate_envelope",
        "human_approval_contract",
        "dry_run_apply_simulation",
        "sandbox_workspace_policy",
        "sandbox_overlay_policy",
        "sandbox_patch_apply",
        "sandbox_post_apply_validation",
        "bounded_agentic_task_operation",
        "agentic_function_task_execution",
        "patch_apply_trace_packet",
        "cli_sandbox_apply_surface",
        "live_workspace_write",
        "unrestricted_patch_apply",
        "git_apply",
        "apply_patch",
        "test_execution",
        "shell_command",
        "dependency_install",
        "external_agent_execution",
        "dominion_runtime",
        "infinite_agent_loop",
        "unknown",
    }
    assert {item.value for item in PatchApplySandboxCapabilityKind} == {
        "define_apply_sandbox_boundary",
        "define_human_approval_boundary",
        "define_bounded_agentic_task_boundary",
        "create_apply_candidate_future_gate",
        "create_human_approval_contract_future_gate",
        "create_dry_run_apply_simulation_future_gate",
        "create_sandbox_workspace_future_gate",
        "perform_sandbox_patch_apply",
        "perform_live_patch_apply",
        "write_sandbox_file",
        "write_live_workspace_file",
        "edit_code_file",
        "call_apply_patch",
        "call_git_apply",
        "run_tests",
        "execute_shell",
        "install_dependency",
        "execute_external_agent",
        "invoke_claude_code",
        "invoke_codex_cli",
        "run_dominion_runtime",
        "run_infinite_agent_loop",
        "unknown",
    }
    assert {item.value for item in PatchApplySandboxDecisionKind} == {
        "allow_boundary_definition",
        "allow_human_approval_boundary_definition",
        "allow_bounded_agentic_task_boundary_definition",
        "allow_design_stage_handoff",
        "deny",
        "block",
        "no_op",
        "require_review",
        "future_gate_required",
        "unknown",
    }
    assert {item.value for item in PatchApplySandboxStatus} == {
        "unknown",
        "draft",
        "boundary_ready",
        "boundary_ready_with_gaps",
        "human_approval_boundary_ready",
        "bounded_agentic_task_boundary_ready",
        "blocked",
        "deferred",
        "future_track",
        "no_op",
    }
    assert {item.value for item in PatchApplySandboxReadinessLevel} == {
        "not_ready",
        "boundary_contract_ready",
        "apply_sandbox_boundary_ready",
        "human_approval_boundary_ready",
        "bounded_agentic_task_boundary_ready",
        "design_handoff_ready_for_v0361",
        "design_handoff_ready_for_v0362",
        "blocked",
        "future_track",
    }
    assert {item.value for item in PatchApplyWritePosture} == {
        "no_write",
        "sandbox_write_future_gated",
        "sandbox_write_allowed_later",
        "live_write_blocked",
        "write_blocked",
        "unknown",
    }
    assert {item.value for item in PatchApplyExecutionPosture} == {
        "no_apply",
        "dry_run_future_gated",
        "sandbox_apply_future_gated",
        "live_apply_blocked",
        "apply_blocked",
        "unknown",
    }
    assert {item.value for item in HumanApprovalPosture} == {
        "approval_not_required_for_boundary",
        "human_approval_contract_future_gated",
        "operator_supplied_approval_required",
        "model_generated_approval_invalid",
        "approval_metadata_only",
        "unknown",
    }
    assert {item.value for item in AgenticTaskExecutionPosture} == {
        "no_agentic_execution",
        "bounded_function_task_boundary_only",
        "single_cycle_future_gated",
        "independent_agent_runtime_blocked",
        "multi_cycle_loop_blocked",
        "external_agent_loop_blocked",
        "dominion_runtime_blocked",
        "unknown",
    }
    assert {item.value for item in AgenticTaskRuntimeKind} == {
        "bounded_function_task",
        "single_cycle_agentic_operation",
        "multi_cycle_agentic_loop",
        "independent_autonomous_agent",
        "external_agent_orchestration",
        "dominion_runtime",
        "infinite_agent_loop",
        "no_runtime",
        "unknown",
    }


def test_patch_apply_sandbox_flags_allow_boundary_readiness_only():
    flags = build_patch_apply_sandbox_flags()

    assert isinstance(flags, PatchApplySandboxFlagSet)
    assert flags.patch_apply_sandbox_boundary_constructed is True
    assert flags.patch_apply_sandbox_policy_defined is True
    assert flags.human_approval_boundary_defined is True
    assert flags.bounded_agentic_task_boundary_defined is True
    assert flags.patch_apply_risk_register_defined is True
    assert flags.ready_for_v0361_apply_candidate_human_approval_contract is True
    assert flags.ready_for_v0362_dry_run_patch_apply_simulation is True
    assert flags.ready_for_patch_apply_sandbox_boundary is True
    assert flags.ready_for_human_approval_boundary is True
    assert flags.ready_for_bounded_agentic_task_boundary is True
    assert flags.ready_for_agentic_function_task_execution_boundary is True
    assert patch_apply_sandbox_flags_preserve_no_apply(flags)


@pytest.mark.parametrize(
    "unsafe_kwarg",
    [
        "ready_for_execution",
        "ready_for_dry_run_apply_simulation",
        "ready_for_sandbox_patch_apply",
        "ready_for_sandbox_workspace_write",
        "ready_for_live_workspace_write",
        "ready_for_patch_application",
        "ready_for_workspace_write",
        "ready_for_code_edit",
        "ready_for_apply_patch",
        "ready_for_git_apply",
        "ready_for_test_execution",
        "ready_for_shell_execution",
        "ready_for_external_agent_execution",
        "ready_for_dominion_runtime",
        "ready_for_independent_agent_runtime",
        "ready_for_multi_cycle_agentic_loop",
        "production_certified",
    ],
)
def test_patch_apply_sandbox_flags_reject_unsafe_true(unsafe_kwarg):
    with pytest.raises(ValueError):
        build_patch_apply_sandbox_flags(**{unsafe_kwarg: True})


def test_source_ref_is_metadata_only():
    source_ref = build_patch_apply_sandbox_source_ref()

    assert isinstance(source_ref, PatchApplySandboxSourceRef)
    assert source_ref.source_summary
    assert source_ref.evidence_refs


def test_sandbox_policy_allows_future_gates_but_blocks_apply_write_and_runtime():
    policy = build_patch_apply_sandbox_policy()

    assert isinstance(policy, PatchApplySandboxPolicy)
    assert policy.allow_boundary_definition is True
    assert policy.allow_human_approval_boundary_definition is True
    assert policy.allow_bounded_agentic_task_boundary_definition is True
    assert policy.allow_apply_candidate_future_gate is True
    assert policy.allow_dry_run_future_gate is True
    assert policy.allow_sandbox_workspace_future_gate is True
    assert policy.allow_sandbox_apply_future_gate is True
    assert policy.allow_dry_run_apply_simulation is False
    assert policy.allow_sandbox_patch_apply is False
    assert policy.allow_sandbox_workspace_write is False
    assert policy.allow_live_workspace_write is False
    assert policy.allow_patch_application is False
    assert policy.allow_workspace_write is False
    assert policy.allow_code_edit is False
    assert policy.allow_apply_patch is False
    assert policy.allow_git_apply is False
    assert policy.allow_test_execution is False
    assert policy.allow_shell is False
    assert policy.allow_dependency_install is False
    assert policy.allow_external_agent_execution is False
    assert policy.allow_dominion_runtime is False
    assert policy.allow_infinite_agent_loop is False
    assert patch_apply_sandbox_policy_blocks_live_write(policy)

    for unsafe_kwarg in (
        "allow_dry_run_apply_simulation",
        "allow_sandbox_patch_apply",
        "allow_sandbox_workspace_write",
        "allow_live_workspace_write",
        "allow_patch_application",
        "allow_workspace_write",
        "allow_code_edit",
        "allow_apply_patch",
        "allow_git_apply",
        "allow_test_execution",
        "allow_shell",
        "allow_dependency_install",
        "allow_external_agent_execution",
        "allow_dominion_runtime",
        "allow_infinite_agent_loop",
    ):
        with pytest.raises(ValueError):
            build_patch_apply_sandbox_policy(**{unsafe_kwarg: True})


def test_human_approval_boundary_rejects_model_and_metadata_approval():
    policy = build_human_approval_boundary_policy()

    assert isinstance(policy, HumanApprovalBoundaryPolicy)
    assert policy.require_operator_supplied_approval is True
    assert policy.allow_approval_contract_future_gate is True
    assert policy.allow_model_generated_approval is False
    assert policy.allow_review_metadata_as_apply_approval is False
    assert policy.allow_apply_without_human_approval is False
    assert human_approval_boundary_rejects_model_approval(policy)

    for unsafe_kwarg in (
        "allow_model_generated_approval",
        "allow_review_metadata_as_apply_approval",
        "allow_apply_without_human_approval",
    ):
        with pytest.raises(ValueError):
            build_human_approval_boundary_policy(**{unsafe_kwarg: True})


def test_agentic_task_boundary_blocks_autonomous_runtime_and_loops():
    policy = build_agentic_task_boundary_policy()

    assert isinstance(policy, AgenticTaskBoundaryPolicy)
    assert policy.allow_bounded_function_task_boundary is True
    assert policy.allow_single_cycle_future_gate is True
    assert policy.allow_single_cycle_execution is False
    assert policy.allow_multi_cycle_loop is False
    assert policy.allow_independent_agent_runtime is False
    assert policy.allow_external_agent_orchestration is False
    assert policy.allow_dominion_runtime is False
    assert policy.allow_infinite_agent_loop is False
    assert policy.require_human_handoff_after_cycle is True
    assert AgenticTaskRuntimeKind.INDEPENDENT_AUTONOMOUS_AGENT in policy.blocked_runtime_kinds
    assert AgenticTaskRuntimeKind.MULTI_CYCLE_AGENTIC_LOOP in policy.blocked_runtime_kinds
    assert agentic_task_boundary_blocks_autonomous_runtime(policy)

    for unsafe_kwarg in (
        "allow_single_cycle_execution",
        "allow_multi_cycle_loop",
        "allow_independent_agent_runtime",
        "allow_external_agent_orchestration",
        "allow_dominion_runtime",
        "allow_infinite_agent_loop",
    ):
        with pytest.raises(ValueError):
            build_agentic_task_boundary_policy(**{unsafe_kwarg: True})
    with pytest.raises(ValueError):
        build_agentic_task_boundary_policy(require_human_handoff_after_cycle=False)


def test_allowed_and_prohibited_surfaces_are_non_executable_metadata():
    allowed = build_patch_apply_sandbox_allowed_surface()
    prohibited = build_patch_apply_sandbox_prohibited_surface()

    assert isinstance(allowed, PatchApplySandboxAllowedSurface)
    assert allowed.allowed_only_for_design_stage is True
    assert allowed.executable_in_v0360 is False
    assert allowed.writes_sandbox is False
    assert allowed.writes_live_workspace is False
    assert allowed.applies_patch is False

    assert isinstance(prohibited, PatchApplySandboxProhibitedSurface)
    assert prohibited.blocks_sandbox_apply is True
    assert prohibited.blocks_live_write is True
    assert prohibited.blocks_runtime_readiness is True

    for unsafe_kwarg in ("executable_in_v0360", "writes_sandbox", "writes_live_workspace", "applies_patch"):
        with pytest.raises(ValueError):
            build_patch_apply_sandbox_allowed_surface(**{unsafe_kwarg: True})
    with pytest.raises(ValueError):
        build_patch_apply_sandbox_prohibited_surface(blocks_runtime_readiness=False)


def test_boundary_is_not_patch_apply_or_execution():
    boundary = build_patch_apply_sandbox_boundary()

    assert isinstance(boundary, PatchApplySandboxBoundary)
    assert boundary.ready_for_v0361_apply_candidate_human_approval_contract is True
    assert boundary.ready_for_v0362_dry_run_patch_apply_simulation is True
    assert boundary.ready_for_patch_apply_sandbox_boundary is True
    assert boundary.ready_for_human_approval_boundary is True
    assert boundary.ready_for_bounded_agentic_task_boundary is True
    assert boundary.ready_for_execution is False
    assert boundary.ready_for_dry_run_apply_simulation is False
    assert boundary.ready_for_sandbox_patch_apply is False
    assert boundary.ready_for_sandbox_workspace_write is False
    assert boundary.ready_for_live_workspace_write is False
    assert boundary.ready_for_patch_application is False
    assert boundary.ready_for_workspace_write is False
    assert boundary.ready_for_code_edit is False
    assert patch_apply_sandbox_boundary_is_not_apply(boundary)

    for unsafe_kwarg in (
        "ready_for_execution",
        "ready_for_dry_run_apply_simulation",
        "ready_for_sandbox_patch_apply",
        "ready_for_sandbox_workspace_write",
        "ready_for_live_workspace_write",
        "ready_for_patch_application",
        "ready_for_workspace_write",
        "ready_for_code_edit",
    ):
        with pytest.raises(ValueError):
            build_patch_apply_sandbox_boundary(**{unsafe_kwarg: True})


def test_permission_decision_and_gate_never_allow_apply_write_or_runtime():
    request = build_patch_apply_sandbox_permission_request()
    decision = build_patch_apply_sandbox_permission_decision(request_id=request.request_id)
    denied = build_patch_apply_sandbox_denied_action()
    gate = build_patch_apply_sandbox_gate_evaluation(decision=decision)

    assert isinstance(decision, PatchApplySandboxPermissionDecision)
    assert decision.bounded_boundary_definition_allowed is True
    assert decision.human_approval_boundary_definition_allowed is True
    assert decision.bounded_agentic_task_boundary_definition_allowed is True
    assert decision.design_stage_handoff_allowed is True
    assert patch_apply_sandbox_decision_is_not_apply_permission(decision)
    assert denied.safe_alternatives
    assert gate.ready_for_execution is False
    assert gate.ready_for_patch_application is False
    assert gate.ready_for_sandbox_patch_apply is False
    assert gate.ready_for_live_workspace_write is False

    for unsafe_kwarg in (
        "sandbox_patch_apply_allowed",
        "sandbox_workspace_write_allowed",
        "live_workspace_write_allowed",
        "patch_application_allowed",
        "workspace_write_allowed",
        "code_edit_allowed",
        "shell_execution_allowed",
        "test_execution_allowed",
        "dependency_install_allowed",
        "external_agent_execution_allowed",
        "dominion_runtime_allowed",
        "independent_agent_runtime_allowed",
        "multi_cycle_agentic_loop_allowed",
    ):
        with pytest.raises(ValueError):
            build_patch_apply_sandbox_permission_decision(**{unsafe_kwarg: True})


def test_risk_register_no_live_write_guarantee_roadmap_and_readiness():
    risk = build_patch_apply_sandbox_risk_register()
    guarantee = build_patch_apply_sandbox_no_live_write_guarantee()
    roadmap = build_v036_roadmap_overview()
    report = build_v0360_readiness_report()

    assert isinstance(risk, PatchApplySandboxRiskRegister)
    for risk_kind in (
        PatchApplySandboxRiskKind.LIVE_WORKSPACE_WRITE_RISK,
        PatchApplySandboxRiskKind.SANDBOX_ESCAPE_RISK,
        PatchApplySandboxRiskKind.HUMAN_APPROVAL_FORGERY_RISK,
        PatchApplySandboxRiskKind.MODEL_GENERATED_APPROVAL_RISK,
        PatchApplySandboxRiskKind.APPLY_PATCH_RISK,
        PatchApplySandboxRiskKind.GIT_APPLY_RISK,
        PatchApplySandboxRiskKind.SHELL_EXECUTION_RISK,
        PatchApplySandboxRiskKind.TEST_EXECUTION_RISK,
        PatchApplySandboxRiskKind.DEPENDENCY_INSTALL_RISK,
        PatchApplySandboxRiskKind.EXTERNAL_AGENT_EXECUTION_RISK,
        PatchApplySandboxRiskKind.DOMINION_RUNTIME_RISK,
        PatchApplySandboxRiskKind.INFINITE_AGENT_LOOP_RISK,
    ):
        assert risk_kind in risk.risk_kinds

    assert isinstance(guarantee, PatchApplySandboxNoLiveWriteGuarantee)
    assert all(getattr(guarantee, name) is True for name in guarantee.__dataclass_fields__ if name.startswith("no_"))

    assert isinstance(roadmap, V036RoadmapOverview)
    assert roadmap.current_release.startswith("v0.36.0")
    assert any("v0.36.1" in item for item in roadmap.next_handoff_releases)
    assert any("v0.36.2" in item for item in roadmap.next_handoff_releases)

    assert isinstance(report, V0360ReadinessReport)
    assert report.ready_for_v0361_apply_candidate_human_approval_contract is True
    assert report.ready_for_v0362_dry_run_patch_apply_simulation is True
    assert report.ready_for_patch_apply_sandbox_boundary is True
    assert report.ready_for_human_approval_boundary is True
    assert report.ready_for_bounded_agentic_task_boundary is True
    assert report.ready_for_agentic_function_task_execution_boundary is True
    assert v0360_readiness_report_is_not_execution_ready(report)

    with pytest.raises(ValueError):
        build_patch_apply_sandbox_no_live_write_guarantee(no_patch_application=False)
    with pytest.raises(ValueError):
        build_v0360_readiness_report(ready_for_execution=True)
    with pytest.raises(ValueError):
        build_v0360_readiness_report(ready_for_sandbox_patch_apply=True)


def test_module_exports_safe_patch_apply_boundary_names():
    from chanta_core.agent_runtime import (
        PatchApplySandboxBoundary,
        build_patch_apply_sandbox_boundary,
        build_v0360_readiness_report,
    )

    boundary = build_patch_apply_sandbox_boundary()
    report = build_v0360_readiness_report()
    assert isinstance(boundary, PatchApplySandboxBoundary)
    assert report.ready_for_execution is False


def test_runtime_forbidden_patterns_are_absent_from_implementation_helpers():
    source = inspect.getsource(boundary_module)

    forbidden_runtime_patterns = [
        "import subprocess",
        "subprocess.",
        "os.system(",
        "shell=True",
        "from pathlib",
        "Path(",
        ".read_text(",
        ".read_bytes(",
        ".write_text(",
        ".write_bytes(",
        " open(",
        ".unlink(",
        ".rename(",
        ".chmod(",
        ".chown(",
        "import requests",
        "import httpx",
        "import urllib",
        "import aiohttp",
        "import socket",
        "os.environ",
        "eval(",
        "exec(",
        "importlib",
        "logging.",
        "json.dump(",
        "sqlite",
    ]

    for pattern in forbidden_runtime_patterns:
        assert pattern not in source
