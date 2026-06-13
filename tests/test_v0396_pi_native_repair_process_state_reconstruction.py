from __future__ import annotations

import pytest

from chanta_core.agent_runtime.repair_process_state_reconstruction import (
    RepairDiagnosticSignalKind,
    RepairMissionStateProjection,
    RepairOCELStyleEventEnvelope,
    RepairOCPXStateProjection,
    RepairPIGDiagnosticInputContext,
    RepairProcessEventKind,
    RepairProcessObjectKind,
    RepairProcessObjectRef,
    RepairProcessObjectRelation,
    RepairProcessRelationKind,
    RepairProcessStateDecision,
    RepairProcessStateDecisionKind,
    RepairProcessStateFlagSet,
    RepairProcessStateInput,
    RepairProcessStateMode,
    RepairProcessStateNoPersistenceNoExecutionGuarantee,
    RepairProcessStatePolicy,
    RepairProcessStateReconstructionReport,
    RepairProcessStateSourceKind,
    RepairProcessStateStatus,
    RepairTraceSegment,
    V0396ReadinessReport,
    build_repair_mission_state_projection,
    build_repair_ocel_style_event_envelope,
    build_repair_ocpx_state_projection,
    build_repair_pig_diagnostic_input_context,
    build_repair_process_object_ref,
    build_repair_process_object_relation,
    build_repair_process_state_decision,
    build_repair_process_state_flags,
    build_repair_process_state_input,
    build_repair_process_state_no_persistence_no_execution_guarantee,
    build_repair_process_state_policy,
    build_repair_process_state_reconstruction_report,
    build_repair_process_state_transition,
    build_repair_trace_segment,
    build_v0396_readiness_report,
    create_pig_diagnostic_input_context,
    create_repair_ocel_style_event_envelopes,
    create_repair_process_object_refs,
    create_repair_process_object_relations,
    create_repair_process_state_reconstruction_report,
    create_repair_process_state_transition,
    default_repair_process_state_policy,
    project_repair_mission_state,
    project_repair_ocpx_state,
    reconstruct_repair_trace_segments,
    repair_ocel_event_envelope_is_not_persisted,
    repair_ocpx_state_projection_is_not_persisted,
    repair_pig_input_context_is_not_recommendation_execution,
    repair_process_state_flags_preserve_no_persistence_or_execution,
    repair_process_state_policy_blocks_persistence_and_runtime,
    repair_process_state_report_is_not_runtime_execution,
    v0396_readiness_report_is_not_execution_ready,
)


def test_v0396_enum_values() -> None:
    assert [item.value for item in RepairProcessStateMode] == [
        "pi_native_repair_process_state_reconstruction",
        "ocel_style_repair_event_envelope",
        "repair_object_reference_model",
        "repair_object_relation_snapshot",
        "repair_trace_segment_reconstruction",
        "ocpx_style_repair_state_projection",
        "repair_process_state_transition",
        "repair_mission_state_projection",
        "pig_diagnostic_input_context",
        "future_self_prompting_next_action_input",
        "blocked",
        "no_op",
        "unknown",
    ]
    assert [item.value for item in RepairProcessStateSourceKind] == [
        "v0395_outcome_comparison_report",
        "v0395_effectiveness_assessment",
        "v0395_regression_signal",
        "v0395_failure_delta_assessment",
        "v0395_do_nothing_comparison",
        "v0394_post_apply_retest_result",
        "v0394_post_apply_retest_run_record",
        "v0394_post_apply_output_capture",
        "v0394_post_apply_retest_audit",
        "v0393_sandbox_apply_result",
        "v0393_sandbox_apply_transaction",
        "v0393_sandbox_apply_audit",
        "v0392_workspace_descriptor",
        "v0392_workspace_isolation_decision",
        "v0392_target_binding",
        "v0391_approval_artifact_decision",
        "v0391_approval_process_state_gate",
        "v0385_safety_report",
        "v0384_proposed_patch_envelope",
        "v0384_proposed_code_hunk",
        "v037_before_test_result",
        "manual_operator_note",
        "test_fixture",
        "unknown",
    ]
    assert "reconstruction_completed" in {item.value for item in RepairProcessStateStatus}
    assert "sandbox_apply_completed" in {item.value for item in RepairProcessEventKind}
    assert "repair_mission" in {item.value for item in RepairProcessObjectKind}
    assert "requires_human_review" in {item.value for item in RepairProcessRelationKind}
    assert "repair_effective_signal" in {item.value for item in RepairDiagnosticSignalKind}
    assert "allow_future_self_prompting_next_action_input" in {item.value for item in RepairProcessStateDecisionKind}


