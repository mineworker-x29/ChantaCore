from __future__ import annotations

from chanta_core.pig.conformance import PIGConformanceService


def main() -> None:
    report = PIGConformanceService().check_recent(limit=20)

    print("status:", report.status)
    print("issue_count:", len(report.issues))
    for issue in report.issues[:5]:
        print(f"- [{issue.severity}] {issue.issue_type}: {issue.title}")


if __name__ == "__main__":
    main()
