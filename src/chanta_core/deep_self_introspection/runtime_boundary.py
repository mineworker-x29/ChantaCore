from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Any, Literal
from uuid import uuid4

from chanta_core.deep_self_introspection.capability_registry import SelfCapabilityRegistryAwarenessService
from chanta_core.utility.time import utc_now_iso


TrackStatus = Literal["enabled", "disabled", "contract_only", "future_track", "blocked", "unknown"]
RuntimeTruthStatus = Literal["passed", "warning", "failed", "blocked"]


@dataclass(frozen=True)
class SelfRuntimeBoundaryViewRequest:
    profile_id: str | None = None
    include_workspace: bool = True
    include_private_boundary: bool = True
    include_tracks: bool = True
    include_store_policy: bool = True
    include_gate_policy: bool = True
    include_capability_boundary: bool = True
    include_external_boundary: bool = True
    include_claim_checks: bool = True
    max_items: int = 500

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)


@dataclass(frozen=True)
class RuntimeProfileDescriptor:
    profile_id: str
    profile_name: str
    profile_type: str
    source: str
    active: bool
    read_only: bool
    mutation_allowed: bool
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {**self.__dict__, "notes": list(self.notes)}


@dataclass(frozen=True)
class RuntimeModeDescriptor:
    mode_id: str
    mode_name: str
    mode_type: str
    active: bool
    persona_loaded: bool
    autonomous_runtime_claim_allowed: bool
    ambient_filesystem_access_allowed: bool
    permission_escalation_allowed: bool
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {**self.__dict__, "notes": list(self.notes)}


@dataclass(frozen=True)
class RuntimeTrackState:
    track_id: str
    track_name: str
    status: TrackStatus
    reason: str | None
    introduced_in: str | None
    safety_notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {**self.__dict__, "safety_notes": list(self.safety_notes)}


@dataclass(frozen=True)
class WorkspaceBoundaryDescriptor:
    boundary_id: str
    root_id: str | None
    root_alias: str | None
    workspace_scope: str
    retrieval_scope_enabled: bool
    direct_file_operation_scope_enabled: bool
    full_path_exposure_allowed: bool
    traversal_block_required: bool
    symlink_escape_block_required: bool
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {**self.__dict__, "notes": list(self.notes)}


@dataclass(frozen=True)
class PrivateBoundaryDescriptor:
    boundary_id: str
    boundary_name: str
    active: bool
    private_material_exposure_allowed: bool
    private_full_path_exposure_allowed: bool
    public_repo_import_allowed: bool
    prompt_raw_injection_allowed: bool
    projection_only: bool
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {**self.__dict__, "notes": list(self.notes)}


@dataclass(frozen=True)
class CanonicalStorePolicyDescriptor:
    policy_id: str
    canonical_store: str
    jsonl_role: str
    markdown_role: str
    canonical_jsonl_allowed: bool
    canonical_markdown_allowed: bool
    ocel_required: bool
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {**self.__dict__, "notes": list(self.notes)}


@dataclass(frozen=True)
class ExecutionBoundaryDescriptor:
    boundary_id: str
    read_only_invocation_allowed: bool
    write_enabled: bool
    shell_enabled: bool
    network_enabled: bool
    mcp_enabled: bool
    plugin_enabled: bool
    external_harness_enabled: bool
    task_creation_enabled: bool
    scheduler_enabled: bool
    candidate_materialization_enabled: bool
    candidate_promotion_enabled: bool
    memory_mutation_enabled: bool
    persona_mutation_enabled: bool
    overlay_mutation_enabled: bool
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {**self.__dict__, "notes": list(self.notes)}


@dataclass(frozen=True)
class RuntimeBoundaryFinding:
    finding_id: str
    severity: str
    finding_type: str
    message: str
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "severity": self.severity,
            "finding_type": self.finding_type,
            "message": self.message,
            "evidence_refs": [dict(item) for item in self.evidence_refs],
            "withdrawal_condition": self.withdrawal_condition,
        }


