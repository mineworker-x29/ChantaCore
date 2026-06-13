from __future__ import annotations

import pytest

from chanta_core.agent_runtime.repair_loop_consolidation import (
    LoopEngineeringPINativeConsolidationRecord,
    RepairLoopAuditTrail,
    RepairLoopBoundaryRegister,
    RepairLoopCapabilityMatrix,
    RepairLoopConsolidationFlagSet,
    RepairLoopConsolidationReadinessLevel,
    RepairLoopConsolidationSourceKind,
    RepairLoopConsolidationStatus,
    RepairLoopGapRegister,
    RepairLoopNoUnsafeExpansionGuarantee,
    RepairLoopReleaseManifest,
    RepairLoopRiskRegister,
    RepairLoopStageConsolidationRecord,
    RepairLoopStageCoverage,
    RepairLoopTrackSnapshot,
    V039ConsolidationReport,
    V040HandoffPacket,
    build_loop_engineering_pi_native_consolidation_record,
    build_repair_loop_audit_trail,
    build_repair_loop_boundary_register,
    build_repair_loop_capability_matrix,
    build_repair_loop_consolidation_flags,
    build_repair_loop_consolidation_validation_report,
    build_repair_loop_gap_register,
    build_repair_loop_no_unsafe_expansion_guarantee,
    build_repair_loop_release_manifest,
    build_repair_loop_risk_register,
    build_repair_loop_stage_consolidation_record,
    build_repair_loop_stage_coverage,
    build_repair_loop_track_snapshot,
    build_v039_consolidation_report,
    build_v040_handoff_packet,
    default_v039_included_versions,
    default_v039_stage_plan,
    default_v040_handoff_plan,
    loop_engineering_record_is_pi_native_absorption,
    repair_loop_audit_confirms_no_unsafe_runtime,
    repair_loop_capability_matrix_is_not_permission_grant,
    repair_loop_consolidation_flags_preserve_no_unsafe_runtime,
    v039_consolidation_report_is_not_execution_ready,
    v040_handoff_packet_is_design_only,
)


def test_v0399_enum_values() -> None:
    assert [item.value for item in RepairLoopConsolidationStatus] == [
        "unknown",
        "draft",
        "consolidated",
        "consolidated_with_warnings",
        "consolidated_with_gaps",
        "handoff_ready_for_v040",
        "blocked",
        "rejected",
        "review_required",
        "no_op",
        "safe_failed",
    ]
    assert [item.value for item in RepairLoopConsolidationReadinessLevel] == [
        "not_ready",
        "boundary_foundation_ready",
        "approval_workspace_apply_ready",
        "retest_comparison_ready",
        "process_state_self_prompting_ready",
        "cli_surface_ready",
        "human_approved_sandbox_repair_apply_loop_v1_ready",
        "design_handoff_ready_for_v040",
        "blocked",
        "future_track",
    ]
    assert [item.value for item in RepairLoopConsolidationSourceKind] == [
        "v0398_cli_loop_surface_report",
        "v0398_loop_bundle_view",
        "v0398_handoff_packet",
        "v0397_self_prompting_report",
        "v0397_draft_packet",
        "v0396_process_state_reconstruction_report",
        "v0395_outcome_comparison_report",
        "v0394_post_apply_retest_result",
        "v0393_sandbox_apply_result",
        "v0392_workspace_isolation_decision",
        "v0391_approval_artifact_decision",
        "v0390_apply_boundary_report",
        "v0389_repair_proposal_consolidation_report",
        "loop_engineering_pi_native_note",
        "manual_operator_note",
        "test_fixture",
        "unknown",
    ]


