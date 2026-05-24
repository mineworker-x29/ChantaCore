import subprocess
import sys
from dataclasses import replace

from chanta_core.deep_self_introspection import (
    CanonicalStorePolicyDescriptor,
    ExecutionBoundaryDescriptor,
    PrivateBoundaryDescriptor,
    RuntimeBoundaryTruthCheckService,
    RuntimeModeDescriptor,
    RuntimeTrackState,
    SelfCapabilityRegistryAwarenessService,
    SelfRuntimeBoundaryAwarenessService,
)


def test_runtime_boundary_snapshot_builds() -> None:
    snapshot = SelfRuntimeBoundaryAwarenessService().view_runtime_boundary()
    assert snapshot.snapshot_id
    assert snapshot.read_only is True
    assert snapshot.mutation_performed is False
    assert snapshot.profile.profile_id
    assert snapshot.mode.mode_id
    assert snapshot.tracks
    assert snapshot.workspace_boundaries
    assert snapshot.private_boundaries
    assert snapshot.store_policy.canonical_store == "ocel"
    assert snapshot.execution_boundary.read_only_invocation_allowed is True
    assert snapshot.limitations


def test_runtime_profile_and_mode_defaults_are_safe() -> None:
    snapshot = SelfRuntimeBoundaryAwarenessService().view_runtime_boundary()
    assert snapshot.profile.active is True
    assert snapshot.profile.read_only is True
    assert snapshot.profile.mutation_allowed is False
    assert snapshot.mode.active is True
    assert snapshot.mode.persona_loaded is False
    assert snapshot.mode.autonomous_runtime_claim_allowed is False
    assert snapshot.mode.ambient_filesystem_access_allowed is False
    assert snapshot.mode.permission_escalation_allowed is False


def test_track_states_include_current_and_future_tracks() -> None:
    snapshot = SelfRuntimeBoundaryAwarenessService().view_runtime_boundary()
    by_id = {item.track_id: item for item in snapshot.tracks}
    assert by_id["track:self_awareness"].status == "enabled"
    assert by_id["track:deep_self_introspection"].status == "enabled"
    assert by_id["track:observation_digestion"].status == "enabled"
    assert by_id["track:self_modification_safety"].status == "future_track"
    assert by_id["track:local_runtime_provider"].status == "future_track"
    assert by_id["track:external_contact_safety"].status == "future_track"
    assert by_id["track:external_adapter_implementation"].status == "future_track"
    assert by_id["track:mission_loop"].status == "future_track"
    assert by_id["track:growth_kernel_bridge"].status == "future_track"


def test_workspace_and_private_boundary_descriptors_are_sanitized() -> None:
    snapshot = SelfRuntimeBoundaryAwarenessService().view_runtime_boundary()
    workspace = snapshot.workspace_boundaries[0]
    assert workspace.root_alias == "primary_workspace"
    assert workspace.retrieval_scope_enabled is True
    assert workspace.direct_file_operation_scope_enabled is False
    assert workspace.full_path_exposure_allowed is False
    assert workspace.traversal_block_required is True
    assert workspace.symlink_escape_block_required is True
    private = snapshot.private_boundaries[0]
    assert private.private_material_exposure_allowed is False
    assert private.private_full_path_exposure_allowed is False
    assert private.public_repo_import_allowed is False
    assert private.prompt_raw_injection_allowed is False
    assert private.projection_only is True


def test_store_policy_and_execution_boundary_are_closed() -> None:
    snapshot = SelfRuntimeBoundaryAwarenessService().view_runtime_boundary()
    policy = snapshot.store_policy
    assert policy.canonical_store == "ocel"
    assert policy.canonical_jsonl_allowed is False
    assert policy.canonical_markdown_allowed is False
    assert policy.ocel_required is True
    boundary = snapshot.execution_boundary
    assert boundary.write_enabled is False
    assert boundary.shell_enabled is False
    assert boundary.network_enabled is False
    assert boundary.mcp_enabled is False
    assert boundary.plugin_enabled is False
    assert boundary.external_harness_enabled is False
    assert boundary.candidate_promotion_enabled is False
    assert boundary.candidate_materialization_enabled is False
    assert boundary.memory_mutation_enabled is False
    assert boundary.persona_mutation_enabled is False
    assert boundary.overlay_mutation_enabled is False


