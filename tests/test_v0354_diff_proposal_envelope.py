import inspect

import pytest

from chanta_core.agent_runtime import (
    DiffProposalDecisionKind,
    DiffProposalEnvelope,
    DiffProposalFlagSet,
    DiffProposalFormat,
    DiffProposalGenerationPolicy,
    DiffProposalHunkKind,
    DiffProposalInput,
    DiffProposalMode,
    DiffProposalNoApplyGuarantee,
    DiffProposalReadinessLevel,
    DiffProposalReport,
    DiffProposalRiskKind,
    DiffProposalRunPreview,
    DiffProposalSourceKind,
    DiffProposalSourceRef,
    DiffProposalStatus,
    DiffProposalTargetFile,
    DiffProposalTargetKind,
    DiffProposalValidationFinding,
    DiffProposalValidationKind,
    DiffProposalValidationReport,
    PatchFileProposal,
    PatchHunkProposal,
    StructuredPatchProposal,
    UnifiedDiffProposal,
    V0354ReadinessReport,
    build_diff_proposal_envelope,
    build_diff_proposal_flags,
    build_diff_proposal_generation_policy,
    build_diff_proposal_input,
    build_diff_proposal_input_from_patch_plan,
    build_diff_proposal_no_apply_guarantee,
    build_diff_proposal_report,
    build_diff_proposal_run_preview,
    build_diff_proposal_source_ref,
    build_diff_proposal_target_file,
    build_diff_proposal_validation_finding,
    build_diff_proposal_validation_report,
    build_patch_file_proposal,
    build_patch_hunk_proposal,
    build_patch_plan,
    build_structured_patch_proposal,
    build_structured_patch_proposal_from_patch_plan,
    build_unified_diff_proposal,
    build_unified_diff_proposal_from_structured_patch,
    build_v0354_readiness_report,
    default_diff_proposal_generation_policy,
    diff_proposal_envelope_is_not_apply,
    diff_proposal_flags_preserve_no_apply,
    diff_proposal_policy_blocks_apply,
    structured_patch_proposal_is_not_write,
    unified_diff_proposal_is_not_git_apply,
    v0354_readiness_report_is_not_execution_ready,
    validate_diff_proposal_envelope,
    validate_patch_file_proposal,
    validate_patch_hunk_proposal,
)
from chanta_core.agent_runtime import patch_diff_proposal as diff_module


def test_v0354_taxonomies_have_required_values() -> None:
    assert [item.value for item in DiffProposalMode] == [
        "plan_only_no_diff",
        "unified_diff_artifact",
        "structured_patch_artifact",
        "combined_unified_and_structured_artifact",
        "blocked",
        "review_required",
        "no_op",
        "unknown",
    ]
    assert [item.value for item in DiffProposalFormat] == [
        "unified_diff",
        "structured_patch",
        "file_level_summary",
        "hunk_level_summary",
        "before_after_preview",
        "proposal_metadata_only",
        "no_diff",
        "unknown",
    ]
    assert [item.value for item in DiffProposalSourceKind] == [
        "v0353_patch_plan",
        "v0353_change_set_graph",
        "v0353_target_file_plan",
        "v0352_patch_context_snapshot",
        "v0352_evidence_bundle",
        "v0351_patch_intent_scope_bundle",
        "v0350_reference_pattern_digest",
        "reference_informed_pattern_use",
        "test_fixture",
        "unknown",
    ]
    assert [item.value for item in DiffProposalStatus] == [
        "unknown",
        "draft",
        "proposal_created",
        "proposal_created_with_gaps",
        "proposal_validated",
        "proposal_validated_with_warnings",
        "blocked",
        "review_required",
        "future_gated",
        "no_op",
    ]
    assert [item.value for item in DiffProposalReadinessLevel] == [
        "not_ready",
        "diff_contract_ready",
        "unified_diff_artifact_ready",
        "structured_patch_artifact_ready",
        "diff_envelope_ready",
        "design_handoff_ready_for_v0355",
        "design_handoff_ready_for_v0356",
        "blocked",
        "future_track",
    ]
    assert [item.value for item in DiffProposalDecisionKind] == [
        "allow_diff_artifact",
        "allow_structured_patch_artifact",
        "allow_metadata_only_artifact",
        "allow_design_stage_handoff",
        "deny",
        "block",
        "no_op",
        "require_review",
        "future_gate_required",
        "unknown",
    ]
    assert [item.value for item in DiffProposalRiskKind] == [
        "insufficient_context_risk",
        "ungrounded_diff_risk",
        "overbroad_diff_risk",
        "scope_escape_risk",
        "secret_exposure_risk",
        "credential_exposure_risk",
        "copied_code_risk",
        "license_or_attribution_risk",
        "unsafe_readiness_flag_risk",
        "provider_network_opening_risk",
        "shell_execution_risk",
        "dependency_install_risk",
        "test_execution_risk",
        "reference_execution_risk",
        "patch_apply_risk",
        "workspace_write_risk",
        "code_edit_risk",
        "raw_source_dump_risk",
        "unknown",
    ]
    assert [item.value for item in DiffProposalTargetKind] == [
        "source_file_proposal",
        "test_file_proposal",
        "documentation_file_proposal",
        "version_doc_proposal",
        "metadata_file_proposal",
        "reference_digest_doc_proposal",
        "blocked_secret_target",
        "blocked_credential_target",
        "blocked_binary_target",
        "blocked_external_target",
        "unknown",
    ]
    assert [item.value for item in DiffProposalHunkKind] == [
        "add_block",
        "remove_block",
        "replace_block",
        "insert_before",
        "insert_after",
        "metadata_only_change",
        "documentation_change",
        "test_change",
        "safety_boundary_change",
        "no_op_hunk",
        "unknown",
    ]
    assert [item.value for item in DiffProposalValidationKind] == [
        "syntax_shape_check",
        "scope_alignment_check",
        "source_context_alignment_check",
        "no_apply_check",
        "no_write_check",
        "no_secret_check",
        "no_command_check",
        "no_dependency_install_check",
        "no_reference_execution_check",
        "review_required_check",
        "unknown",
    ]


