from pathlib import Path

import pytest

from chanta_core.personal_runtime.default_personal_workspace_read_contract import (
    REQUIRED_V0440_EVENT_TYPES,
    REQUIRED_V0440_OBJECT_TYPES,
    V0440WorkspaceObjectType,
    create_v0440_baseline_reflection_diagnostics_contract,
    create_v0440_controlled_workspace_scope,
    create_v0440_file_type_policy,
    create_v0440_integrated_restore_document_manifest,
    create_v0440_ocpm_ready_export_contract,
    create_v0440_pird001_historical_ocpm_reflection_debt,
    create_v0440_read_budget_policy,
    create_v0440_read_disclosure_policy,
    create_v0440_readiness_report,
    create_v0440_safety_boundary_report,
    create_v0440_secret_redaction_policy,
    create_v0440_trace_data_quality_report,
    create_v0440_workspace_evidence_item,
    create_v0440_workspace_read_event_contract,
    create_v0440_workspace_read_request,
    create_v0441_controlled_workspace_read_mvp_handoff,
    create_v0442_workspace_evidence_index_handoff,
    create_v046r_historical_ocpm_research_track_handoff,
    evaluate_v0440_allowlist,
    normalize_v0440_workspace_path,
    simulate_v0440_workspace_read_request,
    validate_v0440_path_inside_root,
)
from chanta_core.schumpeter_tui.command_registry import (
    find_v043111_command_spec,
    render_v043111_palette_text,
)
from chanta_core.schumpeter_tui.runtime_adapter import V04310RuntimeAdapter


ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = ROOT / "docs" / "versions" / "v0.44" / "v0.44.0_controlled_workspace_read_observation_ocpm_debt_restore.md"
CONTRACT_PATH = ROOT / "src" / "chanta_core" / "personal_runtime" / "default_personal_workspace_read_contract.py"
SURFACE_PATH = ROOT / "src" / "chanta_core" / "schumpeter_tui" / "workspace_surface.py"


def test_v0440_controlled_workspace_scope_is_read_only():
    scope = create_v0440_controlled_workspace_scope(
        workspace_root="D:/ChantaResearchGroup/ChantaCore",
        allowed_paths=("docs", "src"),
    )

    assert scope.read_only is True
    assert scope.edit_allowed is False
    assert scope.shell_allowed is False
    assert scope.repo_search_allowed is False
    assert scope.production_certified is False


def test_v0440_scope_requires_explicit_workspace_root():
    with pytest.raises(ValueError, match="workspace_root"):
        create_v0440_controlled_workspace_scope(workspace_root="", allowed_paths=("src",))


def test_v0440_scope_requires_allowlist():
    with pytest.raises(ValueError, match="allowed_paths"):
        create_v0440_controlled_workspace_scope(workspace_root="D:/repo", allowed_paths=())


def test_v0440_path_normalization_blocks_traversal():
    normalized = normalize_v0440_workspace_path("D:/repo", "../secret.env")

    assert normalized.denied_reason == "path_traversal"
    assert normalized.inside_root is False


def test_v0440_inside_root_validation_blocks_outside_paths():
    result = validate_v0440_path_inside_root("D:/repo", "D:/secret.txt")

    assert result.inside_root is False
    assert result.denied_reason == "outside_workspace_root"


def test_v0440_read_budget_policy_has_file_count_and_byte_limits():
    policy = create_v0440_read_budget_policy()

    assert policy.max_file_count > 0
    assert policy.max_total_bytes > 0
    assert policy.max_chars_per_file > 0
    assert policy.production_certified is False


def test_v0440_file_type_policy_denies_binary_by_default():
    policy = create_v0440_file_type_policy()

    assert policy.binary_policy == "deny"
    assert policy.denied_extensions
    assert ".exe" in policy.denied_extensions


def test_v0440_secret_redaction_required():
    policy = create_v0440_secret_redaction_policy()

    assert policy.secret_redaction_required is True
    assert "api_key" in policy.redaction_targets


def test_v0440_read_disclosure_required():
    policy = create_v0440_read_disclosure_policy()

    assert policy.user_visible_disclosure_required is True
    assert policy.disclose_before_read is True


def test_v0440_workspace_read_request_is_simulation_only():
    request = create_v0440_workspace_read_request(
        workspace_root="D:/repo",
        requested_path="src/app.py",
        allowed_paths=("src",),
    )

    assert request.actual_file_content_read is False
    assert request.would_read is True
    assert request.production_certified is False


def test_v0440_does_not_read_actual_file_content(tmp_path):
    target = tmp_path / "allowed" / "secret.txt"
    target.parent.mkdir()
    target.write_text("must not be returned", encoding="utf-8")

    result = simulate_v0440_workspace_read_request(
        workspace_root=str(tmp_path),
        requested_path="allowed/secret.txt",
        allowed_paths=("allowed",),
    )

    assert result.actual_file_content_read is False
    assert result.content_preview is None
    assert result.would_read is True


