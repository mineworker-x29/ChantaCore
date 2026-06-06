import inspect

import pytest

from chanta_core.agent_runtime import (
    AgentProfileRuntimeCoverage,
    AgentStepRunnerCoverage,
    CLIAgentSurfaceCoverage,
    InternalAgentRuntimeMVPConsolidationStatus,
    InternalAgentRuntimeMVPReadinessLevel,
    InternalAgentRuntimeMVPReleaseFlagSet,
    InternalAgentRuntimeMVPSnapshot,
    InternalRuntimeBoundaryCoverage,
    InternalRuntimeMVPAuditTrail,
    InternalRuntimeMVPBoundaryRegister,
    InternalRuntimeMVPCapabilityMatrix,
    InternalRuntimeMVPGapRegister,
    InternalRuntimeMVPReleaseManifest,
    InternalRuntimeMVPRiskRegister,
    PromptAssemblyCoverage,
    ReadOnlyToolRegistryCoverage,
    RuntimeOCELTraceCoverage,
    SessionRuntimeCoverage,
    V033ConsolidationReport,
    V034HandoffPacket,
    WorkspaceInspectionCoverage,
    build_agent_profile_runtime_coverage,
    build_agent_step_runner_coverage,
    build_cli_agent_surface_coverage,
    build_internal_agent_runtime_mvp_release_flags,
    build_internal_agent_runtime_mvp_snapshot,
    build_internal_runtime_boundary_coverage,
    build_internal_runtime_mvp_audit_trail,
    build_internal_runtime_mvp_boundary_register,
    build_internal_runtime_mvp_capability_matrix,
    build_internal_runtime_mvp_gap_register,
    build_internal_runtime_mvp_release_manifest,
    build_internal_runtime_mvp_risk_register,
    build_prompt_assembly_coverage,
    build_readonly_tool_registry_coverage,
    build_runtime_ocel_trace_coverage,
    build_session_runtime_coverage,
    build_v033_consolidation_report,
    build_v034_handoff_packet,
    build_workspace_inspection_coverage,
    internal_agent_runtime_mvp_flags_preserve_unsafe_false,
    internal_agent_runtime_mvp_snapshot_is_not_runtime_expansion,
    internal_runtime_mvp_audit_confirms_no_unsafe_runtime,
    internal_runtime_mvp_capability_matrix_is_not_permission_grant,
    v033_consolidation_report_is_not_general_runtime_ready,
    v034_handoff_packet_is_design_stage_only,
)
from chanta_core.agent_runtime import consolidation as consolidation_module


def test_v0339_status_and_readiness_taxonomies() -> None:
    assert InternalAgentRuntimeMVPConsolidationStatus.CONSOLIDATED.value == "consolidated"
    assert InternalAgentRuntimeMVPConsolidationStatus.CONSOLIDATED_WITH_GAPS.value == "consolidated_with_gaps"
    assert InternalAgentRuntimeMVPConsolidationStatus.BLOCKED.value == "blocked"
    assert InternalAgentRuntimeMVPConsolidationStatus.NO_OP.value == "no_op"
    assert InternalAgentRuntimeMVPReadinessLevel.BOUNDED_RUNTIME_MVP_READY.value == "bounded_runtime_mvp_ready"
    assert InternalAgentRuntimeMVPReadinessLevel.BOUNDED_CLI_MVP_READY.value == "bounded_cli_mvp_ready"
    assert InternalAgentRuntimeMVPReadinessLevel.HANDOFF_READY_FOR_V034.value == "handoff_ready_for_v034"


def test_release_flags_allow_bounded_mvp_but_preserve_unsafe_false() -> None:
    flags = build_internal_agent_runtime_mvp_release_flags()
    assert flags.internal_general_agent_runtime_mvp_v1_ready is True
    assert flags.ready_for_v034_handoff is True
    assert flags.ready_for_bounded_internal_runtime_mvp is True
    assert flags.ready_for_bounded_cli_agent_run is True
    assert flags.ready_for_bounded_agent_step_execution is True
    assert flags.ready_for_safe_workspace_inspection_execution is True
    assert flags.ready_for_bounded_internal_ocel_trace_emission is True
    assert flags.ready_for_execution is False
    assert flags.ready_for_general_agent_execution is False
    assert flags.ready_for_autonomous_agent_runtime is False
    assert flags.ready_for_real_model_invocation is False
    assert flags.ready_for_provider_invocation is False
    assert flags.ready_for_general_tool_execution is False
    assert flags.ready_for_shell_execution is False
    assert flags.ready_for_subprocess_execution is False
    assert flags.ready_for_command_execution is False
    assert flags.ready_for_workspace_write is False
    assert flags.ready_for_code_edit is False
    assert flags.ready_for_patch_application is False
    assert flags.ready_for_persistent_trace_write is False
    assert flags.ready_for_ui_runtime is False
    assert flags.production_certified is False
    assert {"D4", "D5", "D6", "D7", "D8", "D9"}.issubset(set(flags.future_track_levels))
    assert internal_agent_runtime_mvp_flags_preserve_unsafe_false(flags)