@dataclass(frozen=True)
class SelfRuntimeBoundarySnapshot:
    snapshot_id: str
    created_at: str
    request: SelfRuntimeBoundaryViewRequest
    profile: RuntimeProfileDescriptor
    mode: RuntimeModeDescriptor
    tracks: list[RuntimeTrackState]
    workspace_boundaries: list[WorkspaceBoundaryDescriptor]
    private_boundaries: list[PrivateBoundaryDescriptor]
    store_policy: CanonicalStorePolicyDescriptor
    execution_boundary: ExecutionBoundaryDescriptor
    findings: list[RuntimeBoundaryFinding]
    limitations: list[str]
    read_only: bool = True
    mutation_performed: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id,
            "created_at": self.created_at,
            "request": self.request.to_dict(),
            "profile": self.profile.to_dict(),
            "mode": self.mode.to_dict(),
            "tracks": [item.to_dict() for item in self.tracks],
            "workspace_boundaries": [item.to_dict() for item in self.workspace_boundaries],
            "private_boundaries": [item.to_dict() for item in self.private_boundaries],
            "store_policy": self.store_policy.to_dict(),
            "execution_boundary": self.execution_boundary.to_dict(),
            "findings": [item.to_dict() for item in self.findings],
            "limitations": list(self.limitations),
            "read_only": self.read_only,
            "mutation_performed": self.mutation_performed,
        }


@dataclass(frozen=True)
class SelfRuntimeBoundaryTruthReport:
    report_id: str
    snapshot_id: str
    created_at: str
    status: RuntimeTruthStatus
    findings: list[RuntimeBoundaryFinding]
    boundary_truth_summary: dict[str, Any]
    unsafe_claims_detected: int
    boundary_violations_detected: int
    disabled_tracks_confirmed: list[str]
    active_tracks_confirmed: list[str]
    limitations: list[str]
    withdrawal_conditions: list[str]
    validity_horizon: str
    review_status: str = "report_only"
    canonical_promotion_enabled: bool = False
    promoted: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "report_id": self.report_id,
            "snapshot_id": self.snapshot_id,
            "created_at": self.created_at,
            "status": self.status,
            "findings": [item.to_dict() for item in self.findings],
            "boundary_truth_summary": dict(self.boundary_truth_summary),
            "unsafe_claims_detected": self.unsafe_claims_detected,
            "boundary_violations_detected": self.boundary_violations_detected,
            "disabled_tracks_confirmed": list(self.disabled_tracks_confirmed),
            "active_tracks_confirmed": list(self.active_tracks_confirmed),
            "limitations": list(self.limitations),
            "withdrawal_conditions": list(self.withdrawal_conditions),
            "validity_horizon": self.validity_horizon,
            "review_status": self.review_status,
            "canonical_promotion_enabled": self.canonical_promotion_enabled,
            "promoted": self.promoted,
        }


