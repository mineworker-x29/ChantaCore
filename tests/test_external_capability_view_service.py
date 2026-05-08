from pathlib import Path

from chanta_core.external import ExternalCapabilityImportService, ExternalCapabilityRegistryViewService
from chanta_core.ocel.store import OCELStore
from chanta_core.traces.trace_service import TraceService


def _objects(trace_service):
    service = ExternalCapabilityImportService(trace_service=trace_service)
    source = service.register_source(source_name="provided", source_type="provided_dict", trust_level="untrusted")
    descriptor, normalization, candidate = service.import_as_disabled_candidate(
        raw_descriptor={
            "name": "external_writer",
            "type": "tool",
            "permissions": ["write_file", "shell"],
            "risks": ["filesystem_write", "shell_execution"],
        },
        source=source,
    )
    note = service.record_risk_note(
        descriptor_id=descriptor.descriptor_id,
        candidate_id=candidate.candidate_id,
        risk_level="high",
        risk_categories=["shell_execution"],
        message="Review.",
    )
    return source, descriptor, normalization, candidate, note


def test_view_service_build_render_write_and_refresh(tmp_path) -> None:
    store = OCELStore(tmp_path / "external_views.sqlite")
    trace_service = TraceService(ocel_store=store)
    source, descriptor, normalization, candidate, note = _objects(trace_service)
    original_candidate = candidate.to_dict()
    service = ExternalCapabilityRegistryViewService(trace_service=trace_service, root=tmp_path)

    snapshot = service.build_registry_snapshot(
        sources=[source],
        descriptors=[descriptor],
        normalizations=[normalization],
        candidates=[candidate],
        risk_notes=[note],
    )
    views = service.render_default_external_views(
        root=tmp_path,
        sources=[source],
        descriptors=[descriptor],
        normalizations=[normalization],
        candidates=[candidate],
        risk_notes=[note],
    )
    result = service.write_view(
        view=views["external_capabilities"],
        target_path=views["external_capabilities"].target_path,
    )
    refreshed = service.refresh_default_external_views(
        root=tmp_path,
        sources=[source],
        descriptors=[descriptor],
        normalizations=[normalization],
        candidates=[candidate],
        risk_notes=[note],
    )

    assert snapshot.disabled_candidate_count == 1
    assert set(views) == {"external_capabilities", "external_review", "external_risks"}
    assert result.written is True
    assert (tmp_path / ".chanta" / "EXTERNAL_CAPABILITIES.md").exists()
    assert (tmp_path / ".chanta" / "EXTERNAL_REVIEW.md").exists()
    assert (tmp_path / ".chanta" / "EXTERNAL_RISKS.md").exists()
    assert all(item.written for item in refreshed.values())
    assert candidate.to_dict() == original_candidate
    assert candidate.execution_enabled is False
    assert candidate.activation_status == "disabled"


def test_write_view_does_not_parse_markdown_back_into_state(tmp_path) -> None:
    service = ExternalCapabilityRegistryViewService(root=tmp_path)
    target = tmp_path / ".chanta" / "EXTERNAL_CAPABILITIES.md"
    result = service.write_view(view="Generated materialized view.\nCanonical source: OCEL.\n", target_path=target)

    assert result.written is True
    assert Path(result.target_path).read_text(encoding="utf-8").startswith("Generated materialized view.")