def test_truth_check_passes_when_safe() -> None:
    report = SelfRuntimeBoundaryAwarenessService().truth_check()
    assert report.status == "passed"
    assert report.review_status == "report_only"
    assert report.canonical_promotion_enabled is False
    assert report.promoted is False
    assert report.boundary_truth_summary["principle"] == "Runtime boundary truth > persona claim"
    assert report.boundary_truth_summary["canonical_store"] == "ocel"


def test_truth_check_warns_when_track_state_unknown() -> None:
    snapshot = SelfRuntimeBoundaryAwarenessService().view_runtime_boundary()
    unknown_track = RuntimeTrackState(
        track_id="track:unknown",
        track_name="unknown",
        status="unknown",
        reason=None,
        introduced_in=None,
        safety_notes=[],
    )
    report = RuntimeBoundaryTruthCheckService().check_truth(replace(snapshot, tracks=[unknown_track]))
    assert report.status == "warning"
    assert any(item.finding_type == "missing_track_state" for item in report.findings)


def test_truth_check_fails_for_invalid_store_policy() -> None:
    snapshot = SelfRuntimeBoundaryAwarenessService().view_runtime_boundary()
    bad_policy = replace(snapshot.store_policy, canonical_store="jsonl", canonical_jsonl_allowed=True)
    report = RuntimeBoundaryTruthCheckService().check_truth(replace(snapshot, store_policy=bad_policy))
    assert report.status == "failed"
    assert any(item.finding_type == "canonical_store_policy_violation" for item in report.findings)


def test_truth_check_fails_for_execution_boundary_violations() -> None:
    snapshot = SelfRuntimeBoundaryAwarenessService().view_runtime_boundary()
    bad_boundary = replace(
        snapshot.execution_boundary,
        write_enabled=True,
        shell_enabled=True,
        network_enabled=True,
        mcp_enabled=True,
        plugin_enabled=True,
        external_harness_enabled=True,
        candidate_promotion_enabled=True,
        candidate_materialization_enabled=True,
    )
    report = RuntimeBoundaryTruthCheckService().check_truth(replace(snapshot, execution_boundary=bad_boundary))
    finding_types = {item.finding_type for item in report.findings}
    assert report.status == "failed"
    assert "write_enabled_violation" in finding_types
    assert "shell_enabled_violation" in finding_types
    assert "network_enabled_violation" in finding_types
    assert "mcp_enabled_violation" in finding_types
    assert "plugin_enabled_violation" in finding_types
    assert "external_harness_enabled_violation" in finding_types
    assert "candidate_promotion_violation" in finding_types
    assert "materialization_violation" in finding_types


def test_truth_check_fails_for_private_boundary_and_runtime_claims() -> None:
    snapshot = SelfRuntimeBoundaryAwarenessService().view_runtime_boundary()
    private = replace(
        snapshot.private_boundaries[0],
        private_material_exposure_allowed=True,
        private_full_path_exposure_allowed=True,
    )
    mode = replace(
        snapshot.mode,
        autonomous_runtime_claim_allowed=True,
        ambient_filesystem_access_allowed=True,
        permission_escalation_allowed=True,
    )
    report = RuntimeBoundaryTruthCheckService().check_truth(
        replace(snapshot, private_boundaries=[private], mode=mode)
    )
    finding_types = {item.finding_type for item in report.findings}
    assert report.status == "failed"
    assert "private_boundary_violation" in finding_types
    assert "autonomous_runtime_claim_violation" in finding_types
    assert "ambient_filesystem_claim_violation" in finding_types
    assert "runtime_claim_exceeds_boundary" in finding_types


def test_optional_claim_for_disabled_track_is_detected() -> None:
    snapshot = SelfRuntimeBoundaryAwarenessService().view_runtime_boundary()
    report = RuntimeBoundaryTruthCheckService().check_truth(
        snapshot,
        optional_claims=[
            {"claim_type": "track_active", "track_id": "track:self_modification_safety"}
        ],
    )
    assert report.status == "failed"
    assert report.unsafe_claims_detected == 1
    assert any(item.finding_type == "runtime_claim_exceeds_boundary" for item in report.findings)