class RuntimeBoundarySourceService:
    def __init__(self, capability_service: SelfCapabilityRegistryAwarenessService | None = None) -> None:
        self.capability_service = capability_service or SelfCapabilityRegistryAwarenessService()

    def load_profile_descriptor(self) -> RuntimeProfileDescriptor:
        return RuntimeProfileDescriptor(
            profile_id="runtime_profile:public_core",
            profile_name="public_core",
            profile_type="public",
            source="default",
            active=True,
            read_only=True,
            mutation_allowed=False,
            notes=["Known public runtime profile descriptor; no runtime probe is performed."],
        )

    def load_mode_descriptor(self) -> RuntimeModeDescriptor:
        return RuntimeModeDescriptor(
            mode_id="runtime_mode:public_core",
            mode_name="public_core",
            mode_type="public_core",
            active=True,
            persona_loaded=False,
            autonomous_runtime_claim_allowed=False,
            ambient_filesystem_access_allowed=False,
            permission_escalation_allowed=False,
            notes=["Mode descriptor is a read-only public boundary view."],
        )

    def load_track_states(self) -> list[RuntimeTrackState]:
        capability_snapshot = self.capability_service.view_registry()
        active_layers = {record.layer for record in capability_snapshot.records if record.status == "implemented"}
        tracks = [
            RuntimeTrackState(
                track_id="track:core_process_intelligence",
                track_name="Core / Process Intelligence",
                status="enabled",
                reason="OCEL-native substrate is available.",
                introduced_in="v0.10.x",
                safety_notes=["Read-only reporting view."],
            ),
            RuntimeTrackState(
                track_id="track:observation_digestion",
                track_name="Internal Observation + Digestion",
                status="enabled" if {"internal_observation", "internal_digestion"} <= active_layers else "unknown",
                reason="Observation/Digestion capability records are visible.",
                introduced_in="v0.19.x",
                safety_notes=["External behavior remains candidate/report oriented."],
            ),
            RuntimeTrackState(
                track_id="track:self_awareness",
                track_name="OCEL-native Self-Awareness",
                status="enabled" if "self_awareness" in active_layers else "unknown",
                reason="Self-awareness capability records are visible.",
                introduced_in="v0.20.x",
                safety_notes=["Self-awareness is not self-modification."],
            ),
            RuntimeTrackState(
                track_id="track:deep_self_introspection",
                track_name="Deep Self-Introspection",
                status="enabled" if "deep_self_introspection" in active_layers else "unknown",
                reason="Deep self-introspection capability records are visible.",
                introduced_in="v0.21.x",
                safety_notes=["Deep self-introspection is read-only in this version."],
            ),
            *_future_tracks(),
        ]
        return tracks

    def load_workspace_boundaries(self) -> list[WorkspaceBoundaryDescriptor]:
        return [
            WorkspaceBoundaryDescriptor(
                boundary_id="workspace_boundary:primary",
                root_id="workspace_root:primary",
                root_alias="primary_workspace",
                workspace_scope="active",
                retrieval_scope_enabled=True,
                direct_file_operation_scope_enabled=False,
                full_path_exposure_allowed=False,
                traversal_block_required=True,
                symlink_escape_block_required=True,
                notes=["Boundary output uses aliases and does not expose full paths."],
            )
        ]

    def load_private_boundaries(self) -> list[PrivateBoundaryDescriptor]:
        return [
            PrivateBoundaryDescriptor(
                boundary_id="private_boundary:public_chantacore",
                boundary_name="public_chantacore_private_boundary",
                active=True,
                private_material_exposure_allowed=False,
                private_full_path_exposure_allowed=False,
                public_repo_import_allowed=False,
                prompt_raw_injection_allowed=False,
                projection_only=True,
                notes=["Private material is represented only as a boundary state."],
            )
        ]

    def load_store_policy(self) -> CanonicalStorePolicyDescriptor:
        return CanonicalStorePolicyDescriptor(
            policy_id="canonical_store_policy:ocel",
            canonical_store="ocel",
            jsonl_role="export_convenience",
            markdown_role="human_readable_view",
            canonical_jsonl_allowed=False,
            canonical_markdown_allowed=False,
            ocel_required=True,
            notes=["OCEL remains the canonical substrate."],
        )

    def load_execution_boundary(self) -> ExecutionBoundaryDescriptor:
        return ExecutionBoundaryDescriptor(
            boundary_id="execution_boundary:deep_self_runtime",
            read_only_invocation_allowed=True,
            write_enabled=False,
            shell_enabled=False,
            network_enabled=False,
            mcp_enabled=False,
            plugin_enabled=False,
            external_harness_enabled=False,
            task_creation_enabled=False,
            scheduler_enabled=False,
            candidate_materialization_enabled=False,
            candidate_promotion_enabled=False,
            memory_mutation_enabled=False,
            persona_mutation_enabled=False,
            overlay_mutation_enabled=False,
            notes=["Runtime boundary awareness does not enable execution paths."],
        )


