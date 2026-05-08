import pytest

from chanta_core.external.errors import ExternalAssimilationCandidateError
from chanta_core.external.ids import (
    new_external_assimilation_candidate_id,
    new_external_capability_descriptor_id,
    new_external_capability_import_batch_id,
    new_external_capability_normalization_id,
    new_external_capability_risk_note_id,
    new_external_capability_source_id,
)
from chanta_core.external.models import (
    ExternalAssimilationCandidate,
    ExternalCapabilityDescriptor,
    ExternalCapabilityImportBatch,
    ExternalCapabilityNormalizationResult,
    ExternalCapabilityRiskNote,
    ExternalCapabilitySource,
)
from chanta_core.utility.time import utc_now_iso


def test_external_capability_models_to_dict_and_id_prefixes() -> None:
    now = utc_now_iso()
    source = ExternalCapabilitySource(
        source_id=new_external_capability_source_id(),
        source_name="provided",
        source_type="provided_dict",
        source_ref=None,
        trust_level="untrusted",
        status="active",
        created_at=now,
        updated_at=now,
        source_attrs={"k": "v"},
    )
    descriptor = ExternalCapabilityDescriptor(
        descriptor_id=new_external_capability_descriptor_id(),
        source_id=source.source_id,
        capability_name="external_file_writer",
        capability_type="tool",
        description="descriptor",
        provider="provider",
        version="1",
        declared_inputs={"path": "str"},
        declared_outputs={"ok": "bool"},
        declared_permissions=["write_file"],
        declared_risks=["filesystem_write"],
        declared_entrypoint="external.module:run",
        raw_descriptor={"name": "external_file_writer"},
        normalized=False,
        status="imported",
        created_at=now,
        descriptor_attrs={},
    )
    batch = ExternalCapabilityImportBatch(
        batch_id=new_external_capability_import_batch_id(),
        source_id=source.source_id,
        batch_name="batch",
        imported_descriptor_ids=[descriptor.descriptor_id],
        failed_descriptor_refs=[],
        status="completed",
        created_at=now,
        batch_attrs={},
    )
    normalization = ExternalCapabilityNormalizationResult(
        normalization_id=new_external_capability_normalization_id(),
        descriptor_id=descriptor.descriptor_id,
        status="normalized",
        normalized_capability_type="tool",
        normalized_name=descriptor.capability_name,
        normalized_permissions=["filesystem_write"],
        normalized_risk_categories=["filesystem_write"],
        validation_messages=[],
        created_at=now,
        normalization_attrs={},
    )
    candidate = ExternalAssimilationCandidate(
        candidate_id=new_external_assimilation_candidate_id(),
        descriptor_id=descriptor.descriptor_id,
        source_id=source.source_id,
        candidate_type="tool",
        candidate_name=descriptor.capability_name,
        created_at=now,
    )
    note = ExternalCapabilityRiskNote(
        risk_note_id=new_external_capability_risk_note_id(),
        descriptor_id=descriptor.descriptor_id,
        candidate_id=candidate.candidate_id,
        risk_level="medium",
        risk_categories=["filesystem_write"],
        message="review",
        review_required=True,
        source_kind="tool",
        created_at=now,
        risk_attrs={},
    )

    assert source.to_dict()["source_id"].startswith("external_capability_source:")
    assert descriptor.to_dict()["descriptor_id"].startswith("external_capability_descriptor:")
    assert batch.to_dict()["batch_id"].startswith("external_capability_import_batch:")
    assert normalization.to_dict()["normalization_id"].startswith("external_capability_normalization:")
    assert candidate.to_dict()["candidate_id"].startswith("external_assimilation_candidate:")
    assert note.to_dict()["risk_note_id"].startswith("external_capability_risk_note:")
    assert candidate.execution_enabled is False
    assert candidate.activation_status == "disabled"
    assert descriptor.declared_entrypoint == "external.module:run"


def test_active_external_candidate_is_rejected() -> None:
    with pytest.raises(ExternalAssimilationCandidateError):
        ExternalAssimilationCandidate(
            candidate_id="external_assimilation_candidate:bad",
            descriptor_id="external_capability_descriptor:bad",
            source_id=None,
            candidate_type="tool",
            candidate_name="bad",
            activation_status="active",
            created_at=utc_now_iso(),
        )

    with pytest.raises(ExternalAssimilationCandidateError):
        ExternalAssimilationCandidate(
            candidate_id="external_assimilation_candidate:bad",
            descriptor_id="external_capability_descriptor:bad",
            source_id=None,
            candidate_type="tool",
            candidate_name="bad",
            execution_enabled=True,
            created_at=utc_now_iso(),
        )
