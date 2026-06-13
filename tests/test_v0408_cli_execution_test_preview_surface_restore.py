from __future__ import annotations

import re
from pathlib import Path

import pytest

from chanta_core.agent_runtime.repair_mission_loop_cli_preview_surface import (
    CLOSED_CAPABILITIES,
    INTEGRATED_DOC_PATH,
    OPEN_CAPABILITIES,
    PREVIEW_COMMAND_KINDS,
    REQUIRED_FALSE_FLAGS,
    UNSUPPORTED_COMMAND_KINDS,
    CLIPreviewCommandKind,
    CLIPreviewCommandStatus,
    CLIPreviewFalseClaimKind,
    CLIPreviewSurfaceKind,
    audit_cli_preview_false_claim,
    cli_preview_command_spec_preserves_no_execution,
    cli_preview_result_preserves_no_execution,
    cli_preview_surface_is_preview_only,
    cli_readiness_preserves_no_unsafe_runtime,
    create_cli_execution_test_preview_surface,
    create_cli_preview_command_input,
    create_cli_preview_command_spec,
    create_cli_preview_surface_readiness_report,
    create_cli_preview_surface_safety_report,
    create_cli_read_only_view_contract,
    create_cli_unsupported_command_decision,
    create_v0408_integrated_restore_context_snapshot,
    create_v0408_integrated_restore_document_manifest,
    create_v0408_integrated_restore_packet,
    create_v0409_consolidation_handoff,
    create_v041_smoke_run_acceleration_cli_signal,
    integrated_restore_packet_uses_single_doc,
    render_cli_boundary_coverage_preview_view,
    render_cli_checkpoint_preview_view,
    render_cli_denied_action_preview_view,
    render_cli_evidence_matrix_preview_view,
    render_cli_preview_command,
    render_cli_provider_prompt_preview_view,
    render_cli_restore_summary_preview_view,
    render_cli_status_preview_view,
    render_cli_unsafe_flag_preview_view,
    render_cli_v041_readiness_preview_view,
    render_cli_verifier_subagent_preview_view,
    v041_cli_signal_is_not_runtime_start,
)


def test_v0408_cli_preview_surface_kinds_declared() -> None:
    assert {item.value for item in CLIPreviewSurfaceKind} == {
        "status_preview",
        "evidence_matrix_preview",
        "boundary_coverage_preview",
        "denied_action_preview",
        "checkpoint_preview",
        "provider_prompt_preview",
        "verifier_subagent_preview",
        "restore_summary_preview",
        "v041_readiness_preview",
        "unsafe_flag_preview",
        "unsupported_command_preview",
    }


def test_v0408_cli_preview_command_kinds_declared() -> None:
    values = {item.value for item in CLIPreviewCommandKind}

    assert set(PREVIEW_COMMAND_KINDS).issubset(values)
    assert set(UNSUPPORTED_COMMAND_KINDS).issubset(values)


def test_v0408_cli_preview_command_status_values_declared() -> None:
    assert {item.value for item in CLIPreviewCommandStatus} == {
        "preview_only",
        "rendered",
        "blocked",
        "unsupported",
        "unsafe_denied",
        "metadata_only",
        "not_executed",
    }


def test_v0408_command_spec_is_preview_read_only_metadata_only() -> None:
    spec = create_cli_preview_command_spec()

    assert spec.preview_only is True
    assert spec.read_only is True
    assert spec.metadata_only is True
    assert cli_preview_command_spec_preserves_no_execution(spec)


def test_v0408_command_spec_never_grants_execution_prompt_provider_subagent_network_or_credentials() -> None:
    spec = create_cli_preview_command_spec()

    assert spec.execution_allowed is False
    assert spec.mutates_workspace is False
    assert spec.submits_prompt is False
    assert spec.invokes_provider is False
    assert spec.invokes_subagent is False
    assert spec.creates_child_session is False
    assert spec.uses_network is False
    assert spec.accesses_credentials is False
    with pytest.raises(ValueError):
        create_cli_preview_command_spec(execution_allowed=True)


def test_v0408_command_input_is_metadata_only() -> None:
    command_input = create_cli_preview_command_input(requested_execution=True)

    assert command_input.metadata_only is True
    assert command_input.requested_execution is True


def test_v0408_command_result_never_executes_or_mutates() -> None:
    result = render_cli_preview_command()

    assert result.status == "rendered"
    assert cli_preview_result_preserves_no_execution(result)


def test_v0408_read_only_view_contract_blocks_execution_mutation_prompt_provider_subagent_child_network_credentials() -> None:
    contract = create_cli_read_only_view_contract()

    assert contract.view_only is True
    assert contract.no_execution is True
    assert contract.no_workspace_mutation is True
    assert contract.no_prompt_submission is True
    assert contract.no_provider_invocation is True
    assert contract.no_subagent_invocation is True
    assert contract.no_child_session_creation is True
    assert contract.no_network is True
    assert contract.no_credentials is True


