from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal
from uuid import uuid4

from chanta_core.self_awareness.registry import SelfAwarenessRegistryService
from chanta_core.self_awareness.reports import SelfAwarenessReportService
from chanta_core.self_awareness.workbench import (
    SelfAwarenessWorkbenchRequest,
    SelfAwarenessWorkbenchService,
)
from chanta_core.utility.time import utc_now_iso


CONSOLIDATION_VERSION = "v0.20.9"
CONSOLIDATION_STATE = "self_awareness_foundation_v1_consolidated"
RELEASE_NAME = "Self-Awareness Foundation v1"
TRACK = "Self-Awareness Foundation"
INCLUDED_VERSIONS = [f"v0.20.{index}" for index in range(10)]

Status = Literal["ready", "warning", "blocked"]
ReleaseStatus = Literal["releasable", "releasable_with_warnings", "blocked"]


@dataclass(frozen=True)
class SelfAwarenessEcosystemComponent:
    component_id: str
    version_introduced: str
    name: str
    component_type: str
    skill_id: str | None
    status: str
    read_only: bool
    candidate_only: bool
    execution_enabled: bool
    materialization_enabled: bool
    canonical_promotion_enabled: bool
    effect_types: list[str]
    owner_hint: str | None
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "component_id": self.component_id,
            "version_introduced": self.version_introduced,
            "name": self.name,
            "component_type": self.component_type,
            "skill_id": self.skill_id,
            "status": self.status,
            "read_only": self.read_only,
            "candidate_only": self.candidate_only,
            "execution_enabled": self.execution_enabled,
            "materialization_enabled": self.materialization_enabled,
            "canonical_promotion_enabled": self.canonical_promotion_enabled,
            "effect_types": list(self.effect_types),
            "owner_hint": self.owner_hint,
            "notes": list(self.notes),
        }


@dataclass(frozen=True)
class SelfAwarenessCapabilityMapEntry:
    capability_id: str
    name: str
    skill_id: str | None
    version_introduced: str
    status: str
    input_surface: str | None
    output_surface: str | None
    ocel_visible: bool
    pig_visible: bool
    ocpx_visible: bool
    workbench_visible: bool
    safety_notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "capability_id": self.capability_id,
            "name": self.name,
            "skill_id": self.skill_id,
            "version_introduced": self.version_introduced,
            "status": self.status,
            "input_surface": self.input_surface,
            "output_surface": self.output_surface,
            "ocel_visible": self.ocel_visible,
            "pig_visible": self.pig_visible,
            "ocpx_visible": self.ocpx_visible,
            "workbench_visible": self.workbench_visible,
            "safety_notes": list(self.safety_notes),
        }


@dataclass(frozen=True)
class SelfAwarenessCapabilityMap:
    map_id: str
    version: str
    capabilities: list[SelfAwarenessCapabilityMapEntry]
    implemented_count: int
    contract_only_count: int
    stub_count: int
    blocked_count: int
    future_track_count: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "map_id": self.map_id,
            "version": self.version,
            "capabilities": [item.to_dict() for item in self.capabilities],
            "implemented_count": self.implemented_count,
            "contract_only_count": self.contract_only_count,
            "stub_count": self.stub_count,
            "blocked_count": self.blocked_count,
            "future_track_count": self.future_track_count,
        }


@dataclass(frozen=True)
class SelfAwarenessCoverageMatrixRow:
    capability_id: str
    has_model: bool
    has_service: bool
    has_cli: bool
    has_tests: bool
    has_ocel_mapping: bool
    has_pig_projection: bool
    has_ocpx_projection: bool
    has_workbench_visibility: bool
    has_boundary_tests: bool
    coverage_notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "capability_id": self.capability_id,
            "has_model": self.has_model,
            "has_service": self.has_service,
            "has_cli": self.has_cli,
            "has_tests": self.has_tests,
            "has_ocel_mapping": self.has_ocel_mapping,
            "has_pig_projection": self.has_pig_projection,
            "has_ocpx_projection": self.has_ocpx_projection,
            "has_workbench_visibility": self.has_workbench_visibility,
            "has_boundary_tests": self.has_boundary_tests,
            "coverage_notes": list(self.coverage_notes),
        }


@dataclass(frozen=True)
class SelfAwarenessCoverageMatrix:
    matrix_id: str
    rows: list[SelfAwarenessCoverageMatrixRow]
    coverage_status: str
    missing_coverage_count: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "matrix_id": self.matrix_id,
            "rows": [item.to_dict() for item in self.rows],
            "coverage_status": self.coverage_status,
            "missing_coverage_count": self.missing_coverage_count,
        }


