from pathlib import Path

from chanta_core.deep_self_introspection import DeepSelfIntrospectionConformanceService


def test_conformance_passes_for_contract_only_layer() -> None:
    service = DeepSelfIntrospectionConformanceService()
    report = service.run_conformance()
    assert report.passed is True
    assert report.layer == "deep_self_introspection"
    assert report.checked_subject_count == 7
    assert report.checked_skill_count == 7


def test_runtime_files_do_not_contain_forbidden_implementation_calls() -> None:
    runtime_files = [
        Path("src/chanta_core/deep_self_introspection/models.py"),
        Path("src/chanta_core/deep_self_introspection/mapping.py"),
        Path("src/chanta_core/deep_self_introspection/registry.py"),
        Path("src/chanta_core/deep_self_introspection/conformance.py"),
        Path("src/chanta_core/deep_self_introspection/reports.py"),
    ]
    forbidden = [
        "apply_patch",
        "write_file",
        "subprocess",
        "os.system",
        "requests",
        "httpx",
        "mcp.connect",
        "plugin.load",
        "permission_grant",
        "grants_permission=True",
        "mutates_capability_registry=True",
        "mutates_policy=True",
        "memory_auto_promotion",
        "persona_auto_promotion",
        "overlay_auto_mutation",
        "canonical_promotion_enabled=True",
        "promoted=True",
        "materialized=True",
        "execution_enabled=True",
        "chat.completions",
        "exec(",
        "eval(",
    ]
    text = "\n".join(path.read_text(encoding="utf-8") for path in runtime_files)
    for token in forbidden:
        assert token not in text


def test_docs_define_contract_only_ocel_native_boundary() -> None:
    text = Path("docs/versions/v0.21/v0.21.0_deep_self_introspection_contract.md").read_text(encoding="utf-8")
    assert "OCEL-native Deep Self-Introspection Contract" in text
    assert "Deep self-introspection must be OCEL-native." in text
    assert "Deep self-introspection is not self-modification." in text
    assert "v0.21.0 is contract-only." in text
    assert "v0.21.1 Self-Capability Registry Awareness" in text


def test_no_actual_analysis_is_claimed_by_contract_subjects() -> None:
    report = DeepSelfIntrospectionConformanceService().run_conformance()
    assert report.findings == []