class RuntimeBoundaryFindingService:
    def evaluate(
        self,
        snapshot: SelfRuntimeBoundarySnapshot,
        optional_claims: list[dict[str, Any]] | None = None,
    ) -> list[RuntimeBoundaryFinding]:
        findings: list[RuntimeBoundaryFinding] = []
        findings.extend(_evaluate_profile_and_mode(snapshot.profile, snapshot.mode))
        findings.extend(_evaluate_tracks(snapshot.tracks))
        findings.extend(_evaluate_workspace(snapshot.workspace_boundaries))
        findings.extend(_evaluate_private_boundary(snapshot.private_boundaries))
        findings.extend(_evaluate_store_policy(snapshot.store_policy))
        findings.extend(_evaluate_execution_boundary(snapshot.execution_boundary))
        findings.extend(_evaluate_claims(snapshot, optional_claims or []))
        if not findings:
            findings.append(
                _finding(
                    "info",
                    "ok",
                    "Runtime boundary truth check passed.",
                    [{"snapshot_id": snapshot.snapshot_id}],
                    None,
                )
            )
        return findings


class RuntimeBoundaryTruthCheckService:
    def __init__(self, finding_service: RuntimeBoundaryFindingService | None = None) -> None:
        self.finding_service = finding_service or RuntimeBoundaryFindingService()

    def check_truth(
        self,
        snapshot: SelfRuntimeBoundarySnapshot,
        optional_claims: list[dict[str, Any]] | None = None,
    ) -> SelfRuntimeBoundaryTruthReport:
        findings = self.finding_service.evaluate(snapshot, optional_claims=optional_claims)
        status: RuntimeTruthStatus = "passed"
        if any(item.severity in {"error", "critical"} for item in findings):
            status = "failed"
        elif any(item.severity == "warning" for item in findings):
            status = "warning"
        unsafe_claims = sum(1 for item in findings if "claim" in item.finding_type and item.finding_type != "ok")
        boundary_violations = sum(1 for item in findings if item.severity in {"error", "critical"})
        return SelfRuntimeBoundaryTruthReport(
            report_id=f"self_runtime_boundary_truth_report:{uuid4().hex}",
            snapshot_id=snapshot.snapshot_id,
            created_at=utc_now_iso(),
            status=status,
            findings=findings,
            boundary_truth_summary={
                "principle": "Runtime boundary truth > persona claim",
                "canonical_store": snapshot.store_policy.canonical_store,
                "read_only": snapshot.read_only,
                "mutation_performed": snapshot.mutation_performed,
                "write_enabled": snapshot.execution_boundary.write_enabled,
                "shell_enabled": snapshot.execution_boundary.shell_enabled,
                "network_enabled": snapshot.execution_boundary.network_enabled,
                "mcp_enabled": snapshot.execution_boundary.mcp_enabled,
                "plugin_enabled": snapshot.execution_boundary.plugin_enabled,
                "external_harness_enabled": snapshot.execution_boundary.external_harness_enabled,
                "candidate_promotion_enabled": snapshot.execution_boundary.candidate_promotion_enabled,
                "candidate_materialization_enabled": snapshot.execution_boundary.candidate_materialization_enabled,
            },
            unsafe_claims_detected=unsafe_claims,
            boundary_violations_detected=boundary_violations,
            disabled_tracks_confirmed=[item.track_id for item in snapshot.tracks if item.status in {"disabled", "future_track"}],
            active_tracks_confirmed=[item.track_id for item in snapshot.tracks if item.status == "enabled"],
            limitations=[
                "v0.21.2 reports known runtime boundary descriptors only.",
                "Missing information becomes a limitation or finding rather than a probe.",
            ],
            withdrawal_conditions=[
                "Withdraw if runtime boundary awareness performs runtime probing.",
                "Withdraw if it changes profile, mode, workspace, private boundary, permission, or capability state.",
            ],
            validity_horizon="Valid until v0.21.3 Self-Policy/Gate Awareness changes policy boundary assumptions.",
        )


