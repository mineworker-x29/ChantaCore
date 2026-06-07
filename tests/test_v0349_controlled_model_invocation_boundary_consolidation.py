import inspect

import pytest

from chanta_core.agent_runtime import (
    CLIModelBackedSurfaceCoverage,
    ControlledModelInvocationAuditTrail,
    ControlledModelInvocationBoundaryCoverage,
    ControlledModelInvocationBoundaryRegister,
    ControlledModelInvocationCapabilityMatrix,
    ControlledModelInvocationConsolidationReadinessLevel,
    ControlledModelInvocationConsolidationStatus,
    ControlledModelInvocationGapRegister,
    ControlledModelInvocationReleaseFlagSet,
    ControlledModelInvocationReleaseManifest,
    ControlledModelInvocationSnapshot,
    ExistingProviderBoundaryAdapterCoverage,
    ModelBackedStepIntegrationCoverage,
    ModelInvocationTraceCoverage,
    ModelOutputActionQuarantineCoverage,
    ModelRequestEnvelopeCoverage,
    ModelResponseEnvelopeCoverage,
    ProviderProfilePolicyCoverage,
    V034ConsolidationReport,
    V035HandoffPacket,
    build_cli_model_backed_surface_coverage,
    build_controlled_model_invocation_audit_trail,
    build_controlled_model_invocation_boundary_coverage,
    build_controlled_model_invocation_boundary_register,
    build_controlled_model_invocation_capability_matrix,
    build_controlled_model_invocation_gap_register,
    build_controlled_model_invocation_release_flags,
    build_controlled_model_invocation_release_manifest,
    build_controlled_model_invocation_snapshot,
    build_existing_provider_boundary_adapter_coverage,
    build_model_backed_step_integration_coverage,
    build_model_invocation_trace_coverage,
    build_model_output_action_quarantine_coverage,
    build_model_request_envelope_coverage,
    build_model_response_envelope_coverage,
    build_provider_profile_policy_coverage,
    build_v034_consolidation_report,
    build_v035_handoff_packet,
    controlled_model_invocation_audit_confirms_no_unsafe_runtime,
    controlled_model_invocation_capability_matrix_is_not_permission_grant,
    controlled_model_invocation_flags_preserve_unsafe_false,
    controlled_model_invocation_snapshot_is_not_runtime_expansion,
    v034_consolidation_report_is_not_general_runtime_ready,
    v035_handoff_packet_is_design_stage_only,
)
from chanta_core.agent_runtime import model_invocation_consolidation as consolidation_module

ControlledModelInvocationRiskRegister = consolidation_module.ControlledModelInvocationRiskRegister
build_controlled_model_invocation_risk_register = consolidation_module.build_controlled_model_invocation_risk_register


def test_v0349_status_and_readiness_taxonomies() -> None:
    assert ControlledModelInvocationConsolidationStatus.CONSOLIDATED.value == "consolidated"
    assert ControlledModelInvocationConsolidationStatus.CONSOLIDATED_WITH_GAPS.value == "consolidated_with_gaps"
    assert ControlledModelInvocationConsolidationStatus.BLOCKED.value == "blocked"
    assert ControlledModelInvocationConsolidationStatus.NO_OP.value == "no_op"
    assert ControlledModelInvocationConsolidationReadinessLevel.CONTROLLED_BOUNDARY_READY.value == "controlled_boundary_ready"
    assert ControlledModelInvocationConsolidationReadinessLevel.BOUNDED_MODEL_INVOCATION_READY.value == "bounded_model_invocation_ready"
    assert ControlledModelInvocationConsolidationReadinessLevel.CLI_MODEL_BACKED_SURFACE_READY.value == "cli_model_backed_surface_ready"
    assert ControlledModelInvocationConsolidationReadinessLevel.HANDOFF_READY_FOR_V035.value == "handoff_ready_for_v035"