def test_flags_allow_bounded_v039_and_design_handoff_only() -> None:
    flags = build_repair_loop_consolidation_flags()

    assert isinstance(flags, RepairLoopConsolidationFlagSet)
    assert flags.v039_loop_consolidation_layer_constructed is True
    assert flags.human_approved_sandbox_repair_apply_loop_v1_ready is True
    assert flags.ready_for_v040_handoff is True
    assert flags.ready_for_v040_controlled_multi_iteration_loop_boundary_input is True
    assert flags.ready_for_v040_subagent_verification_boundary_input is True
    assert flags.ready_for_v040_model_provider_boundary_input is True
    assert flags.ready_for_v0390_apply_boundary is True
    assert flags.ready_for_v0391_approval_artifact_gate is True
    assert flags.ready_for_v0392_workspace_isolation_contract is True
    assert flags.ready_for_v0393_bounded_sandbox_patch_materialization is True
    assert flags.ready_for_v0393_bounded_sandbox_apply is True
    assert flags.ready_for_v0394_controlled_post_apply_retest is True
    assert flags.ready_for_v0395_before_after_comparison is True
    assert flags.ready_for_v0396_process_state_reconstruction_metadata is True
    assert flags.ready_for_v0397_self_prompting_draft_contract is True
    assert flags.ready_for_v0398_cli_loop_state_surface is True
    assert flags.ready_for_agent_to_subagent_prompt_draft is True
    assert flags.ready_for_cli_preview_surface is True
    assert repair_loop_consolidation_flags_preserve_no_unsafe_runtime(flags)

    assert flags.ready_for_execution is False
    assert flags.ready_for_general_execution is False
    assert flags.ready_for_live_workspace_apply is False
    assert flags.ready_for_approval_less_apply is False
    assert flags.ready_for_prompt_submission_to_model is False
    assert flags.ready_for_model_provider_invocation is False
    assert flags.ready_for_self_prompt_execution is False
    assert flags.ready_for_next_action_execution is False
    assert flags.ready_for_subagent_invocation is False
    assert flags.ready_for_external_agent_execution is False
    assert flags.ready_for_autonomous_loop_runtime is False
    assert flags.ready_for_retry_loop is False
    assert flags.ready_for_multi_cycle_loop is False
    assert flags.ready_for_dominion_runtime is False
    assert flags.ready_for_persistent_trace_write is False
    assert flags.production_certified is False


@pytest.mark.parametrize(
    "field_name",
    [
        "ready_for_execution",
        "ready_for_general_execution",
        "ready_for_live_workspace_apply",
        "ready_for_approval_less_apply",
        "ready_for_unbounded_workspace_mutation",
        "ready_for_prompt_submission_to_model",
        "ready_for_model_provider_invocation",
        "ready_for_self_prompt_execution",
        "ready_for_next_action_execution",
        "ready_for_subagent_invocation",
        "ready_for_external_agent_execution",
        "ready_for_autonomous_loop_runtime",
        "ready_for_retry_loop",
        "ready_for_multi_cycle_loop",
        "ready_for_dominion_runtime",
        "ready_for_persistent_trace_write",
        "production_certified",
    ],
)
def test_flags_reject_unsafe_true(field_name: str) -> None:
    with pytest.raises(ValueError):
        build_repair_loop_consolidation_flags(**{field_name: True})


def test_snapshot_manifest_and_stage_plan_include_v0390_through_v0398() -> None:
    versions = default_v039_included_versions()
    snapshot = build_repair_loop_track_snapshot()
    manifest = build_repair_loop_release_manifest()
    stage_plan = default_v039_stage_plan()

    assert versions == [
        "v0.39.0",
        "v0.39.1",
        "v0.39.2",
        "v0.39.3",
        "v0.39.4",
        "v0.39.5",
        "v0.39.6",
        "v0.39.7",
        "v0.39.8",
    ]
    assert isinstance(snapshot, RepairLoopTrackSnapshot)
    assert all(version in snapshot.included_versions for version in versions)
    assert snapshot.release_flags.production_certified is False
    assert "production certification" in " ".join(snapshot.blocked_capabilities)
    assert isinstance(manifest, RepairLoopReleaseManifest)
    assert all(version in manifest.included_versions for version in versions)
    assert manifest.release_flags.ready_for_execution is False
    assert manifest.focused_test_command
    assert manifest.full_track_test_command
    assert len(stage_plan) == 9


def test_snapshot_rejects_missing_stage_version() -> None:
    with pytest.raises(ValueError):
        build_repair_loop_track_snapshot(included_versions=["v0.39.0"])


