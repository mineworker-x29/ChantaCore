from chanta_core.delegation import (
    DelegatedProcessRunService,
    DelegationConformanceService,
    SidechainContextService,
)
from chanta_core.ocel.store import OCELStore
from chanta_core.traces.trace_service import TraceService


def _build_subjects(tmp_path):
    store = OCELStore(tmp_path / "delegation_conformance.sqlite")
    trace_service = TraceService(ocel_store=store)
    delegation_service = DelegatedProcessRunService(trace_service=trace_service)
    sidechain_service = SidechainContextService(trace_service=trace_service)
    conformance_service = DelegationConformanceService(trace_service=trace_service)
    packet = delegation_service.create_delegation_packet(
        goal="Check conformance.",
        context_summary="Summary.",
        permission_request_ids=["permission_request:1"],
        session_permission_resolution_ids=["session_permission_resolution:1"],
        workspace_write_sandbox_decision_ids=["workspace_write_sandbox_decision:1"],
        shell_network_pre_sandbox_decision_ids=["shell_network_pre_sandbox_decision:1"],
        process_outcome_evaluation_ids=["process_outcome_evaluation:1"],
    )
    delegated_run = delegation_service.create_delegated_process_run(packet_id=packet.packet_id)
    sidechain_context = sidechain_service.create_sidechain_context_from_packet(
        packet=packet,
        delegated_run=delegated_run,
    )
    entries = sidechain_service.build_entries_from_packet(context=sidechain_context, packet=packet)
    sidechain_context = sidechain_service.mark_context_ready(
        context=sidechain_context,
        entry_ids=[entry.entry_id for entry in entries],
    )
    return_envelope = sidechain_service.record_return_envelope(
        sidechain_context_id=sidechain_context.sidechain_context_id,
        packet_id=packet.packet_id,
        delegated_run_id=delegated_run.delegated_run_id,
        status="completed",
        summary="Summary only.",
    )
    contract = conformance_service.register_contract(
        contract_name="Default delegation conformance",
        contract_type="delegation_structure",
    )
    rules = conformance_service.register_default_rules(contract_id=contract.contract_id)
    return store, conformance_service, contract, rules, packet, delegated_run, sidechain_context, return_envelope


def _findings(store: OCELStore):
    return store.fetch_objects_by_type("delegation_conformance_finding")


def test_delegation_conformance_service_registers_contract_rules_and_passes_good_subjects(tmp_path) -> None:
    store, service, contract, rules, packet, delegated_run, sidechain_context, return_envelope = _build_subjects(tmp_path)

    result = service.evaluate_delegation_conformance(
        contract=contract,
        rules=rules,
        packet=packet,
        delegated_run=delegated_run,
        sidechain_context=sidechain_context,
        return_envelope=return_envelope,
    )

    activities = {event["event_activity"] for event in store.fetch_recent_events(200)}
    rule_types = {rule.rule_type for rule in rules}

    assert {
        "delegation_conformance_contract_registered",
        "delegation_conformance_rule_registered",
        "delegation_conformance_run_started",
        "delegation_conformance_finding_recorded",
        "delegation_conformance_result_recorded",
        "delegation_conformance_run_completed",
    }.issubset(activities)
    assert {
        "packet_exists",
        "delegated_run_uses_packet",
        "sidechain_derived_from_packet",
        "no_full_parent_transcript",
        "no_permission_inheritance",
        "summary_only_return",
        "no_full_child_transcript",
        "safety_refs_preserved",
        "required_packet_fields_present",
    }.issubset(rule_types)
    assert result.status == "passed"
    assert result.score == 1.0


def test_delegation_conformance_missing_packet_records_failed_or_inconclusive_findings(tmp_path) -> None:
    store, service, contract, rules, _, delegated_run, sidechain_context, return_envelope = _build_subjects(tmp_path)

    result = service.evaluate_delegation_conformance(
        contract=contract,
        rules=rules,
        packet=None,
        delegated_run=delegated_run,
        sidechain_context=sidechain_context,
        return_envelope=return_envelope,
    )
    statuses = {item["object_attrs"]["rule_type"]: item["object_attrs"]["status"] for item in _findings(store)}

    assert result.status == "failed"
    assert statuses["packet_exists"] == "failed"
    assert statuses["required_packet_fields_present"] == "failed"


def test_delegation_conformance_detects_parent_transcript_permission_and_child_transcript_violations(tmp_path) -> None:
    store, service, contract, rules, packet, delegated_run, sidechain_context, return_envelope = _build_subjects(tmp_path)
    object.__setattr__(sidechain_context, "contains_full_parent_transcript", True)
    object.__setattr__(delegated_run, "inherited_permissions", True)
    object.__setattr__(return_envelope, "contains_full_child_transcript", True)

    result = service.evaluate_delegation_conformance(
        contract=contract,
        rules=rules,
        packet=packet,
        delegated_run=delegated_run,
        sidechain_context=sidechain_context,
        return_envelope=return_envelope,
    )
    statuses = {item["object_attrs"]["rule_type"]: item["object_attrs"]["status"] for item in _findings(store)}

    assert result.status == "failed"
    assert statuses["no_full_parent_transcript"] == "failed"
    assert statuses["no_permission_inheritance"] == "failed"
    assert statuses["summary_only_return"] == "failed"
    assert statuses["no_full_child_transcript"] == "failed"


def test_delegation_conformance_missing_safety_refs_needs_review_without_mutation(tmp_path) -> None:
    _, service, contract, rules, packet, delegated_run, sidechain_context, return_envelope = _build_subjects(tmp_path)
    original_packet = packet.to_dict()
    original_context = sidechain_context.to_dict()
    object.__setattr__(sidechain_context, "safety_ref_ids", [])

    result = service.evaluate_delegation_conformance(
        contract=contract,
        rules=rules,
        packet=packet,
        delegated_run=delegated_run,
        sidechain_context=sidechain_context,
        return_envelope=return_envelope,
    )

    assert result.status == "needs_review"
    assert packet.to_dict() == original_packet
    assert sidechain_context.to_dict()["entry_ids"] == original_context["entry_ids"]
    assert sidechain_context.safety_ref_ids == []
