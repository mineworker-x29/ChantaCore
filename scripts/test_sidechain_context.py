from chanta_core.delegation import DelegatedProcessRunService, SidechainContextService


def main() -> None:
    delegation_service = DelegatedProcessRunService()
    sidechain_service = SidechainContextService(trace_service=delegation_service.trace_service)

    packet = delegation_service.create_delegation_packet(
        goal="Build packet-only sidechain context.",
        context_summary="Summary-only context for sidechain setup.",
        structured_inputs={"target": "sidechain_context"},
        object_refs=[{"object_type": "document", "object_id": "doc:sidechain"}],
        allowed_capabilities=["read_context"],
        expected_output_schema={"type": "object", "required": ["summary"]},
        termination_conditions={"max_steps": 0},
        permission_request_ids=["permission_request:demo"],
        session_permission_resolution_ids=["session_permission_resolution:demo"],
        workspace_write_sandbox_decision_ids=["workspace_write_sandbox_decision:demo"],
        shell_network_pre_sandbox_decision_ids=["shell_network_pre_sandbox_decision:demo"],
        process_outcome_evaluation_ids=["process_outcome_evaluation:demo"],
    )
    run = delegation_service.create_delegated_process_run(packet_id=packet.packet_id)
    context = sidechain_service.create_sidechain_context_from_packet(packet=packet, delegated_run=run)
    entries = sidechain_service.build_entries_from_packet(context=context, packet=packet)
    ready = sidechain_service.mark_context_ready(
        context=context,
        entry_ids=[entry.entry_id for entry in entries],
    )
    sealed = sidechain_service.seal_context(context=ready)
    snapshot = sidechain_service.build_snapshot(context=sealed, entries=entries, summary="Packet-only snapshot.")
    envelope = sidechain_service.record_return_envelope(
        sidechain_context_id=sealed.sidechain_context_id,
        packet_id=packet.packet_id,
        delegated_run_id=run.delegated_run_id,
        status="completed",
        summary="Summary-only return envelope.",
    )

    print(f"packet_id={packet.packet_id}")
    print(f"delegated_run_id={run.delegated_run_id}")
    print(f"sidechain_context_id={sealed.sidechain_context_id}")
    print(f"context_status={sealed.status}")
    print(f"entry_count={len(entries)}")
    print(f"snapshot_id={snapshot.snapshot_id}")
    print(f"envelope_id={envelope.envelope_id}")
    print(f"contains_full_parent_transcript={sealed.contains_full_parent_transcript}")
    print(f"inherited_permissions={sealed.inherited_permissions}")
    print(f"contains_full_child_transcript={envelope.contains_full_child_transcript}")


if __name__ == "__main__":
    main()