def test_required_models_are_exported() -> None:
    for model in [
        DiffProposalFlagSet,
        DiffProposalSourceRef,
        DiffProposalGenerationPolicy,
        DiffProposalInput,
        DiffProposalTargetFile,
        PatchHunkProposal,
        PatchFileProposal,
        UnifiedDiffProposal,
        StructuredPatchProposal,
        DiffProposalEnvelope,
        DiffProposalValidationFinding,
        DiffProposalValidationReport,
        DiffProposalReport,
        DiffProposalRunPreview,
        DiffProposalNoApplyGuarantee,
        V0354ReadinessReport,
    ]:
        assert inspect.isclass(model)


def test_diff_proposal_flags_allow_artifacts_and_block_apply_write_execution() -> None:
    flags = build_diff_proposal_flags()
    assert flags.diff_proposal_layer_constructed is True
    assert flags.unified_diff_artifact_available is True
    assert flags.structured_patch_artifact_available is True
    assert flags.patch_file_proposal_available is True
    assert flags.patch_hunk_proposal_available is True
    assert flags.diff_validation_available is True
    assert flags.ready_for_v0355_patch_risk_conformance_scanner is True
    assert flags.ready_for_v0356_human_review_packet is True
    assert flags.ready_for_diff_proposal_envelope is True
    assert flags.ready_for_unified_diff_proposal is True
    assert flags.ready_for_structured_patch_proposal is True
    assert flags.ready_for_patch_hunk_proposal is True
    assert flags.ready_for_patch_proposal_artifact is True
    assert flags.ready_for_execution is False
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
    assert diff_proposal_flags_preserve_no_apply(flags)


