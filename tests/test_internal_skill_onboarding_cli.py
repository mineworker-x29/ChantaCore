import json

from chanta_core.cli.main import main
from chanta_core.skills.onboarding import InternalSkillOnboardingService


def test_cli_skills_onboarding_list(capsys) -> None:
    exit_code = main(["skills", "onboarding", "list"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Internal Skill Onboarding candidates" in captured.out
    assert "skill:workspace_summary_from_file" in captured.out


def test_cli_skills_onboarding_show(capsys) -> None:
    exit_code = main(["skills", "onboarding", "show", "skill:execution_audit"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Internal Skill Descriptor" in captured.out
    assert "enabled_by_default=false" in captured.out
    assert "runtime_registered=false" in captured.out


def test_cli_skills_onboarding_check_accepts_without_execution(capsys) -> None:
    exit_code = main(
        ["skills", "onboarding", "check", "--skill-id", "skill:workspace_summary_from_file"]
    )
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "status=accepted" in captured.out
    assert "accepted=true" in captured.out
    assert "enabled=false" in captured.out
    assert "skills_executed=false" in captured.out
    assert "runtime_registered=false" in captured.out


def test_cli_skills_onboarding_validate_descriptor_json_reports_needs_fix(tmp_path, capsys) -> None:
    service = InternalSkillOnboardingService()
    descriptor = service.create_descriptor(
        skill_id="skill:dummy_status",
        skill_name="Dummy Status",
        description="Descriptor only.",
        capability_category="runtime_status",
    )
    descriptor_file = tmp_path / "descriptor.json"
    descriptor_file.write_bytes(json.dumps(descriptor.to_dict()).encode("utf-8"))

    exit_code = main(
        [
            "skills",
            "onboarding",
            "validate",
            "--descriptor-json-file",
            str(descriptor_file),
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "status=needs_fix" in captured.out
    assert "first_finding_type=missing_input_contract" in captured.out


def test_cli_skills_onboarding_unknown_descriptor_is_controlled(capsys) -> None:
    exit_code = main(["skills", "onboarding", "check", "--skill-id", "skill:missing"])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "descriptor not found" in captured.err
    assert "Traceback" not in captured.err
