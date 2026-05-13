import json

from chanta_core.cli.main import main
from chanta_core.skills.proposal import SkillInvocationProposal
from chanta_core.utility.time import utc_now_iso


def make_proposal_dict(*, missing_inputs: list[str] | None = None) -> dict[str, object]:
    return SkillInvocationProposal(
        proposal_id="skill_invocation_proposal:cli",
        intent_id="skill_proposal_intent:cli",
        requirement_id="skill_proposal_requirement:cli",
        skill_id="skill:read_workspace_text_file",
        proposal_status="incomplete" if missing_inputs else "proposed",
        invocation_mode="review_only",
        proposed_input_payload={"root_path": "<WORKSPACE_ROOT>", "relative_path": "docs/example.txt"},
        missing_inputs=list(missing_inputs or []),
        confidence=0.8,
        reason="cli test",
        review_required=True,
        executable_now=False,
        created_at=utc_now_iso(),
    ).to_dict()


def test_cli_skill_review_from_json_file_approves_without_execution(tmp_path, capsys) -> None:
    proposal_file = tmp_path / "proposal.json"
    proposal_file.write_bytes(json.dumps(make_proposal_dict()).encode("utf-8"))

    exit_code = main(
        [
            "skill",
            "review",
            "--from-proposal-json-file",
            str(proposal_file),
            "--decision",
            "approve",
            "--reason",
            "complete read-only proposal",
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "status=approved" in captured.out
    assert "bridge_candidate=true" in captured.out
    assert "skills_executed=false" in captured.out
    assert "explicit_invocation_called=false" in captured.out
    assert "execution_gate_called=false" in captured.out


def test_cli_skill_review_missing_input_reports_needs_more_input(tmp_path, capsys) -> None:
    proposal_file = tmp_path / "proposal.json"
    proposal_file.write_bytes(
        json.dumps(make_proposal_dict(missing_inputs=["root_path"])).encode("utf-8")
    )

    exit_code = main(
        [
            "skill",
            "review",
            "--from-proposal-json-file",
            str(proposal_file),
            "--decision",
            "approve",
            "--reason",
            "try approve",
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "status=needs_more_input" in captured.out
    assert "bridge_candidate=false" in captured.out
    assert "first_finding_type=missing_input" in captured.out


def test_cli_skill_review_without_persistence_is_controlled(capsys) -> None:
    exit_code = main(["skill", "review", "skill_invocation_proposal:missing", "--decision", "reject"])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "proposal persistence is not available" in captured.err
    assert "Traceback" not in captured.err
