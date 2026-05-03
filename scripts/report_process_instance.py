from __future__ import annotations

import sys

from chanta_core.ocel.store import OCELStore
from chanta_core.pig.reports import PIGReportService


def find_recent_process_instance_id() -> str | None:
    process_instances = OCELStore().fetch_objects_by_type("process_instance")
    if not process_instances:
        return None
    return str(process_instances[-1]["object_id"])


def build_report(process_instance_id: str | None = None):
    process_instance_id = process_instance_id or find_recent_process_instance_id()
    if not process_instance_id:
        return None
    return PIGReportService().build_process_instance_report(process_instance_id)


def main() -> None:
    process_instance_id = sys.argv[1] if len(sys.argv) > 1 else None
    report = build_report(process_instance_id)
    if report is None:
        print("No process_instance found. Run a process trace first.")
        return
    print(report.report_text)


if __name__ == "__main__":
    main()
