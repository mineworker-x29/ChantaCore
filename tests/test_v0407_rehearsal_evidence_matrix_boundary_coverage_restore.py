from __future__ import annotations

import re
from pathlib import Path

import pytest

from chanta_core.agent_runtime.repair_mission_loop_evidence_matrix import (
    CLOSED_CAPABILITIES,
    INTEGRATED_DOC_PATH,
    OPEN_CAPABILITIES,
    REQUIRED_BOUNDARY_ROWS,
    REQUIRED_DENIED_ACTIONS,
    REQUIRED_FALSE_FLAGS,
    RUNTIME_CLOSURE_CAPABILITIES,
    BoundaryCoverageKind,
    CoverageStatus,
    EvidenceCoverageKind,
    EvidenceFreshnessStatus,
    boundary_coverage_readiness_preserves_no_unsafe_runtime,
    build_boundary_coverage_gap_register,
    build_rehearsal_evidence_matrix,
    create_boundary_coverage_gap,
    create_boundary_coverage_record,
    create_checkpoint_coverage_record,
    create_denied_action_coverage_record,
    create_provider_prompt_boundary_coverage_record,
    create_readiness_flag_coverage_record,
    create_rehearsal_evidence_matrix_row,
    create_rehearsal_evidence_ref,
    create_restore_coverage_record,
    create_runtime_closure_coverage_record,
    create_v0407_integrated_restore_context_snapshot,
    create_v0407_integrated_restore_document_manifest,
    create_v0407_integrated_restore_packet,
    create_v0408_cli_execution_test_preview_surface_handoff,
    create_v041_smoke_run_acceleration_coverage_signal,
    create_verifier_subagent_boundary_coverage_record,
    denied_action_coverage_blocks_all_required_actions,
    integrated_restore_packet_uses_single_doc,
    readiness_flag_coverage_preserves_false,
    rehearsal_evidence_matrix_is_coverage_only,
    runtime_closure_coverage_preserves_closed,
    v041_coverage_signal_is_not_runtime_start,
)


def test_v0407_coverage_status_values_declared() -> None:
    assert {item.value for item in CoverageStatus} == {
        "covered",
        "partially_covered",
        "missing",
        "stale",
        "advisory_only",
        "blocked",
        "not_applicable",
    }


def test_v0407_evidence_freshness_status_values_declared() -> None:
    assert {item.value for item in EvidenceFreshnessStatus} == {
        "fresh",
        "stale",
        "unknown",
        "version_mismatch",
        "artifact_mismatch",
        "test_missing",
        "doc_missing",
    }


def test_v0407_evidence_coverage_kinds_declared() -> None:
    assert {item.value for item in EvidenceCoverageKind} == {
        "implementation_artifact",
        "test_artifact",
        "documentation_artifact",
        "readiness_flag",
        "safety_report",
        "restore_packet",
        "handoff_packet",
        "audit_record",
        "false_claim_audit",
        "withdrawal_condition",
    }


def test_v0407_boundary_coverage_kinds_declared() -> None:
    assert {item.value for item in BoundaryCoverageKind} == {
        "mission_loop_boundary",
        "dry_run_simulation",
        "sandbox_rehearsal",
        "manual_two_iteration_rehearsal",
        "human_checkpoint_gate",
        "negative_runtime_gate",
        "scope_bound_checkpoint_approval",
        "prompt_submission_gate",
        "provider_invocation_gate",
        "provider_output_quarantine",
        "verifier_subagent_request_draft",
        "verifier_evidence_requirement",
        "verifier_context_isolation",
        "verifier_dispatch_gate",
        "verifier_result_quarantine",
        "restore_handoff",
        "standalone_runtime_closed",
        "unsafe_runtime_closed",
    }


def test_v0407_evidence_ref_records_artifact_test_doc_and_freshness() -> None:
    ref = create_rehearsal_evidence_ref()

    assert ref.artifact_path.endswith("repair_mission_loop_evidence_matrix.py")
    assert ref.test_ref.endswith("test_v0407_rehearsal_evidence_matrix_boundary_coverage_restore.py")
    assert ref.doc_ref == INTEGRATED_DOC_PATH
    assert ref.freshness_status == EvidenceFreshnessStatus.FRESH.value


def test_v0407_matrix_row_records_all_required_evidence_buckets() -> None:
    row = create_rehearsal_evidence_matrix_row()

    assert row.implementation_evidence_refs
    assert row.test_evidence_refs
    assert row.documentation_evidence_refs
    assert row.readiness_flag_refs
    assert row.safety_report_refs
    assert row.restore_refs


