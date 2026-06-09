import inspect

import pytest

from chanta_core.agent_runtime import (
    PatchAllowedTarget,
    PatchBlockedTarget,
    PatchIntentDecisionKind,
    PatchIntentEnvelope,
    PatchIntentKind,
    PatchIntentPriority,
    PatchIntentReadinessLevel,
    PatchIntentRiskKind,
    PatchIntentScopeBundle,
    PatchIntentSourceKind,
    PatchIntentStatus,
    PatchIntentValidationReport,
    PatchNonGoalRegister,
    PatchProposalCapabilityKind,
    PatchProposalSurfaceKind,
    PatchReferencePatternUse,
    PatchScopeDecisionKind,
    PatchScopeKind,
    PatchScopePolicy,
    PatchScopeRiskKind,
    PatchScopeValidationReport,
    PatchTargetKind,
    PatchTargetSelector,
    ReferenceHarnessPatternKind,
    ReferencePatternDisposition,
    build_patch_allowed_target,
    build_patch_blocked_target,
    build_patch_intent_envelope,
    build_patch_intent_flags,
    build_patch_intent_scope_bundle,
    build_patch_intent_scope_no_apply_guarantee,
    build_patch_intent_scope_report,
    build_patch_intent_scope_run_preview,
    build_patch_intent_source_ref,
    build_patch_intent_validation_report,
    build_patch_non_goal_register,
    build_patch_reference_pattern_use,
    build_patch_reference_pattern_uses_from_digest_metadata,
    build_patch_scope_policy,
    build_patch_scope_validation_report,
    build_patch_target_selector,
    build_reference_harness_pattern,
    build_reference_pattern_digest,
    build_v0351_readiness_report,
    default_patch_non_goal_register,
    default_patch_scope_policy,
    patch_intent_flags_preserve_no_apply,
    patch_intent_scope_bundle_is_not_patch_plan,
    patch_scope_policy_blocks_write_apply,
    patch_target_selector_is_not_file_access,
    v0351_readiness_report_is_not_execution_ready,
    validate_patch_intent_envelope,
    validate_patch_intent_scope_bundle,
    validate_patch_scope_policy,
    validate_patch_target_selector,
)
from chanta_core.agent_runtime import patch_intent as intent_module


def test_v0351_taxonomies_have_required_values() -> None:
    assert PatchIntentKind.ADD_MISSING_CONTRACT_MODEL.value == "add_missing_contract_model"
    assert PatchIntentKind.UNKNOWN.value == "unknown"
    assert PatchIntentSourceKind.V0350_REFERENCE_PATTERN_DIGEST.value == "v0350_reference_pattern_digest"
    assert PatchIntentStatus.SCOPE_ATTACHED.value == "scope_attached"
    assert PatchIntentReadinessLevel.DESIGN_HANDOFF_READY_FOR_V0352.value == "design_handoff_ready_for_v0352"
    assert PatchIntentDecisionKind.ALLOW_INTENT_METADATA.value == "allow_intent_metadata"
    assert PatchIntentRiskKind.OVERBROAD_SCOPE_RISK.value == "overbroad_scope_risk"
    assert PatchScopeKind.READ_ONLY_REFERENCE_SCOPE.value == "read_only_reference_scope"
    assert PatchTargetKind.SECRET_LIKE_FILE.value == "secret_like_file"
    assert PatchScopeDecisionKind.ALLOW_FUTURE_READONLY_CONTEXT_COLLECTION.value == "allow_future_readonly_context_collection"
    assert PatchScopeRiskKind.BROAD_GLOB_RISK.value == "broad_glob_risk"
    assert PatchIntentPriority.NORMAL.value == "normal"


