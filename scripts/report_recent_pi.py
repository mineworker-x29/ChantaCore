from __future__ import annotations

import json

from chanta_core.pig.reports import PIGReportService


def build_report(limit: int = 50):
    return PIGReportService().build_recent_report(limit=limit)


def main() -> None:
    report = build_report()
    print(report.report_text)
    print(
        "summary:",
        json.dumps(
            {
                "scope": report.scope,
                "event_count": len(report.activity_sequence),
                "conformance_status": (report.conformance_report or {}).get("status"),
            },
            ensure_ascii=False,
            sort_keys=True,
        ),
    )


if __name__ == "__main__":
    main()