@pytest.mark.parametrize(
    "unsafe_flag",
    [
        "ready_for_execution",
        "ready_for_general_agent_execution",
        "ready_for_autonomous_agent_runtime",
        "ready_for_real_model_invocation",
        "ready_for_provider_invocation",
        "ready_for_general_tool_execution",
        "ready_for_shell_execution",
        "ready_for_subprocess_execution",
        "ready_for_command_execution",
        "ready_for_workspace_write",
        "ready_for_code_edit",
        "ready_for_patch_application",
        "ready_for_persistent_trace_write",
        "ready_for_ui_runtime",
    ],
)
def test_release_flags_reject_unsafe_runtime_readiness(unsafe_flag: str) -> None:
    with pytest.raises(ValueError):
        build_internal_agent_runtime_mvp_release_flags(**{unsafe_flag: True})


def test_release_flags_reject_production_certified_and_d4_d9_grant() -> None:
    with pytest.raises(ValueError):
        build_internal_agent_runtime_mvp_release_flags(production_certified=True)
    with pytest.raises(ValueError):
        build_internal_agent_runtime_mvp_release_flags(max_grantable_level="D4")
    with pytest.raises(ValueError):
        build_internal_agent_runtime_mvp_release_flags(future_track_levels=["D4", "D5"])


def test_snapshot_includes_v0330_through_v0338_and_is_not_runtime_expansion() -> None:
    snapshot = build_internal_agent_runtime_mvp_snapshot()
    assert set(consolidation_module.V033_INCLUDED_VERSIONS).issubset(set(snapshot.included_versions))
    assert snapshot.release_name == "Internal General Agent Runtime MVP v1"
    assert "bounded supplied/mock model output agent step runner" in snapshot.bounded_capabilities
    assert "real provider invocation" in snapshot.prohibited_capabilities
    assert snapshot.runtime_expansion is False
    assert internal_agent_runtime_mvp_snapshot_is_not_runtime_expansion(snapshot)

    with pytest.raises(ValueError):
        build_internal_agent_runtime_mvp_snapshot(included_versions=["v0.33.0"])


def test_capability_matrix_lists_bounded_and_prohibited_surfaces() -> None:
    matrix = build_internal_runtime_mvp_capability_matrix()
    joined_enabled = " ".join(matrix.enabled_bounded_capabilities).lower()
    joined_prohibited = " ".join(matrix.prohibited_capabilities).lower()
    assert "workspace inspection" in joined_enabled
    assert "step runner" in joined_enabled
    assert "trace packet" in joined_enabled
    assert "cli" in joined_enabled
    assert "provider" in joined_prohibited
    assert "shell" in joined_prohibited
    assert "write" in joined_prohibited
    assert "general tool" in joined_prohibited
    assert "persistent trace" in joined_prohibited
    assert "ui" in joined_prohibited
    assert matrix.permission_grant is False
    assert internal_runtime_mvp_capability_matrix_is_not_permission_grant(matrix)


def test_coverage_models_for_all_v033_stages() -> None:
    coverages = [
        build_internal_runtime_boundary_coverage(),
        build_agent_profile_runtime_coverage(),
        build_prompt_assembly_coverage(),
        build_session_runtime_coverage(),
        build_readonly_tool_registry_coverage(),
        build_workspace_inspection_coverage(),
        build_agent_step_runner_coverage(),
        build_runtime_ocel_trace_coverage(),
        build_cli_agent_surface_coverage(),
    ]
    expected_types = [
        InternalRuntimeBoundaryCoverage,
        AgentProfileRuntimeCoverage,
        PromptAssemblyCoverage,
        SessionRuntimeCoverage,
        ReadOnlyToolRegistryCoverage,
        WorkspaceInspectionCoverage,
        AgentStepRunnerCoverage,
        RuntimeOCELTraceCoverage,
        CLIAgentSurfaceCoverage,
    ]
    for coverage, expected_type in zip(coverages, expected_types):
        assert isinstance(coverage, expected_type)
        assert coverage.coverage_complete is True
        assert coverage.blocking_gaps == []
        assert coverage.production_certification is False

    with pytest.raises(ValueError):
        InternalRuntimeBoundaryCoverage(
            coverage_id="coverage:blocking",
            version="v0.33.9",
            coverage_complete=True,
            blocking_gaps=["missing focused test"],
        )