class SelfRuntimeBoundaryAwarenessService:
    def __init__(
        self,
        *,
        source_service: RuntimeBoundarySourceService | None = None,
        finding_service: RuntimeBoundaryFindingService | None = None,
        truth_service: RuntimeBoundaryTruthCheckService | None = None,
    ) -> None:
        self.source_service = source_service or RuntimeBoundarySourceService()
        self.finding_service = finding_service or RuntimeBoundaryFindingService()
        self.truth_service = truth_service or RuntimeBoundaryTruthCheckService(self.finding_service)
        self.last_snapshot: SelfRuntimeBoundarySnapshot | None = None
        self.last_truth_report: SelfRuntimeBoundaryTruthReport | None = None

    def view_runtime_boundary(
        self,
        request: SelfRuntimeBoundaryViewRequest | None = None,
    ) -> SelfRuntimeBoundarySnapshot:
        request = request or SelfRuntimeBoundaryViewRequest()
        snapshot = SelfRuntimeBoundarySnapshot(
            snapshot_id=f"self_runtime_boundary_snapshot:{uuid4().hex}",
            created_at=utc_now_iso(),
            request=request,
            profile=self.source_service.load_profile_descriptor(),
            mode=self.source_service.load_mode_descriptor(),
            tracks=self.source_service.load_track_states()[: max(0, request.max_items)] if request.include_tracks else [],
            workspace_boundaries=self.source_service.load_workspace_boundaries() if request.include_workspace else [],
            private_boundaries=self.source_service.load_private_boundaries() if request.include_private_boundary else [],
            store_policy=self.source_service.load_store_policy(),
            execution_boundary=self.source_service.load_execution_boundary(),
            findings=[],
            limitations=[
                "Runtime boundary snapshot is read-only.",
                "No shell, environment, provider, or secret probing is performed.",
                "No full private paths, raw file content, or raw secrets are emitted.",
            ],
        )
        snapshot = replace(snapshot, findings=self.finding_service.evaluate(snapshot))
        self.last_snapshot = snapshot
        return snapshot

    def truth_check(
        self,
        request: SelfRuntimeBoundaryViewRequest | None = None,
        optional_claims: list[dict[str, Any]] | None = None,
    ) -> SelfRuntimeBoundaryTruthReport:
        snapshot = self.view_runtime_boundary(request)
        report = self.truth_service.check_truth(snapshot, optional_claims=optional_claims)
        self.last_truth_report = report
        return report

    def build_pig_report(self) -> dict[str, Any]:
        snapshot = self.last_snapshot or self.view_runtime_boundary()
        boundary = snapshot.execution_boundary
        return {
            "version": "v0.21.2",
            "layer": "deep_self_introspection",
            "subject": "runtime_boundary",
            "principle": "Runtime boundary truth > persona claim",
            "canonical_store": snapshot.store_policy.canonical_store,
            "read_only": snapshot.read_only,
            "write_enabled": boundary.write_enabled,
            "shell_enabled": boundary.shell_enabled,
            "network_enabled": boundary.network_enabled,
            "mcp_enabled": boundary.mcp_enabled,
            "plugin_enabled": boundary.plugin_enabled,
            "external_harness_enabled": boundary.external_harness_enabled,
            "candidate_promotion_enabled": boundary.candidate_promotion_enabled,
            "materialization_enabled": boundary.candidate_materialization_enabled,
            "diagnostics": [
                "runtime awareness is not shell/env probing",
                "disabled tracks must not be claimed as active",
                "private boundary must not leak into public ChantaCore output",
            ],
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "self_runtime_boundary_awareness",
            "version": "v0.21.2",
            "layer": "deep_self_introspection",
            "source_read_models": [
                "SelfCapabilityRegistryState",
                "SelfCapabilityTruthState",
                "SelfAwarenessReleaseState",
                "DeepSelfIntrospectionContractState",
            ],
            "target_read_models": [
                "SelfRuntimeBoundaryState",
                "SelfRuntimeTrackState",
                "SelfWorkspaceBoundaryState",
                "SelfPrivateBoundaryState",
                "SelfCanonicalStorePolicyState",
                "SelfExecutionBoundaryState",
            ],
            "effect_types": ["read_only_observation", "state_candidate_created"],
            "canonical_store": "ocel",
        }

    def render_cli(
        self,
        command: str,
        snapshot: SelfRuntimeBoundarySnapshot | None = None,
        report: SelfRuntimeBoundaryTruthReport | None = None,
    ) -> str:
        snapshot = snapshot or self.last_snapshot or self.view_runtime_boundary()
        report = report or self.last_truth_report
        boundary = snapshot.execution_boundary
        lines = [
            "Self-Runtime Boundary Awareness",
            f"command={command}",
            f"runtime_truth_status={report.status if report else 'not_checked'}",
            "principle=Runtime boundary truth > persona claim",
            f"profile_id={snapshot.profile.profile_id}",
            f"profile_type={snapshot.profile.profile_type}",
            f"mode_id={snapshot.mode.mode_id}",
            f"mode_type={snapshot.mode.mode_type}",
            f"autonomous_runtime_claim_allowed={snapshot.mode.autonomous_runtime_claim_allowed}",
            f"ambient_filesystem_access_allowed={snapshot.mode.ambient_filesystem_access_allowed}",
            f"permission_escalation_allowed={snapshot.mode.permission_escalation_allowed}",
            f"active_tracks={','.join(item.track_id for item in snapshot.tracks if item.status == 'enabled')}",
            f"disabled_tracks={','.join(item.track_id for item in snapshot.tracks if item.status in {'disabled', 'future_track'})}",
            f"workspace_boundaries={len(snapshot.workspace_boundaries)}",
            f"private_boundaries={len(snapshot.private_boundaries)}",
            f"canonical_store={snapshot.store_policy.canonical_store}",
            f"canonical_jsonl_allowed={snapshot.store_policy.canonical_jsonl_allowed}",
            f"write_enabled={boundary.write_enabled}",
            f"shell_enabled={boundary.shell_enabled}",
            f"network_enabled={boundary.network_enabled}",
            f"mcp_enabled={boundary.mcp_enabled}",
            f"plugin_enabled={boundary.plugin_enabled}",
            f"external_harness_enabled={boundary.external_harness_enabled}",
            f"candidate_materialization_enabled={boundary.candidate_materialization_enabled}",
            f"candidate_promotion_enabled={boundary.candidate_promotion_enabled}",
            f"unsafe_claims_detected={report.unsafe_claims_detected if report else 0}",
            "read_only=True",
            "mutation_performed=False",
            "runtime_probe_performed=False",
            "permission_escalation_created=False",
            "raw_file_content_printed=False",
            "private_full_paths_printed=False",
            "raw_secrets_printed=False",
            "environment_variables_dumped=False",
        ]
        return "\n".join(lines)