@pytest.mark.parametrize(
    "unsafe_flag",
    [
        "ready_for_execution",
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
def test_diff_proposal_flags_reject_unsafe_readiness(unsafe_flag: str) -> None:
    with pytest.raises(ValueError):
        build_diff_proposal_flags(**{unsafe_flag: True})


def test_source_ref_policy_and_input_are_metadata_not_apply_request() -> None:
    source_ref = build_diff_proposal_source_ref()
    assert source_ref.source_kind == DiffProposalSourceKind.V0353_PATCH_PLAN
    assert source_ref.source_id == "patch_plan:v0.35.3"

    policy = default_diff_proposal_generation_policy()
    assert policy.allow_unified_diff_text is True
    assert policy.allow_structured_patch is True
    assert policy.allow_before_after_preview is True
    assert policy.require_no_apply is True
    assert policy.require_no_write is True
    assert policy.allow_patch_apply is False
    assert policy.allow_workspace_write is False
    assert policy.allow_code_edit is False
    assert policy.allow_test_execution is False
    assert policy.allow_shell is False
    assert policy.allow_dependency_install is False
    assert diff_proposal_policy_blocks_apply(policy)

    for field in ["allow_patch_apply", "allow_workspace_write", "allow_code_edit", "allow_test_execution", "allow_shell", "allow_dependency_install"]:
        with pytest.raises(ValueError):
            build_diff_proposal_generation_policy(**{field: True})

    diff_input = build_diff_proposal_input()
    assert diff_input.requested_mode == DiffProposalMode.COMBINED_UNIFIED_AND_STRUCTURED_ARTIFACT
    assert "patch_application" in diff_input.prohibited_runtime_actions
    assert "workspace_write" in diff_input.prohibited_runtime_actions
    assert "reference_execution" in diff_input.prohibited_runtime_actions


def test_target_hunk_file_unified_and_structured_artifacts_do_not_apply_or_write() -> None:
    target = build_diff_proposal_target_file()
    assert target.allowed_for_diff_artifact is True
    assert target.allowed_for_apply is False
    assert target.allowed_for_write is False
    with pytest.raises(ValueError):
        build_diff_proposal_target_file(allowed_for_apply=True)
    with pytest.raises(ValueError):
        build_diff_proposal_target_file(allowed_for_write=True)

    hunk = build_patch_hunk_proposal()
    assert hunk.ready_for_apply is False
    assert len(hunk.proposed_hunk_text) <= diff_module.DEFAULT_MAX_UNIFIED_DIFF_CHARS
    with pytest.raises(ValueError):
        build_patch_hunk_proposal(ready_for_apply=True)

    file_proposal = build_patch_file_proposal()
    assert file_proposal.ready_for_apply is False
    assert file_proposal.ready_for_write is False
    assert len(file_proposal.proposed_file_diff_preview) <= diff_module.DEFAULT_MAX_UNIFIED_DIFF_CHARS
    with pytest.raises(ValueError):
        build_patch_file_proposal(ready_for_apply=True)
    with pytest.raises(ValueError):
        build_patch_file_proposal(ready_for_write=True)

    unified = build_unified_diff_proposal()
    assert unified.ready_for_apply is False
    assert unified.ready_for_git_apply is False
    assert unified_diff_proposal_is_not_git_apply(unified)
    with pytest.raises(ValueError):
        build_unified_diff_proposal(ready_for_git_apply=True)

    structured = build_structured_patch_proposal()
    assert structured.ready_for_apply is False
    assert structured.ready_for_write is False
    assert structured_patch_proposal_is_not_write(structured)
    with pytest.raises(ValueError):
        build_structured_patch_proposal(ready_for_apply=True)
    with pytest.raises(ValueError):
        build_structured_patch_proposal(ready_for_write=True)


def test_envelope_reports_guarantee_and_readiness_preserve_no_apply() -> None:
    envelope = build_diff_proposal_envelope()
    assert envelope.ready_for_v0355_patch_risk_conformance_scanner is True
    assert envelope.ready_for_v0356_human_review_packet is True
    assert envelope.ready_for_patch_application is False
    assert envelope.ready_for_workspace_write is False
    assert envelope.ready_for_code_edit is False
    assert envelope.ready_for_execution is False
    assert diff_proposal_envelope_is_not_apply(envelope)
    with pytest.raises(ValueError):
        build_diff_proposal_envelope(ready_for_patch_application=True)

    validation = validate_diff_proposal_envelope(envelope)
    assert validation.valid is True
    assert validation.ready_for_patch_application is False
    assert validation.ready_for_workspace_write is False
    assert validation.ready_for_execution is False

    report = build_diff_proposal_report()
    assert report.diff_proposal_envelope_ready is True
    assert report.unified_diff_artifact_ready is True
    assert report.structured_patch_artifact_ready is True
    assert report.ready_for_patch_application is False
    assert report.ready_for_workspace_write is False
    assert report.ready_for_execution is False

    preview = build_diff_proposal_run_preview()
    assert preview.no_patch_application_guarantee is True
    assert preview.no_workspace_write_guarantee is True
    assert preview.no_git_apply_runtime_call_guarantee is True

    guarantee = build_diff_proposal_no_apply_guarantee()
    for field_name in guarantee.__dataclass_fields__:
        if field_name.startswith("no_"):
            assert getattr(guarantee, field_name) is True

    readiness = build_v0354_readiness_report()
    assert readiness.ready_for_diff_proposal_envelope is True
    assert readiness.ready_for_unified_diff_proposal is True
    assert readiness.ready_for_structured_patch_proposal is True
    assert readiness.ready_for_patch_hunk_proposal is True
    assert readiness.ready_for_patch_proposal_artifact is True
    assert readiness.ready_for_patch_application is False
    assert readiness.ready_for_workspace_write is False
    assert readiness.ready_for_code_edit is False
    assert readiness.ready_for_execution is False
    assert readiness.production_certified is False
    assert v0354_readiness_report_is_not_execution_ready(readiness)


def test_fake_patch_plan_metadata_produces_structured_and_bounded_unified_artifacts() -> None:
    patch_plan = build_patch_plan()
    diff_input = build_diff_proposal_input_from_patch_plan(patch_plan)
    structured = build_structured_patch_proposal_from_patch_plan(patch_plan)
    unified = build_unified_diff_proposal_from_structured_patch(structured)
    envelope = build_diff_proposal_envelope(
        diff_input_id=diff_input.diff_input_id,
        structured_patch=structured,
        unified_diff=unified,
        source_refs=diff_input.source_refs,
    )

    assert diff_input.patch_plan_id == patch_plan.patch_plan_id
    assert structured.file_proposals
    assert unified.diff_text
    assert len(unified.diff_text) <= diff_module.DEFAULT_MAX_UNIFIED_DIFF_CHARS
    assert unified.ready_for_git_apply is False
    assert envelope.structured_patch == structured
    assert envelope.unified_diff == unified
    assert envelope.ready_for_patch_application is False


def test_missing_plan_context_produces_gap_review_required_metadata() -> None:
    diff_input = build_diff_proposal_input_from_patch_plan(None)
    structured = build_structured_patch_proposal_from_patch_plan(None)
    unified = build_unified_diff_proposal_from_structured_patch(structured)
    envelope = build_diff_proposal_envelope(
        diff_input_id=diff_input.diff_input_id,
        mode=DiffProposalMode.REVIEW_REQUIRED,
        status=DiffProposalStatus.PROPOSAL_CREATED_WITH_GAPS,
        readiness_level=DiffProposalReadinessLevel.BLOCKED,
        structured_patch=structured,
        unified_diff=unified,
        gaps=["missing patch plan", "missing context snapshot"],
    )

    assert diff_input.patch_plan_id is None
    assert structured.file_proposals == []
    assert DiffProposalRiskKind.INSUFFICIENT_CONTEXT_RISK in structured.risk_kinds
    assert envelope.gaps
    assert envelope.status == DiffProposalStatus.PROPOSAL_CREATED_WITH_GAPS
    assert envelope.ready_for_patch_application is False
    validation = validate_diff_proposal_envelope(envelope)
    assert validation.valid is True
    assert any(finding.decision_kind == DiffProposalDecisionKind.REQUIRE_REVIEW for finding in validation.findings)


def test_validation_helpers_preserve_no_apply_and_no_write() -> None:
    assert validate_patch_hunk_proposal(build_patch_hunk_proposal()).valid is True
    assert validate_patch_file_proposal(build_patch_file_proposal()).valid is True
    assert validate_diff_proposal_envelope(build_diff_proposal_envelope()).valid is True


def test_rejected_reference_pattern_does_not_produce_unsafe_diff() -> None:
    structured = build_structured_patch_proposal(
        file_proposals=[],
        proposal_summary="Rejected reference pattern produced no file proposals.",
        proposal_rationale="Rejected patterns must not create unsafe diff artifacts.",
        risk_kinds=[DiffProposalRiskKind.UNGROUNDED_DIFF_RISK],
        metadata={"rejected_reference_pattern": True},
    )
    unified = build_unified_diff_proposal_from_structured_patch(structured)
    envelope = build_diff_proposal_envelope(structured_patch=structured, unified_diff=unified, gaps=["rejected reference pattern"])

    assert structured.file_proposals == []
    assert unified.diff_text == ""
    assert envelope.gaps == ["rejected reference pattern"]
    assert envelope.ready_for_patch_application is False
    assert envelope.ready_for_workspace_write is False


def test_helpers_do_not_use_forbidden_runtime_capabilities() -> None:
    source = inspect.getsource(diff_module)
    forbidden_tokens = [
        "import subprocess",
        "subprocess.",
        "os.system",
        "shell=True",
        "Path(",
        ".read_text(",
        ".write_text(",
        ".write_bytes(",
        " open(",
        "import requests",
        "import httpx",
        "import urllib",
        "import aiohttp",
        "import socket",
        "os.environ",
        "eval(",
        "exec(",
        "importlib",
    ]
    for token in forbidden_tokens:
        assert token not in source


def test_helpers_cannot_set_unsafe_readiness_true() -> None:
    with pytest.raises(ValueError):
        build_v0354_readiness_report(ready_for_execution=True)
    with pytest.raises(ValueError):
        build_v0354_readiness_report(ready_for_patch_application=True)
    with pytest.raises(ValueError):
        build_diff_proposal_report(ready_for_workspace_write=True)
    with pytest.raises(ValueError):
        build_diff_proposal_validation_report(ready_for_execution=True)