def test_boundary_risk_and_gap_registers_are_conservative() -> None:
    boundary = build_internal_runtime_mvp_boundary_register()
    assert boundary.runtime_enforcement is False
    for term in ["shell", "subprocess", "real provider", "general tool", "write/edit/patch", "reference execution", "credential access", "persistent trace", "UI runtime", "external control", "authority grant"]:
        assert term.lower() in " | ".join(boundary.prohibited_boundaries).lower()

    risk = build_internal_runtime_mvp_risk_register()
    for surface in consolidation_module.DEFAULT_PROHIBITED_RUNTIME_SURFACES:
        assert surface in risk.prohibited_runtime_surfaces
    assert risk.permission is False

    gap = build_internal_runtime_mvp_gap_register()
    joined_future = " | ".join(gap.future_track_items).lower()
    assert "provider" in joined_future
    assert "patch proposal" in joined_future
    assert "autonomous" in joined_future
    assert "persistent trace" in joined_future
    assert "ui runtime" in joined_future
    assert "external harness" in joined_future


def test_release_manifest_and_audit_trail_are_not_production_release() -> None:
    manifest = build_internal_runtime_mvp_release_manifest()
    assert set(consolidation_module.V033_INCLUDED_VERSIONS).issubset(set(manifest.included_versions))
    assert manifest.production_release is False
    assert manifest.release_flags.ready_for_execution is False

    audit = build_internal_runtime_mvp_audit_trail()
    assert audit.runtime_audit_execution is False
    assert internal_runtime_mvp_audit_confirms_no_unsafe_runtime(audit)

    with pytest.raises(ValueError):
        build_internal_runtime_mvp_audit_trail(no_provider_invocation_confirmed=False)


def test_v034_handoff_packet_is_design_stage_only() -> None:
    packet = build_v034_handoff_packet()
    assert isinstance(packet, V034HandoffPacket)
    assert "v0.33.9" in packet.source_version
    assert "v0.34" in packet.target_version_track
    assert "Controlled Model Invocation Boundary" in packet.recommended_v034_options
    assert "Controlled Patch Proposal Layer" in packet.recommended_v034_options
    assert packet.ready_for_v034 is True
    assert packet.ready_for_execution is False
    assert packet.ready_for_real_model_invocation is False
    assert packet.ready_for_provider_invocation is False
    assert packet.ready_for_workspace_write is False
    assert packet.ready_for_patch_application is False
    assert packet.implementation is False
    assert v034_handoff_packet_is_design_stage_only(packet)

    with pytest.raises(ValueError):
        build_v034_handoff_packet(ready_for_execution=True)
    with pytest.raises(ValueError):
        build_v034_handoff_packet(ready_for_provider_invocation=True)
    with pytest.raises(ValueError):
        build_v034_handoff_packet(ready_for_workspace_write=True)
    with pytest.raises(ValueError):
        build_v034_handoff_packet(ready_for_patch_application=True)


def test_v033_consolidation_report_is_not_general_runtime_ready() -> None:
    report = build_v033_consolidation_report()
    assert isinstance(report, V033ConsolidationReport)
    assert report.ready_for_v034 is True
    assert report.ready_for_bounded_internal_runtime_mvp is True
    assert report.ready_for_bounded_cli_agent_run is True
    assert report.ready_for_execution is False
    assert report.ready_for_general_agent_execution is False
    assert report.ready_for_autonomous_agent_runtime is False
    assert report.ready_for_real_model_invocation is False
    assert report.ready_for_provider_invocation is False
    assert report.ready_for_general_tool_execution is False
    assert report.ready_for_shell_execution is False
    assert report.ready_for_subprocess_execution is False
    assert report.ready_for_workspace_write is False
    assert report.ready_for_code_edit is False
    assert report.ready_for_patch_application is False
    assert report.ready_for_persistent_trace_write is False
    assert report.ready_for_ui_runtime is False
    assert report.production_certified is False
    assert report.runtime_expansion is False
    assert v033_consolidation_report_is_not_general_runtime_ready(report)

    with pytest.raises(ValueError):
        build_v033_consolidation_report(ready_for_execution=True)
    with pytest.raises(ValueError):
        build_v033_consolidation_report(ready_for_provider_invocation=True)
    with pytest.raises(ValueError):
        build_v033_consolidation_report(ready_for_general_tool_execution=True)
    with pytest.raises(ValueError):
        build_v033_consolidation_report(ready_for_shell_execution=True)
    with pytest.raises(ValueError):
        build_v033_consolidation_report(ready_for_workspace_write=True)
    with pytest.raises(ValueError):
        build_v033_consolidation_report(ready_for_persistent_trace_write=True)
    with pytest.raises(ValueError):
        build_v033_consolidation_report(production_certified=True)


