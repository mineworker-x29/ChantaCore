from chanta_core.cli.main import main


def test_cli_observe_propose_works(capsys):
    exit_code = main(["observe", "propose", "이 JSONL 로그 보고 이 agent가 뭘 했는지 봐줘"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Observation/Digestion Proposal" in captured.out
    assert "skill:agent_trace_observe" in captured.out
    assert "review_required=true" in captured.out
    assert "execution_performed=false" in captured.out


def test_cli_digest_propose_works(capsys):
    exit_code = main(["digest", "propose", "이 외부 skill 폴더를 소화해줘"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "skill:external_skill_source_inspect" in captured.out
    assert "skill:external_skill_static_digest" in captured.out
    assert "missing_inputs=" in captured.out


def test_cli_skills_propose_family_works(capsys):
    exit_code = main(
        [
            "skills",
            "propose",
            "--text",
            "JSONL trace를 관찰하고 external skill 후보로 소화해줘",
            "--family",
            "observation-digestion",
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "mixed_observation_digestion" in captured.out
    assert "execution_performed=false" in captured.out
