from __future__ import annotations

from pathlib import Path

import pytest

from chanta_core.cli.main import main
from chanta_core.self_awareness import (
    READ_ONLY_OBSERVATION_EFFECT,
    SelfAwarenessRegistryService,
    SelfAwarenessReportService,
    SelfProjectStructureAwarenessService,
    SelfProjectStructureRequest,
    SelfWorkspacePathPolicyService,
)
from chanta_core.skills.execution_gate import SkillExecutionGateService
from chanta_core.skills.invocation import ExplicitSkillInvocationService


@pytest.fixture()
def fixture_project(tmp_path: Path) -> Path:
    (tmp_path / "README.md").write_text("# Demo\nbody must not appear\n", encoding="utf-8")
    (tmp_path / "pyproject.toml").write_text("[project]\nname='demo'\n", encoding="utf-8")
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "main.py").write_text("import os\nVALUE = 1\n", encoding="utf-8")
    (tmp_path / "app.py").write_text("print('no execution')\n", encoding="utf-8")
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_demo.py").write_text("def test_demo():\n    assert True\n", encoding="utf-8")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "guide.md").write_text("# Guide\n", encoding="utf-8")
    (tmp_path / ".github" / "workflows").mkdir(parents=True)
    (tmp_path / ".github" / "workflows" / "ci.yml").write_text("name: ci\n", encoding="utf-8")
    (tmp_path / "azure-pipelines.yml").write_text("trigger: none\n", encoding="utf-8")
    (tmp_path / "config.yaml").write_text("password: SECRET\n", encoding="utf-8")
    (tmp_path / ".hidden").write_text("hidden\n", encoding="utf-8")
    (tmp_path / "node_modules").mkdir()
    (tmp_path / "node_modules" / "ignored.js").write_text("ignored\n", encoding="utf-8")
    return tmp_path


def _service(root: Path) -> SelfProjectStructureAwarenessService:
    return SelfProjectStructureAwarenessService(
        path_policy_service=SelfWorkspacePathPolicyService(workspace_root=root)
    )


def test_project_structure_candidate_builds_metadata_only_surface(fixture_project: Path) -> None:
    candidate = _service(fixture_project).inspect_project_structure(SelfProjectStructureRequest(max_depth=4))

    paths = {node.relative_path for node in candidate.tree_nodes}
    surface_types = {item.candidate_type for item in candidate.surface_candidates}
    assert candidate.review_status == "candidate_only"
    assert candidate.canonical_promotion_enabled is False
    assert candidate.promoted is False
    assert candidate.relative_path == "."
    assert "README.md" in paths
    assert "src" in paths
    assert "tests" in paths
    assert "body must not appear" not in str(candidate.to_dict())
    assert candidate.file_distribution.by_suffix[".py"] >= 2
    assert candidate.file_distribution.by_top_level_dir["src"] >= 1
    assert {"readme", "docs_root", "source_root", "test_root", "dependency_manifest", "entrypoint_file", "ci_config", "config_file"} <= surface_types
    assert candidate.candidate_attrs["metadata_only_tree"] is True
    assert candidate.candidate_attrs["llm_architecture_inference_used"] is False
    assert candidate.candidate_attrs["dependency_graph_created"] is False
    assert candidate.candidate_attrs["import_resolution_used"] is False
    assert candidate.candidate_attrs["runtime_introspection_used"] is False


def test_tree_nodes_are_workspace_relative_and_have_metadata(fixture_project: Path) -> None:
    candidate = _service(fixture_project).inspect_project_structure(SelfProjectStructureRequest(max_depth=3))
    for node in candidate.tree_nodes:
        assert not Path(node.relative_path).is_absolute()
        assert node.node_type in {"directory", "file"}
        assert node.depth >= 1
        assert "content" not in node.to_dict()
    src = next(node for node in candidate.tree_nodes if node.relative_path == "src")
    assert src.children_count >= 1
    assert src.file_kind == "directory"


def test_limits_hidden_and_noisy_dirs(fixture_project: Path) -> None:
    shallow = _service(fixture_project).inspect_project_structure(SelfProjectStructureRequest(max_depth=1))
    assert all(node.depth <= 1 for node in shallow.tree_nodes)

    limited = _service(fixture_project).inspect_project_structure(SelfProjectStructureRequest(max_entries=2))
    assert limited.truncated is True
    assert limited.truncated_reason == "max_entries"

    paths = {node.relative_path for node in _service(fixture_project).inspect_project_structure(SelfProjectStructureRequest()).tree_nodes}
    assert ".hidden" not in paths
    assert "node_modules" not in paths


def test_tree_building_does_not_read_file_content(fixture_project: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    def fail_read_text(self, *args, **kwargs):  # noqa: ANN001
        raise AssertionError("project tree building must not read file content")

    monkeypatch.setattr(Path, "read_text", fail_read_text)
    candidate = _service(fixture_project).inspect_project_structure(SelfProjectStructureRequest(max_depth=2))
    assert candidate.tree_nodes


def test_project_structure_skill_contract_and_gate(fixture_project: Path) -> None:
    registry = SelfAwarenessRegistryService()
    contract = registry.get_contract("skill:self_awareness_project_structure")
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
        skill_id="skill:self_awareness_project_structure",
        input_payload={"root_path": str(fixture_project), "relative_path": ".", "max_depth": 2},
    )
    output = invocation.last_result.output_payload["output_attrs"]
    assert result.executed is True
    assert output["review_status"] == "candidate_only"
    assert output["canonical_promotion_enabled"] is False
    assert output["candidate_attrs"]["workspace_write_used"] is False


def test_later_surface_skills_remain_contract_only() -> None:
    registry = SelfAwarenessRegistryService()
    for skill_id in [
        "skill:self_awareness_config_surface",
        "skill:self_awareness_test_surface",
        "skill:self_awareness_capability_registry",
        "skill:self_awareness_runtime_boundary",
    ]:
        contract = registry.get_contract(skill_id)
        assert contract is not None
        assert contract.implementation_status == "contract_only"
        assert contract.gate_contract.allow_skill_execution is False


def test_cli_project_structure_works(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["self-awareness", "project", "structure", "--max-depth", "2", "--max-entries", "100"]) == 0
    output = capsys.readouterr().out
    assert "Self-Project Structure Awareness" in output
    assert "review_status=candidate_only" in output
    assert "canonical_promotion_enabled=false" in output
    assert "surface_candidate_count=" in output
    assert "content_printed=false" in output


def test_pig_and_ocpx_project_structure_coverage() -> None:
    report_service = SelfAwarenessReportService()
    pig = report_service.build_pig_report()
    ocpx = report_service.build_ocpx_projection()
    assert pig["version"] == "0.20.9"
    assert pig["state"] == "self_awareness_foundation_v1_consolidated"
    assert pig["workspace_awareness_coverage"]["project_structure"] == "implemented_surface_snapshot"
    assert pig["workspace_awareness_coverage"]["config_surface"] == "candidate_helper_only"
    assert pig["workspace_awareness_coverage"]["test_surface"] == "candidate_helper_only"
    assert pig["llm_architecture_inference_enabled"] is False
    assert pig["dependency_graph_enabled"] is False
    assert pig["runtime_introspection_enabled"] is False
    assert pig["workspace_awareness_coverage"]["surface_verification"] == "implemented_evidence_boundary_candidate_checks"
    assert ocpx["state"] == "self_awareness_foundation_v1_consolidated"
    assert "project_structure_candidate" in ocpx["candidate_types"]
    assert "project_surface_candidate" in ocpx["candidate_types"]
    assert "self_project_structure_candidate_created" in ocpx["event_coverage"]