def test_capability_matrix_classifies_capabilities_without_permission_grant() -> None:
    matrix = build_repair_loop_capability_matrix()

    assert isinstance(matrix, RepairLoopCapabilityMatrix)
    assert any("sandbox" in cap.lower() and "apply" in cap.lower() for cap in matrix.enabled_bounded_capabilities)
    assert any("controlled post-apply re-test" in cap for cap in matrix.enabled_bounded_capabilities)
    assert any("CLI" in cap and "preview" in cap for cap in matrix.preview_only_capabilities)
    assert any("process-state" in cap.lower() for cap in matrix.metadata_only_capabilities)
    assert any("self-prompt" in cap.lower() for cap in matrix.metadata_only_capabilities)
    assert any("live apply" in cap for cap in matrix.blocked_capabilities)
    assert any("prompt execution" in cap for cap in matrix.blocked_capabilities)
    assert any("model invocation" in cap for cap in matrix.blocked_capabilities)
    assert any("subagent invocation" in cap for cap in matrix.blocked_capabilities)
    assert any("autonomous loop" in cap for cap in matrix.blocked_capabilities)
    assert any("Dominion" in cap for cap in matrix.blocked_capabilities)
    assert any("production certification" in cap for cap in matrix.blocked_capabilities)
    assert repair_loop_capability_matrix_is_not_permission_grant(matrix)


def test_stage_coverage_records_and_blocking_gap_rule() -> None:
    coverages = [build_repair_loop_stage_coverage(stage_version=version) for version in default_v039_included_versions()]

    assert len(coverages) == 9
    assert all(isinstance(item, RepairLoopStageCoverage) for item in coverages)
    assert all(item.coverage_complete is True for item in coverages)
    with pytest.raises(ValueError):
        build_repair_loop_stage_coverage(blocking_gaps=["missing"], coverage_complete=True)
    incomplete = build_repair_loop_stage_coverage(blocking_gaps=["missing"], coverage_complete=False)
    assert incomplete.coverage_complete is False


def test_boundary_risk_and_gap_registers_capture_limits() -> None:
    boundary = build_repair_loop_boundary_register()
    risk = build_repair_loop_risk_register()
    gap = build_repair_loop_gap_register()

    assert isinstance(boundary, RepairLoopBoundaryRegister)
    assert any("sandbox-only apply" in item for item in boundary.active_bounded_runtime_boundaries)
    assert any("controlled post-apply re-test" in item for item in boundary.active_bounded_runtime_boundaries)
    assert any("live apply" in item for item in boundary.prohibited_boundaries)
    assert any("prompt execution" in item for item in boundary.prohibited_boundaries)
    assert any("subagent invocation" in item for item in boundary.prohibited_boundaries)
    assert any("Dominion" in item for item in boundary.prohibited_boundaries)

    assert isinstance(risk, RepairLoopRiskRegister)
    assert any("approval confusion" in item for item in risk.known_risks)
    assert any("sandbox/live confusion" in item for item in risk.known_risks)
    assert any("prompt execution confusion" in item for item in risk.known_risks)
    assert any("subagent invocation confusion" in item for item in risk.known_risks)
    assert any("autonomous loop risk" in item for item in risk.known_risks)
    assert any("production certification confusion" in item for item in risk.known_risks)

    assert isinstance(gap, RepairLoopGapRegister)
    assert any("controlled multi-iteration boundary" in item for item in gap.recommended_v040_items)
    assert any("verifier subagent boundary" in item for item in gap.recommended_v040_items)
    assert any("model/provider boundary" in item for item in gap.recommended_v040_items)
    assert any("loop budget gate" in item for item in gap.recommended_v040_items)
    assert any("stop-condition contract" in item for item in gap.recommended_v040_items)
    assert any("human checkpoint gate" in item for item in gap.recommended_v040_items)


def test_audit_trail_confirms_no_unsafe_runtime_and_pi_native_absorption() -> None:
    audit = build_repair_loop_audit_trail()

    assert isinstance(audit, RepairLoopAuditTrail)
    assert audit.no_live_apply_confirmed is True
    assert audit.no_approval_less_apply_confirmed is True
    assert audit.bounded_sandbox_apply_only_confirmed is True
    assert audit.controlled_retest_only_confirmed is True
    assert audit.no_arbitrary_command_confirmed is True
    assert audit.no_shell_confirmed is True
    assert audit.no_raw_subprocess_confirmed is True
    assert audit.no_prompt_submission_confirmed is True
    assert audit.no_model_invocation_confirmed is True
    assert audit.no_prompt_execution_confirmed is True
    assert audit.no_next_action_execution_confirmed is True
    assert audit.no_subagent_invocation_confirmed is True
    assert audit.no_external_agent_confirmed is True
    assert audit.no_autonomous_loop_confirmed is True
    assert audit.no_retry_loop_confirmed is True
    assert audit.no_multi_cycle_loop_confirmed is True
    assert audit.no_dominion_runtime_confirmed is True
    assert audit.no_persistent_trace_write_confirmed is True
    assert audit.no_production_certification_confirmed is True
    assert audit.human_handoff_required_confirmed is True
    assert audit.loop_engineering_absorbed_as_pi_native_confirmed is True
    assert audit.unsafe_readiness_flags_false_confirmed is True
    assert repair_loop_audit_confirms_no_unsafe_runtime(audit)