def test_v0408_preview_surface_contains_required_view_commands() -> None:
    surface = create_cli_execution_test_preview_surface()
    kinds = {spec.command_kind for spec in surface.command_specs}

    assert kinds == set(PREVIEW_COMMAND_KINDS)
    assert cli_preview_surface_is_preview_only(surface)


def test_v0408_preview_surface_does_not_include_executable_apply_retest_test_prompt_provider_or_subagent_commands() -> None:
    surface = create_cli_execution_test_preview_surface()
    kinds = {spec.command_kind for spec in surface.command_specs}

    assert not set(UNSUPPORTED_COMMAND_KINDS).intersection(kinds)
    assert all(spec.execution_allowed is False for spec in surface.command_specs)


def test_v0408_status_preview_summarizes_version_track_closed_runtime_and_handoff() -> None:
    view = render_cli_status_preview_view()

    assert "v0.40.8" in view.current_version
    assert view.closed_runtime_capabilities
    assert view.next_version_handoff.startswith("v0.40.9")
    assert view.standalone_runtime_status == "closed"


def test_v0408_evidence_matrix_preview_summarizes_rows_missing_evidence_and_unsafe_gaps() -> None:
    view = render_cli_evidence_matrix_preview_view()

    assert view.matrix_row_count >= 10
    assert view.missing_evidence_count == 0
    assert view.unsafe_gap_count == 0


def test_v0408_boundary_coverage_preview_summarizes_all_required_boundaries() -> None:
    view = render_cli_boundary_coverage_preview_view()

    for boundary in (
        "mission_loop_boundary",
        "sandbox_rehearsal_boundary",
        "checkpoint_boundary",
        "negative_gate_boundary",
        "provider_prompt_boundary",
        "verifier_subagent_boundary",
        "restore_boundary",
        "standalone_runtime_closed_boundary",
    ):
        assert boundary in view.covered_boundaries


def test_v0408_denied_action_preview_summarizes_denied_actions_without_authority() -> None:
    view = render_cli_denied_action_preview_view()

    assert view.denied_actions
    assert view.decision_status == "blocked"
    assert view.runtime_authority_granted is False


def test_v0408_checkpoint_preview_summarizes_checkpoint_controls() -> None:
    view = render_cli_checkpoint_preview_view()

    assert view.checkpoint_required is True
    assert view.stale_checkpoint_invalid is True
    assert view.broad_approval_rejected is True
    assert view.approval_grants_runtime_authority is False


def test_v0408_provider_prompt_preview_summarizes_submission_provider_network_credential_blocks() -> None:
    view = render_cli_provider_prompt_preview_view()

    assert view.prompt_submission_blocked is True
    assert view.provider_invocation_blocked is True
    assert view.network_blocked is True
    assert view.credential_blocked is True
    assert view.provider_client_creation_blocked is True


def test_v0408_verifier_subagent_preview_summarizes_subagent_child_context_blocks() -> None:
    view = render_cli_verifier_subagent_preview_view()

    assert view.verifier_request_draft_only is True
    assert view.subagent_invocation_blocked is True
    assert view.child_session_creation_blocked is True
    assert view.parent_raw_transcript_sharing_blocked is True


def test_v0408_restore_summary_preview_contains_integrated_doc_path_and_copy_paste_prompt_presence() -> None:
    view = render_cli_restore_summary_preview_view()

    assert view.integrated_doc_path == INTEGRATED_DOC_PATH
    assert view.copy_paste_restore_prompt_present is True
    assert view.next_handoff.startswith("v0.40.9")


def test_v0408_v041_readiness_preview_is_non_authoritative() -> None:
    view = render_cli_v041_readiness_preview_view()

    assert view.conservative_smoke_target == "v0.41.6"
    assert view.claims_standalone_runtime_ready is False


def test_v0408_unsafe_flag_preview_keeps_unsafe_flags_false() -> None:
    view = render_cli_unsafe_flag_preview_view()

    assert view.all_unsafe_flags_false is True
    for flag in REQUIRED_FALSE_FLAGS:
        assert view.unsafe_flags[flag] is False


def test_v0408_unsupported_apply_command_is_denied() -> None:
    decision = create_cli_unsupported_command_decision(CLIPreviewCommandKind.APPLY.value)

    assert decision.blocked is True
    assert decision.executed is False


def test_v0408_unsupported_retest_command_is_denied() -> None:
    assert create_cli_unsupported_command_decision(CLIPreviewCommandKind.RETEST.value).blocked is True


