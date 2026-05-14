from chanta_core.digestion import ObservationToDigestionAdapterBuilderService
from chanta_core.observation import AgentBehaviorInferenceV2
from chanta_core.utility.time import utc_now_iso


def _inference(actions: list[str], confidence: float = 0.9) -> AgentBehaviorInferenceV2:
    return AgentBehaviorInferenceV2(
        inference_id="agent_behavior_inference_v2:public-dummy",
        observed_run_id="observed_agent_run:public-dummy",
        inferred_goal="inspect workspace",
        inferred_goal_confidence=confidence,
        inferred_intent="read only analysis",
        inferred_task_type="workspace_diagnostic",
        inferred_action_sequence=actions,
        inferred_skill_sequence=[],
        inferred_tool_sequence=[],
        touched_object_types=["workspace_text"],
        effect_profile=[],
        outcome_inference="completed",
        outcome_confidence=confidence,
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


def _target_for(actions: list[str]):
    service = ObservationToDigestionAdapterBuilderService()
    capabilities = service.extract_observed_capabilities(inference=_inference(actions))
    targets = service.match_target_skills(capabilities)
    return capabilities[0], targets[0]


def test_read_search_summary_capability_mapping() -> None:
    read_capability, read_target = _target_for(["read_object"])
    search_capability, search_target = _target_for(["search_object"])
    summary_capability, summary_target = _target_for(["summarize_object"])

    assert read_capability.capability_category == "read_file"
    assert read_target.target_skill_id == "skill:read_workspace_text_file"
    assert search_capability.capability_category == "search_file"
    assert "grep" in search_target.target_skill_id or "search" in search_target.target_skill_id
    assert summary_capability.capability_category == "summarize_content"
    assert "summarize" in summary_target.target_skill_id or "summary" in summary_target.target_skill_id


def test_observation_and_digestion_capability_mapping() -> None:
    observation_capability, observation_target = _target_for(["agent_behavior_infer"])
    digestion_capability, digestion_target = _target_for(["external_skill_static_digest"])

    assert observation_capability.capability_category == "observation"
    assert observation_target.target_skill_id == "skill:agent_behavior_infer"
    assert digestion_capability.capability_category == "digestion"
    assert digestion_target.target_skill_id == "skill:external_skill_static_digest"

