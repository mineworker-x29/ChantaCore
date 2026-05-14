from chanta_core.digestion import ObservationToDigestionAdapterBuilderService
from chanta_core.observation import AgentBehaviorInferenceV2
from chanta_core.observation_digest import ExternalSkillBehaviorFingerprint, ObservedAgentRun
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


def test_build_from_inference_creates_mappings_and_review_request() -> None:
    service = ObservationToDigestionAdapterBuilderService()
    result = service.build_from_behavior_inference(_inference(["read_object"]))

    assert result.status == "completed"
    assert service.last_input_mappings
    assert service.last_output_mappings
    assert service.last_review_requests
    assert service.last_adapter_candidates[0].requires_review is True


def test_low_confidence_mapping_creates_finding() -> None:
    service = ObservationToDigestionAdapterBuilderService()
    policy = service.create_default_policy(min_mapping_confidence_for_candidate=0.5)
    result = service.build_from_behavior_inference(_inference(["read_object"], confidence=0.2), policy=policy)

    assert result.status == "completed"
    assert any(item.finding_type == "low_mapping_confidence" for item in service.last_findings)
    assert service.last_adapter_candidates == []


def test_build_from_fingerprint_and_observed_run() -> None:
    service = ObservationToDigestionAdapterBuilderService()
    fingerprint = ExternalSkillBehaviorFingerprint(
        fingerprint_id="external_skill_behavior_fingerprint:public-dummy",
        observed_run_id="observed_agent_run:public-dummy",
        source_runtime="generic_runtime",
        source_skill_name="generic_reader",
        source_tool_name=None,
        observed_event_count=1,
        observed_sequence=["read_object"],
        object_types_touched=["workspace_text"],
        input_shape_summary={"root_ref": "string", "relative_path": "string"},
        output_shape_summary={"summary": "string"},
        side_effect_profile="none",
        permission_profile="read_only",
        verification_profile="evidence_refs",
        failure_modes=[],
        recovery_patterns=[],
        recommended_chantacore_category="read_file",
        risk_class="low",
        confidence=0.9,
        evidence_refs=["evidence:public-dummy"],
        created_at=utc_now_iso(),
    )
    assert service.build_from_behavior_fingerprint(fingerprint).status == "completed"
    assert service.last_adapter_candidates

    run = ObservedAgentRun(
        observed_run_id="observed_agent_run:public-run",
        source_id="agent_observation_source:public",
        batch_id="agent_observation_batch:public",
        source_agent_id=None,
        source_session_id=None,
        inferred_runtime="generic_runtime",
        event_count=1,
        object_count=1,
        relation_count=0,
        observation_confidence=0.85,
        created_at=utc_now_iso(),
        run_attrs={"observed_sequence": ["search_object"], "object_types": ["workspace_text"]},
    )
    assert service.build_from_observed_run(run).status == "completed"
    assert service.last_observed_capabilities[0].capability_category == "search_file"

