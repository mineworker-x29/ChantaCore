from pathlib import Path

from chanta_core.external import ExternalCapabilityImportService, ExternalCapabilityRegistryViewService
from chanta_core.ocel.store import OCELStore
from chanta_core.traces.trace_service import TraceService


def main() -> None:
    root = Path(".pytest-tmp") / "external_capability_views_script"
    store = OCELStore(root / "external_capability_views.sqlite")
    trace_service = TraceService(ocel_store=store)
    import_service = ExternalCapabilityImportService(trace_service=trace_service)
    view_service = ExternalCapabilityRegistryViewService(trace_service=trace_service, root=root)

    source = import_service.register_source(
        source_name="provided descriptor",
        source_type="provided_dict",
        trust_level="untrusted",
    )
    descriptor, normalization, candidate = import_service.import_as_disabled_candidate(
        raw_descriptor={
            "name": "external_file_writer",
            "type": "tool",
            "description": "External descriptor imported as metadata only.",
            "permissions": ["write_file", "shell"],
            "risks": ["filesystem_write", "shell_execution"],
            "entrypoint": "external.module:run",
        },
        source=source,
    )
    risk_notes = [
        import_service.record_risk_note(
            descriptor_id=descriptor.descriptor_id,
            candidate_id=candidate.candidate_id,
            risk_level="high",
            risk_categories=normalization.normalized_risk_categories,
            message="Review required before any activation.",
        )
    ]
    results = view_service.refresh_default_external_views(
        root=root,
        sources=[source],
        descriptors=[descriptor],
        normalizations=[normalization],
        candidates=[candidate],
        risk_notes=risk_notes,
    )

    for key, result in results.items():
        print(f"{key}: {result.target_path} written={result.written}")
        lines = Path(result.target_path).read_text(encoding="utf-8").splitlines()[:6]
        for line in lines:
            print(f"  {line}")
    assert candidate.execution_enabled is False
    assert candidate.activation_status == "disabled"


if __name__ == "__main__":
    main()