def test_v0407_matrix_contains_v0400_through_v0406_rows() -> None:
    matrix = build_rehearsal_evidence_matrix()
    row_ids = {row.row_id for row in matrix.rows}

    for row_id in (
        "v0400_mission_loop_boundary",
        "v0401_sandbox_rehearsal",
        "v0402_manual_checkpoint",
        "v0403_negative_runtime_gate",
        "v0404_scope_bound_checkpoint",
        "v0405_provider_prompt_boundary",
        "v0406_verifier_subagent_boundary",
    ):
        assert row_id in row_ids


def test_v0407_matrix_contains_restore_and_runtime_closure_rows() -> None:
    row_ids = {row.row_id for row in build_rehearsal_evidence_matrix().rows}

    assert "restore_coverage" in row_ids
    assert "standalone_runtime_closed" in row_ids
    assert "unsafe_runtime_closed" in row_ids


def test_v0407_matrix_is_not_runtime_permission() -> None:
    matrix = build_rehearsal_evidence_matrix()

    assert matrix.runtime_authority_granted is False
    assert rehearsal_evidence_matrix_is_coverage_only(matrix)


def test_v0407_matrix_is_not_production_certification() -> None:
    with pytest.raises(ValueError):
        build_rehearsal_evidence_matrix(production_certified=True)


def test_v0407_boundary_coverage_record_never_grants_runtime_authority() -> None:
    record = create_boundary_coverage_record()

    assert record.runtime_authority_granted is False
    with pytest.raises(ValueError):
        create_boundary_coverage_record(runtime_authority_granted=True)


def test_v0407_denied_action_coverage_blocks_all_required_actions() -> None:
    record = create_denied_action_coverage_record()

    assert set(REQUIRED_DENIED_ACTIONS).issubset(record.action_coverage)
    assert denied_action_coverage_blocks_all_required_actions(record)
    with pytest.raises(ValueError):
        create_denied_action_coverage_record(action_coverage={"prompt_submission": CoverageStatus.COVERED.value})


def test_v0407_checkpoint_coverage_confirms_checkpoint_stale_and_broad_approval_blocks() -> None:
    record = create_checkpoint_coverage_record()

    assert record.checkpoint_required_between_iterations is True
    assert record.stale_checkpoint_invalid is True
    assert record.artifact_mismatch_invalid is True
    assert record.broad_approval_rejected is True
    assert record.approval_grants_runtime_authority is False


def test_v0407_provider_prompt_coverage_confirms_submission_provider_network_credentials_and_quarantine() -> None:
    record = create_provider_prompt_boundary_coverage_record()

    assert record.prompt_candidate_metadata_only is True
    assert record.prompt_submission_blocked is True
    assert record.provider_invocation_blocked is True
    assert record.provider_client_creation_blocked is True
    assert record.network_blocked is True
    assert record.credential_blocked is True
    assert record.provider_output_quarantine_required is True


def test_v0407_verifier_subagent_coverage_confirms_subagent_child_session_context_and_quarantine() -> None:
    record = create_verifier_subagent_boundary_coverage_record()

    assert record.verifier_request_draft_metadata_only is True
    assert record.subagent_invocation_blocked is True
    assert record.child_session_creation_blocked is True
    assert record.parent_raw_transcript_sharing_blocked is True
    assert record.subagent_permission_grant_blocked is True
    assert record.context_isolation_required is True
    assert record.evidence_requirement_required is True
    assert record.verifier_result_quarantine_required is True


def test_v0407_restore_coverage_requires_copy_paste_restore_prompt() -> None:
    record = create_restore_coverage_record()

    assert record.copy_paste_restore_prompt_exists is True
    assert record.capability_matrix_exists is True
    assert record.safety_flags_table_exists is True
    assert record.next_version_handoff_exists is True
    assert record.restore_claims_standalone_runtime_opened is False


def test_v0407_readiness_flag_coverage_keeps_unsafe_flags_false() -> None:
    record = create_readiness_flag_coverage_record()

    assert readiness_flag_coverage_preserves_false(record)
    with pytest.raises(ValueError):
        create_readiness_flag_coverage_record(unsafe_readiness_flags={**{flag: False for flag in REQUIRED_FALSE_FLAGS}, "ready_for_execution": True})


def test_v0407_runtime_closure_coverage_keeps_standalone_provider_prompt_subagent_live_network_closed() -> None:
    record = create_runtime_closure_coverage_record()

    assert set(RUNTIME_CLOSURE_CAPABILITIES).issubset(record.closed_capabilities)
    assert runtime_closure_coverage_preserves_closed(record)


