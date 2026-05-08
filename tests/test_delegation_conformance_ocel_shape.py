from chanta_core.delegation import (
    DelegatedProcessRunService,
    DelegationConformanceService,
    SidechainContextService,
)
from chanta_core.ocel.store import OCELStore
from chanta_core.traces.trace_service import TraceService


def test_delegation_conformance_ocel_shape_contains_expected_objects_and_events(tmp_path) -> None:
    store = OCELStore(tmp_path / "delegation_conformance_shape.sqlite")
    trace_service = TraceService(ocel_store=store)
    delegation_service = DelegatedProcessRunService(trace_service=trace_service)
    sidechain_service = SidechainContextService(trace_service=trace_service)
    conformance_service = DelegationConformanceService(trace_service=trace_service)
    packet = delegation_service.create_delegation_packet(goal="Shape.")
    delegated_run = delegation_service.create_delegated_process_run(packet_id=packet.packet_id)
    sidechain_context = sidechain_service.create_sidechain_context_from_packet(
        packet=packet,
        delegated_run=delegated_run,
    )
    return_envelope = sidechain_service.record_return_envelope(
        sidechain_context_id=sidechain_context.sidechain_context_id,
        packet_id=packet.packet_id,
        delegated_run_id=delegated_run.delegated_run_id,
        status="completed",
    )
    contract = conformance_service.register_contract(
        contract_name="Shape",
        contract_type="delegation_structure",
    )
    rules = conformance_service.register_default_rules(contract_id=contract.contract_id)
    result = conformance_service.evaluate_delegation_conformance(
        contract=contract,
        rules=rules,
        packet=packet,
        delegated_run=delegated_run,
        sidechain_context=sidechain_context,
        return_envelope=return_envelope,
    )

    activities = {event["event_activity"] for event in store.fetch_recent_events(200)}

    assert {
        "delegation_conformance_contract_registered",
        "delegation_conformance_rule_registered",
        "delegation_conformance_run_started",
        "delegation_conformance_finding_recorded",
        "delegation_conformance_result_recorded",
        "delegation_conformance_run_completed",
    }.issubset(activities)
    assert store.fetch_objects_by_type("delegation_conformance_contract")
    assert store.fetch_objects_by_type("delegation_conformance_rule")
    assert store.fetch_objects_by_type("delegation_conformance_run")
    assert store.fetch_objects_by_type("delegation_conformance_finding")
    assert store.fetch_objects_by_type("delegation_conformance_result")
    assert store.fetch_object_object_relations_for_object(result.result_id)