def test_v0440_workspace_evidence_item_schema_defined():
    item = create_v0440_workspace_evidence_item(path_label="src/example.py")

    assert item.source_kind == "workspace_read"
    assert item.object_type == V0440WorkspaceObjectType.SOURCE_FILE.value
    assert item.content_hash.startswith("sha256:")
    assert item.production_certified is False


def test_v0440_workspace_read_event_contract_defines_required_objects():
    contract = create_v0440_workspace_read_event_contract()

    assert set(REQUIRED_V0440_OBJECT_TYPES).issubset(set(contract.object_types))


def test_v0440_workspace_read_event_contract_defines_required_events():
    contract = create_v0440_workspace_read_event_contract()

    assert set(REQUIRED_V0440_EVENT_TYPES).issubset(set(contract.event_types))


def test_v0440_ocpm_ready_export_contract_exists():
    contract = create_v0440_ocpm_ready_export_contract()

    assert contract.contract_ready is True
    assert "workspace_read_events" in contract.supported_slices
    assert contract.production_certified is False


def test_v0440_ocpm_export_contract_disables_advanced_ocpm_analysis():
    contract = create_v0440_ocpm_ready_export_contract()

    assert contract.advanced_ocpm_analysis_enabled is False
    assert contract.actual_algorithm_execution is False


def test_v0440_trace_data_quality_report_fields_defined():
    report = create_v0440_trace_data_quality_report(event_count=2, object_count=3, relation_count=4)

    assert report.event_count == 2
    assert report.object_count == 3
    assert report.relation_count == 4
    assert report.readiness_for_ocpm_research in {"not_ready", "sample_only", "ready_for_research"}


def test_v0440_baseline_reflection_diagnostics_labeled_not_advanced_ocpm():
    contract = create_v0440_baseline_reflection_diagnostics_contract()

    assert contract.label == "Rule-based baseline diagnostics, not validated OCPM analytics."
    assert contract.advanced_ocpm_analytics is False


def test_v0440_baseline_reflection_diagnostics_do_not_activate_memory():
    contract = create_v0440_baseline_reflection_diagnostics_contract()

    assert contract.activates_improvement_memory is False
    assert contract.injects_decision_policy is False
    assert contract.generates_patch is False


def test_v0440_pird001_research_debt_registered():
    debt = create_v0440_pird001_historical_ocpm_reflection_debt()

    assert debt.debt_id == "PI-RD-001"
    assert debt.title == "Historical OCPM Reflection Analytics"
    assert debt.status == "deferred"


def test_v0440_pird001_deferred_reason_mentions_episode_boundary_scope_ground_truth_and_algorithm_validation():
    debt = create_v0440_pird001_historical_ocpm_reflection_debt()
    text = debt.deferred_reason.lower()

    for expected in ("episode boundary", "process scope", "ground truth", "algorithm"):
        assert expected in text


def test_v0440_pird001_prohibits_automatic_memory_activation_decision_injection_patch_generation_until_validated():
    debt = create_v0440_pird001_historical_ocpm_reflection_debt()

    prohibited = " ".join(debt.prohibited_until_validated).lower()
    assert "improvement memory" in prohibited
    assert "decision injection" in prohibited
    assert "patch generation" in prohibited
    assert debt.production_certified is False


def test_v0440_workspace_tui_commands_are_preview_not_opened():
    for command in ("/workspace status", "/workspace read", "/ocel quality", "/reflection baseline", "/research debt PI-RD-001"):
        spec = find_v043111_command_spec(command)
        assert spec is not None
        assert spec.availability == "not_opened"


def test_v0440_workspace_commands_do_not_perform_actual_read():
    adapter = V04310RuntimeAdapter(emit_run_report_trace=False)
    result = adapter.execute_slash_command("/workspace open D:/ChantaResearchGroup/ChantaCore")

    assert result.route_kind == "not_opened"
    assert "not opened" in result.rendered_text.lower() or "아직 열리지" in result.rendered_text
    assert result.workspace_read_opened is False
    assert result.repo_search_used is False


def test_v0440_safety_report_keeps_workspace_read_repo_search_shell_git_edit_apply_tools_functions_subagents_memory_core_and_production_false():
    report = create_v0440_safety_boundary_report()

    assert report.actual_workspace_read_opened is False
    assert report.repo_search_opened is False
    assert report.shell_execution_opened is False
    assert report.git_execution_opened is False
    assert report.file_edit_opened is False
    assert report.patch_apply_opened is False
    assert report.provider_tool_calling_opened is False
    assert report.function_calling_opened is False
    assert report.subagent_invocation_opened is False
    assert report.memory_mutation_opened is False
    assert report.core_memory_write_opened is False
    assert report.production_certified is False


def test_v0440_readiness_report_sets_design_contract_flags_true():
    report = create_v0440_readiness_report()

    assert report.controlled_workspace_read_design_ready is True
    assert report.ocel_ready_contract_ready is True
    assert report.ocpm_ready_export_contract_ready is True
    assert report.research_debt_registered is True


