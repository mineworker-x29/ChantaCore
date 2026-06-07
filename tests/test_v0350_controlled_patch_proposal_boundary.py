import inspect

import pytest

from chanta_core.agent_runtime import (
    ControlledPatchProposalFlagSet,
    ControlledPatchProposalTrackKind,
    PatchApplyPosture,
    PatchProposalBoundaryStatus,
    PatchProposalCapabilityKind,
    PatchProposalDecisionKind,
    PatchProposalReadinessLevel,
    PatchProposalRiskKind,
    PatchProposalSurfaceKind,
    PatchWritePosture,
    ReferenceCorpusInspectionStatus,
    ReferenceCorpusKind,
    ReferenceHarnessPatternKind,
    ReferencePatternDisposition,
    build_controlled_patch_proposal_allowed_surface,
    build_controlled_patch_proposal_boundary,
    build_controlled_patch_proposal_flags,
    build_controlled_patch_proposal_gate_evaluation,
    build_controlled_patch_proposal_no_apply_guarantee,
    build_controlled_patch_proposal_permission_decision,
    build_controlled_patch_proposal_permission_request,
    build_controlled_patch_proposal_prohibited_surface,
    build_controlled_patch_proposal_risk_register,
    build_patch_proposal_surface_policy,
    build_reference_corpus_inspection_policy,
    build_reference_corpus_inventory,
    build_reference_harness_pattern,
    build_reference_pattern_adaptation_map,
    build_reference_pattern_digest,
    build_reference_pattern_digest_from_reference_roots,
    build_reference_pattern_rejection_record,
    build_v0350_readiness_report,
    build_v035_roadmap_overview,
    controlled_patch_proposal_boundary_is_not_apply,
    controlled_patch_proposal_decision_is_not_apply,
    controlled_patch_proposal_flags_preserve_no_apply,
    inspect_reference_corpus_readonly,
    patch_proposal_surface_policy_blocks_apply,
    reference_pattern_digest_confirms_no_execution,
    v0350_readiness_report_is_not_execution_ready,
)
from chanta_core.agent_runtime import patch_proposal_boundary as boundary_module


def test_v0350_taxonomies_have_required_values() -> None:
    assert ControlledPatchProposalTrackKind.BOUNDARY_FOUNDATION.value == "boundary_foundation"
    assert ControlledPatchProposalTrackKind.CONSOLIDATION.value == "consolidation"
    assert PatchProposalSurfaceKind.REFERENCE_PATTERN_DIGEST.value == "reference_pattern_digest"
    assert PatchProposalSurfaceKind.PATCH_APPLY.value == "patch_apply"
    assert PatchProposalCapabilityKind.CREATE_REFERENCE_PATTERN_DIGEST.value == "create_reference_pattern_digest"
    assert PatchProposalCapabilityKind.RUN_APPLY_PATCH.value == "run_apply_patch"
    assert PatchProposalRiskKind.PATCH_APPLY_RISK.value == "patch_apply_risk"
    assert PatchProposalRiskKind.REFERENCE_IMPORT_RISK.value == "reference_import_risk"
    assert PatchProposalDecisionKind.ALLOW_REFERENCE_DIGEST_GENERATION.value == "allow_reference_digest_generation"
    assert PatchProposalBoundaryStatus.DIGEST_CREATED_WITH_GAPS.value == "digest_created_with_gaps"
    assert PatchProposalReadinessLevel.DESIGN_HANDOFF_READY_FOR_V0351.value == "design_handoff_ready_for_v0351"
    assert PatchWritePosture.NO_WRITE.value == "no_write"
    assert PatchApplyPosture.NO_APPLY.value == "no_apply"
    assert ReferenceCorpusKind.OPENCODE.value == "opencode"
    assert ReferenceCorpusInspectionStatus.INSPECTED_READONLY.value == "inspected_readonly"
    assert ReferenceHarnessPatternKind.DIFF_PROPOSAL_PATTERN.value == "diff_proposal_pattern"
    assert ReferencePatternDisposition.REJECTED_FOR_SAFETY.value == "rejected_for_safety"