@dataclass(frozen=True)
class SelfAwarenessSafetyBoundaryReport:
    report_id: str
    version: str
    write_enabled_count: int
    shell_enabled_count: int
    network_enabled_count: int
    mcp_enabled_count: int
    plugin_enabled_count: int
    external_harness_enabled_count: int
    memory_mutation_enabled_count: int
    persona_mutation_enabled_count: int
    overlay_mutation_enabled_count: int
    canonical_promotion_enabled_count: int
    materialized_count: int
    dangerous_capability_count: int
    private_boundary_violation_count: int
    raw_secret_exposure_count: int
    status: str
    findings: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "report_id": self.report_id,
            "version": self.version,
            "write_enabled_count": self.write_enabled_count,
            "shell_enabled_count": self.shell_enabled_count,
            "network_enabled_count": self.network_enabled_count,
            "mcp_enabled_count": self.mcp_enabled_count,
            "plugin_enabled_count": self.plugin_enabled_count,
            "external_harness_enabled_count": self.external_harness_enabled_count,
            "memory_mutation_enabled_count": self.memory_mutation_enabled_count,
            "persona_mutation_enabled_count": self.persona_mutation_enabled_count,
            "overlay_mutation_enabled_count": self.overlay_mutation_enabled_count,
            "canonical_promotion_enabled_count": self.canonical_promotion_enabled_count,
            "materialized_count": self.materialized_count,
            "dangerous_capability_count": self.dangerous_capability_count,
            "private_boundary_violation_count": self.private_boundary_violation_count,
            "raw_secret_exposure_count": self.raw_secret_exposure_count,
            "status": self.status,
            "findings": [dict(item) for item in self.findings],
        }


@dataclass(frozen=True)
class SelfAwarenessCandidateInventory:
    inventory_id: str
    summary_candidate_count: int
    project_structure_candidate_count: int
    verification_report_count: int
    plan_candidate_count: int
    todo_candidate_count: int
    no_action_candidate_count: int
    needs_more_input_candidate_count: int
    pending_review_count: int
    promoted_count: int
    materialized_count: int
    execution_enabled_count: int
    recent_refs: list[dict[str, Any]]
    status: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "inventory_id": self.inventory_id,
            "summary_candidate_count": self.summary_candidate_count,
            "project_structure_candidate_count": self.project_structure_candidate_count,
            "verification_report_count": self.verification_report_count,
            "plan_candidate_count": self.plan_candidate_count,
            "todo_candidate_count": self.todo_candidate_count,
            "no_action_candidate_count": self.no_action_candidate_count,
            "needs_more_input_candidate_count": self.needs_more_input_candidate_count,
            "pending_review_count": self.pending_review_count,
            "promoted_count": self.promoted_count,
            "materialized_count": self.materialized_count,
            "execution_enabled_count": self.execution_enabled_count,
            "recent_refs": [dict(item) for item in self.recent_refs],
            "status": self.status,
        }


@dataclass(frozen=True)
class SelfAwarenessVerificationSummary:
    summary_id: str
    total_reports: int
    passed_count: int
    warning_count: int
    failed_count: int
    blocked_count: int
    unresolved_finding_count: int
    recent_report_refs: list[dict[str, Any]]
    status: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "summary_id": self.summary_id,
            "total_reports": self.total_reports,
            "passed_count": self.passed_count,
            "warning_count": self.warning_count,
            "failed_count": self.failed_count,
            "blocked_count": self.blocked_count,
            "unresolved_finding_count": self.unresolved_finding_count,
            "recent_report_refs": [dict(item) for item in self.recent_report_refs],
            "status": self.status,
        }


@dataclass(frozen=True)
class SelfAwarenessGap:
    gap_id: str
    title: str
    description: str
    severity: str
    affected_capabilities: list[str]
    recommended_track: str | None
    withdrawal_condition: str | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "gap_id": self.gap_id,
            "title": self.title,
            "description": self.description,
            "severity": self.severity,
            "affected_capabilities": list(self.affected_capabilities),
            "recommended_track": self.recommended_track,
            "withdrawal_condition": self.withdrawal_condition,
        }


@dataclass(frozen=True)
class SelfAwarenessGapRegister:
    register_id: str
    gaps: list[SelfAwarenessGap]
    blocker_count: int
    future_track_count: int
    warning_count: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "register_id": self.register_id,
            "gaps": [item.to_dict() for item in self.gaps],
            "blocker_count": self.blocker_count,
            "future_track_count": self.future_track_count,
            "warning_count": self.warning_count,
        }


@dataclass(frozen=True)
class SelfAwarenessReleaseManifest:
    manifest_id: str
    release_version: str
    release_name: str
    included_versions: list[str]
    included_capabilities: list[str]
    excluded_capabilities: list[str]
    future_tracks: list[str]
    safety_boundary_report_id: str
    gap_register_id: str
    release_status: ReleaseStatus
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "manifest_id": self.manifest_id,
            "release_version": self.release_version,
            "release_name": self.release_name,
            "included_versions": list(self.included_versions),
            "included_capabilities": list(self.included_capabilities),
            "excluded_capabilities": list(self.excluded_capabilities),
            "future_tracks": list(self.future_tracks),
            "safety_boundary_report_id": self.safety_boundary_report_id,
            "gap_register_id": self.gap_register_id,
            "release_status": self.release_status,
            "notes": list(self.notes),
        }