def test_patch_intent_flags_allow_metadata_handoff_and_block_unsafe_readiness() -> None:
    flags = build_patch_intent_flags()
    assert flags.patch_intent_layer_constructed is True
    assert flags.patch_scope_policy_defined is True
    assert flags.target_selector_defined is True
    assert flags.non_goal_register_defined is True
    assert flags.reference_digest_consumed is True
    assert flags.ready_for_v0352_readonly_patch_context_collector is True
    assert flags.ready_for_v0353_reference_informed_patch_plan is True
    assert flags.ready_for_patch_intent_artifact is True
    assert flags.ready_for_patch_scope_policy is True
    assert flags.ready_for_patch_context_collection is False
    assert flags.ready_for_patch_plan is False
    assert flags.ready_for_diff_proposal is False
    assert flags.ready_for_patch_proposal is False
    assert flags.ready_for_patch_application is False
    assert flags.ready_for_workspace_write is False
    assert flags.ready_for_code_edit is False
    assert flags.ready_for_apply_patch is False
    assert flags.ready_for_git_apply is False
    assert flags.ready_for_test_execution is False
    assert flags.ready_for_shell_execution is False
    assert flags.ready_for_subprocess_execution is False
    assert flags.ready_for_command_execution is False
    assert flags.ready_for_dependency_install is False
    assert flags.ready_for_reference_execution is False
    assert flags.ready_for_reference_import is False
    assert flags.ready_for_provider_invocation is False
    assert flags.ready_for_direct_network_access is False
    assert flags.ready_for_credential_access is False
    assert flags.ready_for_secret_read is False
    assert flags.production_certified is False
    assert patch_intent_flags_preserve_no_apply(flags)