def test_flag_set_allows_boundary_handoff_but_blocks_unsafe_readiness() -> None:
    flags = build_controlled_patch_proposal_flags()
    assert flags.patch_proposal_boundary_constructed is True
    assert flags.reference_corpus_policy_defined is True
    assert flags.reference_pattern_digest_created is True
    assert flags.patch_proposal_surface_policy_defined is True
    assert flags.patch_proposal_risk_register_defined is True
    assert flags.ready_for_v0351_patch_intent_scope_policy is True
    assert flags.ready_for_v0352_readonly_patch_context_collector is True
    assert flags.ready_for_reference_pattern_digest is True
    assert flags.ready_for_execution is False
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
    assert controlled_patch_proposal_flags_preserve_no_apply(flags)


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
        "ready_for_patch_proposal",
    ],
)
def test_flags_reject_unsafe_readiness(unsafe_flag: str) -> None:
    with pytest.raises(ValueError):
        build_controlled_patch_proposal_flags(**{unsafe_flag: True})


def test_reference_policy_blocks_runtime_reference_actions() -> None:
    policy = build_reference_corpus_inspection_policy()
    assert policy.allow_execution is False
    assert policy.allow_import is False
    assert policy.allow_dependency_install is False
    assert policy.allow_test_run is False
    assert policy.allow_shell is False
    assert policy.allow_secret_file_read is False
    assert policy.allow_raw_source_dump is False
    assert policy.max_files_per_corpus >= 0
    assert policy.max_file_chars >= 0
    assert policy.max_excerpt_chars >= 0

    for field in ["allow_execution", "allow_import", "allow_dependency_install", "allow_test_run", "allow_shell", "allow_secret_file_read", "allow_raw_source_dump"]:
        with pytest.raises(ValueError):
            build_reference_corpus_inspection_policy(**{field: True})


def test_inventory_pattern_digest_adaptation_and_rejection_models() -> None:
    inventory = build_reference_corpus_inventory(
        corpus_kind=ReferenceCorpusKind.OPENCODE,
        root_path_ref="references/OpenCode",
        inspection_status=ReferenceCorpusInspectionStatus.INSPECTED_READONLY,
        inspected_file_refs=["references/OpenCode/notes/05_tool_system_analysis.md"],
        summary="OpenCode inventory metadata only.",
    )
    assert inventory.import_or_execution is False

    observed = build_reference_harness_pattern(disposition=ReferencePatternDisposition.OBSERVED)
    adapted = build_reference_harness_pattern(pattern_id="pattern:adapted", disposition=ReferencePatternDisposition.ADAPTED_TO_CHANTACORE)
    rejected = build_reference_harness_pattern(
        pattern_id="pattern:rejected",
        disposition=ReferencePatternDisposition.REJECTED_FOR_SAFETY,
        pattern_kind=ReferenceHarnessPatternKind.UNSAFE_EXECUTION_PATTERN,
        rejection_reason="Runtime execution rejected.",
    )
    future = build_reference_harness_pattern(
        pattern_id="pattern:future",
        disposition=ReferencePatternDisposition.FUTURE_TRACK,
        future_track_note="Diff proposal envelope is later-stage.",
    )
    digest = build_reference_pattern_digest(corpus_inventories=[inventory], patterns=[observed, adapted, rejected, future])
    assert digest.no_execution_confirmed is True
    assert digest.no_import_confirmed is True
    assert digest.no_install_confirmed is True
    assert digest.no_test_run_confirmed is True
    assert digest.no_secret_read_confirmed is True
    assert digest.executable is False
    assert reference_pattern_digest_confirms_no_execution(digest)

    adaptation_map = build_reference_pattern_adaptation_map()
    assert adaptation_map.implementation_execution is False
    rejection = build_reference_pattern_rejection_record()
    assert "Patch application" in rejection.reason

    with pytest.raises(ValueError):
        build_reference_harness_pattern(disposition=ReferencePatternDisposition.REJECTED_FOR_SAFETY)
    with pytest.raises(ValueError):
        build_reference_pattern_digest(no_execution_confirmed=False)