def test_v0407_gap_register_marks_unsafe_runtime_readiness_as_blocking() -> None:
    gap = create_boundary_coverage_gap(
        gap_id="unsafe-runtime-readiness-gap",
        gap_kind="blocking_gap",
        description="unsafe runtime readiness flag became true",
        blocking=True,
        recommended_target="rollback",
    )
    register = build_boundary_coverage_gap_register((gap,))

    assert register.blocking_gap_count == 1
    assert register.unsafe_runtime_gap_count == 1
    assert register.coverage_can_complete is False


def test_v0407_gap_register_allows_minor_docs_index_gap_as_non_blocking() -> None:
    gap = create_boundary_coverage_gap(
        gap_id="minor-docs-index-gap",
        gap_kind="documentation_gap",
        description="minor docs index omission",
        blocking=False,
    )
    register = build_boundary_coverage_gap_register((gap,))

    assert register.blocking_gap_count == 0
    assert register.non_blocking_gap_count == 1
    assert register.coverage_can_complete is True


def test_v0407_safety_report_keeps_runtime_and_standalone_false() -> None:
    from chanta_core.agent_runtime.repair_mission_loop_evidence_matrix import create_boundary_coverage_safety_report

    report = create_boundary_coverage_safety_report()

    assert report.safe_for_v0407_coverage_consolidation is True
    assert report.safe_for_runtime_execution is False
    assert report.safe_for_live_workspace_apply is False
    assert report.safe_for_model_provider_invocation is False
    assert report.safe_for_prompt_submission is False
    assert report.safe_for_subagent_invocation is False
    assert report.safe_for_child_session_creation is False
    assert report.safe_for_parent_raw_transcript_sharing is False
    assert report.safe_for_standalone_default_personal_runtime is False
    assert report.production_certified is False


def test_v0407_readiness_report_keeps_unsafe_flags_false() -> None:
    from chanta_core.agent_runtime.repair_mission_loop_evidence_matrix import create_boundary_coverage_readiness_report

    report = create_boundary_coverage_readiness_report()

    for flag in REQUIRED_FALSE_FLAGS:
        assert getattr(report, flag) is False
    assert boundary_coverage_readiness_preserves_no_unsafe_runtime(report)
    with pytest.raises(ValueError):
        create_boundary_coverage_readiness_report(ready_for_subagent_invocation=True)


def test_v0407_integrated_restore_snapshot_lists_version_chain_and_open_closed_capabilities() -> None:
    snapshot = create_v0407_integrated_restore_context_snapshot()

    assert len(snapshot.baseline_versions) == 8
    assert set(OPEN_CAPABILITIES).issubset(snapshot.open_capabilities)
    assert set(CLOSED_CAPABILITIES).issubset(snapshot.closed_capabilities)


def test_v0407_restore_packet_uses_single_integrated_doc_path() -> None:
    packet = create_v0407_integrated_restore_packet()

    assert packet.single_integrated_doc_path == INTEGRATED_DOC_PATH
    assert integrated_restore_packet_uses_single_doc(packet)


def test_v0407_restore_packet_marks_separate_restore_doc_created_false() -> None:
    packet = create_v0407_integrated_restore_packet()

    assert packet.separate_restore_doc_created is False
    with pytest.raises(ValueError):
        create_v0407_integrated_restore_packet(separate_restore_doc_created=True)


def test_v0407_integrated_restore_manifest_disallows_separate_restore_doc() -> None:
    manifest = create_v0407_integrated_restore_document_manifest()

    assert manifest.integrated_doc_required is True
    assert manifest.separate_restore_doc_allowed is False
    assert manifest.separate_restore_doc_created is False
    assert manifest.suitable_for_new_session_handoff is True


def test_v0407_integrated_document_exists_and_has_required_restore_sections() -> None:
    text = Path(INTEGRATED_DOC_PATH).read_text(encoding="utf-8")

    for heading in (
        "Restore Purpose",
        "One-Screen Restore Summary",
        "Current Version and Track Identity",
        "Version Chain Summary",
        "v0.40.7 Rehearsal Evidence Matrix Summary",
        "Boundary Coverage Summary",
        "Capability Matrix",
        "Safety Flag Canonical Values",
        "Withdrawal Conditions",
        "v0.40.8 Recommended Next Step",
    ):
        assert heading in text


def test_v0407_integrated_document_contains_copy_paste_restore_prompt() -> None:
    text = Path(INTEGRATED_DOC_PATH).read_text(encoding="utf-8")

    assert "Copy-Paste Restore Prompt for Future GPT/Codex Session" in text
    assert "You are continuing ChantaCore after v0.40.7." in text
    assert "v0.40.8 CLI Execution-Test Preview Surface" in text