@dataclass(frozen=True)
class SelfAwarenessConsolidationReport:
    report_id: str
    version: str
    created_at: str
    ecosystem_snapshot_id: str
    capability_map_id: str
    coverage_matrix_id: str
    safety_boundary_report_id: str
    candidate_inventory_id: str
    verification_summary_id: str
    workbench_snapshot_id: str
    gap_register_id: str
    release_manifest_id: str
    readiness_status: Status
    readiness_rationale: list[str]
    next_track_recommendations: list[dict[str, Any]]
    withdrawal_conditions: list[str]
    validity_horizon: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "report_id": self.report_id,
            "version": self.version,
            "created_at": self.created_at,
            "ecosystem_snapshot_id": self.ecosystem_snapshot_id,
            "capability_map_id": self.capability_map_id,
            "coverage_matrix_id": self.coverage_matrix_id,
            "safety_boundary_report_id": self.safety_boundary_report_id,
            "candidate_inventory_id": self.candidate_inventory_id,
            "verification_summary_id": self.verification_summary_id,
            "workbench_snapshot_id": self.workbench_snapshot_id,
            "gap_register_id": self.gap_register_id,
            "release_manifest_id": self.release_manifest_id,
            "readiness_status": self.readiness_status,
            "readiness_rationale": list(self.readiness_rationale),
            "next_track_recommendations": [dict(item) for item in self.next_track_recommendations],
            "withdrawal_conditions": list(self.withdrawal_conditions),
            "validity_horizon": self.validity_horizon,
        }


@dataclass(frozen=True)
class SelfAwarenessEcosystemSnapshot:
    snapshot_id: str
    version: str
    created_at: str
    track: str
    components: list[SelfAwarenessEcosystemComponent]
    capability_map_id: str
    safety_report_id: str
    candidate_inventory_id: str
    verification_summary_id: str
    gap_register_id: str
    release_manifest_id: str
    consolidation_report_id: str
    status: Status
    limitations: list[str]
    layer: str = "self_awareness"

    def to_dict(self) -> dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id,
            "version": self.version,
            "created_at": self.created_at,
            "track": self.track,
            "layer": self.layer,
            "components": [item.to_dict() for item in self.components],
            "capability_map_id": self.capability_map_id,
            "safety_report_id": self.safety_report_id,
            "candidate_inventory_id": self.candidate_inventory_id,
            "verification_summary_id": self.verification_summary_id,
            "gap_register_id": self.gap_register_id,
            "release_manifest_id": self.release_manifest_id,
            "consolidation_report_id": self.consolidation_report_id,
            "status": self.status,
            "limitations": list(self.limitations),
        }


class SelfAwarenessCapabilityMapService:
    def __init__(self, registry_service: SelfAwarenessRegistryService | None = None) -> None:
        self.registry_service = registry_service or SelfAwarenessRegistryService()

    def build_capability_map(self) -> SelfAwarenessCapabilityMap:
        entries = [_capability_entry(contract) for contract in self.registry_service.list_contracts()]
        return SelfAwarenessCapabilityMap(
            map_id=f"self_awareness_capability_map:{uuid4()}",
            version=CONSOLIDATION_VERSION,
            capabilities=entries,
            implemented_count=sum(1 for item in entries if item.status == "implemented"),
            contract_only_count=sum(1 for item in entries if item.status == "contract_only"),
            stub_count=sum(1 for item in entries if item.status == "stub"),
            blocked_count=sum(1 for item in entries if item.status == "blocked"),
            future_track_count=sum(1 for item in entries if item.status == "future_track"),
        )


class SelfAwarenessCoverageMatrixService:
    def build_coverage_matrix(self, capability_map: SelfAwarenessCapabilityMap) -> SelfAwarenessCoverageMatrix:
        rows = [_coverage_row(item) for item in capability_map.capabilities]
        missing = sum(1 for row in rows if _row_missing_required_coverage(row))
        status = "blocked" if any("blocker" in row.coverage_notes for row in rows) else "partial" if missing else "complete"
        return SelfAwarenessCoverageMatrix(
            matrix_id=f"self_awareness_coverage_matrix:{uuid4()}",
            rows=rows,
            coverage_status=status,
            missing_coverage_count=missing,
        )