def test_runtime_skills_are_visible_in_capability_registry_as_read_only() -> None:
    snapshot = SelfCapabilityRegistryAwarenessService().view_registry()
    records = {record.skill_id: record for record in snapshot.records}
    assert records["skill:deep_self_runtime_boundary_view"].status == "implemented"
    assert records["skill:deep_self_runtime_boundary_truth_check"].status == "implemented"
    assert records["skill:deep_self_runtime_boundary_view"].read_only is True
    assert records["skill:deep_self_runtime_boundary_truth_check"].read_only is True
    assert records["skill:deep_self_policy_gate_map"].status == "implemented"
    assert records["skill:deep_self_trace_integrity_check"].status == "implemented"
    assert records["skill:deep_self_context_projection_view"].status == "implemented"
    assert records["skill:deep_self_context_projection_gap_report"].status == "implemented"
    assert records["skill:deep_self_candidate_memory_boundary_report"].status == "implemented"
    assert records["skill:deep_self_promotion_boundary_check"].status == "implemented"
    assert records["skill:deep_self_claim_consistency_check"].status == "implemented"


def test_pig_and_ocpx_projection_build() -> None:
    service = SelfRuntimeBoundaryAwarenessService()
    pig = service.build_pig_report()
    assert pig["version"] == "v0.21.2"
    assert pig["subject"] == "runtime_boundary"
    assert pig["principle"] == "Runtime boundary truth > persona claim"
    assert pig["canonical_store"] == "ocel"
    assert pig["write_enabled"] is False
    assert pig["shell_enabled"] is False
    assert pig["network_enabled"] is False
    assert pig["mcp_enabled"] is False
    assert pig["plugin_enabled"] is False
    assert pig["external_harness_enabled"] is False
    assert "runtime awareness is not shell/env probing" in pig["diagnostics"]
    ocpx = service.build_ocpx_projection()
    assert ocpx["state"] == "self_runtime_boundary_awareness"
    assert "SelfCapabilityRegistryState" in ocpx["source_read_models"]
    assert "SelfCapabilityTruthState" in ocpx["source_read_models"]
    assert "SelfRuntimeBoundaryState" in ocpx["target_read_models"]
    assert "SelfRuntimeTrackState" in ocpx["target_read_models"]
    assert "SelfWorkspaceBoundaryState" in ocpx["target_read_models"]
    assert "SelfPrivateBoundaryState" in ocpx["target_read_models"]
    assert "SelfCanonicalStorePolicyState" in ocpx["target_read_models"]
    assert "SelfExecutionBoundaryState" in ocpx["target_read_models"]


def test_cli_runtime_views_work() -> None:
    commands = [
        ["deep-self", "runtime", "boundary"],
        ["deep-self", "runtime", "truth-check"],
        ["deep-self", "runtime", "tracks"],
        ["deep-self", "runtime", "workspace-boundary"],
        ["deep-self", "runtime", "private-boundary"],
        ["deep-self", "runtime", "store-policy"],
        ["deep-self", "runtime", "execution-boundary"],
    ]
    for command in commands:
        result = subprocess.run(
            [sys.executable, "-m", "chanta_core.cli", *command],
            check=True,
            capture_output=True,
            text=True,
        )
        assert "Self-Runtime Boundary Awareness" in result.stdout
        assert "Runtime boundary truth > persona claim" in result.stdout
        assert "canonical_store=ocel" in result.stdout
        assert "write_enabled=False" in result.stdout
        assert "shell_enabled=False" in result.stdout
        assert "network_enabled=False" in result.stdout
        assert "raw_file_content_printed=False" in result.stdout
        assert "private_full_paths_printed=False" in result.stdout
        assert "raw_secrets_printed=False" in result.stdout
        assert "environment_variables_dumped=False" in result.stdout


def test_descriptor_types_exported() -> None:
    assert CanonicalStorePolicyDescriptor
    assert ExecutionBoundaryDescriptor
    assert PrivateBoundaryDescriptor
    assert RuntimeModeDescriptor