def test_v0408_unsupported_run_tests_command_is_denied() -> None:
    assert create_cli_unsupported_command_decision(CLIPreviewCommandKind.RUN_TESTS.value).blocked is True


def test_v0408_unsupported_submit_prompt_provider_subagent_child_session_commands_are_denied() -> None:
    for kind in (
        CLIPreviewCommandKind.SUBMIT_PROMPT.value,
        CLIPreviewCommandKind.INVOKE_PROVIDER.value,
        CLIPreviewCommandKind.INVOKE_SUBAGENT.value,
        CLIPreviewCommandKind.CREATE_CHILD_SESSION.value,
    ):
        decision = create_cli_unsupported_command_decision(kind)
        assert decision.blocked is True
        assert decision.executed is False
        assert decision.safe_alternative


def test_v0408_unsupported_dominion_and_production_commands_are_denied() -> None:
    assert create_cli_unsupported_command_decision(CLIPreviewCommandKind.DOMINION_RUNTIME.value).blocked is True
    assert create_cli_unsupported_command_decision(CLIPreviewCommandKind.PRODUCTION_CERTIFY.value).blocked is True


def test_v0408_false_cli_execution_ready_claim_is_blocked() -> None:
    audit = audit_cli_preview_false_claim(CLIPreviewFalseClaimKind.CLI_EXECUTION_READY.value)

    assert audit.claim_allowed is False
    assert audit.readiness_flag_modified is False


def test_v0408_false_apply_retest_prompt_provider_subagent_claims_are_blocked() -> None:
    for kind in (
        CLIPreviewFalseClaimKind.APPLY_COMMAND_READY.value,
        CLIPreviewFalseClaimKind.RETEST_COMMAND_READY.value,
        CLIPreviewFalseClaimKind.PROMPT_SUBMISSION_READY.value,
        CLIPreviewFalseClaimKind.PROVIDER_INVOCATION_READY.value,
        CLIPreviewFalseClaimKind.SUBAGENT_INVOCATION_READY.value,
    ):
        assert audit_cli_preview_false_claim(kind).claim_allowed is False


def test_v0408_false_standalone_dominion_and_production_claims_are_blocked() -> None:
    for kind in (
        CLIPreviewFalseClaimKind.STANDALONE_DEFAULT_PERSONAL_RUNTIME_READY.value,
        CLIPreviewFalseClaimKind.DOMINION_RUNTIME_READY.value,
        CLIPreviewFalseClaimKind.PRODUCTION_CERTIFIED.value,
    ):
        assert audit_cli_preview_false_claim(kind).claim_allowed is False


def test_v0408_safety_report_keeps_cli_execution_and_runtime_false() -> None:
    report = create_cli_preview_surface_safety_report()

    assert report.safe_for_v0408_cli_preview_surface is True
    assert report.safe_for_cli_runtime_execution is False
    assert report.safe_for_apply_command is False
    assert report.safe_for_retest_command is False
    assert report.safe_for_test_execution is False
    assert report.safe_for_prompt_submission is False
    assert report.safe_for_model_provider_invocation is False
    assert report.safe_for_subagent_invocation is False
    assert report.production_certified is False


def test_v0408_readiness_report_keeps_unsafe_flags_false() -> None:
    report = create_cli_preview_surface_readiness_report()

    assert report.cli_preview_surface_defined is True
    for flag in REQUIRED_FALSE_FLAGS:
        assert getattr(report, flag) is False
    assert cli_readiness_preserves_no_unsafe_runtime(report)
    with pytest.raises(ValueError):
        create_cli_preview_surface_readiness_report(ready_for_cli_runtime_execution=True)


def test_v0408_integrated_restore_snapshot_lists_version_chain_and_open_closed_capabilities() -> None:
    snapshot = create_v0408_integrated_restore_context_snapshot()

    assert len(snapshot.baseline_versions) == 9
    assert set(OPEN_CAPABILITIES).issubset(snapshot.open_capabilities)
    assert set(CLOSED_CAPABILITIES).issubset(snapshot.closed_capabilities)


def test_v0408_restore_packet_uses_single_integrated_doc_path() -> None:
    packet = create_v0408_integrated_restore_packet()

    assert packet.single_integrated_doc_path == INTEGRATED_DOC_PATH
    assert integrated_restore_packet_uses_single_doc(packet)


def test_v0408_restore_packet_marks_separate_restore_doc_created_false() -> None:
    packet = create_v0408_integrated_restore_packet()

    assert packet.separate_restore_doc_created is False
    with pytest.raises(ValueError):
        create_v0408_integrated_restore_packet(separate_restore_doc_created=True)


def test_v0408_integrated_restore_manifest_disallows_separate_restore_doc() -> None:
    manifest = create_v0408_integrated_restore_document_manifest()

    assert manifest.integrated_doc_required is True
    assert manifest.separate_restore_doc_allowed is False
    assert manifest.separate_restore_doc_created is False
    assert manifest.suitable_for_new_session_handoff is True