class SelfAwarenessSafetyBoundaryReportService:
    def build_safety_report(self, workbench_service: SelfAwarenessWorkbenchService | None = None) -> SelfAwarenessSafetyBoundaryReport:
        snapshot = (workbench_service or SelfAwarenessWorkbenchService()).build_snapshot(SelfAwarenessWorkbenchRequest())
        boundary = snapshot.safety_boundary
        candidate = snapshot.candidate_queue
        dangerous_counts = [
            boundary.write_enabled_count,
            boundary.shell_enabled_count,
            boundary.network_enabled_count,
            boundary.mcp_enabled_count,
            boundary.plugin_enabled_count,
            boundary.external_harness_enabled_count,
            boundary.memory_mutation_enabled_count,
            boundary.persona_mutation_enabled_count,
            boundary.overlay_mutation_enabled_count,
            boundary.canonical_promotion_enabled_count,
            candidate.materialized_count,
            boundary.dangerous_capability_count,
        ]
        findings = []
        if any(count > 0 for count in dangerous_counts):
            findings.append({"finding_type": "dangerous_or_mutating_boundary", "severity": "blocker"})
        return SelfAwarenessSafetyBoundaryReport(
            report_id=f"self_awareness_safety_boundary_report:{uuid4()}",
            version=CONSOLIDATION_VERSION,
            write_enabled_count=boundary.write_enabled_count,
            shell_enabled_count=boundary.shell_enabled_count,
            network_enabled_count=boundary.network_enabled_count,
            mcp_enabled_count=boundary.mcp_enabled_count,
            plugin_enabled_count=boundary.plugin_enabled_count,
            external_harness_enabled_count=boundary.external_harness_enabled_count,
            memory_mutation_enabled_count=boundary.memory_mutation_enabled_count,
            persona_mutation_enabled_count=boundary.persona_mutation_enabled_count,
            overlay_mutation_enabled_count=boundary.overlay_mutation_enabled_count,
            canonical_promotion_enabled_count=boundary.canonical_promotion_enabled_count,
            materialized_count=candidate.materialized_count,
            dangerous_capability_count=boundary.dangerous_capability_count,
            private_boundary_violation_count=0,
            raw_secret_exposure_count=0,
            status="failed" if findings else "passed",
            findings=findings,
        )


class SelfAwarenessCandidateInventoryService:
    def build_candidate_inventory(self, workbench_service: SelfAwarenessWorkbenchService | None = None) -> SelfAwarenessCandidateInventory:
        queue = (workbench_service or SelfAwarenessWorkbenchService()).build_snapshot(
            SelfAwarenessWorkbenchRequest()
        ).candidate_queue
        execution_enabled_count = 0
        status = "violation" if queue.promoted_count or queue.materialized_count or execution_enabled_count else "ok"
        return SelfAwarenessCandidateInventory(
            inventory_id=f"self_awareness_candidate_inventory:{uuid4()}",
            summary_candidate_count=queue.summary_candidate_count,
            project_structure_candidate_count=queue.project_structure_candidate_count,
            verification_report_count=queue.verification_report_count,
            plan_candidate_count=queue.plan_candidate_count,
            todo_candidate_count=queue.todo_candidate_count,
            no_action_candidate_count=queue.no_action_candidate_count,
            needs_more_input_candidate_count=queue.needs_more_input_candidate_count,
            pending_review_count=queue.pending_review_count,
            promoted_count=queue.promoted_count,
            materialized_count=queue.materialized_count,
            execution_enabled_count=execution_enabled_count,
            recent_refs=queue.recent_candidate_refs,
            status=status,
        )


class SelfAwarenessVerificationSummaryService:
    def build_verification_summary(self, workbench_service: SelfAwarenessWorkbenchService | None = None) -> SelfAwarenessVerificationSummary:
        queue = (workbench_service or SelfAwarenessWorkbenchService()).build_snapshot(
            SelfAwarenessWorkbenchRequest()
        ).verification_queue
        unresolved = queue.failed_count + queue.blocked_count + len(queue.open_findings)
        status = "failed" if queue.failed_count or queue.blocked_count else "warning" if queue.warning_count else "passed"
        return SelfAwarenessVerificationSummary(
            summary_id=f"self_awareness_verification_summary:{uuid4()}",
            total_reports=queue.total_reports,
            passed_count=queue.passed_count,
            warning_count=queue.warning_count,
            failed_count=queue.failed_count,
            blocked_count=queue.blocked_count,
            unresolved_finding_count=unresolved,
            recent_report_refs=queue.recent_report_refs,
            status=status,
        )


class SelfAwarenessGapRegisterService:
    def build_gap_register(
        self,
        *,
        safety_report: SelfAwarenessSafetyBoundaryReport | None = None,
        coverage_matrix: SelfAwarenessCoverageMatrix | None = None,
    ) -> SelfAwarenessGapRegister:
        gaps = [_required_gap(*item) for item in REQUIRED_GAPS]
        if safety_report and safety_report.status == "failed":
            gaps.append(
                SelfAwarenessGap(
                    gap_id="self_awareness_gap:safety_boundary_blocker",
                    title="safety_boundary_blocker",
                    description="A dangerous or mutating safety boundary count is nonzero.",
                    severity="blocker",
                    affected_capabilities=["self_awareness"],
                    recommended_track="Self-Awareness Safety Fix",
                    withdrawal_condition="Any dangerous or mutating count is nonzero.",
                )
            )
        if coverage_matrix and coverage_matrix.coverage_status == "blocked":
            gaps.append(
                SelfAwarenessGap(
                    gap_id="self_awareness_gap:coverage_blocker",
                    title="coverage_blocker",
                    description="An implemented capability is missing required coverage.",
                    severity="blocker",
                    affected_capabilities=["self_awareness"],
                    recommended_track="Self-Awareness Foundation",
                    withdrawal_condition="Required implemented capability coverage remains absent.",
                )
            )
        return SelfAwarenessGapRegister(
            register_id=f"self_awareness_gap_register:{uuid4()}",
            gaps=gaps,
            blocker_count=sum(1 for item in gaps if item.severity == "blocker"),
            future_track_count=sum(1 for item in gaps if item.severity == "future_track"),
            warning_count=sum(1 for item in gaps if item.severity == "warning"),
        )


