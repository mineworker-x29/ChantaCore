from chanta_core.ocel.store import OCELStore
from chanta_core.ocpx.loader import OCPXLoader
from chanta_core.pig.feedback import PIGFeedbackService
from tests.test_ocel_store import make_record


def test_pig_context_includes_conformance_report_by_default(tmp_path) -> None:
    store = OCELStore(tmp_path / "pig_context_conformance.sqlite")
    store.append_record(make_record())
    service = PIGFeedbackService(ocpx_loader=OCPXLoader(store=store))

    context = service.build_recent_context(limit=20)

    assert context.conformance_report is not None
    assert context.conformance_report["status"] in {
        "conformant",
        "warning",
        "nonconformant",
        "unknown",
    }
    assert "Conformance" in context.context_text


def test_pig_context_can_exclude_conformance_report(tmp_path) -> None:
    store = OCELStore(tmp_path / "pig_context_no_conformance.sqlite")
    store.append_record(make_record())
    service = PIGFeedbackService(ocpx_loader=OCPXLoader(store=store))

    context = service.build_recent_context(limit=20, include_conformance=False)

    assert context.conformance_report is None
    assert "Conformance" not in context.context_text