def test_release_flags_allow_bounded_controlled_readiness_but_preserve_unsafe_false() -> None:
    flags = build_controlled_model_invocation_release_flags()
    assert flags.controlled_model_invocation_boundary_v1_ready is True
    assert flags.ready_for_v035_handoff is True
    assert flags.ready_for_controlled_model_invocation_boundary is True
    assert flags.ready_for_controlled_existing_boundary_invocation is True
    assert flags.ready_for_bounded_model_backed_step_execution is True
    assert flags.ready_for_agent_step_runner_model_integration is True
    assert flags.ready_for_cli_model_backed_surface is True
    assert flags.ready_for_model_invocation_trace_packet_creation is True
    assert flags.ready_for_bounded_model_invocation_ocel_trace_emission is True
    assert flags.ready_for_execution is False
    assert flags.ready_for_general_agent_execution is False
    assert flags.ready_for_autonomous_agent_runtime is False
    assert flags.ready_for_direct_provider_invocation is False
    assert flags.ready_for_provider_invocation is False
    assert flags.ready_for_provider_sdk_invocation is False
    assert flags.ready_for_direct_network_access is False
    assert flags.ready_for_credential_access is False
    assert flags.ready_for_secret_read is False
    assert flags.ready_for_general_tool_execution is False
    assert flags.ready_for_shell_execution is False
    assert flags.ready_for_subprocess_execution is False
    assert flags.ready_for_command_execution is False
    assert flags.ready_for_workspace_write is False
    assert flags.ready_for_code_edit is False
    assert flags.ready_for_patch_proposal is False
    assert flags.ready_for_patch_application is False
    assert flags.ready_for_persistent_trace_write is False
    assert flags.ready_for_ui_runtime is False
    assert flags.production_certified is False
    assert {"D4", "D5", "D6", "D7", "D8", "D9"}.issubset(set(flags.future_track_levels))
    assert controlled_model_invocation_flags_preserve_unsafe_false(flags)


@pytest.mark.parametrize(
    "unsafe_flag",
    [
        "ready_for_execution",
        "ready_for_general_agent_execution",
        "ready_for_autonomous_agent_runtime",
        "ready_for_direct_provider_invocation",
        "ready_for_provider_invocation",
        "ready_for_provider_sdk_invocation",
        "ready_for_direct_network_access",
        "ready_for_credential_access",
        "ready_for_secret_read",
        "ready_for_general_tool_execution",
        "ready_for_shell_execution",
        "ready_for_subprocess_execution",
        "ready_for_command_execution",
        "ready_for_workspace_write",
        "ready_for_code_edit",
        "ready_for_patch_proposal",
        "ready_for_patch_application",
        "ready_for_persistent_trace_write",
        "ready_for_ui_runtime",
    ],
)
def test_release_flags_reject_unsafe_runtime_readiness(unsafe_flag: str) -> None:
    with pytest.raises(ValueError):
        build_controlled_model_invocation_release_flags(**{unsafe_flag: True})


def test_release_flags_reject_production_certified_and_d4_d9_grant() -> None:
    with pytest.raises(ValueError):
        build_controlled_model_invocation_release_flags(production_certified=True)
    with pytest.raises(ValueError):
        build_controlled_model_invocation_release_flags(max_grantable_level="D4")
    with pytest.raises(ValueError):
        build_controlled_model_invocation_release_flags(future_track_levels=["D4", "D5"])


def test_snapshot_includes_v0340_through_v0348_and_is_not_runtime_expansion() -> None:
    snapshot = build_controlled_model_invocation_snapshot()
    assert set(consolidation_module.V034_INCLUDED_VERSIONS).issubset(set(snapshot.included_versions))
    assert snapshot.release_name == "Controlled Model Invocation Boundary v1"
    assert "existing provider boundary adapter through injected project-local boundary only" in snapshot.controlled_capabilities
    assert "direct provider SDK invocation" in snapshot.prohibited_capabilities
    assert snapshot.runtime_expansion is False
    assert controlled_model_invocation_snapshot_is_not_runtime_expansion(snapshot)

    with pytest.raises(ValueError):
        build_controlled_model_invocation_snapshot(included_versions=["v0.34.0"])


