from chanta_core.external.history_adapter import (
    external_assimilation_candidates_to_history_entries,
    external_capability_descriptors_to_history_entries,
    external_capability_risk_notes_to_history_entries,
)
from chanta_core.external.models import (
    ExternalAssimilationCandidate,
    ExternalCapabilityDescriptor,
    ExternalCapabilityRiskNote,
)
from chanta_core.utility.time import utc_now_iso


def test_external_capability_history_adapters_include_refs_and_priority() -> None:
    now = utc_now_iso()
    descriptor = ExternalCapabilityDescriptor(
        descriptor_id="external_capability_descriptor:history",
        source_id="external_capability_source:history",
        capability_name="external_tool",
        capability_type="tool",
        description=None,
        provider=None,
        version=None,
        declared_inputs={},
        declared_outputs={},
        declared_permissions=[],
        declared_risks=[],
        declared_entrypoint=None,
        raw_descriptor={"name": "external_tool"},
        normalized=True,
        status="normalized",
        created_at=now,
        descriptor_attrs={},
    )
    candidate = ExternalAssimilationCandidate(
        candidate_id="external_assimilation_candidate:history",
        descriptor_id=descriptor.descriptor_id,
        source_id=descriptor.source_id,
        candidate_type="tool",
        candidate_name="external_tool",
        linked_tool_descriptor_id="tool_descriptor:future",
        linked_permission_scope_id="permission_scope:future",
        created_at=now,
    )
    note = ExternalCapabilityRiskNote(
        risk_note_id="external_capability_risk_note:history",
        descriptor_id=descriptor.descriptor_id,
        candidate_id=candidate.candidate_id,
        risk_level="critical",
        risk_categories=["external_code_execution"],
        message="Critical review.",
        review_required=True,
        source_kind="tool",
        created_at=now,
        risk_attrs={},
    )

    descriptor_entry = external_capability_descriptors_to_history_entries([descriptor])[0]
    candidate_entry = external_assimilation_candidates_to_history_entries([candidate])[0]
    note_entry = external_capability_risk_notes_to_history_entries([note])[0]

    assert descriptor_entry.source == "external_capability"
    assert candidate_entry.source == "external_capability"
    assert note_entry.source == "external_capability"
    assert descriptor_entry.refs[0]["descriptor_id"] == descriptor.descriptor_id
    assert candidate_entry.refs[0]["candidate_id"] == candidate.candidate_id
    assert candidate_entry.refs[0]["linked_tool_descriptor_id"] == "tool_descriptor:future"
    assert candidate_entry.refs[0]["linked_permission_scope_id"] == "permission_scope:future"
    assert note_entry.refs[0]["risk_note_id"] == note.risk_note_id
    assert note_entry.priority >= 90