@pytest.mark.parametrize(
    "unsafe_flag",
    [
        "ready_for_execution",
        "ready_for_patch_context_collection",
        "ready_for_patch_plan",
        "ready_for_diff_proposal",
        "ready_for_patch_proposal",
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
def test_patch_intent_flags_reject_unsafe_readiness(unsafe_flag: str) -> None:
    with pytest.raises(ValueError):
        build_patch_intent_flags(**{unsafe_flag: True})


def test_source_ref_and_reference_pattern_use_are_metadata_only() -> None:
    source = build_patch_intent_source_ref()
    assert source.source_kind == PatchIntentSourceKind.V0350_REFERENCE_PATTERN_DIGEST
    assert "v0.35.0_reference_pattern_digest.md" in source.evidence_refs[0]

    adapted = build_patch_reference_pattern_use()
    assert adapted.rejected is False
    assert adapted.future_track is False
    assert adapted.adapted_intent_kind == PatchIntentKind.ALIGN_WITH_REFERENCE_PATTERN

    rejected = build_patch_reference_pattern_use(
        pattern_use_id="pattern_use:rejected",
        rejected=True,
        rejection_reason="Runtime reference execution is rejected.",
    )
    assert rejected.rejected is True
    assert rejected.rejection_reason

    future = build_patch_reference_pattern_use(
        pattern_use_id="pattern_use:future",
        adapted_intent_kind=PatchIntentKind.PREPARE_FUTURE_TRACK,
        future_track=True,
    )
    assert future.future_track is True

    with pytest.raises(ValueError):
        build_patch_reference_pattern_use(rejected=True)


def test_intent_envelope_is_not_patch_proposal_or_execution() -> None:
    intent = build_patch_intent_envelope()
    assert isinstance(intent, PatchIntentEnvelope)
    assert intent.ready_for_patch_proposal is False
    assert intent.ready_for_patch_application is False
    assert intent.ready_for_execution is False
    assert intent.source_refs
    assert intent.reference_pattern_uses

    with pytest.raises(ValueError):
        build_patch_intent_envelope(ready_for_patch_proposal=True)
    with pytest.raises(ValueError):
        build_patch_intent_envelope(ready_for_patch_application=True)
    with pytest.raises(ValueError):
        build_patch_intent_envelope(ready_for_execution=True)

    report = validate_patch_intent_envelope(intent)
    assert isinstance(report, PatchIntentValidationReport)
    assert report.valid is True
    assert report.ready_for_execution is False
    assert report.ready_for_patch_proposal is False


def test_scope_policy_blocks_write_apply_and_unsafe_target_kinds() -> None:
    policy = default_patch_scope_policy()
    assert isinstance(policy, PatchScopePolicy)
    assert policy.allow_source_targets is True
    assert policy.allow_test_targets is True
    assert policy.allow_doc_targets is True
    assert policy.allow_reference_targets_for_readonly_context is True
    assert policy.allow_secret_targets is False
    assert policy.allow_credential_targets is False
    assert policy.allow_binary_targets is False
    assert policy.allow_external_targets is False
    assert policy.allow_workspace_write is False
    assert policy.allow_code_edit is False
    assert policy.allow_patch_application is False
    assert patch_scope_policy_blocks_write_apply(policy)

    for field in [
        "allow_secret_targets",
        "allow_credential_targets",
        "allow_binary_targets",
        "allow_external_targets",
        "allow_workspace_write",
        "allow_code_edit",
        "allow_patch_application",
    ]:
        with pytest.raises(ValueError):
            build_patch_scope_policy(**{field: True})

    report = validate_patch_scope_policy(policy)
    assert isinstance(report, PatchScopeValidationReport)
    assert report.valid is True
    assert report.ready_for_execution is False
    assert report.ready_for_file_access is False
    assert report.ready_for_write is False


def test_target_selector_allowed_and_blocked_targets_are_not_file_access() -> None:
    selector = build_patch_target_selector()
    assert isinstance(selector, PatchTargetSelector)
    assert selector.selected_for_future_context is True
    assert selector.selected_for_future_patch_proposal is False
    assert selector.selected_for_write is False
    assert patch_target_selector_is_not_file_access(selector)

    with pytest.raises(ValueError):
        build_patch_target_selector(selected_for_future_patch_proposal=True)
    with pytest.raises(ValueError):
        build_patch_target_selector(selected_for_write=True)
    with pytest.raises(ValueError):
        build_patch_target_selector(blocked=True)

    allowed = build_patch_allowed_target()
    assert isinstance(allowed, PatchAllowedTarget)
    assert allowed.allow_future_readonly_context is True
    assert allowed.allow_future_patch_proposal is False
    assert allowed.allow_write is False
    assert allowed.allow_apply is False
    with pytest.raises(ValueError):
        build_patch_allowed_target(allow_write=True)
    with pytest.raises(ValueError):
        build_patch_allowed_target(allow_apply=True)

    blocked = build_patch_blocked_target()
    assert isinstance(blocked, PatchBlockedTarget)
    assert blocked.reason
    assert blocked.safe_alternative

    selector_report = validate_patch_target_selector(selector)
    assert selector_report.ready_for_file_access is False


def test_non_goal_register_prohibits_apply_write_shell_test_install_reference_execution() -> None:
    register = default_patch_non_goal_register()
    assert isinstance(register, PatchNonGoalRegister)
    prohibited = {PatchProposalCapabilityKind(item) for item in register.prohibited_capabilities}
    for required in [
        PatchProposalCapabilityKind.EXECUTE_PATCH_APPLY,
        PatchProposalCapabilityKind.WRITE_WORKSPACE_FILE,
        PatchProposalCapabilityKind.EDIT_CODE_FILE,
        PatchProposalCapabilityKind.RUN_GIT_APPLY,
        PatchProposalCapabilityKind.RUN_APPLY_PATCH,
        PatchProposalCapabilityKind.RUN_TESTS,
        PatchProposalCapabilityKind.EXECUTE_SHELL,
        PatchProposalCapabilityKind.INSTALL_DEPENDENCY,
        PatchProposalCapabilityKind.EXECUTE_REFERENCE_HARNESS,
    ]:
        assert required in prohibited

    surfaces = {PatchProposalSurfaceKind(item) for item in register.prohibited_surfaces}
    assert PatchProposalSurfaceKind.PATCH_APPLY in surfaces
    assert PatchProposalSurfaceKind.FILE_WRITE in surfaces
    assert PatchProposalSurfaceKind.CODE_EDIT in surfaces
    assert PatchProposalSurfaceKind.REFERENCE_CODE_EXECUTION in surfaces

    with pytest.raises(ValueError):
        build_patch_non_goal_register(prohibited_capabilities=[PatchProposalCapabilityKind.EXECUTE_PATCH_APPLY])


def test_bundle_report_preview_guarantee_and_readiness_are_not_plan_or_execution() -> None:
    bundle = build_patch_intent_scope_bundle()
    assert isinstance(bundle, PatchIntentScopeBundle)
    assert patch_intent_scope_bundle_is_not_patch_plan(bundle)
    assert bundle.ready_for_patch_context_collection is False
    assert bundle.ready_for_patch_plan is False
    assert bundle.ready_for_diff_proposal is False
    assert bundle.ready_for_patch_proposal is False
    assert bundle.ready_for_patch_application is False
    assert bundle.ready_for_execution is False

    for field in [
        "ready_for_patch_context_collection",
        "ready_for_patch_plan",
        "ready_for_diff_proposal",
        "ready_for_patch_proposal",
        "ready_for_patch_application",
        "ready_for_execution",
    ]:
        with pytest.raises(ValueError):
            build_patch_intent_scope_bundle(**{field: True})

    report = build_patch_intent_scope_report(bundle=bundle)
    assert report.ready_for_patch_context_collection is False
    assert report.ready_for_patch_plan is False
    assert report.ready_for_patch_proposal is False
    assert report.ready_for_execution is False

    preview = build_patch_intent_scope_run_preview()
    for name in preview.__dataclass_fields__:
        if name.startswith("no_"):
            assert getattr(preview, name) is True

    guarantee = build_patch_intent_scope_no_apply_guarantee()
    for name in guarantee.__dataclass_fields__:
        if name.startswith("no_"):
            assert getattr(guarantee, name) is True

    readiness = build_v0351_readiness_report()
    assert readiness.ready_for_v0352_readonly_patch_context_collector is True
    assert readiness.ready_for_v0353_reference_informed_patch_plan is True
    assert readiness.ready_for_patch_intent_artifact is True
    assert readiness.ready_for_patch_scope_policy is True
    assert readiness.ready_for_execution is False
    assert readiness.ready_for_patch_context_collection is False
    assert readiness.ready_for_patch_plan is False
    assert readiness.ready_for_diff_proposal is False
    assert readiness.ready_for_patch_proposal is False
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
    assert v0351_readiness_report_is_not_execution_ready(readiness)

    bundle_report = validate_patch_intent_scope_bundle(bundle)
    assert bundle_report.ready_for_execution is False


def test_reference_pattern_digest_metadata_consumption_preserves_rejected_and_future_dispositions() -> None:
    observed = build_reference_harness_pattern(
        pattern_id="pattern:opencode:permission",
        pattern_kind=ReferenceHarnessPatternKind.PERMISSION_GATE_PATTERN,
        disposition=ReferencePatternDisposition.OBSERVED,
        pattern_summary="Permission gates separate request and approval metadata.",
        confidence="high",
    )
    rejected = build_reference_harness_pattern(
        pattern_id="pattern:hermes:runtime",
        pattern_kind=ReferenceHarnessPatternKind.UNSAFE_EXECUTION_PATTERN,
        disposition=ReferencePatternDisposition.REJECTED_FOR_SAFETY,
        pattern_summary="Runtime execution behavior is not adopted.",
        rejection_reason="Reference runtime execution remains prohibited.",
        confidence="high",
    )
    future = build_reference_harness_pattern(
        pattern_id="pattern:opencode:diff",
        pattern_kind=ReferenceHarnessPatternKind.DIFF_PROPOSAL_PATTERN,
        disposition=ReferencePatternDisposition.FUTURE_TRACK,
        pattern_summary="Diff proposal structure is later-track design input.",
        future_track_note="Use in v0.35.4 only.",
        confidence="medium",
    )
    digest = build_reference_pattern_digest(patterns=[observed, rejected, future])
    uses = build_patch_reference_pattern_uses_from_digest_metadata(digest)
    assert len(uses) == 3
    assert uses[0].adapted_intent_kind == PatchIntentKind.TIGHTEN_SAFETY_BOUNDARY
    assert uses[1].rejected is True
    assert uses[1].rejection_reason == "Reference runtime execution remains prohibited."
    assert uses[2].future_track is True
    assert uses[2].adapted_intent_kind == PatchIntentKind.PREPARE_FUTURE_TRACK
    assert all(isinstance(item, PatchReferencePatternUse) for item in uses)


def test_validation_handles_unknown_intent_without_execution_readiness() -> None:
    intent = build_patch_intent_envelope(intent_kind=PatchIntentKind.UNKNOWN)
    report = validate_patch_intent_envelope(intent)
    assert report.valid is False
    assert any(finding.blocks_validation for finding in report.findings)
    assert report.ready_for_execution is False
    assert report.ready_for_patch_proposal is False


def test_module_source_has_no_runtime_execution_write_apply_or_context_collection_calls() -> None:
    source = inspect.getsource(intent_module)
    forbidden_patterns = [
        "import subprocess",
        "subprocess.",
        "os.system",
        "shell=True",
        "apply_patch(",
        "write_text(",
        "write_bytes(",
        "open(",
        "read_text(",
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