def test_capability_matrix_lists_controlled_bounded_and_prohibited_surfaces() -> None:
    matrix = build_controlled_model_invocation_capability_matrix()
    joined_enabled = " ".join([*matrix.enabled_controlled_capabilities, *matrix.enabled_bounded_capabilities]).lower()
    joined_prohibited = " ".join(matrix.prohibited_capabilities).lower()
    assert "request envelope" in joined_enabled
    assert "response envelope" in joined_enabled
    assert "existing provider boundary" in joined_enabled
    assert "action quarantine" in joined_enabled
    assert "model-backed step" in joined_enabled
    assert "trace packet" in joined_enabled
    assert "cli" in joined_enabled
    assert "direct provider sdk" in joined_prohibited
    assert "direct network" in joined_prohibited
    assert "credential" in joined_prohibited
    assert "shell" in joined_prohibited
    assert "write" in joined_prohibited
    assert "patch proposal" in joined_prohibited
    assert "patch application" in joined_prohibited
    assert "general tool" in joined_prohibited
    assert "autonomous" in joined_prohibited
    assert "persistent trace" in joined_prohibited
    assert "ui" in joined_prohibited
    assert matrix.permission_grant is False
    assert controlled_model_invocation_capability_matrix_is_not_permission_grant(matrix)


def test_coverage_models_for_all_v034_stages() -> None:
    coverages = [
        build_controlled_model_invocation_boundary_coverage(),
        build_provider_profile_policy_coverage(),
        build_model_request_envelope_coverage(),
        build_model_response_envelope_coverage(),
        build_existing_provider_boundary_adapter_coverage(),
        build_model_output_action_quarantine_coverage(),
        build_model_backed_step_integration_coverage(),
        build_model_invocation_trace_coverage(),
        build_cli_model_backed_surface_coverage(),
    ]
    expected_types = [
        ControlledModelInvocationBoundaryCoverage,
        ProviderProfilePolicyCoverage,
        ModelRequestEnvelopeCoverage,
        ModelResponseEnvelopeCoverage,
        ExistingProviderBoundaryAdapterCoverage,
        ModelOutputActionQuarantineCoverage,
        ModelBackedStepIntegrationCoverage,
        ModelInvocationTraceCoverage,
        CLIModelBackedSurfaceCoverage,
    ]
    for coverage, expected_type in zip(coverages, expected_types):
        assert isinstance(coverage, expected_type)
        assert coverage.coverage_complete is True
        assert coverage.blocking_gaps == []
        assert coverage.production_certification is False

    with pytest.raises(ValueError):
        ControlledModelInvocationBoundaryCoverage(
            coverage_id="coverage:blocking",
            version="v0.34.9",
            stage_version="v0.34.0",
            coverage_complete=True,
            blocking_gaps=["missing focused test"],
        )


def test_boundary_risk_and_gap_registers_are_conservative() -> None:
    boundary = build_controlled_model_invocation_boundary_register()
    assert boundary.runtime_enforcement is False
    for term in ["direct provider SDK", "direct network", "credential", "secret", "shell", "subprocess", "command", "workspace write", "code edit", "patch proposal", "patch application", "reference", "general tool", "autonomous", "persistent trace", "UI", "external control", "authority"]:
        assert term.lower() in " | ".join(boundary.prohibited_boundaries).lower()

    risk = build_controlled_model_invocation_risk_register()
    for surface in consolidation_module.DEFAULT_PROHIBITED_RUNTIME_SURFACES:
        assert surface in risk.prohibited_runtime_surfaces
    assert risk.permission is False

    gap = build_controlled_model_invocation_gap_register()
    joined_future = " | ".join(gap.future_track_items).lower()
    assert "controlled patch proposal" in joined_future
    assert "patch apply" in joined_future
    assert "autonomous" in joined_future
    assert "persistent trace" in joined_future
    assert "ui runtime" in joined_future
    assert "external harness" in joined_future