def test_v0408_integrated_document_exists_and_has_required_restore_sections() -> None:
    text = Path(INTEGRATED_DOC_PATH).read_text(encoding="utf-8")

    for heading in (
        "Restore Purpose",
        "One-Screen Restore Summary",
        "Current Version and Track Identity",
        "Version Chain Summary",
        "v0.40.8 CLI Preview Surface Summary",
        "Preview Command Catalog",
        "Unsupported Command Policy",
        "Read-Only View Contract",
        "Capability Matrix",
        "Safety Flag Canonical Values",
        "Withdrawal Conditions",
        "v0.40.9 Recommended Next Step",
    ):
        assert heading in text


def test_v0408_integrated_document_contains_copy_paste_restore_prompt() -> None:
    text = Path(INTEGRATED_DOC_PATH).read_text(encoding="utf-8")

    assert "Copy-Paste Restore Prompt for Future GPT/Codex Session" in text
    assert "You are continuing ChantaCore after v0.40.8." in text
    assert "v0.40.9 Controlled Mission Loop Preparation Consolidation & v0.41 Default Personal Runtime Handoff" in text


def test_v0408_no_separate_v0408_restore_document_created() -> None:
    assert not Path("docs/versions/v0.40/v0.40.8_restore_document.md").exists()


def test_v0408_no_separate_v0408_release_document_created() -> None:
    assert not Path("docs/versions/v0.40/v0.40.8_cli_execution_test_preview_surface.md").exists()
    assert not Path("docs/versions/v0.40/v0.40.8_cli_preview_coverage.md").exists()


def test_v0408_v0409_handoff_targets_consolidation_and_v041_handoff() -> None:
    handoff = create_v0409_consolidation_handoff()

    assert handoff.target_version == "v0.40.9 Controlled Mission Loop Preparation Consolidation & v0.41 Default Personal Runtime Handoff"
    assert "prepare v0.41.0 Default Personal Profile Runtime" in handoff.recommended_focus


def test_v0408_v041_acceleration_signal_is_non_authoritative() -> None:
    signal = create_v041_smoke_run_acceleration_cli_signal()

    assert signal.conservative_target == "v0.41.6"
    assert signal.earliest_candidate_target == "v0.41.6"
    assert v041_cli_signal_is_not_runtime_start(signal)


def test_v0408_preview_command_to_rendered_result_flow_never_executes() -> None:
    command_input = create_cli_preview_command_input(CLIPreviewCommandKind.EVIDENCE_MATRIX_PREVIEW.value)
    result = render_cli_preview_command(command_input)

    assert result.status == "rendered"
    assert cli_preview_result_preserves_no_execution(result)


def test_v0408_unsupported_command_to_denied_decision_flow() -> None:
    command_input = create_cli_preview_command_input(CLIPreviewCommandKind.APPLY.value, requested_execution=True)
    result = render_cli_preview_command(command_input)

    assert result.status == "unsafe_denied"
    assert result.executed is False


def test_v0408_preview_surface_to_restore_packet_flow() -> None:
    surface = create_cli_execution_test_preview_surface()
    packet = create_v0408_integrated_restore_packet()

    assert cli_preview_surface_is_preview_only(surface)
    assert packet.single_integrated_doc_path == INTEGRATED_DOC_PATH


def test_v0408_v041_readiness_preview_does_not_claim_standalone_runtime_ready() -> None:
    view = render_cli_v041_readiness_preview_view()

    assert view.claims_standalone_runtime_ready is False


def test_v0408_no_forbidden_runtime_call_patterns() -> None:
    source = Path("src/chanta_core/agent_runtime/repair_mission_loop_cli_preview_surface.py").read_text(encoding="utf-8")
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
        r"run_subagent",
        r"spawn_agent",
        r"pytest",
        r"unittest",
        r"os\.remove",
        r"Path\.write_text",
        r"\bopen\(",
    ]

    for pattern in forbidden_runtime_patterns:
        assert re.search(pattern, source) is None
    metadata_hits = [
        line
        for line in source.splitlines()
        if "credential" in line.lower()
        or "create_child_session" in line.lower()
        or "invoke_subagent" in line.lower()
        or "prompt_submit" in line.lower()
        or "provider_invoke" in line.lower()
        or "client_create" in line.lower()
    ]
    assert metadata_hits
    assert all(
        (
            "credential" in line.lower()
            or "create_child_session" in line.lower()
            or "invoke_subagent" in line.lower()
            or "prompt_submit" in line.lower()
            or "provider_invoke" in line.lower()
            or "client_create" in line.lower()
        )
        for line in metadata_hits
    )
