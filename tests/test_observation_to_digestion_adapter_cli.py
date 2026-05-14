import json

from chanta_core.cli.main import main


def test_cli_digest_adapter_build_from_inference(tmp_path, capsys) -> None:
    path = tmp_path / "inference.json"
    payload = {
        "inference_id": "agent_behavior_inference_v2:public-dummy",
        "observed_run_id": "observed_agent_run:public-dummy",
        "inferred_goal": "inspect workspace",
        "inferred_goal_confidence": 0.9,
        "inferred_intent": "read only analysis",
        "inferred_task_type": "workspace_diagnostic",
        "inferred_action_sequence": ["read_object"],
        "inferred_skill_sequence": [],
        "inferred_tool_sequence": [],
        "touched_object_types": ["workspace_text"],
        "effect_profile": [],
        "outcome_inference": "completed",
        "outcome_confidence": 0.9,
        "confirmed_observations": ["public dummy observation"],
        "data_based_interpretations": [],
        "likely_hypotheses": [],
        "estimates": [],
        "unknown_or_needs_verification": [],
        "failure_signals": [],
        "recovery_signals": [],
        "evidence_refs": ["evidence:public-dummy"],
        "uncertainty_notes": [],
        "withdrawal_conditions": ["withdraw if dummy evidence is replaced"],
        "created_at": "2026-01-01T00:00:00Z",
        "inference_attrs": {},
    }
    path.write_bytes(json.dumps(payload).encode("utf-8"))

    assert main(["digest", "adapter-build", "from-inference", "--inference-json-file", str(path)]) == 0
    out = capsys.readouterr().out
    assert "Observation-to-Digestion Adapter Build" in out
    assert "observed_capabilities=1" in out
    assert "target_skill_candidates=1" in out
    assert "adapter_candidates=1" in out
    assert "review_status=pending_review" in out
    assert "canonical_import_enabled=false" in out
    assert "execution_enabled=false" in out