def test_surface_policy_allowed_and_prohibited_surfaces_are_conservative() -> None:
    policy = build_patch_proposal_surface_policy()
    assert policy.allow_reference_digest is True
    assert policy.allow_patch_intent_artifact is True
    assert policy.allow_patch_scope_policy is True
    assert policy.allow_patch_apply is False
    assert policy.allow_workspace_write is False
    assert policy.allow_code_edit is False
    assert policy.allow_shell is False
    assert policy.allow_test_execution is False
    assert policy.allow_dependency_install is False
    assert patch_proposal_surface_policy_blocks_apply(policy)

    for field in ["allow_patch_apply", "allow_workspace_write", "allow_code_edit", "allow_shell", "allow_test_execution", "allow_dependency_install"]:
        with pytest.raises(ValueError):
            build_patch_proposal_surface_policy(**{field: True})

    allowed = build_controlled_patch_proposal_allowed_surface()
    assert allowed.allowed_only_for_design_stage is True
    assert allowed.executable_in_v0350 is False
    assert allowed.writes_files is False
    assert allowed.applies_patch is False
    with pytest.raises(ValueError):
        build_controlled_patch_proposal_allowed_surface(writes_files=True)

    prohibited = build_controlled_patch_proposal_prohibited_surface()
    assert prohibited.blocks_apply is True
    assert prohibited.blocks_write is True
    assert prohibited.blocks_runtime_readiness is True


def test_boundary_decision_gate_risk_guarantee_and_readiness_are_not_apply() -> None:
    boundary = build_controlled_patch_proposal_boundary()
    assert boundary.ready_for_v0351_patch_intent_scope_policy is True
    assert boundary.ready_for_v0352_readonly_patch_context_collector is True
    assert boundary.ready_for_patch_proposal is False
    assert boundary.ready_for_patch_application is False
    assert boundary.ready_for_workspace_write is False
    assert boundary.ready_for_code_edit is False
    assert boundary.ready_for_execution is False
    assert boundary.patch_proposal_generation is False
    assert boundary.patch_application is False
    assert controlled_patch_proposal_boundary_is_not_apply(boundary)

    for flag in ["ready_for_patch_application", "ready_for_workspace_write", "ready_for_code_edit", "ready_for_execution", "ready_for_patch_proposal"]:
        with pytest.raises(ValueError):
            build_controlled_patch_proposal_boundary(**{flag: True})

    request = build_controlled_patch_proposal_permission_request()
    decision = build_controlled_patch_proposal_permission_decision(request_id=request.request_id)
    assert controlled_patch_proposal_decision_is_not_apply(decision)
    for field in ["patch_apply_allowed", "workspace_write_allowed", "code_edit_allowed", "shell_allowed", "test_execution_allowed", "dependency_install_allowed"]:
        with pytest.raises(ValueError):
            build_controlled_patch_proposal_permission_decision(**{field: True})

    gate = build_controlled_patch_proposal_gate_evaluation(decision=decision)
    assert gate.ready_for_execution is False
    assert gate.ready_for_patch_application is False

    risk = build_controlled_patch_proposal_risk_register()
    joined_risks = " ".join(str(item) for item in risk.risk_kinds)
    for term in ["patch_apply", "workspace_write", "code_edit", "shell", "test", "dependency", "reference_execution", "reference_import", "secret", "scope_escape"]:
        assert term in joined_risks
    assert risk.permission is False

    guarantee = build_controlled_patch_proposal_no_apply_guarantee()
    for name in guarantee.__dataclass_fields__:
        if name.startswith("no_"):
            assert getattr(guarantee, name) is True

    roadmap = build_v035_roadmap_overview()
    assert roadmap.ready_for_execution is False
    assert roadmap.ready_for_patch_application is False

    report = build_v0350_readiness_report()
    assert report.ready_for_v0351_patch_intent_scope_policy is True
    assert report.ready_for_v0352_readonly_patch_context_collector is True
    assert report.ready_for_reference_pattern_digest is True
    assert report.ready_for_execution is False
    assert report.ready_for_patch_proposal is False
    assert report.ready_for_patch_application is False
    assert report.ready_for_workspace_write is False
    assert report.ready_for_code_edit is False
    assert report.ready_for_apply_patch is False
    assert report.ready_for_git_apply is False
    assert report.ready_for_test_execution is False
    assert report.ready_for_shell_execution is False
    assert report.ready_for_dependency_install is False
    assert report.ready_for_reference_execution is False
    assert report.ready_for_reference_import is False
    assert report.production_certified is False
    assert v0350_readiness_report_is_not_execution_ready(report)


