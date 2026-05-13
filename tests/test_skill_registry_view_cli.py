from chanta_core.cli.main import main


def test_skill_registry_cli_list_works(capsys):
    exit_code = main(["skills", "registry", "list"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Skill Registry View" in captured.out
    assert "skill:agent_trace_observe" in captured.out
    assert "skills_executed=false" in captured.out


def test_skill_registry_cli_show_works(capsys):
    exit_code = main(["skills", "registry", "show", "skill:agent_trace_observe"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Skill Registry Detail" in captured.out
    assert "skill_id=skill:agent_trace_observe" in captured.out
    assert "execution_enabled=False" in captured.out


def test_skill_registry_cli_observation_and_digestion_filters(capsys):
    observation_code = main(["skills", "registry", "observation"])
    observation = capsys.readouterr()
    digestion_code = main(["skills", "registry", "digestion"])
    digestion = capsys.readouterr()

    assert observation_code == 0
    assert digestion_code == 0
    assert "internal_observation" in observation.out
    assert "internal_digestion" not in observation.out
    assert "internal_digestion" in digestion.out
    assert "internal_observation" not in digestion.out


def test_skill_registry_cli_risk_observability_and_findings(capsys):
    assert main(["skills", "registry", "risk"]) == 0
    risk = capsys.readouterr()
    assert "Skill Registry Risk" in risk.out
    assert "read_only=10" in risk.out

    assert main(["skills", "registry", "observability"]) == 0
    observability = capsys.readouterr()
    assert "Skill Registry Observability" in observability.out
    assert "pig_visible=true" in observability.out

    assert main(["skills", "registry", "findings"]) == 0
    findings = capsys.readouterr()
    assert "Skill Registry Findings" in findings.out
