from __future__ import annotations

import sys

from chanta_core.ocel.store import OCELStore
from chanta_core.pig.reports import PIGReportService


def find_recent_session_id() -> str | None:
    events = OCELStore().fetch_recent_events(limit=1)
    if not events:
        return None
    session_id = events[0].get("event_attrs", {}).get("session_id")
    return str(session_id) if session_id else None


def build_report(session_id: str | None = None):
    session_id = session_id or find_recent_session_id()
    if not session_id:
        return None
    return PIGReportService().build_session_report(session_id)


def main() -> None:
    session_id = sys.argv[1] if len(sys.argv) > 1 else None
    report = build_report(session_id)
    if report is None:
        print("No session found. Run a process trace first.")
        return
    print(report.report_text)


if __name__ == "__main__":
    main()