def test_v0407_no_separate_v0407_restore_document_created() -> None:
    assert not Path("docs/versions/v0.40/v0.40.7_restore_document.md").exists()


def test_v0407_no_separate_v0407_release_document_created() -> None:
    assert not Path("docs/versions/v0.40/v0.40.7_rehearsal_evidence_matrix.md").exists()
    assert not Path("docs/versions/v0.40/v0.40.7_boundary_coverage.md").exists()


def test_v0407_v0408_handoff_targets_cli_execution_test_preview_surface() -> None:
    handoff = create_v0408_cli_execution_test_preview_surface_handoff()

    assert handoff.target_version == "v0.40.8 CLI Execution-Test Preview Surface"
    assert "preview-only CLI surface" in handoff.recommended_focus
    assert "no standalone runtime" in handoff.recommended_focus


def test_v0407_v041_acceleration_signal_is_non_authoritative() -> None:
    signal = create_v041_smoke_run_acceleration_coverage_signal()

    assert signal.conservative_target == "v0.41.6"
    assert signal.earliest_candidate_target == "v0.41.6"
    assert v041_coverage_signal_is_not_runtime_start(signal)


def test_v0407_boundary_matrix_to_gap_register_to_safety_report_flow() -> None:
    from chanta_core.agent_runtime.repair_mission_loop_evidence_matrix import create_boundary_coverage_safety_report

    matrix = build_rehearsal_evidence_matrix()
    gap_register = build_boundary_coverage_gap_register()
    safety_report = create_boundary_coverage_safety_report(matrix)

    assert matrix.coverage_complete is True
    assert gap_register.coverage_can_complete is True
    assert safety_report.safe_for_v0407_coverage_consolidation is True
    assert safety_report.safe_for_runtime_execution is False


def test_v0407_restore_coverage_to_integrated_restore_packet_flow() -> None:
    restore = create_restore_coverage_record()
    packet = create_v0407_integrated_restore_packet()

    assert restore.copy_paste_restore_prompt_exists is True
    assert packet.single_integrated_doc_path == INTEGRATED_DOC_PATH


def test_v0407_missing_required_boundary_evidence_increases_missing_evidence_count() -> None:
    row = create_rehearsal_evidence_matrix_row(
        row_id="v0400_mission_loop_boundary",
        coverage_status=CoverageStatus.MISSING.value,
        missing_evidence=("test_artifact",),
    )
    matrix = build_rehearsal_evidence_matrix(rows=(row,), coverage_complete=False, missing_evidence_count=10)

    assert matrix.coverage_complete is False
    assert matrix.missing_evidence_count == 10


def test_v0407_false_runtime_readiness_gap_blocks_coverage_completion() -> None:
    gap = create_boundary_coverage_gap(
        gap_id="ready-for-subagent-runtime-gap",
        gap_kind="blocking_gap",
        description="unsafe runtime readiness true",
        blocking=True,
    )
    register = build_boundary_coverage_gap_register((gap,))

    assert register.coverage_can_complete is False


def test_v0407_no_forbidden_runtime_call_patterns() -> None:
    source = Path("src/chanta_core/agent_runtime/repair_mission_loop_evidence_matrix.py").read_text(encoding="utf-8")
    forbidden_runtime_patterns = [
        r"\bsubprocess\b",
        r"shell=True",
        r"os\.system",
        r"\beval\(",
        r"\bexec\(",
        r"\brequests\b",
        r"\bhttpx\b",
        r"\burllib\b",
        r"\bsocket\b",
        r"\bopenai\b",
        r"\banthropic\b",
        r"\bollama\b",
        r"\blmstudio\b",
        r"apply_patch",
        r"git apply",
        r"git worktree",
        r"api_key",
        r"\bsecret\b",
        r"invoke_subagent",
        r"run_subagent",
        r"create_child_session",
        r"spawn_agent",
        r"prompt_submit",
        r"provider_invoke",
        r"client_create",
    ]

    for pattern in forbidden_runtime_patterns:
        assert re.search(pattern, source) is None
    metadata_hits = [
        line
        for line in source.splitlines()
        if "credential" in line.lower() or "child_session" in line.lower() or "provider_client" in line.lower()
    ]
    assert metadata_hits
    assert all(
        (
            "credential" in line.lower()
            or "child_session" in line.lower()
            or "provider_client" in line.lower()
        )
        for line in metadata_hits
    )
