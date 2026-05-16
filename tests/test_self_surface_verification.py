from __future__ import annotations

import json
from pathlib import Path

from chanta_core.cli.main import main
from chanta_core.self_awareness import (
    READ_ONLY_OBSERVATION_EFFECT,
    SelfAwarenessRegistryService,
    SelfAwarenessReportService,
    SelfSurfaceVerificationRequest,
    SelfSurfaceVerificationService,
)
from chanta_core.skills.execution_gate import SkillExecutionGateService
from chanta_core.skills.invocation import ExplicitSkillInvocationService


def _valid_project_payload() -> dict:
    return {
        "candidate_id": "candidate:project",
        "review_status": "candidate_only",
        "canonical_promotion_enabled": False,
        "promoted": False,
        "effect_types": ["read_only_observation", "state_candidate_created"],
        "tree_nodes": [{"relative_path": "README.md", "node_type": "file"}],
        "surface_candidates": [
            {
                "candidate_type": "readme",
                "relative_path": "README.md",
                "reason": "README filename pattern",
                "evidence_refs": [{"relative_path": "README.md"}],
            }
        ],
        "evidence_refs": [{"relative_path": ".", "line_number": 1}],
        "limitations": ["metadata_only_surface_mapping"],
    }


def _verify(target_type: str, payload: dict, *, strictness: str = "standard"):
    return SelfSurfaceVerificationService().verify_surface(
        SelfSurfaceVerificationRequest(
            target_type=target_type,
            target_id=payload.get("candidate_id"),
            target_payload=payload,
            strictness=strictness,
        )
    )


def test_valid_project_structure_candidate_passes() -> None:
    report = _verify("project_structure_candidate", _valid_project_payload())
    assert report.status == "passed"
    assert report.review_status == "candidate_only"
    assert report.canonical_promotion_enabled is False
    assert report.promoted is False
    assert report.evidence_coverage["coverage_status"] == "sufficient"
    assert report.boundary_status["boundary_status"] == "ok"
    assert report.candidate_status["candidate_status"] == "ok"
    assert READ_ONLY_OBSERVATION_EFFECT in report.report_attrs["effect_types"]
    assert "state_candidate_created" in report.report_attrs["effect_types"]


def test_missing_evidence_and_invalid_line_refs_are_findings() -> None:
    missing = _valid_project_payload()
    missing["evidence_refs"] = []
    report = _verify("project_structure_candidate", missing)
    assert report.status == "warning"
    assert any(item.finding_type == "missing_evidence_ref" for item in report.findings)

    invalid = _valid_project_payload()
    invalid["evidence_refs"] = [{"relative_path": "README.md", "line_number": 0}]
    report = _verify("project_structure_candidate", invalid)
    assert any(item.finding_type == "invalid_line_ref" for item in report.findings)


def test_search_markdown_and_python_evidence_findings() -> None:
    search = {
        "effect_types": ["read_only_observation"],
        "matches": [{"relative_path": "", "line_number": None}],
        "evidence_refs": [{"relative_path": "app.py"}],
    }
    search_report = _verify("workspace_search_result", search)
    assert search_report.status == "failed"
    assert any(item.finding_type == "search_match_without_source" for item in search_report.findings)

    structure = {
        "effect_types": ["read_only_observation", "state_candidate_created"],
        "review_status": "candidate_only",
        "canonical_promotion_enabled": False,
        "promoted": False,
        "markdown": {"headings": [{"title": "Missing line"}]},
        "python": {"imports": [{"name": "os"}], "top_level_functions": [], "top_level_classes": [], "top_level_assignments": []},
        "evidence_refs": [{"relative_path": "README.md"}],
    }
    structure_report = _verify("structure_summary_candidate", structure)
    assert any(item.finding_type == "invalid_line_ref" for item in structure_report.findings)