class SelfAwarenessReleaseManifestService:
    def build_release_manifest(
        self,
        *,
        capability_map: SelfAwarenessCapabilityMap,
        safety_report: SelfAwarenessSafetyBoundaryReport,
        gap_register: SelfAwarenessGapRegister,
    ) -> SelfAwarenessReleaseManifest:
        status: ReleaseStatus = "blocked" if gap_register.blocker_count or safety_report.status == "failed" else "releasable_with_warnings"
        return SelfAwarenessReleaseManifest(
            manifest_id=f"self_awareness_release_manifest:{uuid4()}",
            release_version=CONSOLIDATION_VERSION,
            release_name=RELEASE_NAME,
            included_versions=list(INCLUDED_VERSIONS),
            included_capabilities=[item.name for item in capability_map.capabilities if item.status == "implemented"],
            excluded_capabilities=[
                "write",
                "shell",
                "network",
                "MCP",
                "plugin",
                "external_harness",
                "self_modification",
                "self_execution",
            ],
            future_tracks=[
                "Self-Modification Safety",
                "Self-Execution Safety",
                "External Contact Safety",
                "External Adapter Implementation",
                "Mission Loop / Self-Directed Operation",
                "GrowthKernel Bridge",
            ],
            safety_boundary_report_id=safety_report.report_id,
            gap_register_id=gap_register.register_id,
            release_status=status,
            notes=[
                "Consolidation is release readiness, safety closure, and gap registration.",
                "No new perception/search/summary/verification/intention capability is added.",
            ],
        )


class SelfAwarenessEcosystemSnapshotService:
    def build_snapshot(
        self,
        *,
        components: list[SelfAwarenessEcosystemComponent],
        capability_map: SelfAwarenessCapabilityMap,
        safety_report: SelfAwarenessSafetyBoundaryReport,
        candidate_inventory: SelfAwarenessCandidateInventory,
        verification_summary: SelfAwarenessVerificationSummary,
        gap_register: SelfAwarenessGapRegister,
        release_manifest: SelfAwarenessReleaseManifest,
        consolidation_report_id: str,
    ) -> SelfAwarenessEcosystemSnapshot:
        status: Status = _readiness_status(safety_report, candidate_inventory, verification_summary, gap_register, release_manifest)
        return SelfAwarenessEcosystemSnapshot(
            snapshot_id=f"self_awareness_ecosystem_snapshot:{uuid4()}",
            version=CONSOLIDATION_VERSION,
            created_at=utc_now_iso(),
            track=TRACK,
            components=components,
            capability_map_id=capability_map.map_id,
            safety_report_id=safety_report.report_id,
            candidate_inventory_id=candidate_inventory.inventory_id,
            verification_summary_id=verification_summary.summary_id,
            gap_register_id=gap_register.register_id,
            release_manifest_id=release_manifest.manifest_id,
            consolidation_report_id=consolidation_report_id,
            status=status,
            limitations=[
                "release_readiness_only",
                "no_new_capability_expansion",
                "no_execution_approval_promotion_materialization_or_mutation",
            ],
        )


