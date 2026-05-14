from chanta_core.digestion import ObservationToDigestionAdapterBuilderService
from chanta_core.observation import AgentBehaviorInferenceV2
from chanta_core.utility.time import utc_now_iso


def _build(actions: list[str]):
    service = ObservationToDigestionAdapterBuilderService()
    inference = AgentBehaviorInferenceV2(
        inference_id="agent_behavior_inference_v2:public-dummy",
        observed_run_id="observed_agent_run:public-dummy",
        inferred_goal="inspect capability",
        inferred_goal_confidence=0.9,
        inferred_intent="classification",
        inferred_task_type="adapter_candidate",
        inferred_action_sequence=actions,
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
    return service


def test_unsupported_shell_write_network_mcp_plugin_detection() -> None:
    cases = [
        (["execute_action", "shell command"], "shell_execution"),
        (["workspace_file_changed"], "write_file"),
        (["external_system_touched", "network"], "network_access"),
        (["mcp server tool resource"], "mcp_connection"),
        (["plugin load extension"], "plugin_loading"),
    ]
    for actions, expected in cases:
        service = _build(actions)
        assert any(item.feature_type == expected for item in service.last_unsupported_features)
        candidate = service.last_adapter_candidates[0]
        assert candidate.review_status == "pending_review"
        assert candidate.canonical_import_enabled is False
        assert candidate.execution_enabled is False

