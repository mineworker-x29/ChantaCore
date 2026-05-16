from __future__ import annotations

from pathlib import Path

import pytest

from chanta_core.cli.main import main
from chanta_core.self_awareness import (
    READ_ONLY_OBSERVATION_EFFECT,
    SelfAwarenessRegistryService,
    SelfAwarenessReportService,
    SelfStructureSummaryRequest,
    SelfStructureSummaryService,
    SelfWorkspacePathPolicyService,
)
from chanta_core.skills.execution_gate import SkillExecutionGateService
from chanta_core.skills.invocation import ExplicitSkillInvocationService


@pytest.fixture()
def workspace_root(tmp_path: Path) -> Path:
    return tmp_path


def _service(root: Path) -> SelfStructureSummaryService:
    return SelfStructureSummaryService(
        path_policy_service=SelfWorkspacePathPolicyService(workspace_root=root)
    )


def test_markdown_heading_frontmatter_and_line_ranges(workspace_root: Path) -> None:
    (workspace_root / "README.md").write_text(
        "---\ntitle: Secret Title\nowner: team\n---\n# Intro\nbody\n## Details\ntext\n",
        encoding="utf-8",
    )
    candidate = _service(workspace_root).summarize(SelfStructureSummaryRequest(path="README.md", summary_mode="markdown"))

    assert candidate.markdown is not None
    assert candidate.markdown.heading_count == 2
    assert candidate.markdown.headings[0].level == 1
    assert candidate.markdown.headings[0].title == "Intro"
    assert candidate.markdown.headings[0].line_number == 5
    assert candidate.markdown.max_heading_depth == 2
    assert candidate.markdown.frontmatter_keys == ["title", "owner"]
    assert "Secret Title" not in str(candidate.markdown.to_dict())
    assert candidate.markdown.section_line_ranges[0]["start_line"] == 5


def test_python_symbol_extraction_and_syntax_error(workspace_root: Path) -> None:
    (workspace_root / "module.py").write_text(
        "import os\nfrom pathlib import Path\nVALUE = 1\n@decorator\nclass A:\n    pass\nasync def arun():\n    pass\ndef run():\n    pass\n",
        encoding="utf-8",
    )
    candidate = _service(workspace_root).summarize(SelfStructureSummaryRequest(path="module.py", summary_mode="python"))

    assert candidate.python is not None
    assert [item.name for item in candidate.python.imports] == ["os", "pathlib.Path"]
    assert [item.name for item in candidate.python.top_level_classes] == ["A"]
    assert candidate.python.top_level_classes[0].decorators == ["decorator"]
    assert {item.name for item in candidate.python.top_level_functions} == {"arun", "run"}
    assert {item.symbol_type for item in candidate.python.top_level_functions} == {"async_function", "function"}
    assert [item.name for item in candidate.python.top_level_assignments] == ["VALUE"]
    assert candidate.python.parse_error is None

    (workspace_root / "broken.py").write_text("def broken(:\n", encoding="utf-8")
    broken = _service(workspace_root).summarize(SelfStructureSummaryRequest(path="broken.py", summary_mode="python"))
    assert broken.python is not None
    assert broken.python.parse_error
    assert broken.confidence == "medium"


def test_shallow_key_summaries_do_not_expose_values(workspace_root: Path) -> None:
    (workspace_root / "data.json").write_text('{"token": "SECRET", "nested": {"child": 1}}', encoding="utf-8")
    (workspace_root / "pyproject.toml").write_text("[project]\nname='demo'\n[tool.demo]\nkey='SECRET'\n", encoding="utf-8")
    (workspace_root / "config.yaml").write_text("password: SECRET\nnested:\n  child: value\n", encoding="utf-8")
    service = _service(workspace_root)

    json_candidate = service.summarize(SelfStructureSummaryRequest(path="data.json", summary_mode="json"))
    toml_candidate = service.summarize(SelfStructureSummaryRequest(path="pyproject.toml", summary_mode="toml"))
    yaml_candidate = service.summarize(SelfStructureSummaryRequest(path="config.yaml", summary_mode="yaml"))

    assert json_candidate.shallow_keys is not None
    assert json_candidate.shallow_keys.top_level_keys == ["token", "nested"]
    assert json_candidate.shallow_keys.nested_key_preview == {"nested": ["child"]}
    assert toml_candidate.shallow_keys is not None
    assert "project" in toml_candidate.shallow_keys.top_level_keys
    assert yaml_candidate.shallow_keys is not None
    assert yaml_candidate.shallow_keys.top_level_keys == ["password", "nested"]
    assert "SECRET" not in str(json_candidate.shallow_keys.to_dict())
    assert "SECRET" not in str(toml_candidate.shallow_keys.to_dict())
    assert "SECRET" not in str(yaml_candidate.shallow_keys.to_dict())