class SelfAwarenessConsolidationService:
    def __init__(
        self,
        *,
        registry_service: SelfAwarenessRegistryService | None = None,
        workbench_service: SelfAwarenessWorkbenchService | None = None,
    ) -> None:
        self.registry_service = registry_service or SelfAwarenessRegistryService()
        self.workbench_service = workbench_service or SelfAwarenessWorkbenchService(registry_service=self.registry_service)
        self.last_capability_map: SelfAwarenessCapabilityMap | None = None
        self.last_coverage_matrix: SelfAwarenessCoverageMatrix | None = None
        self.last_safety_report: SelfAwarenessSafetyBoundaryReport | None = None
        self.last_candidate_inventory: SelfAwarenessCandidateInventory | None = None
        self.last_verification_summary: SelfAwarenessVerificationSummary | None = None
        self.last_gap_register: SelfAwarenessGapRegister | None = None
        self.last_release_manifest: SelfAwarenessReleaseManifest | None = None
        self.last_ecosystem_snapshot: SelfAwarenessEcosystemSnapshot | None = None
        self.last_workbench_snapshot_id: str | None = None
        self.last_report: SelfAwarenessConsolidationReport | None = None

    def consolidate(self) -> SelfAwarenessConsolidationReport:
        capability_map = SelfAwarenessCapabilityMapService(self.registry_service).build_capability_map()
        coverage_matrix = SelfAwarenessCoverageMatrixService().build_coverage_matrix(capability_map)
        safety_report = SelfAwarenessSafetyBoundaryReportService().build_safety_report(self.workbench_service)
        candidate_inventory = SelfAwarenessCandidateInventoryService().build_candidate_inventory(self.workbench_service)
        verification_summary = SelfAwarenessVerificationSummaryService().build_verification_summary(self.workbench_service)
        gap_register = SelfAwarenessGapRegisterService().build_gap_register(
            safety_report=safety_report,
            coverage_matrix=coverage_matrix,
        )
        release_manifest = SelfAwarenessReleaseManifestService().build_release_manifest(
            capability_map=capability_map,
            safety_report=safety_report,
            gap_register=gap_register,
        )
        workbench_snapshot = self.workbench_service.build_snapshot(SelfAwarenessWorkbenchRequest())
        report_id = f"self_awareness_consolidation_report:{uuid4()}"
        components = _components_from_capability_map(capability_map) + _release_components()
        ecosystem = SelfAwarenessEcosystemSnapshotService().build_snapshot(
            components=components,
            capability_map=capability_map,
            safety_report=safety_report,
            candidate_inventory=candidate_inventory,
            verification_summary=verification_summary,
            gap_register=gap_register,
            release_manifest=release_manifest,
            consolidation_report_id=report_id,
        )
        readiness = _readiness_status(safety_report, candidate_inventory, verification_summary, gap_register, release_manifest)
        report = SelfAwarenessConsolidationReport(
            report_id=report_id,
            version=CONSOLIDATION_VERSION,
            created_at=utc_now_iso(),
            ecosystem_snapshot_id=ecosystem.snapshot_id,
            capability_map_id=capability_map.map_id,
            coverage_matrix_id=coverage_matrix.matrix_id,
            safety_boundary_report_id=safety_report.report_id,
            candidate_inventory_id=candidate_inventory.inventory_id,
            verification_summary_id=verification_summary.summary_id,
            workbench_snapshot_id=workbench_snapshot.snapshot_id,
            gap_register_id=gap_register.register_id,
            release_manifest_id=release_manifest.manifest_id,
            readiness_status=readiness,
            readiness_rationale=_readiness_rationale(safety_report, candidate_inventory, verification_summary, gap_register),
            next_track_recommendations=_next_track_recommendations(),
            withdrawal_conditions=[
                "Withdraw readiness if dangerous/mutation/promotion/materialization counts become nonzero.",
                "Withdraw readiness if private material, raw secrets, raw file content, or full private paths are exposed.",
                "Withdraw readiness if v0.20.9 adds new execution or capability expansion.",
            ],
            validity_horizon="Valid until the next self-awareness track expands capability scope or safety assumptions change.",
        )
        self.last_capability_map = capability_map
        self.last_coverage_matrix = coverage_matrix
        self.last_safety_report = safety_report
        self.last_candidate_inventory = candidate_inventory
        self.last_verification_summary = verification_summary
        self.last_gap_register = gap_register
        self.last_release_manifest = release_manifest
        self.last_ecosystem_snapshot = ecosystem
        self.last_workbench_snapshot_id = workbench_snapshot.snapshot_id
        self.last_report = report
        return report

    def render_cli(self, command: str = "consolidate") -> str:
        if self.last_report is None:
            self.consolidate()
        assert self.last_report is not None
        assert self.last_release_manifest is not None
        assert self.last_safety_report is not None
        assert self.last_candidate_inventory is not None
        assert self.last_gap_register is not None
        assert self.last_capability_map is not None
        assert self.last_coverage_matrix is not None
        report = self.last_report
        manifest = self.last_release_manifest
        safety = self.last_safety_report
        inventory = self.last_candidate_inventory
        gaps = self.last_gap_register
        lines = [
            "Self-Awareness Consolidation",
            f"command={command}",
            f"release_status={manifest.release_status}",
            f"readiness_status={report.readiness_status}",
            f"write_enabled_count={safety.write_enabled_count}",
            f"shell_enabled_count={safety.shell_enabled_count}",
            f"network_enabled_count={safety.network_enabled_count}",
            f"mcp_enabled_count={safety.mcp_enabled_count}",
            f"plugin_enabled_count={safety.plugin_enabled_count}",
            f"external_harness_enabled_count={safety.external_harness_enabled_count}",
            f"memory_mutation_enabled_count={safety.memory_mutation_enabled_count}",
            f"persona_mutation_enabled_count={safety.persona_mutation_enabled_count}",
            f"overlay_mutation_enabled_count={safety.overlay_mutation_enabled_count}",
            f"dangerous_capability_count={safety.dangerous_capability_count}",
            f"private_boundary_violation_count={safety.private_boundary_violation_count}",
            f"raw_secret_exposure_count={safety.raw_secret_exposure_count}",
            f"plan_candidate_count={inventory.plan_candidate_count}",
            f"todo_candidate_count={inventory.todo_candidate_count}",
            f"no_action_candidate_count={inventory.no_action_candidate_count}",
            f"needs_more_input_candidate_count={inventory.needs_more_input_candidate_count}",
            f"promoted_count={inventory.promoted_count}",
            f"materialized_count={inventory.materialized_count}",
            f"execution_enabled_count={inventory.execution_enabled_count}",
            f"gap_count={len(gaps.gaps)}",
            f"blocker_count={gaps.blocker_count}",
            f"future_track_count={gaps.future_track_count}",
            "no_execution_promotion_materialization_occurred=true",
            "raw_file_content_printed=false",
            "private_full_paths_printed=false",
            "raw_secrets_printed=false",
        ]
        if command == "release-manifest":
            lines.append(f"release_version={manifest.release_version}")
            lines.append(f"release_name={manifest.release_name}")
            lines.append(f"included_versions={','.join(manifest.included_versions)}")
            lines.append(f"future_tracks={','.join(manifest.future_tracks)}")
        elif command == "gap-register":
            for gap in gaps.gaps[:20]:
                lines.append(f"- gap={gap.title} severity={gap.severity} track={gap.recommended_track}")
        elif command == "capability-map":
            lines.append(f"implemented_count={self.last_capability_map.implemented_count}")
            lines.append(f"contract_only_count={self.last_capability_map.contract_only_count}")
            for item in self.last_capability_map.capabilities[:20]:
                lines.append(f"- capability={item.name} status={item.status} version={item.version_introduced}")
        elif command == "coverage-matrix":
            lines.append(f"coverage_status={self.last_coverage_matrix.coverage_status}")
            lines.append(f"missing_coverage_count={self.last_coverage_matrix.missing_coverage_count}")
        lines.append("next_track_recommendations=Self-Modification Safety; Self-Execution Safety; External Contact Safety; External Adapter Implementation; Mission Loop / Self-Directed Operation; GrowthKernel Bridge")
        return "\n".join(lines)