def test_release_manifest_and_audit_trail_are_not_production_release() -> None:
    manifest = build_controlled_model_invocation_release_manifest()
    assert set(consolidation_module.V034_INCLUDED_VERSIONS).issubset(set(manifest.included_versions))
    assert manifest.production_release is False
    assert manifest.release_flags.ready_for_execution is False

    audit = build_controlled_model_invocation_audit_trail()
    assert isinstance(audit, ControlledModelInvocationAuditTrail)
    assert audit.runtime_audit_execution is False
    assert controlled_model_invocation_audit_confirms_no_unsafe_runtime(audit)

    with pytest.raises(ValueError):
        build_controlled_model_invocation_audit_trail(no_direct_provider_invocation_confirmed=False)


def test_v035_handoff_packet_is_design_stage_only() -> None:
    packet = build_v035_handoff_packet()
    assert isinstance(packet, V035HandoffPacket)
    assert "v0.34.9" in packet.source_version
    assert "v0.35" in packet.target_version_track
    assert "Controlled Patch Proposal Layer" in packet.recommended_next_track
    assert packet.ready_for_v035 is True
    assert packet.ready_for_execution is False
    assert packet.ready_for_patch_proposal is False
    assert packet.ready_for_patch_application is False
    assert packet.ready_for_workspace_write is False
    assert packet.ready_for_code_edit is False
    assert packet.ready_for_direct_provider_invocation is False
    assert packet.implementation is False
    assert v035_handoff_packet_is_design_stage_only(packet)

    with pytest.raises(ValueError):
        build_v035_handoff_packet(ready_for_execution=True)
    with pytest.raises(ValueError):
        build_v035_handoff_packet(ready_for_patch_proposal=True)
    with pytest.raises(ValueError):
        build_v035_handoff_packet(ready_for_patch_application=True)
    with pytest.raises(ValueError):
        build_v035_handoff_packet(ready_for_workspace_write=True)
    with pytest.raises(ValueError):
        build_v035_handoff_packet(ready_for_direct_provider_invocation=True)


def test_v034_consolidation_report_is_not_general_runtime_ready() -> None:
    report = build_v034_consolidation_report()
    assert isinstance(report, V034ConsolidationReport)
    assert report.ready_for_v035 is True
    assert report.ready_for_controlled_model_invocation_boundary_v1 is True
    assert report.ready_for_controlled_existing_boundary_invocation is True
    assert report.ready_for_bounded_model_backed_step_execution is True
    assert report.ready_for_cli_model_backed_surface is True
    assert report.ready_for_model_invocation_trace_packet_creation is True
    assert report.ready_for_execution is False
    assert report.ready_for_general_agent_execution is False
    assert report.ready_for_autonomous_agent_runtime is False
    assert report.ready_for_direct_provider_invocation is False
    assert report.ready_for_provider_sdk_invocation is False
    assert report.ready_for_direct_network_access is False
    assert report.ready_for_credential_access is False
    assert report.ready_for_secret_read is False
    assert report.ready_for_general_tool_execution is False
    assert report.ready_for_shell_execution is False
    assert report.ready_for_subprocess_execution is False
    assert report.ready_for_workspace_write is False
    assert report.ready_for_code_edit is False
    assert report.ready_for_patch_proposal is False
    assert report.ready_for_patch_application is False
    assert report.ready_for_persistent_trace_write is False
    assert report.ready_for_ui_runtime is False
    assert report.production_certified is False
    assert report.runtime_expansion is False
    assert v034_consolidation_report_is_not_general_runtime_ready(report)

    for unsafe_flag in [
        "ready_for_execution",
        "ready_for_direct_provider_invocation",
        "ready_for_provider_sdk_invocation",
        "ready_for_direct_network_access",
        "ready_for_credential_access",
        "ready_for_general_tool_execution",
        "ready_for_shell_execution",
        "ready_for_workspace_write",
        "ready_for_patch_proposal",
        "ready_for_patch_application",
        "ready_for_persistent_trace_write",
        "ready_for_ui_runtime",
    ]:
        with pytest.raises(ValueError):
            build_v034_consolidation_report(**{unsafe_flag: True})
    with pytest.raises(ValueError):
        build_v034_consolidation_report(production_certified=True)