def test_plain_text_preview_and_read_budgets(workspace_root: Path) -> None:
    (workspace_root / "note.txt").write_text("\nalpha\npassword=SECRET\nbeta\ngamma\n", encoding="utf-8")
    candidate = _service(workspace_root).summarize(
        SelfStructureSummaryRequest(path="note.txt", summary_mode="plain_text", max_bytes=20, max_lines=3)
    )
    assert candidate.plain_text is not None
    assert candidate.plain_text.first_non_empty_lines[0] == "alpha"
    assert "SECRET" not in str(candidate.to_dict())
    assert candidate.plain_text.redacted is True
    assert candidate.plain_text.truncated is True
    assert "truncated_by_read_budget" in candidate.limitations


def test_candidate_semantics_and_effects(workspace_root: Path) -> None:
    (workspace_root / "README.md").write_text("# Title\n", encoding="utf-8")
    candidate = _service(workspace_root).summarize(SelfStructureSummaryRequest(path="README.md"))
    assert candidate.review_status == "candidate_only"
    assert candidate.canonical_promotion_enabled is False
    assert candidate.promoted is False
    assert candidate.evidence_refs
    assert candidate.confidence == "high"
    assert READ_ONLY_OBSERVATION_EFFECT in candidate.candidate_attrs["effect_types"]
    assert "state_candidate_created" in candidate.candidate_attrs["effect_types"]
    assert candidate.candidate_attrs["memory_mutation_used"] is False
    assert candidate.candidate_attrs["persona_mutation_used"] is False
    assert candidate.candidate_attrs["overlay_mutation_used"] is False


def test_structure_contracts_have_read_only_safety_flags() -> None:
    registry = SelfAwarenessRegistryService()
    for skill_id in ["skill:self_awareness_markdown_structure", "skill:self_awareness_python_symbols"]:
        contract = registry.get_contract(skill_id)
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


def test_later_self_awareness_skills_remain_contract_only() -> None:
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


def test_gate_invokes_structure_summary_read_only(workspace_root: Path) -> None:
    (workspace_root / "README.md").write_text("# Title\n", encoding="utf-8")
    invocation = ExplicitSkillInvocationService()
    gate = SkillExecutionGateService(explicit_skill_invocation_service=invocation)
    result = gate.gate_explicit_invocation(
        skill_id="skill:self_awareness_markdown_structure",
        input_payload={"root_path": str(workspace_root), "path": "README.md", "summary_mode": "markdown"},
    )
    output = invocation.last_result.output_payload["output_attrs"]
    assert result.executed is True
    assert output["review_status"] == "candidate_only"
    assert output["canonical_promotion_enabled"] is False
    assert output["candidate_attrs"]["workspace_write_used"] is False


def test_cli_markdown_python_and_auto_summarize(capsys) -> None:
    assert main(["self-awareness", "summarize", "markdown", "README.md"]) == 0
    markdown_output = capsys.readouterr().out
    assert "Self-Structure Summarization" in markdown_output
    assert "review_status=candidate_only" in markdown_output
    assert "canonical_promotion_enabled=false" in markdown_output

    assert main(["self-awareness", "summarize", "python", "src/chanta_core/cli/main.py", "--max-lines", "80"]) == 0
    python_output = capsys.readouterr().out
    assert "summary_kind=python" in python_output
    assert "function_count=" in python_output

    assert main(["self-awareness", "summarize", "auto", "pyproject.toml"]) == 0
    auto_output = capsys.readouterr().out
    assert "summary_kind=toml" in auto_output
    assert "top_level_keys=" in auto_output


def test_pig_and_ocpx_report_structure_coverage() -> None:
    report_service = SelfAwarenessReportService()
    pig = report_service.build_pig_report()
    ocpx = report_service.build_ocpx_projection()
    assert pig["version"] == "0.20.9"
    assert pig["state"] == "self_awareness_foundation_v1_consolidated"
    assert pig["workspace_awareness_coverage"]["markdown_structure"] == "implemented_deterministic"
    assert pig["workspace_awareness_coverage"]["python_symbols"] == "implemented_deterministic"
    assert pig["workspace_awareness_coverage"]["shallow_key_summary"] == "helper_deterministic"
    assert pig["llm_summary_enabled"] is False
    assert pig["canonical_promotion_enabled"] is False
    assert pig["workspace_awareness_coverage"]["project_structure"] == "implemented_surface_snapshot"
    assert ocpx["state"] == "self_awareness_foundation_v1_consolidated"
    assert "summary_candidate" in ocpx["candidate_types"]
    assert "state_candidate_created" in ocpx["effect_types"]
    assert "self_structure_summary_candidate_created" in ocpx["event_coverage"]
