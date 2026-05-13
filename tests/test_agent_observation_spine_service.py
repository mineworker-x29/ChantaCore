from chanta_core.observation import AgentObservationSpineService
from chanta_core.observation_digest import ObservedAgentRun
from chanta_core.utility.time import utc_now_iso


def _run() -> ObservedAgentRun:
    return ObservedAgentRun(
        observed_run_id="observed_agent_run:demo",
        source_id="agent_observation_source:demo",
        batch_id="agent_observation_batch:demo",
        source_agent_id=None,
        source_session_id=None,
        inferred_runtime="generic_jsonl",
        event_count=2,
        object_count=1,
        relation_count=1,
        observation_confidence=0.7,
        created_at=utc_now_iso(),
    )


def test_default_policy_collectors_adapters_and_environment_snapshot() -> None:
    service = AgentObservationSpineService()
    policy = service.create_default_policy()
    collectors = service.register_collector_contracts()
    adapters = service.register_adapter_profiles()
    agent = service.register_agent_instance(source_runtime="generic_jsonl")
    environment = service.create_environment_snapshot(agent_instance=agent)

    assert policy.allow_runtime_hook_observation is False
    assert policy.allow_event_bus_observation is False
    assert policy.allow_sidecar_observation is False
    assert {collector.collector_kind for collector in collectors} >= {"batch_file", "event_bus", "sidecar"}
    assert next(collector for collector in collectors if collector.collector_kind == "batch_file").enabled is True
    assert next(collector for collector in collectors if collector.collector_kind == "event_bus").enabled is False
    assert any(adapter.adapter_name == "GenericJSONLTranscriptAdapter" and adapter.implemented for adapter in adapters)
    assert any(not adapter.implemented for adapter in adapters)
    assert environment.sandbox_enabled is True
    assert environment.network_enabled is False
    assert environment.shell_enabled is False
    assert environment.write_enabled is False


def test_normalize_objects_relations_and_behavior_inference_v2() -> None:
    service = AgentObservationSpineService()
    first = service.normalize_event_v2({"id": "u1", "role": "user", "content": "inspect this"})
    second = service.normalize_event_v2({"id": "t1", "tool": "search", "input": {"q": "fixture"}})
    objects = service.create_observed_objects(observed_run_id="observed_agent_run:demo")
    relations = service.create_observed_relations(observed_run_id="observed_agent_run:demo")
    inference = service.create_behavior_inference_v2(observed_run=_run(), events=[first, second])

    assert first.evidence_ref
    assert first.withdrawal_conditions
    assert objects
    assert relations[0].causal_claim is False
    assert inference.confirmed_observations
    assert inference.data_based_interpretations
    assert inference.likely_hypotheses
    assert inference.estimates
    assert inference.unknown_or_needs_verification
    assert inference.evidence_refs
    assert inference.withdrawal_conditions