def test_v0440_readiness_report_keeps_actual_read_and_advanced_ocpm_false():
    report = create_v0440_readiness_report()

    assert report.actual_workspace_read_mvp_open is False
    assert report.advanced_ocpm_analysis_enabled is False
    assert report.production_certified is False


def test_v0441_handoff_targets_controlled_workspace_read_mvp():
    handoff = create_v0441_controlled_workspace_read_mvp_handoff()

    assert handoff.target_version == "v0.44.1"
    assert "Controlled Workspace Read MVP" in handoff.title


def test_v0442_handoff_targets_workspace_evidence_index():
    handoff = create_v0442_workspace_evidence_index_handoff()

    assert handoff.target_version == "v0.44.2"
    assert "Workspace Evidence Index" in handoff.title


def test_v046r_handoff_targets_offline_historical_ocpm_research_track():
    handoff = create_v046r_historical_ocpm_research_track_handoff()

    assert handoff.target_version == "v0.46-R"
    assert "offline" in " ".join(handoff.research_steps).lower()


def test_v0440_integrated_document_exists_and_has_required_sections():
    text = DOC_PATH.read_text(encoding="utf-8")

    for title in (
        "Restore Purpose",
        "One-Screen Restore Summary",
        "Current Version and Track Identity",
        "Why v0.44 Was Redesigned",
        "Controlled Workspace Read Design",
        "Workspace Root and Allowlist Policy",
        "Path Validation and Denial Policy",
        "Read Budget and File Type Policy",
        "Secret Redaction and Read Disclosure",
        "Workspace Evidence Model",
        "OCEL-Ready Workspace Read Event Contract",
        "OCPM-Ready Export Contract",
        "Trace Data Quality Report Contract",
        "Baseline Reflection Diagnostics",
        "PI-RD-001 Historical OCPM Reflection Analytics Research Debt",
        "Why Advanced OCPM Is Deferred",
        "TUI Workspace / Observation Command Preview",
        "Still-Closed Capabilities",
        "Required Test Commands",
        "Manual Acceptance Commands",
        "Withdrawal Conditions",
        "v0.44.1 Controlled Workspace Read MVP Handoff",
        "v0.44.2 Workspace Evidence Index Handoff",
        "v0.46-R Historical OCPM Research Track Handoff",
        "Copy-Paste Restore Prompt for Future GPT/Codex Session",
    ):
        assert f"## {title}" in text


def test_v0440_integrated_document_contains_pird001_and_restore_prompt():
    text = DOC_PATH.read_text(encoding="utf-8")

    assert "PI-RD-001" in text
    assert "Schumpeter v0.44.0 defines the Controlled Workspace Read and Observation foundation." in text
    assert "Copy-Paste Restore Prompt" in text


def test_v0440_no_forbidden_runtime_call_patterns():
    text = "\n".join((CONTRACT_PATH.read_text(encoding="utf-8"), SURFACE_PATH.read_text(encoding="utf-8")))
    forbidden_patterns = (
        "sub" + "process",
        "shell" + "=True",
        "os." + "system",
        "git " + "status",
        "Path." + "read_text",
        "Path." + "read_bytes",
        "os." + "walk",
        "Path." + "rglob",
        "glob(",
        "provider tool call",
        "function call",
        "CORE_MEMORY " + "write",
    )

    for forbidden in forbidden_patterns:
        assert forbidden not in text


def test_v0440_no_actual_file_open_read_repo_scan_shell_git_provider_tool_or_memory_mutation():
    text = "\n".join((CONTRACT_PATH.read_text(encoding="utf-8"), SURFACE_PATH.read_text(encoding="utf-8")))
    forbidden_patterns = (
        "open(",
        ".read()",
        ".read_text(",
        ".read_bytes(",
        "rglob(",
        "os.walk",
        "subprocess",
        "os.system",
        "git status",
        "execute_run_command",
        "provider_client",
        "mutate_memory",
        "CORE_MEMORY",
    )

    for forbidden in forbidden_patterns:
        assert forbidden not in text


def test_v0440_palette_shows_preview_commands_as_future_surface():
    text = render_v043111_palette_text("/workspace")

    assert "/workspace status" in text
    assert "[not_opened]" in text


def test_v0440_integrated_document_manifest_points_to_single_doc():
    manifest = create_v0440_integrated_restore_document_manifest()

    assert manifest.document_paths == ("docs/versions/v0.44/v0.44.0_controlled_workspace_read_observation_ocpm_debt_restore.md",)
    assert manifest.fragmented_documents_created is False


def test_v0440_allowlist_denies_unlisted_paths():
    decision = evaluate_v0440_allowlist("docs/report.md", allowed_paths=("src",), denied_paths=())

    assert decision.allowlisted is False
    assert decision.denied_reason == "path_not_allowlisted"