@pytest.mark.parametrize(
    "field_name",
    [
        "no_live_apply_confirmed",
        "no_approval_less_apply_confirmed",
        "no_shell_confirmed",
        "no_model_invocation_confirmed",
        "no_subagent_invocation_confirmed",
        "no_autonomous_loop_confirmed",
        "no_production_certification_confirmed",
        "unsafe_readiness_flags_false_confirmed",
    ],
)
def test_audit_trail_rejects_false_confirmations(field_name: str) -> None:
    with pytest.raises(ValueError):
        build_repair_loop_audit_trail(**{field_name: False})


def test_stage_records_exist_for_all_v039_stages() -> None:
    records = [build_repair_loop_stage_consolidation_record(stage_version=version) for version in default_v039_included_versions()]

    assert len(records) == 9
    assert all(isinstance(record, RepairLoopStageConsolidationRecord) for record in records)
    assert {record.stage_version for record in records} == set(default_v039_included_versions())
    assert all(record.confirmation_booleans["metadata_only_consolidation"] is True for record in records)


def test_loop_engineering_record_is_pi_native_absorption_only() -> None:
    record = build_loop_engineering_pi_native_consolidation_record()

    assert isinstance(record, LoopEngineeringPINativeConsolidationRecord)
    assert record.external_term == "Loop Engineering"
    assert record.adopted_as_top_level_concept is False
    assert "Self-Prompting Mission Loop" in record.pi_native_terms
    assert "Process-State-Driven Self-Prompting" in record.pi_native_terms
    assert any("system/loop prompts" in item for item in record.absorbed_patterns)
    assert any("worktree/parallel isolation" in item for item in record.absorbed_patterns)
    assert any("maker/checker" in item for item in record.absorbed_patterns)
    assert any("control panel" in item for item in record.absorbed_patterns)
    assert any("unrestricted autonomous loop" in item for item in record.rejected_patterns)
    assert record.human_handoff_required is True
    assert record.autonomous_loop_opened is False
    assert record.subagent_invocation_opened is False
    assert record.prompt_execution_opened is False
    assert record.model_invocation_opened is False
    assert loop_engineering_record_is_pi_native_absorption(record)


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        ("adopted_as_top_level_concept", True),
        ("autonomous_loop_opened", True),
        ("subagent_invocation_opened", True),
        ("prompt_execution_opened", True),
        ("model_invocation_opened", True),
    ],
)
def test_loop_engineering_record_rejects_runtime_or_top_level_adoption(field_name: str, value: bool) -> None:
    with pytest.raises(ValueError):
        build_loop_engineering_pi_native_consolidation_record(**{field_name: value})


def test_v040_handoff_packet_is_design_only() -> None:
    packet = build_v040_handoff_packet()

    assert isinstance(packet, V040HandoffPacket)
    assert "Controlled Multi-Iteration Mission Loop & Subagent Verification Boundary" in packet.target_track
    assert packet.recommended_next_release == "v0.40.0 Controlled Multi-Iteration Mission Loop Boundary Foundation"
    assert any("max iteration" in item for item in packet.required_loop_safety_gates)
    assert any("stop-condition" in item for item in packet.required_loop_safety_gates)
    assert any("budget" in item for item in packet.required_budget_gates)
    assert any("verifier subagent" in item for item in packet.required_subagent_gates)
    assert any("model/provider" in item for item in packet.required_model_provider_gates)
    assert packet.ready_for_v040_design_handoff is True
    assert packet.ready_for_v040_execution is False
    assert packet.ready_for_autonomous_loop_runtime is False
    assert packet.ready_for_subagent_invocation is False
    assert packet.ready_for_model_provider_invocation is False
    assert packet.ready_for_prompt_execution is False
    assert packet.ready_for_live_apply is False
    assert packet.ready_for_dominion_runtime is False
    assert packet.production_certified is False
    assert v040_handoff_packet_is_design_only(packet)


