from __future__ import annotations

from pathlib import Path

from chanta_core.ocel.store import OCELStore
from chanta_core.traces.trace_service import TraceService
from chanta_core.verification import VerificationService
from chanta_core.verification.read_only_skills import ReadOnlyVerificationSkillService


def main() -> int:
    store = OCELStore(Path("data/verification/test_read_only_verification_skills.sqlite"))
    verification_service = VerificationService(trace_service=TraceService(ocel_store=store))
    skill_service = ReadOnlyVerificationSkillService(
        verification_service=verification_service,
        root=Path("."),
        ocel_store=store,
    )

    results = [
        skill_service.verify_file_exists(path="pyproject.toml"),
        skill_service.verify_tool_available(tool_name="python"),
        skill_service.verify_runtime_python_info(),
        skill_service.verify_ocel_object_type_exists(
            object_type="verification_result",
            known_object_types=["verification_result"],
        ),
        skill_service.verify_ocel_event_activity_exists(
            event_activity="verification_result_recorded",
            known_event_activities=["verification_result_recorded"],
        ),
    ]

    for result in results:
        print(f"{result.result_id}: {result.status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
