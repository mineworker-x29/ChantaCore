from __future__ import annotations

from chanta_core.ocel.store import OCELStore
from chanta_core.ocel.validators import OCELValidator
from chanta_core.ocpx.loader import OCPXLoader
from chanta_core.pig.reports import PIGReportService


def main() -> None:
    store = OCELStore()
    report = PIGReportService(ocpx_loader=OCPXLoader(store=store)).build_recent_report(50)
    readiness = OCELValidator(store).validate_export_readiness()
    print(report.report_text)
    print("")
    print("Export Readiness:")
    print(f"- valid: {readiness['valid']}")
    print(f"- events: {readiness['event_count']}")
    print(f"- objects: {readiness['object_count']}")
    print(f"- relations: {readiness['relation_count']}")


if __name__ == "__main__":
    main()
