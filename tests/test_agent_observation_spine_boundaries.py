from chanta_core.observation import AgentObservationSpineService


def test_unimplemented_adapters_and_collectors_do_not_activate_live_collection() -> None:
    service = AgentObservationSpineService()
    collectors = service.register_collector_contracts()
    adapters = service.register_adapter_profiles()

    assert next(item for item in collectors if item.collector_kind == "sidecar").enabled is False
    assert next(item for item in collectors if item.collector_kind == "event_bus").enabled is False
    assert next(item for item in collectors if item.collector_kind == "runtime_hook").enabled is False
    assert all(adapter.adapter_attrs["execution_enabled"] is False for adapter in adapters)
    assert any(adapter.implemented is False for adapter in adapters)


def test_spine_policy_has_no_external_execution_or_live_bus() -> None:
    policy = AgentObservationSpineService().create_default_policy()

    assert policy.allow_batch_file_observation is True
    assert policy.allow_tail_file_observation is False
    assert policy.allow_runtime_hook_observation is False
    assert policy.allow_event_bus_observation is False
    assert policy.allow_sidecar_observation is False
    assert policy.allow_causal_claims_by_default is False
