from chanta_core.observation import CrossHarnessTraceAdapterService


def test_default_policy_requires_redaction_confidence_evidence_withdrawal():
    policy = CrossHarnessTraceAdapterService().create_default_policy()

    assert policy.require_redaction is True
    assert policy.require_confidence is True
    assert policy.require_evidence_ref is True
    assert policy.require_withdrawal_conditions is True
    assert policy.allow_causal_claims_by_default is False
    assert policy.to_dict()["policy_id"].startswith("cross_harness_trace_adapter_policy:")


def test_adapter_contract_models_register_safe_defaults():
    contracts = CrossHarnessTraceAdapterService().register_adapter_contracts()

    generic = next(item for item in contracts if item.adapter_name == "GenericJSONLTranscriptAdapter")
    assert generic.implemented is True
    assert generic.read_only is True
    assert generic.supports_runtime_hook is False
    assert generic.supports_event_bus is False

    stub = next(item for item in contracts if item.adapter_name == "CodexTaskLogAdapter")
    assert stub.implemented is False
    assert stub.enabled is False
