from tests.test_pig_reports import seed_trace

from chanta_core.ocel.store import OCELStore
from chanta_core.ocpx.loader import OCPXLoader
from chanta_core.pig.reports import PIGReportService


def test_pig_report_text_has_operator_sections(tmp_path) -> None:
    store = OCELStore(tmp_path / "quality.sqlite")
    seed_trace(store)
    report = PIGReportService(ocpx_loader=OCPXLoader(store=store)).build_recent_report(50)

    for section in [
        "ChantaCore PI Report",
        "Trace",
        "Objects",
        "Relation",
        "Variant",
        "Performance Precursor",
        "Conformance",
        "Guidance / Decision",
        "Skill Usage",
        "Tool Usage",
        "Editing / Patch",
        "Worker / Scheduler",
        "Human / External PI",
    ]:
        assert section in report.report_text
    data = report.to_dict()
    assert data["report_attrs"]["read_only"] is True
    assert "worker_summary" in data["report_attrs"]