def _future_tracks() -> list[RuntimeTrackState]:
    return [
        RuntimeTrackState(
            track_id="track:self_modification_safety",
            track_name="Self-Modification Safety",
            status="future_track",
            reason="Self-modification safety is outside v0.21.2.",
            introduced_in="v0.22.x",
            safety_notes=["Disabled in the current public runtime boundary view."],
        ),
        RuntimeTrackState(
            track_id="track:local_runtime_provider",
            track_name="v0.24.x Local Runtime Provider",
            status="future_track",
            reason="Local runtime provider and self-execution safety are outside v0.21.2.",
            introduced_in="v0.24.x",
            safety_notes=["Disabled in the current public runtime boundary view."],
        ),
        RuntimeTrackState(
            track_id="track:external_contact_safety",
            track_name="External Contact Safety",
            status="future_track",
            reason="External contact safety is outside v0.21.2.",
            introduced_in="v0.24.x",
            safety_notes=["Network, MCP, plugin, and provider access stay disabled here."],
        ),
        RuntimeTrackState(
            track_id="track:external_adapter_implementation",
            track_name="External Adapter Implementation",
            status="future_track",
            reason="External adapters are not enabled by runtime boundary awareness.",
            introduced_in="v0.25.x",
            safety_notes=["No adapter enablement occurs."],
        ),
        RuntimeTrackState(
            track_id="track:mission_loop",
            track_name="Mission Loop / Self-Directed Operation",
            status="future_track",
            reason="Autonomous operation is not part of v0.21.2.",
            introduced_in="future",
            safety_notes=["No autonomous mission loop is enabled."],
        ),
        RuntimeTrackState(
            track_id="track:growth_kernel_bridge",
            track_name="GrowthKernel Bridge",
            status="future_track",
            reason="Growth bridge is not part of v0.21.2.",
            introduced_in="future",
            safety_notes=["No bridge mutation or activation occurs."],
        ),
    ]