def test_flags_allow_metadata_and_future_input_only() -> None:
    flags = build_repair_process_state_flags()

    assert isinstance(flags, RepairProcessStateFlagSet)
    assert flags.ready_for_pi_native_repair_process_state_reconstruction is True
    assert flags.ready_for_ocel_style_repair_event_envelope is True
    assert flags.ready_for_ocpx_style_repair_state_projection is True
    assert flags.ready_for_repair_mission_state_projection is True
    assert flags.ready_for_pig_diagnostic_input_context is True
    assert flags.ready_for_future_self_prompting_next_action_input is True
    assert flags.ready_for_v0397_self_prompting_next_action_draft is True
    assert flags.ready_for_repair_process_state_projection is True
    assert repair_process_state_flags_preserve_no_persistence_or_execution(flags)

    assert flags.ready_for_execution is False
    assert flags.ready_for_ocel_event_write is False
    assert flags.ready_for_ocel_file_write is False
    assert flags.ready_for_ocpx_state_persistence is False
    assert flags.ready_for_pig_recommendation_execution is False
    assert flags.ready_for_pig_runtime_authority is False
    assert flags.ready_for_self_prompt_generation is False
    assert flags.production_certified is False


@pytest.mark.parametrize(
    "field_name",
    [
        "ready_for_execution",
        "ready_for_test_execution",
        "ready_for_patch_application",
        "ready_for_apply_patch",
        "ready_for_git_apply",
        "ready_for_ocel_event_write",
        "ready_for_ocel_file_write",
        "ready_for_ocpx_state_persistence",
        "ready_for_pig_recommendation_execution",
        "ready_for_pig_runtime_authority",
        "ready_for_self_prompt_generation",
        "ready_for_self_prompt_auto_execution",
        "ready_for_next_action_draft_generation",
        "ready_for_next_action_auto_execution",
        "ready_for_agent_to_subagent_prompt_generation",
        "ready_for_subagent_auto_invocation",
        "ready_for_external_agent_execution",
        "ready_for_model_provider_invocation",
        "ready_for_autonomous_loop_runtime",
        "ready_for_retry_loop",
        "ready_for_multi_cycle_loop",
        "ready_for_repair_execution",
        "ready_for_dominion_runtime",
        "ready_for_persistent_trace_write",
        "production_certified",
    ],
)
def test_flags_reject_unsafe_true(field_name: str) -> None:
    with pytest.raises(ValueError):
        build_repair_process_state_flags(**{field_name: True})


def test_policy_allows_reconstruction_metadata_and_blocks_runtime() -> None:
    policy = default_repair_process_state_policy()

    assert isinstance(policy, RepairProcessStatePolicy)
    assert policy.allow_ocel_style_event_envelope is True
    assert policy.allow_object_reference_modeling is True
    assert policy.allow_object_relation_snapshot is True
    assert policy.allow_trace_segment_reconstruction is True
    assert policy.allow_ocpx_style_state_projection is True
    assert policy.allow_process_state_transition is True
    assert policy.allow_mission_state_projection is True
    assert policy.allow_pig_diagnostic_input_context is True
    assert policy.allow_future_self_prompting_next_action_input is True
    assert policy.require_outcome_comparison_report is True
    assert policy.require_sandbox_apply_result is True
    assert policy.require_post_apply_retest_result is True
    assert policy.require_do_nothing_comparison is True
    assert policy.require_human_handoff is True
    assert repair_process_state_policy_blocks_persistence_and_runtime(policy)


