from chanta_core.external import ExternalCapabilityImportService, ExternalCapabilityRegistryViewService
from chanta_core.external.views import (
    render_external_capabilities_view,
    render_external_review_view,
    render_external_risks_view,
)
from chanta_core.ocel.store import OCELStore
from chanta_core.traces.trace_service import TraceService


def _sample_objects(tmp_path, include_enabled: bool = False):
    service = ExternalCapabilityImportService(
        trace_service=TraceService(ocel_store=OCELStore(tmp_path / "view_renderers.sqlite")),
    )
    source = service.register_source(
        source_name="provided",
        source_type="provided_dict",
        trust_level="untrusted",
    )
    descriptor, normalization, candidate = service.import_as_disabled_candidate(
        raw_descriptor={
            "name": "z_writer",
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
    if include_enabled:
        object.__setattr__(candidate, "execution_enabled", True)
    snapshot = ExternalCapabilityRegistryViewService().build_registry_snapshot(
        sources=[source],
        descriptors=[descriptor],
        normalizations=[normalization],
        candidates=[candidate],
        risk_notes=[note],
    )
    return source, descriptor, normalization, candidate, note, snapshot


def test_capabilities_view_warnings_and_disabled_candidates(tmp_path) -> None:
    source, descriptor, normalization, candidate, note, snapshot = _sample_objects(tmp_path)

    view = render_external_capabilities_view(
        snapshot=snapshot,
        sources=[source],
        descriptors=[descriptor],
        normalizations=[normalization],
        candidates=[candidate],
        risk_notes=[note],
        target_path=".chanta/EXTERNAL_CAPABILITIES.md",
    )

    assert "Generated materialized view." in view.content
    assert "Canonical source: OCEL." in view.content
    assert "not the canonical external capability registry" in view.content
    assert "Edits to this file do not enable or disable capabilities." in view.content
    assert "No external capability is executable from this view." in view.content
    assert "## Disabled Candidates" in view.content
    assert candidate.candidate_id in view.content
    assert view.canonical is False


def test_review_and_risk_views_state_boundaries(tmp_path) -> None:
    source, descriptor, normalization, candidate, note, snapshot = _sample_objects(tmp_path)

    review = render_external_review_view(
        snapshot=snapshot,
        candidates=[candidate],
        descriptors=[descriptor],
        risk_notes=[note],
        target_path=".chanta/EXTERNAL_REVIEW.md",
    )
    risks = render_external_risks_view(
        snapshot=snapshot,
        risk_notes=[note],
        descriptors=[descriptor],
        candidates=[candidate],
        target_path=".chanta/EXTERNAL_RISKS.md",
    )

    assert "This file is not a review queue." in review.content
    assert "does not approve, reject, activate" in review.content
    assert "Formal review workflow belongs to a later version." in review.content
    assert "This file is not an enforcement policy." in risks.content
    assert "does not block or allow external capabilities" in risks.content
    assert "Risk notes are advisory records only." in risks.content


def test_execution_enabled_candidates_produce_warning_and_output_is_deterministic(tmp_path) -> None:
    source, descriptor, normalization, candidate, note, snapshot = _sample_objects(tmp_path, include_enabled=True)

    first = render_external_capabilities_view(
        snapshot=snapshot,
        sources=[source],
        descriptors=[descriptor],
        normalizations=[normalization],
        candidates=[candidate],
        risk_notes=[note],
        target_path=".chanta/EXTERNAL_CAPABILITIES.md",
    )
    second = render_external_capabilities_view(
        snapshot=snapshot,
        sources=[source],
        descriptors=[descriptor],
        normalizations=[normalization],
        candidates=[candidate],
        risk_notes=[note],
        target_path=".chanta/EXTERNAL_CAPABILITIES.md",
    )

    assert "## Execution-Enabled Warning" in first.content
    assert first.content == second.content