def _evaluate_profile_and_mode(
    profile: RuntimeProfileDescriptor,
    mode: RuntimeModeDescriptor,
) -> list[RuntimeBoundaryFinding]:
    findings: list[RuntimeBoundaryFinding] = []
    if not profile.profile_id or profile.profile_type == "unknown":
        findings.append(_finding("warning", "missing_runtime_profile", "Runtime profile is missing or unknown.", []))
    if profile.mutation_allowed:
        findings.append(_finding("error", "runtime_claim_exceeds_boundary", "Runtime profile allows mutation.", []))
    if mode.autonomous_runtime_claim_allowed:
        findings.append(_finding("error", "autonomous_runtime_claim_violation", "Autonomous runtime claim is allowed.", []))
    if mode.ambient_filesystem_access_allowed:
        findings.append(_finding("error", "ambient_filesystem_claim_violation", "Ambient filesystem access claim is allowed.", []))
    if mode.permission_escalation_allowed:
        findings.append(_finding("error", "runtime_claim_exceeds_boundary", "Permission escalation claim is allowed.", []))
    return findings


def _evaluate_tracks(tracks: list[RuntimeTrackState]) -> list[RuntimeBoundaryFinding]:
    findings: list[RuntimeBoundaryFinding] = []
    if not tracks:
        findings.append(_finding("warning", "missing_track_state", "No runtime track states are visible.", []))
    for track in tracks:
        if track.status == "unknown":
            findings.append(
                _finding(
                    "warning",
                    "missing_track_state",
                    f"Runtime track state is unknown for {track.track_id}.",
                    [{"track_id": track.track_id}],
                )
            )
    return findings


def _evaluate_workspace(boundaries: list[WorkspaceBoundaryDescriptor]) -> list[RuntimeBoundaryFinding]:
    findings: list[RuntimeBoundaryFinding] = []
    if not boundaries:
        findings.append(_finding("warning", "workspace_scope_ambiguous", "Workspace boundary is not visible.", []))
    for boundary in boundaries:
        evidence = [{"boundary_id": boundary.boundary_id}]
        if boundary.workspace_scope == "unknown":
            findings.append(_finding("warning", "workspace_scope_ambiguous", "Workspace scope is unknown.", evidence))
        if boundary.full_path_exposure_allowed:
            findings.append(_finding("error", "private_boundary_violation", "Workspace boundary allows full path exposure.", evidence))
        if not boundary.traversal_block_required:
            findings.append(_finding("error", "workspace_scope_ambiguous", "Traversal blocking is not required.", evidence))
        if not boundary.symlink_escape_block_required:
            findings.append(_finding("error", "workspace_scope_ambiguous", "Symlink escape blocking is not required.", evidence))
    return findings


def _evaluate_private_boundary(boundaries: list[PrivateBoundaryDescriptor]) -> list[RuntimeBoundaryFinding]:
    findings: list[RuntimeBoundaryFinding] = []
    if not boundaries:
        findings.append(_finding("warning", "private_boundary_violation", "Private boundary descriptor is not visible.", []))
    for boundary in boundaries:
        evidence = [{"boundary_id": boundary.boundary_id}]
        if boundary.private_material_exposure_allowed:
            findings.append(_finding("error", "private_boundary_violation", "Private material exposure is allowed.", evidence))
        if boundary.private_full_path_exposure_allowed:
            findings.append(_finding("error", "private_boundary_violation", "Private full path exposure is allowed.", evidence))
        if boundary.public_repo_import_allowed:
            findings.append(_finding("error", "private_boundary_violation", "Private material import into public repo is allowed.", evidence))
        if boundary.prompt_raw_injection_allowed:
            findings.append(_finding("error", "private_boundary_violation", "Raw private prompt injection is allowed.", evidence))
        if not boundary.projection_only:
            findings.append(_finding("error", "private_boundary_violation", "Private boundary is not projection-only.", evidence))
    return findings


