from pathlib import Path

from chanta_core.external import ExternalCapabilityImportService, infer_risk_level
from chanta_core.ocel.store import OCELStore
from chanta_core.traces.trace_service import TraceService


def main() -> None:
    db_path = Path(".pytest-tmp") / "external_capability_import_script.sqlite"
    service = ExternalCapabilityImportService(
        trace_service=TraceService(ocel_store=OCELStore(db_path)),
    )
    source = service.register_source(
        source_name="provided external descriptor",
        source_type="provided_dict",
        trust_level="untrusted",
    )
    raw_descriptor = {
        "name": "external_file_writer",
        "type": "tool",
        "description": "External descriptor imported as metadata only.",
        "permissions": ["write_file", "shell"],
        "risks": ["filesystem_write", "shell_execution"],
        "entrypoint": "external.module:run",
    }
    descriptor = service.import_descriptor(raw_descriptor=raw_descriptor, source_id=source.source_id)
    normalization = service.normalize_descriptor(descriptor=descriptor)
    risk_note = service.record_risk_note(
        descriptor_id=descriptor.descriptor_id,
        risk_level=infer_risk_level(normalization.normalized_risk_categories),
        risk_categories=normalization.normalized_risk_categories,
        message="Review required before any activation.",
    )
    candidate = service.create_assimilation_candidate(
        descriptor=descriptor,
        normalization=normalization,
        linked_risk_note_ids=[risk_note.risk_note_id],
    )

    print(f"source_id={source.source_id}")
    print(f"descriptor_id={descriptor.descriptor_id} status={descriptor.status}")
    print(f"normalization_id={normalization.normalization_id} status={normalization.status}")
    print(f"risk_note_id={risk_note.risk_note_id} risk_level={risk_note.risk_level}")
    print(
        "candidate_id="
        f"{candidate.candidate_id} activation_status={candidate.activation_status} "
        f"execution_enabled={candidate.execution_enabled}"
    )
    assert candidate.execution_enabled is False
    assert candidate.activation_status == "disabled"
    assert descriptor.declared_entrypoint == "external.module:run"


if __name__ == "__main__":
    main()
