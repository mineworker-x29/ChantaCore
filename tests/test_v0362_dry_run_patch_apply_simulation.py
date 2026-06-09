import inspect

import pytest

from chanta_core.agent_runtime import (
    DryRunApplyDecisionKind,
    DryRunApplyMode,
    DryRunApplyReadinessLevel,
    DryRunApplyRiskKind,
    DryRunApplySourceKind,
    DryRunApplyStatus,
    DryRunConflictKind,
    DryRunFileDeltaKind,
    DryRunHunkAlignmentStatus,
    align_dry_run_hunk_to_source_image,
    build_apply_candidate_envelope,
    build_dry_run_apply_decision,
    build_dry_run_apply_flags,
    build_dry_run_apply_input,
    build_dry_run_apply_input_from_apply_candidate,
    build_dry_run_apply_no_write_guarantee,
    build_dry_run_apply_policy,
    build_dry_run_apply_report,
    build_dry_run_apply_run_preview,
    build_dry_run_apply_simulation_result,
    build_dry_run_apply_source_ref,
    build_dry_run_apply_validation_finding,
    build_dry_run_apply_validation_report,
    build_dry_run_conflict,
    build_dry_run_hunk_alignment,
    build_dry_run_hunk_input,
    build_dry_run_simulated_file_delta,
    build_dry_run_simulated_file_result,
    build_dry_run_source_image,
    build_dry_run_target_file_image,
    build_v0362_readiness_report,
    default_dry_run_apply_policy,
    dry_run_apply_decision_is_not_apply_permission,
    dry_run_apply_flags_preserve_no_write,
    dry_run_apply_policy_blocks_write_apply,
    dry_run_apply_result_is_not_apply,
    dry_run_simulated_delta_is_not_write,
    parse_unified_diff_to_dry_run_hunks,
    run_dry_run_apply_simulation,
    simulate_dry_run_file_delta,
    v0362_readiness_report_is_not_execution_ready,
    validate_dry_run_apply_simulation_result,
)
import chanta_core.agent_runtime.patch_apply_dry_run as dry_run


SIMPLE_DIFF = """--- a/src/example.py
+++ b/src/example.py
@@ -1,3 +1,3 @@
 alpha
-beta
+BETA
 gamma
"""


def values(enum_cls):
    return {item.value for item in enum_cls}


def test_taxonomies_are_complete():
    assert values(DryRunApplyMode) == {
        "unified_diff_dry_run",
        "structured_patch_dry_run",
        "combined_diff_dry_run",
        "metadata_only_dry_run",
        "blocked",
        "no_op",
        "unknown",
    }
    assert values(DryRunApplySourceKind) == {
        "v0361_apply_candidate_envelope",
        "v0361_human_approval_contract",
        "v0361_apply_eligibility_decision",
        "v0354_diff_proposal_envelope",
        "v0354_unified_diff_proposal",
        "v0354_structured_patch_proposal",
        "v0352_patch_context_snapshot",
        "v0352_evidence_bundle",
        "in_memory_source_image",
        "test_fixture",
        "unknown",
    }
    assert values(DryRunApplyStatus) == {
        "unknown",
        "draft",
        "input_validated",
        "simulation_ready",
        "simulation_completed",
        "simulation_completed_with_conflicts",
        "blocked",
        "review_required",
        "future_gated",
        "no_op",
        "safe_failed",
    }
    assert values(DryRunApplyReadinessLevel) == {
        "not_ready",
        "dry_run_contract_ready",
        "dry_run_input_ready",
        "hunk_alignment_ready",
        "conflict_report_ready",
        "simulated_delta_ready",
        "design_handoff_ready_for_v0363",
        "design_handoff_ready_for_v0364",
        "blocked",
        "future_track",
    }
    assert values(DryRunApplyDecisionKind) == {
        "allow_dry_run_simulation",
        "allow_hunk_alignment",
        "allow_conflict_detection",
        "allow_simulated_delta_metadata",
        "eligible_for_future_sandbox_workspace",
        "deny",
        "block",
        "no_op",
        "require_review",
        "future_gate_required",
        "unknown",
    }
    assert values(DryRunApplyRiskKind) == {
        "invalid_apply_candidate_risk",
        "missing_human_approval_risk",
        "invalid_human_approval_risk",
        "missing_diff_risk",
        "malformed_diff_risk",
        "missing_source_image_risk",
        "stale_source_context_risk",
        "hunk_alignment_failure_risk",
        "patch_conflict_risk",
        "scope_mismatch_risk",
        "secret_exposure_risk",
        "live_workspace_write_risk",
        "sandbox_write_confusion_risk",
        "patch_apply_confusion_risk",
        "apply_patch_risk",
        "git_apply_risk",
        "shell_execution_risk",
        "test_execution_risk",
        "dependency_install_risk",
        "external_agent_execution_risk",
        "dominion_runtime_risk",
        "unknown",
    }
    assert values(DryRunHunkAlignmentStatus) == {
        "unknown",
        "aligned_exact",
        "aligned_with_offset",
        "aligned_with_fuzz",
        "not_found",
        "ambiguous",
        "stale_context",
        "blocked",
        "skipped",
    }
    assert values(DryRunConflictKind) == {
        "no_conflict",
        "missing_target_source",
        "malformed_hunk",
        "context_not_found",
        "ambiguous_context",
        "stale_source",
        "overlapping_hunks",
        "blocked_target",
        "scope_violation",
        "secret_target",
        "binary_target",
        "unsupported_operation",
        "unknown",
    }
    assert values(DryRunFileDeltaKind) == {
        "no_change",
        "simulated_addition",
        "simulated_deletion",
        "simulated_replacement",
        "simulated_file_create",
        "simulated_file_delete",
        "simulated_metadata_change",
        "unsupported_delta",
        "blocked_delta",
        "unknown",
    }