@pytest.mark.parametrize(
    "field_name",
    [
        "ready_for_v040_execution",
        "ready_for_autonomous_loop_runtime",
        "ready_for_subagent_invocation",
        "ready_for_model_provider_invocation",
        "ready_for_prompt_execution",
        "ready_for_live_apply",
        "ready_for_dominion_runtime",
        "production_certified",
    ],
)
def test_v040_handoff_rejects_execution_flags(field_name: str) -> None:
    with pytest.raises(ValueError):
        build_v040_handoff_packet(**{field_name: True})


def test_v039_consolidation_report_is_v1_ready_but_not_execution_ready() -> None:
    report = build_v039_consolidation_report()

    assert isinstance(report, V039ConsolidationReport)
    assert report.human_approved_sandbox_repair_apply_loop_v1_ready is True
    assert report.ready_for_v040_handoff is True
    assert report.consolidation_status == RepairLoopConsolidationStatus.HANDOFF_READY_FOR_V040
    assert report.readiness_level == RepairLoopConsolidationReadinessLevel.HUMAN_APPROVED_SANDBOX_REPAIR_APPLY_LOOP_V1_READY
    assert len(report.stage_coverages) == 9
    assert len(report.stage_records) == 9
    assert report.production_certified is False
    assert report.ready_for_execution is False
    assert report.ready_for_live_apply is False
    assert report.ready_for_prompt_execution is False
    assert report.ready_for_subagent_invocation is False
    assert report.ready_for_model_provider_invocation is False
    assert report.ready_for_autonomous_loop_runtime is False
    assert report.ready_for_dominion_runtime is False
    assert v039_consolidation_report_is_not_execution_ready(report)


@pytest.mark.parametrize(
    "field_name",
    [
        "ready_for_execution",
        "production_certified",
        "ready_for_live_apply",
        "ready_for_prompt_execution",
        "ready_for_subagent_invocation",
        "ready_for_model_provider_invocation",
        "ready_for_autonomous_loop_runtime",
        "ready_for_dominion_runtime",
    ],
)
def test_v039_consolidation_report_rejects_runtime_flags(field_name: str) -> None:
    with pytest.raises(ValueError):
        build_v039_consolidation_report(**{field_name: True})


def test_validation_report_and_no_unsafe_expansion_guarantee() -> None:
    validation = build_repair_loop_consolidation_validation_report()
    guarantee = build_repair_loop_no_unsafe_expansion_guarantee()

    assert validation.consolidation_only_confirmed is True
    assert validation.no_new_runtime_expansion_confirmed is True
    assert validation.no_runtime_execution_confirmed is True
    assert validation.no_production_certification_confirmed is True

    assert isinstance(guarantee, RepairLoopNoUnsafeExpansionGuarantee)
    assert guarantee.no_runtime_execution is True
    assert guarantee.no_live_apply is True
    assert guarantee.no_approval_less_apply is True
    assert guarantee.no_arbitrary_command is True
    assert guarantee.no_shell is True
    assert guarantee.no_raw_subprocess is True
    assert guarantee.no_prompt_submission is True
    assert guarantee.no_model_invocation is True
    assert guarantee.no_prompt_execution is True
    assert guarantee.no_next_action_execution is True
    assert guarantee.no_subagent_invocation is True
    assert guarantee.no_external_agent is True
    assert guarantee.no_autonomous_loop is True
    assert guarantee.no_retry_loop is True
    assert guarantee.no_multi_cycle_loop is True
    assert guarantee.no_automatic_repair is True
    assert guarantee.no_dominion_runtime is True
    assert guarantee.no_ocel_file_write is True
    assert guarantee.no_ocpx_persistence is True
    assert guarantee.no_persistent_trace_write is True
    assert guarantee.no_production_certification is True


def test_default_v040_handoff_plan_names_expected_boundaries() -> None:
    plan = default_v040_handoff_plan()

    assert any("Controlled Multi-Iteration Mission Loop Boundary" in item for item in plan)
    assert any("max-iteration policy" in item for item in plan)
    assert any("loop stop-condition contract" in item for item in plan)
    assert any("verifier subagent boundary" in item for item in plan)
    assert any("model/provider boundary gate" in item for item in plan)
    assert any("loop budget" in item for item in plan)
    assert any("human checkpoint gate" in item for item in plan)
