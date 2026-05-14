from chanta_core.digestion import (
    ObservationToDigestionAdapterBuilderService,
    adapter_candidates_to_history_entries,
    adapter_findings_to_history_entries,
    observed_capability_candidates_to_history_entries,
    target_skill_candidates_to_history_entries,
    unsupported_features_to_history_entries,
)
from chanta_core.observation import AgentBehaviorInferenceV2
from chanta_core.utility.time import utc_now_iso


def test_history_entries_use_adapter_builder_source_and_priorities() -> None:
    service = ObservationToDigestionAdapterBuilderService()
    inference = AgentBehaviorInferenceV2(
        inference_id="agent_behavior_inference_v2:public-dummy",
        observed_run_id="observed_agent_run:public-dummy",
        inferred_goal="inspect capability",
        inferred_goal_confidence=0.9,
        inferred_intent="classification",
        inferred_task_type="adapter_candidate",
        inferred_action_sequence=["execute_action", "shell command"],
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

    entries = [
        *observed_capability_candidates_to_history_entries(service.last_observed_capabilities),
        *target_skill_candidates_to_history_entries(service.last_target_candidates),
        *adapter_candidates_to_history_entries(service.last_adapter_candidates),
        *unsupported_features_to_history_entries(service.last_unsupported_features),
        *adapter_findings_to_history_entries(service.last_findings),
    ]

    assert entries
    assert {item.source for item in entries} == {"observation_to_digestion_adapter_builder"}
    assert max(item.priority for item in entries) >= 90