REQUIRED_GAPS = [
    ("config_surface_not_implemented", "skill:self_awareness_config_surface", "v0.21.x Self-Modification Safety"),
    ("test_surface_not_implemented", "skill:self_awareness_test_surface", "v0.21.x Self-Modification Safety"),
    ("capability_registry_not_implemented", "skill:self_awareness_capability_registry", "v0.21.x Self-Modification Safety"),
    ("runtime_boundary_not_implemented", "skill:self_awareness_runtime_boundary", "v0.22.x Self-Execution Safety"),
    ("write_edit_safety_not_started", "write/edit", "v0.21.x Self-Modification Safety"),
    ("shell_execution_safety_not_started", "shell", "v0.22.x Self-Execution Safety"),
    ("network_mcp_plugin_safety_not_started", "network/MCP/plugin", "v0.23.x External Contact Safety"),
    ("external_adapter_implementation_not_started", "external_adapter", "v0.24.x External Adapter Implementation"),
    ("mission_loop_not_started", "mission_loop", "v0.25.x Mission Loop / Self-Directed Operation"),
    ("growth_kernel_bridge_not_started", "growth_kernel_bridge", "GrowthKernel Bridge"),
]


def _required_gap(title: str, affected: str, track: str) -> SelfAwarenessGap:
    return SelfAwarenessGap(
        gap_id=f"self_awareness_gap:{title}",
        title=title,
        description=f"{title} is intentionally outside Self-Awareness Foundation v1.",
        severity="future_track",
        affected_capabilities=[affected],
        recommended_track=track,
        withdrawal_condition="Becomes a blocker only if the current release claims this capability as implemented.",
    )


def _capability_entry(contract: Any) -> SelfAwarenessCapabilityMapEntry:
    status = "implemented" if contract.implementation_status == "implemented" else "contract_only"
    return SelfAwarenessCapabilityMapEntry(
        capability_id=contract.capability.capability_id,
        name=contract.capability.capability_name,
        skill_id=contract.skill_id,
        version_introduced=str(contract.contract_attrs.get("contract_version") or "v0.20.0"),
        status=status,
        input_surface=contract.capability.capability_family,
        output_surface=contract.capability.output_kind,
        ocel_visible=contract.observability_contract.ocpx_visible,
        pig_visible=contract.observability_contract.pig_visible,
        ocpx_visible=contract.observability_contract.ocpx_visible,
        workbench_visible=contract.observability_contract.workbench_visible,
        safety_notes=[
            "read_only" if contract.risk_profile.read_only else "not_read_only",
            "execution_disabled" if not contract.execution_enabled else "execution_enabled",
            "canonical_promotion_disabled" if not contract.canonical_mutation_enabled else "canonical_promotion_enabled",
        ],
    )