@pytest.mark.parametrize(
    "field_name",
    [
        "allow_ocel_event_write",
        "allow_ocel_file_write",
        "allow_ocpx_state_persistence",
        "allow_pig_recommendation_execution",
        "allow_pig_runtime_authority",
        "allow_self_prompt_generation",
        "allow_self_prompt_auto_execution",
        "allow_next_action_draft_generation",
        "allow_next_action_auto_execution",
        "allow_subagent_auto_invocation",
        "allow_external_agent_execution",
        "allow_model_provider_invocation",
        "allow_test_execution",
        "allow_patch_application",
        "allow_repair_execution",
        "allow_subprocess",
        "allow_shell",
        "allow_network_access",
        "allow_dominion_runtime",
    ],
)
def test_policy_rejects_persistence_or_runtime_allow(field_name: str) -> None:
    with pytest.raises(ValueError):
        build_repair_process_state_policy(**{field_name: True})


def test_process_state_input_is_metadata_only() -> None:
    process_input = build_repair_process_state_input()

    assert isinstance(process_input, RepairProcessStateInput)
    for action in [
        "ocel_write",
        "ocpx_persistence",
        "pig_execution",
        "self_prompt_generation",
        "self_prompt_execution",
        "subagent_invocation",
        "model_provider",
        "external_agent",
        "test_execution",
        "patch_apply",
        "rollback",
        "repair_execution",
        "Dominion",
    ]:
        assert action in process_input.prohibited_runtime_actions


def test_object_ref_and_relation_are_metadata_only() -> None:
    obj = build_repair_process_object_ref()
    relation = build_repair_process_object_relation()

    assert isinstance(obj, RepairProcessObjectRef)
    assert obj.object_ref_id
    assert isinstance(relation, RepairProcessObjectRelation)
    assert relation.source_object_ref_id
    assert relation.target_object_ref_id


def test_event_envelope_is_not_persisted() -> None:
    envelope = build_repair_ocel_style_event_envelope()

    assert isinstance(envelope, RepairOCELStyleEventEnvelope)
    assert envelope.bounded is True
    assert envelope.persisted is False
    assert envelope.written_to_ocel_file is False
    assert envelope.written_to_jsonl is False
    assert repair_ocel_event_envelope_is_not_persisted(envelope)

    with pytest.raises(ValueError):
        build_repair_ocel_style_event_envelope(persisted=True)


def test_trace_segment_incomplete_when_gaps_exist() -> None:
    segment = build_repair_trace_segment(complete=False, gaps=["missing before-test event"])

    assert isinstance(segment, RepairTraceSegment)
    assert segment.complete is False
    with pytest.raises(ValueError):
        build_repair_trace_segment(complete=True, gaps=["gap"])


def test_ocpx_projection_is_not_persisted_or_authority() -> None:
    projection = build_repair_ocpx_state_projection()

    assert isinstance(projection, RepairOCPXStateProjection)
    assert projection.persisted is False
    assert projection.ocpx_state_written is False
    assert projection.runtime_authority_granted is False
    assert projection.human_review_required is True
    assert repair_ocpx_state_projection_is_not_persisted(projection)

    with pytest.raises(ValueError):
        build_repair_ocpx_state_projection(ocpx_state_written=True)


def test_transition_mission_and_pig_context_block_runtime() -> None:
    transition = build_repair_process_state_transition()
    mission = build_repair_mission_state_projection()
    pig_context = build_repair_pig_diagnostic_input_context()

    assert transition.runtime_authority_granted is False
    assert mission.human_handoff_required is True
    assert mission.future_self_prompting_input_ready is True
    assert mission.next_action_generated is False
    assert mission.next_action_executed is False
    assert mission.self_prompt_generated is False
    assert mission.self_prompt_executed is False
    assert mission.subagent_invoked is False
    assert mission.runtime_authority_granted is False
    assert pig_context.human_review_required is True
    assert pig_context.pig_recommendation_executed is False
    assert pig_context.pig_runtime_authority_granted is False
    assert pig_context.next_action_draft_generated is False
    assert repair_pig_input_context_is_not_recommendation_execution(pig_context)

    with pytest.raises(ValueError):
        build_repair_mission_state_projection(self_prompt_generated=True)
    with pytest.raises(ValueError):
        build_repair_pig_diagnostic_input_context(pig_recommendation_executed=True)