def test_flags_allow_dry_run_readiness_but_preserve_no_write_apply():
    flags = build_dry_run_apply_flags()

    assert flags.dry_run_apply_layer_constructed is True
    assert flags.hunk_alignment_available is True
    assert flags.conflict_detection_available is True
    assert flags.simulated_delta_available is True
    assert flags.ready_for_dry_run_apply_simulation is True
    assert flags.ready_for_future_sandbox_workspace_input is True
    assert flags.ready_for_v0363_sandbox_workspace_overlay_policy is True
    assert flags.ready_for_v0364_sandbox_patch_apply_engine is True
    assert dry_run_apply_flags_preserve_no_write(flags)


@pytest.mark.parametrize(
    "flag_name",
    [
        "ready_for_execution",
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
def test_flags_reject_unsafe_readiness(flag_name):
    with pytest.raises(ValueError):
        build_dry_run_apply_flags(**{flag_name: True})


def test_source_ref_policy_input_and_images_are_metadata_only():
    source_ref = build_dry_run_apply_source_ref()
    policy = default_dry_run_apply_policy()
    dry_input = build_dry_run_apply_input()
    source_image = build_dry_run_source_image()
    target_image = build_dry_run_target_file_image()

    assert source_ref.source_kind == DryRunApplySourceKind.V0361_APPLY_CANDIDATE_ENVELOPE
    assert policy.allow_unified_diff_parse is True
    assert policy.allow_hunk_alignment is True
    assert policy.allow_conflict_detection is True
    assert policy.allow_simulated_delta is True
    assert policy.allow_future_sandbox_workspace_input is True
    assert dry_run_apply_policy_blocks_write_apply(policy)
    assert "apply" in dry_input.prohibited_runtime_actions
    assert "write" in dry_input.prohibited_runtime_actions
    assert "shell" in dry_input.prohibited_runtime_actions
    assert source_image.safe_for_simulation is True
    assert target_image.ready_for_write is False

    with pytest.raises(ValueError):
        build_dry_run_source_image(metadata={"binary": True}, safe_for_simulation=True)
    with pytest.raises(ValueError):
        build_dry_run_target_file_image(ready_for_write=True)


@pytest.mark.parametrize(
    "allow_name",
    [
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
    ],
)
def test_policy_rejects_unsafe_allow_flags(allow_name):
    with pytest.raises(ValueError):
        build_dry_run_apply_policy(**{allow_name: True})


def test_hunk_alignment_conflict_delta_and_result_are_not_apply():
    hunk = build_dry_run_hunk_input()
    alignment = build_dry_run_hunk_alignment()
    conflict = build_dry_run_conflict()
    delta = build_dry_run_simulated_file_delta()
    file_result = build_dry_run_simulated_file_result()
    result = build_dry_run_apply_simulation_result()

    assert hunk.hunk_header.startswith("@@")
    assert alignment.alignment_status == DryRunHunkAlignmentStatus.ALIGNED_EXACT
    assert conflict.blocks_future_sandbox_apply is True
    assert delta.ready_for_write is False
    assert delta.ready_for_apply is False
    assert dry_run_simulated_delta_is_not_write(delta)
    assert file_result.ready_for_write is False
    assert file_result.ready_for_apply is False
    assert result.simulation_successful is True
    assert result.eligible_for_future_sandbox_workspace_input is True
    assert result.ready_for_sandbox_patch_apply is False
    assert result.ready_for_patch_application is False
    assert dry_run_apply_result_is_not_apply(result)

    with pytest.raises(ValueError):
        build_dry_run_simulated_file_delta(ready_for_apply=True)
    with pytest.raises(ValueError):
        build_dry_run_apply_simulation_result(ready_for_patch_application=True)


def test_parse_unified_diff_and_exact_hunk_alignment():
    hunks = parse_unified_diff_to_dry_run_hunks(SIMPLE_DIFF)
    source_image = build_dry_run_source_image(source_text="alpha\nbeta\ngamma\n")
    alignment = align_dry_run_hunk_to_source_image(hunks[0], source_image)

    assert len(hunks) == 1
    assert hunks[0].target_path_ref == "src/example.py"
    assert hunks[0].removed_lines == ["beta"]
    assert hunks[0].proposed_lines == ["alpha", "BETA", "gamma"]
    assert alignment.alignment_status == DryRunHunkAlignmentStatus.ALIGNED_EXACT
    assert alignment.matched_line_start == 1
    assert alignment.matched_line_end == 3


def test_context_not_found_and_ambiguous_context_conflicts_are_reported():
    hunk = parse_unified_diff_to_dry_run_hunks(SIMPLE_DIFF)[0]
    missing_source = build_dry_run_source_image(source_text="alpha\nother\ngamma\n")
    missing_result = simulate_dry_run_file_delta(hunk, missing_source)

    assert missing_result.simulation_successful is False
    assert missing_result.conflicts[0].conflict_kind == DryRunConflictKind.CONTEXT_NOT_FOUND
    assert missing_result.ready_for_future_sandbox_workspace_input is False

    ambiguous_source = build_dry_run_source_image(source_text="alpha\nbeta\ngamma\nalpha\nbeta\ngamma\n")
    ambiguous_alignment = align_dry_run_hunk_to_source_image(hunk, ambiguous_source)
    ambiguous_result = simulate_dry_run_file_delta(hunk, ambiguous_source, ambiguous_alignment)

    assert ambiguous_alignment.alignment_status == DryRunHunkAlignmentStatus.AMBIGUOUS
    assert ambiguous_result.conflicts[0].conflict_kind == DryRunConflictKind.AMBIGUOUS_CONTEXT


def test_simulate_replacement_in_memory_only():
    hunk = parse_unified_diff_to_dry_run_hunks(SIMPLE_DIFF)[0]
    source_image = build_dry_run_source_image(source_text="alpha\nbeta\ngamma\n")
    file_result = simulate_dry_run_file_delta(hunk, source_image)
    delta = file_result.simulated_deltas[0]

    assert file_result.simulation_successful is True
    assert file_result.ready_for_future_sandbox_workspace_input is True
    assert delta.delta_kind == DryRunFileDeltaKind.SIMULATED_REPLACEMENT
    assert delta.after_preview == "alpha\nBETA\ngamma"
    assert delta.ready_for_write is False
    assert delta.ready_for_apply is False
    assert file_result.target_file_image.ready_for_write is False


def test_run_dry_run_apply_simulation_success_and_blocks():
    dry_input = build_dry_run_apply_input()
    source_image = build_dry_run_source_image(source_text="alpha\nbeta\ngamma\n")
    result = run_dry_run_apply_simulation(dry_input, SIMPLE_DIFF, [source_image])

    assert result.simulation_successful is True
    assert result.eligible_for_future_sandbox_workspace_input is True
    assert result.ready_for_v0363_sandbox_workspace_overlay_policy is True
    assert result.ready_for_v0364_sandbox_patch_apply_engine is True
    assert result.ready_for_sandbox_patch_apply is False
    assert result.ready_for_patch_application is False

    missing_approval = build_dry_run_apply_input(human_approval_contract_id=None)
    blocked = run_dry_run_apply_simulation(missing_approval, SIMPLE_DIFF, [source_image])
    assert blocked.simulation_successful is False
    assert blocked.status == DryRunApplyStatus.BLOCKED
    assert blocked.conflicts[0].conflict_kind == DryRunConflictKind.UNSUPPORTED_OPERATION

    malformed = run_dry_run_apply_simulation(dry_input, "not a unified diff", [source_image])
    assert malformed.simulation_successful is False
    assert malformed.status == DryRunApplyStatus.SAFE_FAILED
    assert malformed.conflicts[0].conflict_kind == DryRunConflictKind.MALFORMED_HUNK


def test_build_input_from_apply_candidate_consumes_metadata_only():
    candidate = build_apply_candidate_envelope()
    dry_input = build_dry_run_apply_input_from_apply_candidate(candidate)

    assert dry_input.apply_candidate_id == candidate.apply_candidate_id
    assert dry_input.human_approval_contract_id == candidate.approval_contract.approval_contract_id
    assert dry_input.diff_envelope_id == candidate.diff_envelope_id
    assert dry_input.unified_diff_id == candidate.unified_diff_id


def test_decision_validation_report_preview_guarantee_and_readiness_preserve_no_write():
    result = build_dry_run_apply_simulation_result()
    validation = validate_dry_run_apply_simulation_result(result)
    decision = build_dry_run_apply_decision()
    report = build_dry_run_apply_report(simulation_result=result, validation_report=validation, decision=decision)
    preview = build_dry_run_apply_run_preview()
    guarantee = build_dry_run_apply_no_write_guarantee()
    readiness = build_v0362_readiness_report()

    assert validation.certifies_patch_application is False
    assert dry_run_apply_decision_is_not_apply_permission(decision)
    assert report.simulation_successful is True
    assert report.ready_for_execution is False
    assert report.ready_for_patch_application is False
    assert preview.ready_for_future_sandbox_workspace_input is True
    assert all(getattr(guarantee, name) is True for name in guarantee.__dataclass_fields__ if name.startswith("no_"))
    assert readiness.ready_for_dry_run_apply_simulation is True
    assert readiness.ready_for_future_sandbox_workspace_input is True
    assert v0362_readiness_report_is_not_execution_ready(readiness)

    with pytest.raises(ValueError):
        build_dry_run_apply_validation_report(certifies_patch_application=True)
    with pytest.raises(ValueError):
        build_dry_run_apply_decision(ready_for_apply=True)
    with pytest.raises(ValueError):
        build_dry_run_apply_no_write_guarantee(no_patch_application=False)
    with pytest.raises(ValueError):
        build_v0362_readiness_report(ready_for_execution=True)


def test_module_exports_import_cleanly_from_agent_runtime():
    from chanta_core.agent_runtime import (  # noqa: PLC0415
        DryRunApplySimulationResult,
        DryRunSourceImage,
        V0362ReadinessReport,
    )

    assert DryRunApplySimulationResult is not None
    assert DryRunSourceImage is not None
    assert V0362ReadinessReport is not None


def test_dry_run_helpers_do_not_contain_runtime_execution_or_file_write_patterns():
    source = inspect.getsource(dry_run)

    forbidden_patterns = [
        "import subprocess",
        "subprocess.",
        "os.system",
        "shell=True",
        "Path.write_text",
        "Path.write_bytes",
        ".write_text(",
        ".write_bytes(",
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
    ]
    for pattern in forbidden_patterns:
        assert pattern not in source