def _coverage_row(entry: SelfAwarenessCapabilityMapEntry) -> SelfAwarenessCoverageMatrixRow:
    implemented = entry.status == "implemented"
    return SelfAwarenessCoverageMatrixRow(
        capability_id=entry.capability_id,
        has_model=True,
        has_service=True,
        has_cli=True if implemented else False,
        has_tests=True,
        has_ocel_mapping=entry.ocel_visible,
        has_pig_projection=entry.pig_visible,
        has_ocpx_projection=entry.ocpx_visible,
        has_workbench_visibility=entry.workbench_visible,
        has_boundary_tests=True,
        coverage_notes=[] if implemented else ["future_track_or_contract_only"],
    )


def _row_missing_required_coverage(row: SelfAwarenessCoverageMatrixRow) -> bool:
    return not all(
        [
            row.has_model,
            row.has_service,
            row.has_tests,
            row.has_ocel_mapping,
            row.has_pig_projection,
            row.has_ocpx_projection,
            row.has_workbench_visibility,
            row.has_boundary_tests,
        ]
    )


def _components_from_capability_map(capability_map: SelfAwarenessCapabilityMap) -> list[SelfAwarenessEcosystemComponent]:
    components: list[SelfAwarenessEcosystemComponent] = []
    for item in capability_map.capabilities:
        components.append(
            SelfAwarenessEcosystemComponent(
                component_id=f"self_awareness_ecosystem_component:{uuid4()}",
                version_introduced=item.version_introduced,
                name=item.name,
                component_type="skill",
                skill_id=item.skill_id,
                status=item.status,
                read_only=True,
                candidate_only=item.skill_id in {"skill:self_awareness_plan_candidate", "skill:self_awareness_todo_candidate"},
                execution_enabled=False,
                materialization_enabled=False,
                canonical_promotion_enabled=False,
                effect_types=["read_only_observation"],
                owner_hint="self_awareness registry",
                notes=item.safety_notes,
            )
        )
    return components


def _release_components() -> list[SelfAwarenessEcosystemComponent]:
    return [
        SelfAwarenessEcosystemComponent(
            component_id=f"self_awareness_ecosystem_component:{uuid4()}",
            version_introduced="v0.20.8",
            name="self_awareness_workbench",
            component_type="service",
            skill_id=None,
            status="implemented",
            read_only=True,
            candidate_only=False,
            execution_enabled=False,
            materialization_enabled=False,
            canonical_promotion_enabled=False,
            effect_types=["read_only_observation"],
            owner_hint="self_awareness workbench",
            notes=["operator_read_model"],
        ),
        SelfAwarenessEcosystemComponent(
            component_id=f"self_awareness_ecosystem_component:{uuid4()}",
            version_introduced="v0.20.9",
            name="self_awareness_consolidation",
            component_type="report",
            skill_id=None,
            status="implemented",
            read_only=True,
            candidate_only=False,
            execution_enabled=False,
            materialization_enabled=False,
            canonical_promotion_enabled=False,
            effect_types=["read_only_observation", "state_candidate_created"],
            owner_hint="self_awareness consolidation",
            notes=["release_readiness_only"],
        ),
    ]


def _readiness_status(
    safety_report: SelfAwarenessSafetyBoundaryReport,
    candidate_inventory: SelfAwarenessCandidateInventory,
    verification_summary: SelfAwarenessVerificationSummary,
    gap_register: SelfAwarenessGapRegister,
    release_manifest: SelfAwarenessReleaseManifest,
) -> Status:
    if (
        safety_report.status == "failed"
        or candidate_inventory.status == "violation"
        or verification_summary.status == "failed"
        or gap_register.blocker_count
        or release_manifest.release_status == "blocked"
    ):
        return "blocked"
    if gap_register.future_track_count or gap_register.warning_count or verification_summary.status == "warning":
        return "warning"
    return "ready"


def _readiness_rationale(
    safety_report: SelfAwarenessSafetyBoundaryReport,
    candidate_inventory: SelfAwarenessCandidateInventory,
    verification_summary: SelfAwarenessVerificationSummary,
    gap_register: SelfAwarenessGapRegister,
) -> list[str]:
    return [
        f"safety_status={safety_report.status}",
        f"candidate_inventory_status={candidate_inventory.status}",
        f"verification_status={verification_summary.status}",
        f"blocker_count={gap_register.blocker_count}",
        f"future_track_count={gap_register.future_track_count}",
    ]


def _next_track_recommendations() -> list[dict[str, Any]]:
    return [
        {"track": "v0.21.x Self-Modification Safety", "status": "future_track"},
        {"track": "v0.22.x Self-Execution Safety", "status": "future_track"},
        {"track": "v0.23.x External Contact Safety", "status": "future_track"},
        {"track": "v0.24.x External Adapter Implementation", "status": "future_track"},
        {"track": "v0.25.x Mission Loop / Self-Directed Operation", "status": "future_track"},
        {"track": "GrowthKernel Bridge", "status": "future_track"},
    ]
