import json

from chanta_core.cli.main import main
from chanta_core.skills.proposal import SkillInvocationProposal
from chanta_core.skills.proposal_review import SkillProposalReviewService
from chanta_core.utility.time import utc_now_iso


def make_bridge_payload(root_path: str, *, decision: str = "approve") -> dict[str, object]:
    proposal = SkillInvocationProposal(
        proposal_id="skill_invocation_proposal:cli_bridge",
        intent_id="skill_proposal_intent:cli_bridge",
        requirement_id="skill_proposal_requirement:cli_bridge",
        skill_id="skill:read_workspace_text_file",
        proposal_status="proposed",
        invocation_mode="review_only",
        proposed_input_payload={"root_path": root_path, "relative_path": "note.txt"},
        missing_inputs=[],
        confidence=0.8,
        reason="cli bridge",
        review_required=True,
        executable_now=False,
        created_at=utc_now_iso(),
    )
    review_service = SkillProposalReviewService()
    review_result = review_service.review_proposal(
        proposal=proposal,
        decision=decision,
        reviewer_type="human",
        reviewer_id="tester",
        reason="approved" if decision == "approve" else "not approved",
    )
    return {
        "proposal": proposal.to_dict(),
        "review_decision": review_service.last_decision.to_dict(),
        "review_result": review_result.to_dict(),
    }


def test_cli_skill_bridge_executes_approved_json(tmp_path, capsys) -> None:
    (tmp_path / "note.txt").write_bytes(b"public-safe text")
    bridge_file = tmp_path / "bridge.json"
    bridge_file.write_bytes(json.dumps(make_bridge_payload(str(tmp_path))).encode("utf-8"))

    exit_code = main(["skill", "bridge", "--bridge-json-file", str(bridge_file)])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "status=bridged_executed" in captured.out
    assert "executed=true" in captured.out
    assert "gate_result_id=" in captured.out
    assert "explicit_invocation_result_id=" in captured.out


def test_cli_skill_bridge_rejects_unapproved_json(tmp_path, capsys) -> None:
    bridge_file = tmp_path / "bridge.json"
    bridge_file.write_bytes(json.dumps(make_bridge_payload(str(tmp_path), decision="reject")).encode("utf-8"))

    exit_code = main(["skill", "bridge", "--bridge-json-file", str(bridge_file)])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "status=bridge_denied" in captured.out
    assert "executed=false" in captured.out
    assert "first_violation_type=review_not_approved" in captured.out


def test_cli_skill_bridge_without_persistence_is_controlled(capsys) -> None:
    exit_code = main(["skill", "bridge", "skill_proposal_review_result:missing"])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "persistence is not available" in captured.err
    assert "Traceback" not in captured.err