def test_reconstruction_helpers_create_metadata_graph() -> None:
    process_input = build_repair_process_state_input()
    objects = create_repair_process_object_refs(process_input)
    relations = create_repair_process_object_relations(objects)
    events = create_repair_ocel_style_event_envelopes(objects, relations)
    segments = reconstruct_repair_trace_segments(events, objects, relations)
    projection = project_repair_ocpx_state(segments, events, objects, relations)
    transition = create_repair_process_state_transition(projection)
    mission = project_repair_mission_state(projection)
    pig_context = create_pig_diagnostic_input_context(projection, mission)

    assert len(objects) >= 4
    assert len(relations) >= 3
    assert len(events) >= 4
    assert segments[0].complete is True
    assert projection.runtime_authority_granted is False
    assert transition.runtime_authority_granted is False
    assert mission.human_handoff_required is True
    assert pig_context.pig_recommendation_executed is False


def test_decision_report_and_readiness_block_runtime() -> None:
    decision = build_repair_process_state_decision()
    report = create_repair_process_state_reconstruction_report(build_repair_process_state_input())
    readiness = build_v0396_readiness_report(reconstruction_report=report)

    assert isinstance(decision, RepairProcessStateDecision)
    assert decision.ready_for_future_self_prompting_next_action_input is True
    assert decision.process_state_reconstruction_allowed_now is True
    assert decision.ocel_event_write_allowed_now is False
    assert decision.ocpx_state_persistence_allowed_now is False
    assert decision.pig_recommendation_execution_allowed_now is False
    assert decision.self_prompt_generation_allowed_now is False
    assert decision.self_prompt_execution_allowed_now is False
    assert decision.next_action_generation_allowed_now is False
    assert decision.next_action_execution_allowed_now is False
    assert decision.subagent_invocation_allowed_now is False
    assert decision.model_provider_invocation_allowed_now is False
    assert decision.external_agent_allowed_now is False
    assert decision.patch_apply_allowed_now is False
    assert decision.test_execution_allowed_now is False
    assert decision.repair_execution_allowed_now is False
    assert decision.dominion_runtime_allowed_now is False
    assert decision.production_certified is False

    assert isinstance(report, RepairProcessStateReconstructionReport)
    assert report.reconstruction_completed is True
    assert report.ready_for_future_self_prompting_next_action_input is True
    assert report.persisted is False
    assert report.ocel_file_written is False
    assert report.jsonl_written is False
    assert report.ocpx_state_persisted is False
    assert report.pig_recommendation_executed is False
    assert report.self_prompt_generated is False
    assert report.self_prompt_executed is False
    assert report.next_action_generated is False
    assert report.next_action_executed is False
    assert report.subagent_invoked is False
    assert report.model_invoked is False
    assert report.external_agent_invoked is False
    assert report.patch_applied_by_v0396 is False
    assert report.tests_run_by_v0396 is False
    assert report.repair_executed_by_v0396 is False
    assert report.dominion_runtime_invoked is False
    assert report.production_certified is False
    assert report.ready_for_execution is False
    assert repair_process_state_report_is_not_runtime_execution(report)

    assert isinstance(readiness, V0396ReadinessReport)
    assert readiness.ready_for_v0397_self_prompting_next_action_draft is True
    assert readiness.ready_for_pi_native_repair_process_state_reconstruction is True
    assert readiness.ready_for_ocel_style_repair_event_envelope is True
    assert readiness.ready_for_ocpx_style_repair_state_projection is True
    assert readiness.ready_for_repair_mission_state_projection is True
    assert readiness.ready_for_pig_diagnostic_input_context is True
    assert readiness.ready_for_future_self_prompting_next_action_input is True
    assert readiness.ocel_event_write_enabled is False
    assert readiness.ocel_file_write_enabled is False
    assert readiness.ocpx_state_persistence_enabled is False
    assert readiness.pig_recommendation_execution_enabled is False
    assert readiness.self_prompt_generation_enabled is False
    assert readiness.self_prompt_execution_enabled is False
    assert readiness.next_action_generation_enabled is False
    assert readiness.next_action_execution_enabled is False
    assert readiness.subagent_invocation_enabled is False
    assert readiness.model_invocation_enabled is False
    assert readiness.external_agent_enabled is False
    assert readiness.patch_apply_enabled is False
    assert readiness.test_execution_enabled is False
    assert readiness.repair_execution_enabled is False
    assert readiness.dominion_runtime_enabled is False
    assert readiness.production_certified is False
    assert readiness.ready_for_execution is False
    assert v0396_readiness_report_is_not_execution_ready(readiness)


