from chanta_core.digestion import ObservationToDigestionAdapterBuilderService
from chanta_core.observation import AgentBehaviorInferenceV2
from chanta_core.ocel.store import OCELStore
from chanta_core.utility.time import utc_now_iso


def test_ocel_objects_events_emitted(tmp_path) -> None:
    store = OCELStore(tmp_path / "adapter_builder.sqlite")
    service = ObservationToDigestionAdapterBuilderService(ocel_store=store)
    inference = AgentBehaviorInferenceV2(
        inference_id="agent_behavior_inference_v2:public-dummy",
        observed_run_id="observed_agent_run:public-dummy",
        inferred_goal="inspect workspace",
        inferred_goal_confidence=0.9,
        inferred_intent="read only analysis",
        inferred_task_type="workspace_diagnostic",
        inferred_action_sequence=["read_object"],
        inferred_skill_sequence=[],
        inferred_tool_sequence=[],
        touched_object_types=["workspace_text"],
        effect_profile=[],
        outcome_inference="completed",
        outcome_confidence=0.9,
        confirmed_observations=["public dummy observation"],
        data_based_interpretations=[],
        likely_hypotheses=[],
        estimates=[],
        unknown_or_needs_verification=[],
        failure_signals=[],
        recovery_signals=[],
        evidence_refs=["evidence:public-dummy"],
        uncertainty_notes=[],
        withdrawal_conditions=["withdraw if dummy evidence is replaced"],
        created_at=utc_now_iso(),
    )

    service.build_from_behavior_inference(inference)
    events = store.fetch_recent_events(20)

    assert store.fetch_object_count() >= 7
    assert {event["event_activity"] for event in events} >= {
        "observed_capability_candidate_created",
        "chantacore_target_skill_candidate_created",
        "adapter_input_mapping_spec_created",
        "adapter_output_mapping_spec_created",
        "observation_digestion_adapter_candidate_created",
        "observation_digestion_adapter_review_requested",
        "observation_digestion_adapter_build_result_recorded",
    }

