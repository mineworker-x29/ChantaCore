from pathlib import Path

from chanta_core.cli.main import main
from chanta_core.skills.registry_view import SKILL_LAYERS


SELF_AWARENESS_FILES = [
    Path("src/chanta_core/self_awareness/models.py"),
    Path("src/chanta_core/self_awareness/registry.py"),
    Path("src/chanta_core/self_awareness/conformance.py"),
    Path("src/chanta_core/self_awareness/reports.py"),
    Path("src/chanta_core/self_awareness/mapping.py"),
    Path("src/chanta_core/self_awareness/code_text_perception.py"),
    Path("src/chanta_core/self_awareness/code_search_awareness.py"),
    Path("src/chanta_core/self_awareness/structure_summarization.py"),
    Path("src/chanta_core/self_awareness/project_structure_awareness.py"),
    Path("src/chanta_core/self_awareness/surface_verification.py"),
    Path("src/chanta_core/self_awareness/self_directed_intention.py"),
    Path("src/chanta_core/self_awareness/workbench.py"),
    Path("src/chanta_core/self_awareness/consolidation.py"),
    Path("src/chanta_core/ocel/self_awareness_mapping.py"),
    Path("docs/versions/v0.20/v0.20.0_self_awareness_layer_contract.md"),
    Path("docs/versions/v0.20/v0.20.3_self_code_search_awareness.md"),
    Path("docs/versions/v0.20/v0.20.4_self_structure_summarization.md"),
    Path("docs/versions/v0.20/v0.20.5_self_project_structure_awareness.md"),
    Path("docs/versions/v0.20/v0.20.6_self_surface_verification.md"),
    Path("docs/versions/v0.20/v0.20.7_self_directed_intention_candidate.md"),
    Path("docs/versions/v0.20/v0.20.8_self_awareness_workbench.md"),
    Path("docs/versions/v0.20/v0.20.9_self_awareness_consolidation.md"),
]


def test_skill_layer_registry_knows_self_awareness() -> None:
    assert "self_awareness" in SKILL_LAYERS


def test_cli_registry_output_is_read_only_and_redacted(capsys) -> None:
    exit_code = main(["self-awareness", "registry"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "layer=self_awareness" in captured.out
    assert "execution_enabled=false" in captured.out
    assert "dangerous_capability_count=0" in captured.out
    assert "write_mutation_count=0" in captured.out
    assert "shell_usage_count=0" in captured.out
    assert "network_usage_count=0" in captured.out
    assert "memory_mutation_count=0" in captured.out
    assert "persona_mutation_count=0" in captured.out
    assert "overlay_mutation_count=0" in captured.out
    assert "ChantaResearchGroup" + "_Members" not in captured.out
    assert "message_to_future_" + "ve" + "ra" not in captured.out
    assert "message_to_" + "minero" not in captured.out


def test_cli_conformance_output_has_safe_counts(capsys) -> None:
    exit_code = main(["self-awareness", "conformance"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Self-Awareness Conformance" in captured.out
    assert "layer=self_awareness" in captured.out
    assert "dangerous_capability_count=0" in captured.out
    assert "execution_enabled_count=0" in captured.out
    assert "canonical_mutation_enabled_count=0" in captured.out


def test_cli_pig_and_ocpx_outputs_build(capsys) -> None:
    assert main(["self-awareness", "pig-report"]) == 0
    pig = capsys.readouterr()
    assert "Self-Awareness PIG Report" in pig.out
    assert "dangerous_capability_count=0" in pig.out

    assert main(["self-awareness", "ocpx-projection"]) == 0
    ocpx = capsys.readouterr()
    assert "Self-Awareness OCPX Projection" in ocpx.out
    assert "state=self_awareness_foundation_v1_consolidated" in ocpx.out


def test_version_document_identity_and_boundaries() -> None:
    text = Path("docs/versions/v0.20/v0.20.0_self_awareness_layer_contract.md").read_text(encoding="utf-8")

    assert "Self-Awareness Layer Contract" in text
    assert "Basic/Foundation" in text
    assert "Self-awareness is not self-modification." in text
    assert "OCEL remains the canonical process substrate" in text


def test_new_self_awareness_files_do_not_import_private_material_or_execution_implementations() -> None:
    forbidden_private = [
        "ChantaResearchGroup" + "_Members",
        "message_to_future_" + "ve" + "ra",
        "message_to_" + "minero",
        "Ve" + "ra private",
        "Chanta" + "Ve" + "ra private",
    ]
    forbidden_runtime = [
        "sub" + "process",
        "requests" + ".get",
        "ht" + "tpx",
        "mcp" + ".connect",
        "plugin" + ".load",
        "external_harness_" + "execution=True",
        "memory_auto_" + "promotion",
        "persona_auto_" + "promotion",
        "overlay_auto_" + "mutation",
        "canonical_" + "jsonl",
    ]
    for path in SELF_AWARENESS_FILES:
        text = path.read_text(encoding="utf-8")
        for token in forbidden_private:
            assert token not in text
        for token in forbidden_runtime:
            assert token not in text