@pytest.mark.parametrize(
    "field_name",
    [
        "ocel_event_write_allowed_now",
        "ocpx_state_persistence_allowed_now",
        "pig_recommendation_execution_allowed_now",
        "self_prompt_generation_allowed_now",
        "next_action_generation_allowed_now",
        "subagent_invocation_allowed_now",
        "model_provider_invocation_allowed_now",
        "external_agent_allowed_now",
        "patch_apply_allowed_now",
        "test_execution_allowed_now",
        "repair_execution_allowed_now",
        "dominion_runtime_allowed_now",
        "production_certified",
    ],
)
def test_decision_rejects_unsafe_allowed_now(field_name: str) -> None:
    with pytest.raises(ValueError):
        build_repair_process_state_decision(**{field_name: True})


@pytest.mark.parametrize(
    "field_name",
    [
        "persisted",
        "ocel_file_written",
        "jsonl_written",
        "ocpx_state_persisted",
        "pig_recommendation_executed",
        "self_prompt_generated",
        "next_action_generated",
        "subagent_invoked",
        "model_invoked",
        "external_agent_invoked",
        "patch_applied_by_v0396",
        "tests_run_by_v0396",
        "repair_executed_by_v0396",
        "dominion_runtime_invoked",
        "production_certified",
        "ready_for_execution",
    ],
)
def test_report_rejects_unsafe_runtime_markers(field_name: str) -> None:
    with pytest.raises(ValueError):
        build_repair_process_state_reconstruction_report(**{field_name: True})


@pytest.mark.parametrize(
    "field_name",
    [
        "self_prompt_generation_enabled",
        "ready_for_execution",
        "ocel_event_write_enabled",
        "ocpx_state_persistence_enabled",
        "pig_recommendation_execution_enabled",
        "next_action_generation_enabled",
        "subagent_invocation_enabled",
        "model_invocation_enabled",
        "external_agent_enabled",
        "patch_apply_enabled",
        "test_execution_enabled",
        "repair_execution_enabled",
        "dominion_runtime_enabled",
        "production_certified",
    ],
)
def test_readiness_rejects_unsafe_enabled_true(field_name: str) -> None:
    with pytest.raises(ValueError):
        build_v0396_readiness_report(**{field_name: True})


def test_no_persistence_no_execution_guarantee_all_true() -> None:
    guarantee = build_repair_process_state_no_persistence_no_execution_guarantee()

    assert isinstance(guarantee, RepairProcessStateNoPersistenceNoExecutionGuarantee)
    assert guarantee.no_ocel_file_write is True
    assert guarantee.no_jsonl_write is True
    assert guarantee.no_ocpx_persistence is True
    assert guarantee.no_trace_persistence is True
    assert guarantee.no_pig_execution is True
    assert guarantee.no_pig_runtime_authority is True
    assert guarantee.no_self_prompt_generation is True
    assert guarantee.no_self_prompt_execution is True
    assert guarantee.no_next_action_generation is True
    assert guarantee.no_next_action_execution is True
    assert guarantee.no_subagent_invocation is True
    assert guarantee.no_model_invocation is True
    assert guarantee.no_external_agent is True
    assert guarantee.no_test_execution is True
    assert guarantee.no_patch_application is True
    assert guarantee.no_rollback_execution is True
    assert guarantee.no_repair_execution is True
    assert guarantee.no_autonomous_loop is True
    assert guarantee.no_retry_loop is True
    assert guarantee.no_multi_cycle_loop is True
    assert guarantee.no_dominion_runtime is True
    assert guarantee.no_production_certification is True
