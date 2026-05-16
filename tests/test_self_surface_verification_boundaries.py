from __future__ import annotations

import json
from pathlib import Path

import pytest

from chanta_core.cli.main import main
from chanta_core.self_awareness import SelfSurfaceVerificationRequest, SelfSurfaceVerificationService


def _base_payload() -> dict:
    return {
        "candidate_id": "candidate:boundary",
        "review_status": "candidate_only",
        "canonical_promotion_enabled": False,
        "promoted": False,
        "effect_types": ["read_only_observation", "state_candidate_created"],
        "evidence_refs": [{"relative_path": "README.md", "line_number": 1}],
        "limitations": ["metadata_only"],
    }


def _verify(payload: dict):
    return SelfSurfaceVerificationService().verify_surface(
        SelfSurfaceVerificationRequest(
            target_type="project_structure_candidate",
            target_id=payload.get("candidate_id"),
            target_payload=payload,
        )
    )


@pytest.mark.parametrize(
    "flag",
    [
        "mutates_workspace",
        "mutates_memory",
        "mutates_persona",
        "mutates_overlay",
        "uses_shell",
        "uses_network",
        "uses_mcp",
        "loads_plugin",
        "executes_external_harness",
        "dangerous_capability",
    ],
)
def test_boundary_flags_are_detected(flag: str) -> None:
    payload = _base_payload()
    payload[flag] = True
    report = _verify(payload)
    assert report.status == "failed"
    assert any(item.finding_type in {"unexpected_mutation_flag", "unexpected_execution_flag"} for item in report.findings)


@pytest.mark.parametrize("flag", ["canonical_promotion_enabled", "promoted"])
def test_candidate_promotion_flags_are_detected(flag: str) -> None:
    payload = _base_payload()
    payload[flag] = True
    report = _verify(payload)
    assert report.status == "failed"
    assert any(item.finding_type == "candidate_promotion_violation" for item in report.findings)
    assert report.canonical_promotion_enabled is False
    assert report.promoted is False


def test_unredacted_secret_like_snippet_is_detected() -> None:
    payload = _base_payload()
    payload["matches"] = [
        {
            "relative_path": "README.md",
            "line_number": 1,
            "snippet": {"line": "password=RAW_SECRET_VALUE"},
        }
    ]
    report = _verify(payload)
    assert report.status == "failed"
    assert any(item.finding_type == "unredacted_secret_risk" for item in report.findings)
    assert "RAW_SECRET_VALUE" not in str([item.to_dict() for item in report.findings])


def test_missing_read_only_effect_warns() -> None:
    payload = _base_payload()
    payload["effect_types"] = ["state_candidate_created"]
    report = _verify(payload)
    assert report.status == "warning"
    assert any(item.finding_type == "unexpected_execution_flag" for item in report.findings)


def test_report_itself_remains_candidate_only() -> None:
    report = _verify(_base_payload())
    assert report.review_status == "candidate_only"
    assert report.canonical_promotion_enabled is False
    assert report.promoted is False
    assert report.report_attrs["workspace_write_used"] is False
    assert report.report_attrs["shell_execution_used"] is False
    assert report.report_attrs["network_access_used"] is False
    assert report.report_attrs["mcp_connection_used"] is False
    assert report.report_attrs["plugin_loading_used"] is False
    assert report.report_attrs["external_harness_execution_used"] is False
    assert report.report_attrs["model_judge_used"] is False
    assert report.report_attrs["memory_mutation_used"] is False
    assert report.report_attrs["persona_mutation_used"] is False
    assert report.report_attrs["overlay_mutation_used"] is False


def test_cli_failed_output_does_not_show_raw_secret(tmp_path: Path, capsys) -> None:
    payload = _base_payload()
    payload["snippet"] = "api_key=RAW_SECRET_VALUE"
    path = tmp_path / "bad.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    assert main(["self-awareness", "verify", "surface", "--target-payload", str(path)]) == 0
    output = capsys.readouterr().out
    assert "status=failed" in output
    assert "unredacted_secret_risk" in output
    assert "RAW_SECRET_VALUE" not in output
    assert "content_printed=false" in output