def test_consolidation_dataclasses_can_be_constructed_directly_with_valid_inputs() -> None:
    flags = ControlledModelInvocationReleaseFlagSet(
        flag_set_id="flags:direct",
        version="v0.34.9",
        controlled_model_invocation_boundary_v1_ready=True,
        ready_for_controlled_existing_boundary_invocation=True,
    )
    snapshot = ControlledModelInvocationSnapshot(
        snapshot_id="snapshot:direct",
        version="v0.34.9",
        release_name="Controlled Model Invocation Boundary v1",
        included_versions=list(consolidation_module.V034_INCLUDED_VERSIONS),
        included_modules=["src/chanta_core/agent_runtime/model_invocation_consolidation.py"],
        included_artifact_groups=["consolidation"],
        release_flags=flags,
        consolidation_status=ControlledModelInvocationConsolidationStatus.CONSOLIDATED,
        readiness_level=ControlledModelInvocationConsolidationReadinessLevel.CONTROLLED_BOUNDARY_READY,
        summary="Direct construction remains bounded metadata.",
    )
    matrix = ControlledModelInvocationCapabilityMatrix(
        capability_matrix_id="matrix:direct",
        version="v0.34.9",
        prohibited_capabilities=list(consolidation_module.DEFAULT_PROHIBITED_CAPABILITIES),
    )
    manifest = ControlledModelInvocationReleaseManifest(
        release_manifest_id="manifest:direct",
        version="v0.34.9",
        release_name="Controlled Model Invocation Boundary v1",
        snapshot_id=snapshot.snapshot_id,
        included_versions=list(consolidation_module.V034_INCLUDED_VERSIONS),
        included_modules=[],
        included_docs=[],
        included_tests=[],
        focused_test_command="python -m pytest tests/test_v0349_controlled_model_invocation_boundary_consolidation.py",
        full_track_test_command="python -m pytest tests/test_v0349_controlled_model_invocation_boundary_consolidation.py",
        release_flags=flags,
    )
    boundary = ControlledModelInvocationBoundaryRegister(
        boundary_register_id="boundary:direct",
        version="v0.34.9",
        prohibited_boundaries=list(consolidation_module.DEFAULT_PROHIBITED_BOUNDARIES),
    )
    risk = ControlledModelInvocationRiskRegister(
        risk_register_id="risk:direct",
        version="v0.34.9",
        prohibited_runtime_surfaces=list(consolidation_module.DEFAULT_PROHIBITED_RUNTIME_SURFACES),
    )
    gap = ControlledModelInvocationGapRegister(
        gap_register_id="gap:direct",
        version="v0.34.9",
        future_track_items=list(consolidation_module.DEFAULT_FUTURE_TRACK_ITEMS),
    )
    assert snapshot.runtime_expansion is False
    assert matrix.permission_grant is False
    assert manifest.production_release is False
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
        "read_text(",
        "read_bytes(",
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
        "os.environ",
        "dotenv",
    ]
    for pattern in forbidden_patterns:
        assert pattern not in source

    unsafe_true_patterns = [
        "ready_for_execution=True",
        "ready_for_general_agent_execution=True",
        "ready_for_autonomous_agent_runtime=True",
        "ready_for_direct_provider_invocation=True",
        "ready_for_provider_sdk_invocation=True",
        "ready_for_direct_network_access=True",
        "ready_for_credential_access=True",
        "ready_for_secret_read=True",
        "ready_for_general_tool_execution=True",
        "ready_for_shell_execution=True",
        "ready_for_subprocess_execution=True",
        "ready_for_command_execution=True",
        "ready_for_workspace_write=True",
        "ready_for_code_edit=True",
        "ready_for_patch_proposal=True",
        "ready_for_patch_application=True",
        "ready_for_persistent_trace_write=True",
        "ready_for_ui_runtime=True",
        "production_certified=True",
    ]
    compact = source.replace(" ", "")
    for pattern in unsafe_true_patterns:
        assert pattern not in compact
