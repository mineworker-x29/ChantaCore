import pytest

from chanta_core.ocel.store import OCELStore
from chanta_core.traces.trace_service import TraceService
from chanta_core.verification import VerificationService
from chanta_core.verification.errors import VerificationError
from chanta_core.verification.read_only_skills import ReadOnlyVerificationSkillService


def make_service(tmp_path, *, store: OCELStore | None = None) -> ReadOnlyVerificationSkillService:
    store = store or OCELStore(tmp_path / "read_only_skills.sqlite")
    verification_service = VerificationService(trace_service=TraceService(ocel_store=store))
    return ReadOnlyVerificationSkillService(
        verification_service=verification_service,
        root=tmp_path,
        ocel_store=store,
    )


def test_list_skills_includes_required_skills(tmp_path) -> None:
    service = make_service(tmp_path)
    names = {spec.skill_name for spec in service.list_skills()}

    assert {
        "verify_file_exists",
        "verify_path_type",
        "verify_tool_available",
        "verify_runtime_python_info",
        "verify_ocel_object_type_exists",
        "verify_ocel_event_activity_exists",
        "verify_materialized_view_warning",
        "verify_tool_registry_view_warning",
    }.issubset(names)


def test_verify_file_exists_passes_and_fails(tmp_path) -> None:
    service = make_service(tmp_path)
    existing = tmp_path / "exists.txt"
    existing.write_text("present", encoding="utf-8")

    passed = service.verify_file_exists(path="exists.txt")
    failed = service.verify_file_exists(path="missing.txt")

    assert passed.status == "passed"
    assert failed.status == "failed"


def test_verify_path_type_file_directory_any(tmp_path) -> None:
    service = make_service(tmp_path)
    file_path = tmp_path / "file.txt"
    file_path.write_text("present", encoding="utf-8")
    directory = tmp_path / "dir"
    directory.mkdir()

    assert service.verify_path_type(path="file.txt", expected_type="file").status == "passed"
    assert service.verify_path_type(path="dir", expected_type="directory").status == "passed"
    assert service.verify_path_type(path="dir", expected_type="any").status == "passed"
    assert service.verify_path_type(path="dir", expected_type="file").status == "failed"
    with pytest.raises(VerificationError):
        service.verify_path_type(path="dir", expected_type="socket")


def test_verify_tool_available_uses_path_resolution_without_execution(tmp_path, monkeypatch) -> None:
    service = make_service(tmp_path)
    calls: list[str] = []

    def fake_which(tool_name: str) -> str | None:
        calls.append(tool_name)
        return "C:/fake/python.exe" if tool_name == "python" else None

    monkeypatch.setattr("chanta_core.verification.read_only_skills.shutil.which", fake_which)

    passed = service.verify_tool_available(tool_name="python")
    failed = service.verify_tool_available(tool_name="missing-tool")

    assert calls == ["python", "missing-tool"]
    assert passed.status == "passed"
    assert failed.status == "failed"
    assert passed.result_attrs["outcome"]["outcome_attrs"]["executed"] is False


def test_verify_runtime_python_info_records_runtime_status(tmp_path) -> None:
    service = make_service(tmp_path)

    result = service.verify_runtime_python_info()

    assert result.status == "passed"
    assert result.result_attrs["outcome"]["evidence_kind"] == "runtime_status"


def test_ocel_object_type_and_event_activity_fallbacks(tmp_path) -> None:
    service = make_service(tmp_path)

    object_result = service.verify_ocel_object_type_exists(
        object_type="verification_result",
        known_object_types=["verification_result"],
    )
    event_result = service.verify_ocel_event_activity_exists(
        event_activity="verification_result_recorded",
        known_event_activities=["verification_result_recorded"],
    )
    missing = service.verify_ocel_event_activity_exists(
        event_activity="not_seen",
        known_event_activities=[],
    )

    assert object_result.status == "passed"
    assert event_result.status == "passed"
    assert missing.status == "failed"


def test_materialized_view_warning_passes_and_fails(tmp_path) -> None:
    service = make_service(tmp_path)
    good = tmp_path / "MEMORY.md"
    bad = tmp_path / "BAD.md"
    good.write_text(
        "Generated materialized view\nCanonical source: OCEL\nThis file is not canonical.\nEdits do not update canonical source.",
        encoding="utf-8",
    )
    bad.write_text("plain note", encoding="utf-8")

    assert service.verify_materialized_view_warning(path="MEMORY.md").status == "passed"
    assert service.verify_materialized_view_warning(path="BAD.md").status == "failed"


def test_tool_registry_view_warning_passes_and_fails(tmp_path) -> None:
    service = make_service(tmp_path)
    good = tmp_path / "TOOL_POLICY.md"
    bad = tmp_path / "BAD_TOOL_POLICY.md"
    good.write_text(
        "This file is not PermissionPolicy. It does not grant, deny, allow, ask, block, or sandbox tool usage. Enforcement belongs to a future permission layer.",
        encoding="utf-8",
    )
    bad.write_text("tool list", encoding="utf-8")

    assert service.verify_tool_registry_view_warning(path="TOOL_POLICY.md").status == "passed"
    assert service.verify_tool_registry_view_warning(path="BAD_TOOL_POLICY.md").status == "failed"


def test_run_skill_dispatches_known_local_methods_only(tmp_path) -> None:
    service = make_service(tmp_path)
    result = service.run_skill(
        skill_name="verify_runtime_python_info",
        kwargs={},
    )

    assert result.status == "passed"
    with pytest.raises(VerificationError):
        service.run_skill(skill_name="external_skill", kwargs={})
