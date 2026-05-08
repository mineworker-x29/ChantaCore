from chanta_core.delegation import (
    DelegatedProcessRunService,
    DelegationConformanceService,
    SidechainContextService,
)


def main() -> None:
    delegation_service = DelegatedProcessRunService()
    sidechain_service = SidechainContextService(trace_service=delegation_service.trace_service)
    conformance_service = DelegationConformanceService(trace_service=delegation_service.trace_service)

    packet = delegation_service.create_delegation_packet(
        goal="Check delegation conformance.",
        context_summary="Summary-only packet context.",
        structured_inputs={"target": "delegation_conformance"},
        allowed_capabilities=["read_context"],
        permission_request_ids=["permission_request:demo"],
        workspace_write_sandbox_decision_ids=["workspace_write_sandbox_decision:demo"],
        shell_network_pre_sandbox_decision_ids=["shell_network_pre_sandbox_decision:demo"],
        process_outcome_evaluation_ids=["process_outcome_evaluation:demo"],
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
        summary="Summary-only return envelope.",
    )

    contract = conformance_service.register_contract(
        contract_name="Default delegation conformance",
        contract_type="delegation_structure",
        description="Structural delegation conformance check.",
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

    print(f"contract_id={contract.contract_id}")
    print(f"rule_count={len(rules)}")
    print(f"result_id={result.result_id}")
    print(f"status={result.status}")
    print(f"score={result.score}")


if __name__ == "__main__":
    main()
