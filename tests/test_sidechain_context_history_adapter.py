from chanta_core.delegation.history_adapter import (
    sidechain_context_entries_to_history_entries,
    sidechain_context_snapshots_to_history_entries,
    sidechain_contexts_to_history_entries,
    sidechain_return_envelopes_to_history_entries,
)
from chanta_core.delegation.sidechain import (
    SidechainContext,
    SidechainContextEntry,
    SidechainContextSnapshot,
    SidechainReturnEnvelope,
)
from chanta_core.utility.time import utc_now_iso


def test_sidechain_history_adapter_converts_contexts_entries_snapshots_and_envelopes() -> None:
    context = SidechainContext(
        sidechain_context_id="sidechain_context:history",
        packet_id="delegation_packet:history",
        delegated_run_id="delegated_process_run:history",
        parent_session_id="session:parent",
        child_session_id="session:child",
        parent_process_instance_id="process_instance:parent",
        child_process_instance_id="process_instance:child",
        context_type="delegation",
        isolation_mode="packet_only",
        status="ready",
        created_at=utc_now_iso(),
        entry_ids=["sidechain_context_entry:history"],
        safety_ref_ids=["permission_request:history"],
        contains_full_parent_transcript=False,
        inherited_permissions=False,
        context_attrs={},
    )
    entry = SidechainContextEntry(
        entry_id="sidechain_context_entry:history",
        sidechain_context_id=context.sidechain_context_id,
        entry_type="risk_ref",
        title="Risk",
        content=None,
        content_ref="shell_network_pre_sandbox_decision:history",
        payload={"ref_id": "shell_network_pre_sandbox_decision:history"},
        source_kind="shell_network_pre_sandbox_decision",
        source_ref="shell_network_pre_sandbox_decision:history",
        priority=85,
        created_at=utc_now_iso(),
        entry_attrs={},
    )
    snapshot = SidechainContextSnapshot(
        snapshot_id="sidechain_context_snapshot:history",
        sidechain_context_id=context.sidechain_context_id,
        packet_id=context.packet_id,
        delegated_run_id=context.delegated_run_id,
        created_at=utc_now_iso(),
        entry_ids=[entry.entry_id],
        entry_count=1,
        summary="Snapshot.",
        snapshot_attrs={},
    )
    envelope = SidechainReturnEnvelope(
        envelope_id="sidechain_return_envelope:history",
        sidechain_context_id=context.sidechain_context_id,
        delegated_run_id=context.delegated_run_id,
        packet_id=context.packet_id,
        status="failed",
        summary="Failed summary.",
        output_payload={},
        evidence_refs=[],
        recommendation_refs=[],
        failure={"reason": "test"},
        contains_full_child_transcript=False,
        created_at=utc_now_iso(),
        envelope_attrs={},
    )

    context_entry = sidechain_contexts_to_history_entries([context])[0]
    risk_entry = sidechain_context_entries_to_history_entries([entry])[0]
    snapshot_entry = sidechain_context_snapshots_to_history_entries([snapshot])[0]
    envelope_entry = sidechain_return_envelopes_to_history_entries([envelope])[0]

    assert context_entry.source == "sidechain_context"
    assert risk_entry.source == "sidechain_context"
    assert snapshot_entry.source == "sidechain_context"
    assert envelope_entry.source == "sidechain_context"
    assert context_entry.refs[0]["sidechain_context_id"] == context.sidechain_context_id
    assert context_entry.refs[0]["packet_id"] == context.packet_id
    assert context_entry.refs[0]["delegated_run_id"] == context.delegated_run_id
    assert risk_entry.refs[0]["entry_id"] == entry.entry_id
    assert snapshot_entry.refs[0]["snapshot_id"] == snapshot.snapshot_id
    assert envelope_entry.refs[0]["envelope_id"] == envelope.envelope_id
    assert risk_entry.priority >= 80
    assert envelope_entry.priority >= 90