def test_surface_candidate_and_truncation_findings() -> None:
    weak = {
        "effect_types": ["read_only_observation", "state_candidate_created"],
        "candidate_type": "readme",
        "relative_path": "README.md",
        "evidence_refs": [{"relative_path": "README.md"}],
    }
    weak_report = _verify("surface_candidate", weak)
    assert any(item.finding_type == "project_surface_candidate_weak_evidence" for item in weak_report.findings)

    truncated = _valid_project_payload()
    truncated["truncated"] = True
    truncated["limitations"] = []
    truncated_report = _verify("project_structure_candidate", truncated)
    assert any(item.finding_type == "truncated_result_requires_limitation" for item in truncated_report.findings)


def test_unsupported_target_type_blocks_and_strict_upgrades_warning() -> None:
    blocked = _verify("unsupported", {})
    assert blocked.status == "blocked"
    assert any(item.finding_type == "unsupported_target_type" for item in blocked.findings)

    missing = _valid_project_payload()
    missing["evidence_refs"] = []
    strict = _verify("project_structure_candidate", missing, strictness="strict")
    assert strict.status == "failed"
    assert any(item.severity == "error" for item in strict.findings)


def test_surface_verify_contract_and_gate(tmp_path: Path) -> None:
    registry = SelfAwarenessRegistryService()
    contract = registry.get_contract("skill:self_awareness_surface_verify")
    assert contract is not None
    assert contract.implementation_status == "implemented"
    assert contract.effect_type == READ_ONLY_OBSERVATION_EFFECT
    assert contract.execution_enabled is False
    assert contract.canonical_mutation_enabled is False
    assert contract.risk_profile.mutates_workspace is False
    assert contract.risk_profile.mutates_memory is False
    assert contract.risk_profile.mutates_persona is False
    assert contract.risk_profile.uses_shell is False
    assert contract.risk_profile.uses_network is False
    assert contract.risk_profile.uses_mcp is False
    assert contract.risk_profile.loads_plugin is False
    assert contract.risk_profile.executes_external_harness is False
    assert contract.risk_profile.dangerous_capability is False

    invocation = ExplicitSkillInvocationService()
    gate = SkillExecutionGateService(explicit_skill_invocation_service=invocation)
    result = gate.gate_explicit_invocation(
        skill_id="skill:self_awareness_surface_verify",
        input_payload={
            "root_path": str(tmp_path),
            "target_type": "project_structure_candidate",
            "target_payload": _valid_project_payload(),
        },
    )
    output = invocation.last_result.output_payload["output_attrs"]
    assert result.executed is True
    assert output["review_status"] == "candidate_only"
    assert output["canonical_promotion_enabled"] is False
    assert output["report_attrs"]["test_execution_used"] is False


def test_cli_verify_surface_with_payload(tmp_path: Path, capsys) -> None:
    payload_path = tmp_path / "payload.json"
    payload_path.write_text(json.dumps(_valid_project_payload()), encoding="utf-8")

    assert main(["self-awareness", "verify", "surface", "--target-payload", str(payload_path)]) == 0
    output = capsys.readouterr().out
    assert "Self-Surface Verification" in output
    assert "status=passed" in output
    assert "canonical_promotion_enabled=false" in output
    assert "promoted=false" in output
    assert "content_printed=false" in output


def test_pig_and_ocpx_surface_verification_coverage() -> None:
    reports = SelfAwarenessReportService()
    pig = reports.build_pig_report()
    ocpx = reports.build_ocpx_projection()
    assert pig["version"] == "0.20.9"
    assert pig["state"] == "self_awareness_foundation_v1_consolidated"
    assert pig["workspace_awareness_coverage"]["surface_verification"] == "implemented_evidence_boundary_candidate_checks"
    assert pig["llm_judge_enabled"] is False
    assert pig["test_execution_enabled"] is False
    assert pig["shell_execution_enabled"] is False
    assert ocpx["state"] == "self_awareness_foundation_v1_consolidated"
    assert "surface_verification_report" in ocpx["candidate_types"]
    assert "self_surface_verification_report_created" in ocpx["event_coverage"]
