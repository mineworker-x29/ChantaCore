from chanta_core.delegation.ids import (
    new_sidechain_context_entry_id,
    new_sidechain_context_id,
    new_sidechain_context_snapshot_id,
    new_sidechain_return_envelope_id,
)
from chanta_core.delegation.sidechain import (
    SidechainContext,
    SidechainContextEntry,
    SidechainContextSnapshot,
    SidechainReturnEnvelope,
)
from chanta_core.utility.time import utc_now_iso


def test_sidechain_ids_use_expected_prefixes() -> None:
    assert new_sidechain_context_id().startswith("sidechain_context:")
    assert new_sidechain_context_entry_id().startswith("sidechain_context_entry:")
    assert new_sidechain_context_snapshot_id().startswith("sidechain_context_snapshot:")
    assert new_sidechain_return_envelope_id().startswith("sidechain_return_envelope:")


def test_sidechain_context_to_dict_records_boundaries() -> None:
    context = SidechainContext(
        sidechain_context_id="sidechain_context:1",
        packet_id="delegation_packet:1",
        delegated_run_id="delegated_process_run:1",
        parent_session_id="session:parent",
        child_session_id="session:child",
        parent_process_instance_id="process_instance:parent",
        child_process_instance_id="process_instance:child",
        context_type="delegation",
        isolation_mode="packet_only",
        status="created",
        created_at=utc_now_iso(),
        entry_ids=["sidechain_context_entry:1"],
        safety_ref_ids=["permission_request:1"],
        contains_full_parent_transcript=False,
        inherited_permissions=False,
        context_attrs={"packet_metadata_only": True},
    )

    data = context.to_dict()

    assert data["sidechain_context_id"] == "sidechain_context:1"
    assert data["packet_id"] == "delegation_packet:1"
    assert data["delegated_run_id"] == "delegated_process_run:1"
    assert data["entry_ids"] == ["sidechain_context_entry:1"]
    assert data["safety_ref_ids"] == ["permission_request:1"]
    assert data["contains_full_parent_transcript"] is False
    assert data["inherited_permissions"] is False


def test_sidechain_entry_snapshot_and_return_envelope_to_dict() -> None:
    entry = SidechainContextEntry(
        entry_id="sidechain_context_entry:1",
        sidechain_context_id="sidechain_context:1",
        entry_type="goal",
        title="Goal",
        content="Check context.",
        content_ref=None,
        payload={"goal": "Check context."},
        source_kind="delegation_packet",
        source_ref="delegation_packet:1",
        priority=70,
        created_at=utc_now_iso(),
        entry_attrs={"packet_id": "delegation_packet:1"},
    )
    snapshot = SidechainContextSnapshot(
        snapshot_id="sidechain_context_snapshot:1",
        sidechain_context_id="sidechain_context:1",
        packet_id="delegation_packet:1",
        delegated_run_id="delegated_process_run:1",
        created_at=utc_now_iso(),
        entry_ids=[entry.entry_id],
        entry_count=1,
        summary="Snapshot.",
        snapshot_attrs={},
    )
    envelope = SidechainReturnEnvelope(
        envelope_id="sidechain_return_envelope:1",
        sidechain_context_id="sidechain_context:1",
        delegated_run_id="delegated_process_run:1",
        packet_id="delegation_packet:1",
        status="completed",
        summary="Summary only.",
        output_payload={"ok": True},
        evidence_refs=[{"ref_id": "evidence:1"}],
        recommendation_refs=[{"ref_id": "recommendation:1"}],
        failure=None,
        contains_full_child_transcript=False,
        created_at=utc_now_iso(),
        envelope_attrs={},
    )

    assert entry.to_dict()["entry_type"] == "goal"
    assert snapshot.to_dict()["entry_count"] == 1
    assert envelope.to_dict()["contains_full_child_transcript"] is False
    assert envelope.to_dict()["summary"] == "Summary only."