def _evaluate_store_policy(policy: CanonicalStorePolicyDescriptor) -> list[RuntimeBoundaryFinding]:
    findings: list[RuntimeBoundaryFinding] = []
    evidence = [{"policy_id": policy.policy_id}]
    if policy.canonical_store != "ocel" or not policy.ocel_required:
        findings.append(_finding("error", "canonical_store_policy_violation", "Canonical store policy does not require OCEL.", evidence))
    if policy.canonical_jsonl_allowed:
        findings.append(_finding("error", "canonical_store_policy_violation", "JSONL is allowed as canonical store.", evidence))
    if policy.canonical_markdown_allowed:
        findings.append(_finding("error", "canonical_store_policy_violation", "Markdown is allowed as canonical store.", evidence))
    return findings


def _evaluate_execution_boundary(boundary: ExecutionBoundaryDescriptor) -> list[RuntimeBoundaryFinding]:
    checks = [
        ("write_enabled", boundary.write_enabled, "write_enabled_violation"),
        ("shell_enabled", boundary.shell_enabled, "shell_enabled_violation"),
        ("network_enabled", boundary.network_enabled, "network_enabled_violation"),
        ("mcp_enabled", boundary.mcp_enabled, "mcp_enabled_violation"),
        ("plugin_enabled", boundary.plugin_enabled, "plugin_enabled_violation"),
        ("external_harness_enabled", boundary.external_harness_enabled, "external_harness_enabled_violation"),
        ("candidate_promotion_enabled", boundary.candidate_promotion_enabled, "candidate_promotion_violation"),
        ("candidate_materialization_enabled", boundary.candidate_materialization_enabled, "materialization_violation"),
        ("memory_mutation_enabled", boundary.memory_mutation_enabled, "runtime_claim_exceeds_boundary"),
        ("persona_mutation_enabled", boundary.persona_mutation_enabled, "runtime_claim_exceeds_boundary"),
        ("overlay_mutation_enabled", boundary.overlay_mutation_enabled, "runtime_claim_exceeds_boundary"),
    ]
    findings = []
    for field_name, value, finding_type in checks:
        if value:
            findings.append(
                _finding(
                    "error",
                    finding_type,
                    f"Execution boundary unexpectedly enables {field_name}.",
                    [{"boundary_id": boundary.boundary_id, "field": field_name}],
                )
            )
    return findings


def _evaluate_claims(
    snapshot: SelfRuntimeBoundarySnapshot,
    claims: list[dict[str, Any]],
) -> list[RuntimeBoundaryFinding]:
    findings: list[RuntimeBoundaryFinding] = []
    disabled_tracks = {item.track_id for item in snapshot.tracks if item.status in {"disabled", "future_track", "blocked"}}
    for claim in claims:
        claim_type = str(claim.get("claim_type") or "")
        evidence = [dict(claim)]
        if claim_type == "track_active" and claim.get("track_id") in disabled_tracks:
            findings.append(_finding("error", "runtime_claim_exceeds_boundary", "Disabled track was claimed as active.", evidence))
        if claim_type == "ambient_filesystem_access" and claim.get("claimed_allowed"):
            findings.append(_finding("error", "ambient_filesystem_claim_violation", "Ambient filesystem access was claimed as allowed.", evidence))
        if claim_type == "autonomous_runtime" and claim.get("claimed_allowed"):
            findings.append(_finding("error", "autonomous_runtime_claim_violation", "Autonomous runtime was claimed as allowed.", evidence))
    return findings


def _finding(
    severity: str,
    finding_type: str,
    message: str,
    evidence_refs: list[dict[str, Any]],
    withdrawal_condition: str | None = "Withdraw runtime boundary judgment unless the boundary evidence is corrected.",
) -> RuntimeBoundaryFinding:
    return RuntimeBoundaryFinding(
        finding_id=f"runtime_boundary_finding:{uuid4().hex}",
        severity=severity,
        finding_type=finding_type,
        message=message,
        evidence_refs=evidence_refs,
        withdrawal_condition=withdrawal_condition,
    )