def test_consolidation_dataclasses_can_be_constructed_directly_with_valid_inputs() -> None:
    flags = InternalAgentRuntimeMVPReleaseFlagSet(
        flag_set_id="flags:direct",
        version="v0.33.9",
        internal_general_agent_runtime_mvp_v1_ready=True,
        ready_for_bounded_internal_runtime_mvp=True,
    )
    snapshot = InternalAgentRuntimeMVPSnapshot(
        snapshot_id="snapshot:direct",
        version="v0.33.9",
        release_name="Internal General Agent Runtime MVP v1",
        included_versions=list(consolidation_module.V033_INCLUDED_VERSIONS),
        included_modules=["src/chanta_core/agent_runtime/consolidation.py"],
        included_artifact_groups=["consolidation"],
        release_flags=flags,
        consolidation_status=InternalAgentRuntimeMVPConsolidationStatus.CONSOLIDATED,
        readiness_level=InternalAgentRuntimeMVPReadinessLevel.BOUNDED_RUNTIME_MVP_READY,
        summary="Direct construction remains bounded metadata.",
    )
    matrix = InternalRuntimeMVPCapabilityMatrix(
        capability_matrix_id="matrix:direct",
        version="v0.33.9",
        prohibited_capabilities=list(consolidation_module.DEFAULT_PROHIBITED_CAPABILITIES),
    )
    manifest = InternalRuntimeMVPReleaseManifest(
        release_manifest_id="manifest:direct",
        version="v0.33.9",
        release_name="Internal General Agent Runtime MVP v1",
        snapshot_id=snapshot.snapshot_id,
        included_versions=list(consolidation_module.V033_INCLUDED_VERSIONS),
        included_modules=[],
        included_docs=[],
        included_tests=[],
        focused_test_command="python -m pytest tests/test_v0339_internal_general_agent_runtime_mvp_consolidation.py",
        full_track_test_command="python -m pytest tests/test_v0339_internal_general_agent_runtime_mvp_consolidation.py",
        release_flags=flags,
    )
    audit = InternalRuntimeMVPAuditTrail(audit_trail_id="audit:direct", version="v0.33.9")
    boundary = InternalRuntimeMVPBoundaryRegister(
        boundary_register_id="boundary:direct",
        version="v0.33.9",
        prohibited_boundaries=list(consolidation_module.DEFAULT_PROHIBITED_BOUNDARIES),
    )
    risk = InternalRuntimeMVPRiskRegister(
        risk_register_id="risk:direct",
        version="v0.33.9",
        prohibited_runtime_surfaces=list(consolidation_module.DEFAULT_PROHIBITED_RUNTIME_SURFACES),
    )
    gap = InternalRuntimeMVPGapRegister(
        gap_register_id="gap:direct",
        version="v0.33.9",
        future_track_items=list(consolidation_module.DEFAULT_FUTURE_TRACK_ITEMS),
    )
    assert snapshot.runtime_expansion is False
    assert matrix.permission_grant is False
    assert manifest.production_release is False
    assert audit.runtime_audit_execution is False
    assert boundary.runtime_enforcement is False
    assert risk.permission is False
    assert gap.blocking_gaps == []


def test_consolidation_helpers_are_pure_conservative_source() -> None:
    source = inspect.getsource(consolidation_module)
    forbidden_patterns = [
        "import subprocess",
        "subprocess.",
        "os.system",
        "shell=True",
        "requests.",
        "httpx.",
        "urllib.",
        "aiohttp.",
        "socket.",
        "eval(",
        "exec(",
        "importlib",
        "write_text(",
        "write_bytes(",
        "open(",
        "unlink(",
        ".rmdir(",
        ".mkdir(",
        ".rename(",
        "Path.replace(",
        ".chmod(",
        ".chown(",
        "shutil.",
        "sqlite",
        "logging.",
    ]
    for pattern in forbidden_patterns:
        assert pattern not in source

    unsafe_true_patterns = [
        "ready_for_execution=True",
        "ready_for_general_agent_execution=True",
        "ready_for_autonomous_agent_runtime=True",
        "ready_for_real_model_invocation=True",
        "ready_for_provider_invocation=True",
        "ready_for_general_tool_execution=True",
        "ready_for_shell_execution=True",
        "ready_for_subprocess_execution=True",
        "ready_for_command_execution=True",
        "ready_for_workspace_write=True",
        "ready_for_code_edit=True",
        "ready_for_patch_application=True",
        "ready_for_persistent_trace_write=True",
        "ready_for_ui_runtime=True",
        "production_certified=True",
    ]
    compact = source.replace(" ", "")
    for pattern in unsafe_true_patterns:
        assert pattern not in compact