def test_fake_reference_corpus_digest_is_readonly_and_missing_corpus_recorded(tmp_path) -> None:
    fake = tmp_path / "OpenCode"
    fake.mkdir()
    (fake / "README.md").write_text("CLI, tool registry, permission gate, patch review notes.", encoding="utf-8")
    (fake / "session_context.ts").write_text("session context collection metadata only", encoding="utf-8")
    (fake / ".env").write_text("SHOULD_NOT_BE_READ=1", encoding="utf-8")

    inventory, patterns = inspect_reference_corpus_readonly(fake, ReferenceCorpusKind.OPENCODE)
    assert inventory.inspection_status == ReferenceCorpusInspectionStatus.INSPECTED_READONLY
    assert inventory.import_or_execution is False
    assert any("README.md" in ref for ref in inventory.inspected_file_refs)
    assert any(".env" in ref for ref in inventory.skipped_file_refs)
    assert any("blocked secret-like" in reason for reason in inventory.skipped_reasons)
    assert any(pattern.pattern_kind == ReferenceHarnessPatternKind.CLI_SURFACE_PATTERN for pattern in patterns)
    assert any(pattern.disposition == ReferencePatternDisposition.REJECTED_FOR_SAFETY for pattern in patterns)

    missing_inventory, missing_patterns = inspect_reference_corpus_readonly(tmp_path / "missing", ReferenceCorpusKind.HERMES)
    assert missing_inventory.inspection_status == ReferenceCorpusInspectionStatus.NOT_FOUND
    assert missing_inventory.import_or_execution is False
    assert missing_patterns[0].disposition == ReferencePatternDisposition.INSUFFICIENT_EVIDENCE

    digest = build_reference_pattern_digest_from_reference_roots(
        {
            ReferenceCorpusKind.OPENCODE: fake,
            ReferenceCorpusKind.HERMES: tmp_path / "missing",
        }
    )
    assert reference_pattern_digest_confirms_no_execution(digest)
    assert len(digest.corpus_inventories) == 2


def test_module_source_has_no_runtime_execution_or_apply_patterns() -> None:
    source = inspect.getsource(boundary_module)
    forbidden_patterns = [
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
        "pip ",
        "npm ",
        "logging.",
    ]
    for pattern in forbidden_patterns:
        assert pattern not in source

    compact = source.replace(" ", "")
    unsafe_true_patterns = [
        "ready_for_execution=True",
        "ready_for_patch_application=True",
        "ready_for_workspace_write=True",
        "ready_for_code_edit=True",
        "ready_for_apply_patch=True",
        "ready_for_git_apply=True",
        "ready_for_test_execution=True",
        "ready_for_shell_execution=True",
        "ready_for_dependency_install=True",
        "ready_for_reference_execution=True",
        "ready_for_reference_import=True",
        "ready_for_patch_proposal=True",
        "production_certified=True",
    ]
    for pattern in unsafe_true_patterns:
        assert pattern not in compact
