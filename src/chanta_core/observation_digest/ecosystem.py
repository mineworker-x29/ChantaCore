from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from chanta_core.context.history import ContextHistoryEntry, new_context_history_entry_id
from chanta_core.observation_digest.service import DIGESTION_SKILL_IDS, OBSERVATION_SKILL_IDS
from chanta_core.ocel.models import OCELEvent, OCELObject, OCELRecord, OCELRelation
from chanta_core.ocel.store import OCELStore
from chanta_core.skills.ids import (
    new_observation_digestion_capability_map_id,
    new_observation_digestion_consolidation_finding_id,
    new_observation_digestion_consolidation_report_id,
    new_observation_digestion_ecosystem_component_id,
    new_observation_digestion_ecosystem_snapshot_id,
    new_observation_digestion_gap_register_id,
    new_observation_digestion_release_manifest_id,
    new_observation_digestion_safety_boundary_report_id,
)
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso


ECOSYSTEM_SOURCE = "observation_digestion_ecosystem_consolidation"
READINESS_LEVELS = {"ready", "partial", "contract_only", "stub_only", "blocked", "future_track", "unknown"}


@dataclass(frozen=True)
class ObservationDigestionEcosystemSnapshot:
    snapshot_id: str
    version: str
    observation_skill_count: int
    digestion_skill_count: int
    registry_entry_count: int
    proposal_surface_count: int
    invocation_binding_count: int
    conformance_report_count: int
    static_digestion_report_count: int
    observation_spine_object_count: int
    adapter_contract_count: int
    adapter_candidate_count: int
    unsupported_feature_count: int
    pending_review_count: int
    executable_external_candidate_count: int
    created_at: str
    snapshot_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id,
            "version": self.version,
            "observation_skill_count": self.observation_skill_count,
            "digestion_skill_count": self.digestion_skill_count,
            "registry_entry_count": self.registry_entry_count,
            "proposal_surface_count": self.proposal_surface_count,
            "invocation_binding_count": self.invocation_binding_count,
            "conformance_report_count": self.conformance_report_count,
            "static_digestion_report_count": self.static_digestion_report_count,
            "observation_spine_object_count": self.observation_spine_object_count,
            "adapter_contract_count": self.adapter_contract_count,
            "adapter_candidate_count": self.adapter_candidate_count,
            "unsupported_feature_count": self.unsupported_feature_count,
            "pending_review_count": self.pending_review_count,
            "executable_external_candidate_count": self.executable_external_candidate_count,
            "created_at": self.created_at,
            "snapshot_attrs": dict(self.snapshot_attrs),
        }


@dataclass(frozen=True)
class ObservationDigestionEcosystemComponent:
    component_id: str
    snapshot_id: str
    component_name: str
    component_kind: str
    status: str
    readiness_level: str
    object_refs: list[str]
    dependency_refs: list[str]
    finding_refs: list[str]
    created_at: str
    component_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "component_id": self.component_id,
            "snapshot_id": self.snapshot_id,
            "component_name": self.component_name,
            "component_kind": self.component_kind,
            "status": self.status,
            "readiness_level": self.readiness_level,
            "object_refs": list(self.object_refs),
            "dependency_refs": list(self.dependency_refs),
            "finding_refs": list(self.finding_refs),
            "created_at": self.created_at,
            "component_attrs": dict(self.component_attrs),
        }


@dataclass(frozen=True)
class ObservationDigestionCapabilityMap:
    capability_map_id: str
    snapshot_id: str
    capability_name: str
    capability_family: str
    source_component_ref: str
    related_skill_ids: list[str]
    related_candidate_ids: list[str]
    supported_now: bool
    requires_review: bool
    execution_enabled: bool
    future_track_hint: str | None
    created_at: str
    map_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "capability_map_id": self.capability_map_id,
            "snapshot_id": self.snapshot_id,
            "capability_name": self.capability_name,
            "capability_family": self.capability_family,
            "source_component_ref": self.source_component_ref,
            "related_skill_ids": list(self.related_skill_ids),
            "related_candidate_ids": list(self.related_candidate_ids),
            "supported_now": self.supported_now,
            "requires_review": self.requires_review,
            "execution_enabled": self.execution_enabled,
            "future_track_hint": self.future_track_hint,
            "created_at": self.created_at,
            "map_attrs": dict(self.map_attrs),
        }


@dataclass(frozen=True)
class ObservationDigestionSafetyBoundaryReport:
    safety_report_id: str
    snapshot_id: str
    external_harness_execution_allowed: bool
    external_script_execution_allowed: bool
    shell_allowed: bool
    network_allowed: bool
    write_allowed: bool
    mcp_allowed: bool
    plugin_allowed: bool
    memory_mutation_allowed: bool
    persona_mutation_allowed: bool
    overlay_mutation_allowed: bool
    raw_transcript_export_allowed: bool
    full_body_export_allowed: bool
    finding_ids: list[str]
    status: str
    created_at: str
    report_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "safety_report_id": self.safety_report_id,
            "snapshot_id": self.snapshot_id,
            "external_harness_execution_allowed": self.external_harness_execution_allowed,
            "external_script_execution_allowed": self.external_script_execution_allowed,
            "shell_allowed": self.shell_allowed,
            "network_allowed": self.network_allowed,
            "write_allowed": self.write_allowed,
            "mcp_allowed": self.mcp_allowed,
            "plugin_allowed": self.plugin_allowed,
            "memory_mutation_allowed": self.memory_mutation_allowed,
            "persona_mutation_allowed": self.persona_mutation_allowed,
            "overlay_mutation_allowed": self.overlay_mutation_allowed,
            "raw_transcript_export_allowed": self.raw_transcript_export_allowed,
            "full_body_export_allowed": self.full_body_export_allowed,
            "finding_ids": list(self.finding_ids),
            "status": self.status,
            "created_at": self.created_at,
            "report_attrs": dict(self.report_attrs),
        }


@dataclass(frozen=True)
class ObservationDigestionGapRegister:
    gap_register_id: str
    snapshot_id: str
    gap_type: str
    gap_name: str
    description: str
    severity: str
    affected_components: list[str]
    future_track_hint: str
    blocking: bool
    created_at: str
    gap_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "gap_register_id": self.gap_register_id,
            "snapshot_id": self.snapshot_id,
            "gap_type": self.gap_type,
            "gap_name": self.gap_name,
            "description": self.description,
            "severity": self.severity,
            "affected_components": list(self.affected_components),
            "future_track_hint": self.future_track_hint,
            "blocking": self.blocking,
            "created_at": self.created_at,
            "gap_attrs": dict(self.gap_attrs),
        }


@dataclass(frozen=True)
class ObservationDigestionReleaseManifest:
    release_manifest_id: str
    version: str
    snapshot_id: str
    included_versions: list[str]
    included_components: list[str]
    accepted_boundaries: list[str]
    known_limitations: list[str]
    future_tracks: list[str]
    status: str
    created_at: str
    manifest_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "release_manifest_id": self.release_manifest_id,
            "version": self.version,
            "snapshot_id": self.snapshot_id,
            "included_versions": list(self.included_versions),
            "included_components": list(self.included_components),
            "accepted_boundaries": list(self.accepted_boundaries),
            "known_limitations": list(self.known_limitations),
            "future_tracks": list(self.future_tracks),
            "status": self.status,
            "created_at": self.created_at,
            "manifest_attrs": dict(self.manifest_attrs),
        }


@dataclass(frozen=True)
class ObservationDigestionConsolidationFinding:
    finding_id: str
    snapshot_id: str
    subject_ref: str
    finding_type: str
    status: str
    severity: str
    message: str
    evidence_ref: str | None
    created_at: str
    finding_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "snapshot_id": self.snapshot_id,
            "subject_ref": self.subject_ref,
            "finding_type": self.finding_type,
            "status": self.status,
            "severity": self.severity,
            "message": self.message,
            "evidence_ref": self.evidence_ref,
            "created_at": self.created_at,
            "finding_attrs": dict(self.finding_attrs),
        }


@dataclass(frozen=True)
class ObservationDigestionConsolidationReport:
    report_id: str
    snapshot_id: str
    release_manifest_id: str
    status: str
    total_component_count: int
    ready_component_count: int
    partial_component_count: int
    contract_only_component_count: int
    blocked_component_count: int
    finding_ids: list[str]
    gap_register_ids: list[str]
    summary: str
    created_at: str
    report_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "report_id": self.report_id,
            "snapshot_id": self.snapshot_id,
            "release_manifest_id": self.release_manifest_id,
            "status": self.status,
            "total_component_count": self.total_component_count,
            "ready_component_count": self.ready_component_count,
            "partial_component_count": self.partial_component_count,
            "contract_only_component_count": self.contract_only_component_count,
            "blocked_component_count": self.blocked_component_count,
            "finding_ids": list(self.finding_ids),
            "gap_register_ids": list(self.gap_register_ids),
            "summary": self.summary,
            "created_at": self.created_at,
            "report_attrs": dict(self.report_attrs),
        }


class ObservationDigestionEcosystemConsolidationService:
    def __init__(
        self,
        *,
        trace_service: TraceService | None = None,
        ocel_store: OCELStore | None = None,
        unavailable_components: set[str] | None = None,
        external_candidate_fixtures: list[dict[str, Any]] | None = None,
        adapter_candidate_fixtures: list[dict[str, Any]] | None = None,
        unsupported_feature_fixtures: list[dict[str, Any]] | None = None,
    ) -> None:
        self.trace_service = trace_service or TraceService(ocel_store=ocel_store or OCELStore())
        self.unavailable_components = set(unavailable_components or set())
        self.external_candidate_fixtures = list(external_candidate_fixtures or [])
        self.adapter_candidate_fixtures = list(adapter_candidate_fixtures or [])
        self.unsupported_feature_fixtures = list(unsupported_feature_fixtures or [])
        self.last_snapshot: ObservationDigestionEcosystemSnapshot | None = None
        self.last_components: list[ObservationDigestionEcosystemComponent] = []
        self.last_capability_maps: list[ObservationDigestionCapabilityMap] = []
        self.last_safety_report: ObservationDigestionSafetyBoundaryReport | None = None
        self.last_gap_registers: list[ObservationDigestionGapRegister] = []
        self.last_release_manifest: ObservationDigestionReleaseManifest | None = None
        self.last_findings: list[ObservationDigestionConsolidationFinding] = []
        self.last_report: ObservationDigestionConsolidationReport | None = None

    def create_ecosystem_snapshot(self, *, version: str = "0.19.9") -> ObservationDigestionEcosystemSnapshot:
        executable_count = self._executable_external_candidate_count()
        pending_review_count = sum(
            1 for item in self.adapter_candidate_fixtures if str(item.get("review_status")) == "pending_review"
        )
        snapshot = ObservationDigestionEcosystemSnapshot(
            snapshot_id=new_observation_digestion_ecosystem_snapshot_id(),
            version=version,
            observation_skill_count=len(OBSERVATION_SKILL_IDS),
            digestion_skill_count=len(DIGESTION_SKILL_IDS),
            registry_entry_count=len(OBSERVATION_SKILL_IDS) + len(DIGESTION_SKILL_IDS),
            proposal_surface_count=1,
            invocation_binding_count=3,
            conformance_report_count=1,
            static_digestion_report_count=1,
            observation_spine_object_count=8,
            adapter_contract_count=4,
            adapter_candidate_count=len(self.adapter_candidate_fixtures),
            unsupported_feature_count=len(self.unsupported_feature_fixtures),
            pending_review_count=pending_review_count,
            executable_external_candidate_count=executable_count,
            created_at=utc_now_iso(),
            snapshot_attrs={"read_only": True, "summary_only": True},
        )
        self.last_snapshot = snapshot
        self._record_model(
            "observation_digestion_ecosystem_snapshot_created",
            "observation_digestion_ecosystem_snapshot",
            snapshot.snapshot_id,
            snapshot,
        )
        if executable_count:
            self.record_finding(
                snapshot_id=snapshot.snapshot_id,
                subject_ref=snapshot.snapshot_id,
                finding_type="executable_external_candidate_detected",
                status="open",
                severity="high",
                message="External candidate fixture reports execution enablement.",
                evidence_ref=snapshot.snapshot_id,
            )
        return snapshot

    def collect_skill_components(
        self,
        snapshot: ObservationDigestionEcosystemSnapshot,
    ) -> list[ObservationDigestionEcosystemComponent]:
        components: list[ObservationDigestionEcosystemComponent] = []
        components.append(
            self._component(
                snapshot,
                component_name="observation_internal_skill_seed_pack",
                component_kind="internal_skill",
                readiness_level="ready",
                object_refs=OBSERVATION_SKILL_IDS,
                dependency_refs=[],
            )
        )
        components.append(
            self._component(
                snapshot,
                component_name="digestion_internal_skill_seed_pack",
                component_kind="internal_skill",
                readiness_level="ready",
                object_refs=DIGESTION_SKILL_IDS,
                dependency_refs=[],
            )
        )
        return components

    def collect_registry_components(
        self,
        snapshot: ObservationDigestionEcosystemSnapshot,
    ) -> list[ObservationDigestionEcosystemComponent]:
        return [
            self._component(
                snapshot,
                component_name="skill_registry_view",
                component_kind="registry",
                readiness_level="ready",
                object_refs=["skill_registry_view"],
                dependency_refs=OBSERVATION_SKILL_IDS + DIGESTION_SKILL_IDS,
            )
        ]

    def collect_proposal_components(
        self,
        snapshot: ObservationDigestionEcosystemSnapshot,
    ) -> list[ObservationDigestionEcosystemComponent]:
        return [
            self._component(
                snapshot,
                component_name="observation_digest_proposal_surface",
                component_kind="proposal_surface",
                readiness_level="ready",
                object_refs=["observation_digest_proposal_policy"],
                dependency_refs=["skill_registry_view"],
            )
        ]

    def collect_invocation_components(
        self,
        snapshot: ObservationDigestionEcosystemSnapshot,
    ) -> list[ObservationDigestionEcosystemComponent]:
        return [
            self._component(
                snapshot,
                component_name="observation_digest_gated_invocation_surface",
                component_kind="invocation_surface",
                readiness_level="ready",
                object_refs=["observation_digest_invocation_policy"],
                dependency_refs=["observation_digest_proposal_surface"],
            )
        ]

    def collect_conformance_components(
        self,
        snapshot: ObservationDigestionEcosystemSnapshot,
    ) -> list[ObservationDigestionEcosystemComponent]:
        return [
            self._component(
                snapshot,
                component_name="observation_digest_conformance_smoke",
                component_kind="conformance",
                readiness_level="ready",
                object_refs=["observation_digest_conformance_report"],
                dependency_refs=["observation_digest_gated_invocation_surface"],
            )
        ]

    def collect_static_digestion_components(
        self,
        snapshot: ObservationDigestionEcosystemSnapshot,
    ) -> list[ObservationDigestionEcosystemComponent]:
        return [
            self._component(
                snapshot,
                component_name="external_skill_static_digestion",
                component_kind="static_digestion",
                readiness_level="ready",
                object_refs=["external_skill_static_digestion_report"],
                dependency_refs=DIGESTION_SKILL_IDS,
            )
        ]

    def collect_observation_spine_components(
        self,
        snapshot: ObservationDigestionEcosystemSnapshot,
    ) -> list[ObservationDigestionEcosystemComponent]:
        return [
            self._component(
                snapshot,
                component_name="agent_observation_spine",
                component_kind="observation_spine",
                readiness_level="ready",
                object_refs=["agent_behavior_inference_v2", "agent_movement_ontology_term"],
                dependency_refs=OBSERVATION_SKILL_IDS,
            )
        ]

    def collect_adapter_contract_components(
        self,
        snapshot: ObservationDigestionEcosystemSnapshot,
    ) -> list[ObservationDigestionEcosystemComponent]:
        return [
            self._component(
                snapshot,
                component_name="cross_harness_trace_adapter_contracts",
                component_kind="cross_harness_adapter",
                readiness_level="contract_only",
                object_refs=["harness_trace_adapter_contract"],
                dependency_refs=["agent_observation_spine"],
            )
        ]

    def collect_adapter_candidate_components(
        self,
        snapshot: ObservationDigestionEcosystemSnapshot,
    ) -> list[ObservationDigestionEcosystemComponent]:
        return [
            self._component(
                snapshot,
                component_name="observation_to_digestion_adapter_candidate_builder",
                component_kind="adapter_candidate_builder",
                readiness_level="ready",
                object_refs=["observation_digestion_adapter_candidate"],
                dependency_refs=["agent_observation_spine", "external_skill_static_digestion"],
            )
        ]

    def build_capability_map(
        self,
        snapshot: ObservationDigestionEcosystemSnapshot,
    ) -> list[ObservationDigestionCapabilityMap]:
        specs = [
            (
                "agent trace observation",
                "observation",
                "agent_observation_spine",
                OBSERVATION_SKILL_IDS,
                [],
                True,
                False,
                None,
            ),
            (
                "external skill digestion",
                "digestion",
                "external_skill_static_digestion",
                DIGESTION_SKILL_IDS,
                [],
                True,
                True,
                None,
            ),
            (
                "observed behavior adapter mapping",
                "adapter_mapping",
                "observation_to_digestion_adapter_candidate_builder",
                ["skill:external_skill_adapter_candidate"],
                [str(item.get("adapter_candidate_id")) for item in self.adapter_candidate_fixtures],
                True,
                True,
                None,
            ),
            ("write safety track", "future_write", "future_track", [], [], False, True, "v0.20+ write safety track"),
            ("shell safety track", "future_shell", "future_track", [], [], False, True, "v0.20+ shell safety track"),
            ("network safety track", "future_network", "future_track", [], [], False, True, "v0.20+ network safety track"),
            ("MCP safety track", "future_mcp", "future_track", [], [], False, True, "v0.20+ MCP safety track"),
            ("plugin safety track", "future_plugin", "future_track", [], [], False, True, "v0.20+ plugin safety track"),
        ]
        maps: list[ObservationDigestionCapabilityMap] = []
        for name, family, source_ref, skill_ids, candidate_ids, supported, review, future_hint in specs:
            item = ObservationDigestionCapabilityMap(
                capability_map_id=new_observation_digestion_capability_map_id(),
                snapshot_id=snapshot.snapshot_id,
                capability_name=name,
                capability_family=family,
                source_component_ref=source_ref,
                related_skill_ids=list(skill_ids),
                related_candidate_ids=list(candidate_ids),
                supported_now=supported,
                requires_review=review,
                execution_enabled=False,
                future_track_hint=future_hint,
                created_at=utc_now_iso(),
                map_attrs={"read_only": True},
            )
            self.last_capability_maps.append(item)
            maps.append(item)
            self._record_model(
                "observation_digestion_capability_map_created",
                "observation_digestion_capability_map",
                item.capability_map_id,
                item,
                object_links=[(item.capability_map_id, snapshot.snapshot_id, "capability_map_belongs_to_snapshot")],
            )
        return maps

    def build_safety_boundary_report(
        self,
        snapshot: ObservationDigestionEcosystemSnapshot,
    ) -> ObservationDigestionSafetyBoundaryReport:
        report = ObservationDigestionSafetyBoundaryReport(
            safety_report_id=new_observation_digestion_safety_boundary_report_id(),
            snapshot_id=snapshot.snapshot_id,
            external_harness_execution_allowed=False,
            external_script_execution_allowed=False,
            shell_allowed=False,
            network_allowed=False,
            write_allowed=False,
            mcp_allowed=False,
            plugin_allowed=False,
            memory_mutation_allowed=False,
            persona_mutation_allowed=False,
            overlay_mutation_allowed=False,
            raw_transcript_export_allowed=False,
            full_body_export_allowed=False,
            finding_ids=[item.finding_id for item in self.last_findings if item.severity == "high"],
            status="closed",
            created_at=utc_now_iso(),
            report_attrs={"dangerous_capabilities_disabled": True, "read_only": True},
        )
        self.last_safety_report = report
        self._record_model(
            "observation_digestion_safety_boundary_report_created",
            "observation_digestion_safety_boundary_report",
            report.safety_report_id,
            report,
            object_links=[(report.safety_report_id, snapshot.snapshot_id, "safety_report_summarizes_snapshot")],
        )
        return report

    def build_gap_register(
        self,
        snapshot: ObservationDigestionEcosystemSnapshot,
    ) -> list[ObservationDigestionGapRegister]:
        specs = [
            ("external_adapter", "full external adapters", "Complete external adapter implementations.", "medium", "v0.20+ adapter implementation track"),
            ("observer", "sidecar observer", "Live sidecar observation is not enabled.", "medium", "v0.20+ observer track"),
            ("collector", "event bus collector", "Event bus collection remains future work.", "medium", "v0.20+ collector track"),
            ("safety", "write safety track", "Workspace write safety remains future work.", "high", "v0.20+ write safety track"),
            ("safety", "shell safety track", "Shell safety remains future work.", "high", "v0.20+ shell safety track"),
            ("safety", "network safety track", "Network safety remains future work.", "high", "v0.20+ network safety track"),
            ("safety", "MCP safety track", "MCP safety remains future work.", "high", "v0.20+ MCP safety track"),
            ("safety", "plugin safety track", "Plugin safety remains future work.", "high", "v0.20+ plugin safety track"),
            ("collector", "enterprise collector", "Enterprise collector packaging remains future work.", "medium", "v0.20+ enterprise collector track"),
            ("foundation", "basic foundation skill pack", "A smaller foundation skill pack remains future work.", "medium", "v0.20+ foundation skill pack"),
        ]
        gaps: list[ObservationDigestionGapRegister] = []
        for gap_type, name, description, severity, future_hint in specs:
            gap = ObservationDigestionGapRegister(
                gap_register_id=new_observation_digestion_gap_register_id(),
                snapshot_id=snapshot.snapshot_id,
                gap_type=gap_type,
                gap_name=name,
                description=description,
                severity=severity,
                affected_components=["observation_digest_ecosystem"],
                future_track_hint=future_hint,
                blocking=False,
                created_at=utc_now_iso(),
                gap_attrs={"future_track": True},
            )
            self.last_gap_registers.append(gap)
            gaps.append(gap)
            self._record_model(
                "observation_digestion_gap_registered",
                "observation_digestion_gap_register",
                gap.gap_register_id,
                gap,
                object_links=[(gap.gap_register_id, snapshot.snapshot_id, "gap_register_belongs_to_snapshot")],
            )
        return gaps

    def build_release_manifest(
        self,
        snapshot: ObservationDigestionEcosystemSnapshot,
    ) -> ObservationDigestionReleaseManifest:
        manifest = ObservationDigestionReleaseManifest(
            release_manifest_id=new_observation_digestion_release_manifest_id(),
            version=snapshot.version,
            snapshot_id=snapshot.snapshot_id,
            included_versions=[f"v0.19.{index}" for index in range(10)],
            included_components=[item.component_name for item in self.last_components],
            accepted_boundaries=[
                "external candidates remain review-only",
                "dangerous capabilities remain disabled",
                "raw transcript and full body export remain disabled by default",
            ],
            known_limitations=[
                "no full external adapter implementations",
                "no sidecar observer",
                "no event bus collector",
                "no enterprise collector",
                "no write, shell, network, MCP, or plugin safety tracks",
            ],
            future_tracks=[item.gap_name for item in self.last_gap_registers],
            status="consolidated",
            created_at=utc_now_iso(),
            manifest_attrs={"read_only": True},
        )
        self.last_release_manifest = manifest
        self._record_model(
            "observation_digestion_release_manifest_created",
            "observation_digestion_release_manifest",
            manifest.release_manifest_id,
            manifest,
            object_links=[(manifest.release_manifest_id, snapshot.snapshot_id, "release_manifest_summarizes_snapshot")],
        )
        return manifest

    def record_finding(
        self,
        *,
        snapshot_id: str,
        subject_ref: str,
        finding_type: str,
        status: str,
        severity: str,
        message: str,
        evidence_ref: str | None,
        finding_attrs: dict[str, Any] | None = None,
    ) -> ObservationDigestionConsolidationFinding:
        finding = ObservationDigestionConsolidationFinding(
            finding_id=new_observation_digestion_consolidation_finding_id(),
            snapshot_id=snapshot_id,
            subject_ref=subject_ref,
            finding_type=finding_type,
            status=status,
            severity=severity,
            message=message,
            evidence_ref=evidence_ref,
            created_at=utc_now_iso(),
            finding_attrs=finding_attrs or {},
        )
        self.last_findings.append(finding)
        self._record_model(
            "observation_digestion_consolidation_finding_recorded",
            "observation_digestion_consolidation_finding",
            finding.finding_id,
            finding,
            object_links=[(finding.finding_id, snapshot_id, "consolidation_report_includes_finding")],
        )
        return finding

    def record_consolidation_report(
        self,
        snapshot: ObservationDigestionEcosystemSnapshot,
        manifest: ObservationDigestionReleaseManifest,
    ) -> ObservationDigestionConsolidationReport:
        readiness = self._readiness_counts()
        status = "warning" if self.last_findings else "completed"
        report = ObservationDigestionConsolidationReport(
            report_id=new_observation_digestion_consolidation_report_id(),
            snapshot_id=snapshot.snapshot_id,
            release_manifest_id=manifest.release_manifest_id,
            status=status,
            total_component_count=len(self.last_components),
            ready_component_count=readiness.get("ready", 0),
            partial_component_count=readiness.get("partial", 0),
            contract_only_component_count=readiness.get("contract_only", 0),
            blocked_component_count=readiness.get("blocked", 0),
            finding_ids=[item.finding_id for item in self.last_findings],
            gap_register_ids=[item.gap_register_id for item in self.last_gap_registers],
            summary=(
                f"components={len(self.last_components)} ready={readiness.get('ready', 0)} "
                f"gaps={len(self.last_gap_registers)} findings={len(self.last_findings)}"
            ),
            created_at=utc_now_iso(),
            report_attrs={
                "executable_external_candidate_count": snapshot.executable_external_candidate_count,
                "dangerous_capabilities_disabled": True,
            },
        )
        self.last_report = report
        links = [(report.report_id, snapshot.snapshot_id, "consolidation_report_summarizes_snapshot")]
        links.extend((report.report_id, gap.gap_register_id, "consolidation_report_includes_gap") for gap in self.last_gap_registers)
        links.extend((report.report_id, finding.finding_id, "consolidation_report_includes_finding") for finding in self.last_findings)
        self._record_model(
            "observation_digestion_consolidation_report_recorded",
            "observation_digestion_consolidation_report",
            report.report_id,
            report,
            object_links=links,
        )
        return report

    def consolidate(self) -> ObservationDigestionConsolidationReport:
        self._clear()
        snapshot = self.create_ecosystem_snapshot()
        self.collect_skill_components(snapshot)
        self.collect_registry_components(snapshot)
        self.collect_proposal_components(snapshot)
        self.collect_invocation_components(snapshot)
        self.collect_conformance_components(snapshot)
        self.collect_static_digestion_components(snapshot)
        self.collect_observation_spine_components(snapshot)
        self.collect_adapter_contract_components(snapshot)
        self.collect_adapter_candidate_components(snapshot)
        self.build_capability_map(snapshot)
        self.build_safety_boundary_report(snapshot)
        self.build_gap_register(snapshot)
        manifest = self.build_release_manifest(snapshot)
        return self.record_consolidation_report(snapshot, manifest)

    def render_ecosystem_summary(self) -> str:
        if self.last_report is None:
            self.consolidate()
        snapshot = self.last_snapshot
        report = self.last_report
        assert snapshot is not None and report is not None
        lines = [
            "Observation/Digestion Ecosystem",
            f"version={snapshot.version}",
            f"observation_skill_count={snapshot.observation_skill_count}",
            f"digestion_skill_count={snapshot.digestion_skill_count}",
            f"registry_entry_count={snapshot.registry_entry_count}",
            f"adapter_contract_count={snapshot.adapter_contract_count}",
            f"adapter_candidate_count={snapshot.adapter_candidate_count}",
            f"unsupported_feature_count={snapshot.unsupported_feature_count}",
            f"pending_review_count={snapshot.pending_review_count}",
            f"executable_external_candidate_count={snapshot.executable_external_candidate_count}",
            f"components={report.total_component_count}",
            f"ready={report.ready_component_count}",
            f"partial={report.partial_component_count}",
            f"contract_only={report.contract_only_component_count}",
            f"blocked={report.blocked_component_count}",
        ]
        return "\n".join(lines)

    def render_capability_map_cli(self, *, limit: int | None = None) -> str:
        if not self.last_capability_maps:
            self.consolidate()
        items = self.last_capability_maps[:limit] if limit else self.last_capability_maps
        lines = ["Observation/Digestion Capability Map"]
        for item in items:
            lines.append(
                f"- {item.capability_family}: {item.capability_name} "
                f"supported_now={str(item.supported_now).lower()} "
                f"execution_enabled={str(item.execution_enabled).lower()}"
            )
        return "\n".join(lines)

    def render_gap_register_cli(self, *, limit: int | None = None) -> str:
        if not self.last_gap_registers:
            self.consolidate()
        items = self.last_gap_registers[:limit] if limit else self.last_gap_registers
        lines = ["Observation/Digestion Gap Register"]
        for item in items:
            lines.append(f"- {item.gap_type}: {item.gap_name} future_track={item.future_track_hint}")
        return "\n".join(lines)

    def render_release_manifest_cli(self) -> str:
        if self.last_release_manifest is None:
            self.consolidate()
        manifest = self.last_release_manifest
        assert manifest is not None
        lines = [
            "Observation/Digestion Release Manifest",
            f"version={manifest.version}",
            "included_versions=" + ",".join(manifest.included_versions),
            "future_tracks=" + ",".join(manifest.future_tracks),
            f"status={manifest.status}",
        ]
        return "\n".join(lines)

    def _component(
        self,
        snapshot: ObservationDigestionEcosystemSnapshot,
        *,
        component_name: str,
        component_kind: str,
        readiness_level: str,
        object_refs: list[str],
        dependency_refs: list[str],
    ) -> ObservationDigestionEcosystemComponent:
        effective_readiness = readiness_level if readiness_level in READINESS_LEVELS else "unknown"
        status = "available"
        finding_refs: list[str] = []
        if component_name in self.unavailable_components:
            effective_readiness = "partial"
            status = "unavailable"
            finding = self.record_finding(
                snapshot_id=snapshot.snapshot_id,
                subject_ref=component_name,
                finding_type="component_unavailable",
                status="open",
                severity="medium",
                message=f"Component unavailable during ecosystem consolidation: {component_name}.",
                evidence_ref=snapshot.snapshot_id,
            )
            finding_refs.append(finding.finding_id)
        component = ObservationDigestionEcosystemComponent(
            component_id=new_observation_digestion_ecosystem_component_id(),
            snapshot_id=snapshot.snapshot_id,
            component_name=component_name,
            component_kind=component_kind,
            status=status,
            readiness_level=effective_readiness,
            object_refs=list(object_refs),
            dependency_refs=list(dependency_refs),
            finding_refs=finding_refs,
            created_at=utc_now_iso(),
            component_attrs={"read_only": True},
        )
        self.last_components.append(component)
        self._record_model(
            "observation_digestion_ecosystem_component_recorded",
            "observation_digestion_ecosystem_component",
            component.component_id,
            component,
            object_links=[(component.component_id, snapshot.snapshot_id, "ecosystem_component_belongs_to_snapshot")],
        )
        return component

    def _record_model(
        self,
        activity: str,
        object_type: str,
        object_id: str,
        model: Any,
        *,
        object_links: list[tuple[str, str, str]] | None = None,
    ) -> None:
        event_id = f"event:{uuid4()}"
        objects = [OCELObject(object_id=object_id, object_type=object_type, object_attrs=model.to_dict())]
        relations = [
            OCELRelation.event_object(event_id=event_id, object_id=object_id, qualifier=f"{object_type}_object")
        ]
        for source_id, target_id, qualifier in object_links or []:
            relations.append(
                OCELRelation.object_object(
                    source_object_id=source_id,
                    target_object_id=target_id,
                    qualifier=qualifier,
                )
            )
        self.trace_service.record_session_ocel_record(
            OCELRecord(
                event=OCELEvent(
                    event_id=event_id,
                    event_activity=activity,
                    event_timestamp=utc_now_iso(),
                    event_attrs={"source": ECOSYSTEM_SOURCE, "read_only": True, "summary_only": True},
                ),
                objects=objects,
                relations=relations,
            )
        )

    def _executable_external_candidate_count(self) -> int:
        return sum(1 for item in self.external_candidate_fixtures if bool(item.get("execution_enabled")))

    def _readiness_counts(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for component in self.last_components:
            counts[component.readiness_level] = counts.get(component.readiness_level, 0) + 1
        return counts

    def _clear(self) -> None:
        self.last_snapshot = None
        self.last_components = []
        self.last_capability_maps = []
        self.last_safety_report = None
        self.last_gap_registers = []
        self.last_release_manifest = None
        self.last_findings = []
        self.last_report = None


def ecosystem_snapshots_to_history_entries(
    snapshots: list[ObservationDigestionEcosystemSnapshot],
) -> list[ContextHistoryEntry]:
    return [
        _entry(
            content=f"Observation/Digestion ecosystem snapshot: {item.version}",
            created_at=item.created_at,
            priority=55,
            refs=[{"ref_type": "observation_digestion_ecosystem_snapshot", "ref_id": item.snapshot_id}],
            attrs={"snapshot_id": item.snapshot_id, "version": item.version},
        )
        for item in snapshots
    ]


def ecosystem_components_to_history_entries(
    components: list[ObservationDigestionEcosystemComponent],
) -> list[ContextHistoryEntry]:
    return [
        _entry(
            content=f"Ecosystem component: {item.component_name}\nReadiness: {item.readiness_level}",
            created_at=item.created_at,
            priority=90 if item.readiness_level == "blocked" else 65,
            refs=[{"ref_type": "observation_digestion_ecosystem_component", "ref_id": item.component_id}],
            attrs={"component_id": item.component_id, "readiness_level": item.readiness_level},
        )
        for item in components
    ]


def capability_maps_to_history_entries(maps: list[ObservationDigestionCapabilityMap]) -> list[ContextHistoryEntry]:
    return [
        _entry(
            content=f"Capability map: {item.capability_family}\n{item.capability_name}",
            created_at=item.created_at,
            priority=70 if item.future_track_hint else 55,
            refs=[{"ref_type": "observation_digestion_capability_map", "ref_id": item.capability_map_id}],
            attrs={"capability_map_id": item.capability_map_id, "capability_family": item.capability_family},
        )
        for item in maps
    ]


def safety_boundary_reports_to_history_entries(
    reports: list[ObservationDigestionSafetyBoundaryReport],
) -> list[ContextHistoryEntry]:
    return [
        _entry(
            content=f"Safety boundary report: {item.status}",
            created_at=item.created_at,
            priority=95 if _has_open_boundary(item) else 55,
            refs=[{"ref_type": "observation_digestion_safety_boundary_report", "ref_id": item.safety_report_id}],
            attrs={"safety_report_id": item.safety_report_id, "status": item.status},
        )
        for item in reports
    ]


def gap_registers_to_history_entries(gaps: list[ObservationDigestionGapRegister]) -> list[ContextHistoryEntry]:
    return [
        _entry(
            content=f"Ecosystem gap: {item.gap_name}\n{item.future_track_hint}",
            created_at=item.created_at,
            priority=70,
            refs=[{"ref_type": "observation_digestion_gap_register", "ref_id": item.gap_register_id}],
            attrs={"gap_register_id": item.gap_register_id, "gap_type": item.gap_type},
        )
        for item in gaps
    ]


def release_manifests_to_history_entries(
    manifests: list[ObservationDigestionReleaseManifest],
) -> list[ContextHistoryEntry]:
    return [
        _entry(
            content=f"Observation/Digestion release manifest: {item.version}",
            created_at=item.created_at,
            priority=55,
            refs=[{"ref_type": "observation_digestion_release_manifest", "ref_id": item.release_manifest_id}],
            attrs={"release_manifest_id": item.release_manifest_id, "version": item.version},
        )
        for item in manifests
    ]


def consolidation_findings_to_history_entries(
    findings: list[ObservationDigestionConsolidationFinding],
) -> list[ContextHistoryEntry]:
    return [
        _entry(
            content=f"Ecosystem consolidation finding: {item.finding_type}\n{item.message}",
            created_at=item.created_at,
            priority=90 if item.severity in {"high", "critical"} else 70,
            refs=[{"ref_type": "observation_digestion_consolidation_finding", "ref_id": item.finding_id}],
            attrs={"finding_id": item.finding_id, "severity": item.severity},
        )
        for item in findings
    ]


def consolidation_reports_to_history_entries(
    reports: list[ObservationDigestionConsolidationReport],
) -> list[ContextHistoryEntry]:
    return [
        _entry(
            content=f"Ecosystem consolidation report: {item.status}\n{item.summary}",
            created_at=item.created_at,
            priority=70 if item.status == "warning" else 55,
            refs=[{"ref_type": "observation_digestion_consolidation_report", "ref_id": item.report_id}],
            attrs={"report_id": item.report_id, "status": item.status},
        )
        for item in reports
    ]


def _entry(
    *,
    content: str,
    created_at: str,
    priority: int,
    refs: list[dict[str, Any]],
    attrs: dict[str, Any],
) -> ContextHistoryEntry:
    return ContextHistoryEntry(
        entry_id=new_context_history_entry_id(),
        session_id=None,
        process_instance_id=None,
        role="context",
        content=content,
        created_at=created_at,
        source=ECOSYSTEM_SOURCE,
        priority=priority,
        refs=refs,
        entry_attrs=attrs,
    )


def _has_open_boundary(report: ObservationDigestionSafetyBoundaryReport) -> bool:
    return any(
        [
            report.external_harness_execution_allowed,
            report.external_script_execution_allowed,
            report.shell_allowed,
            report.network_allowed,
            report.write_allowed,
            report.mcp_allowed,
            report.plugin_allowed,
            report.memory_mutation_allowed,
            report.persona_mutation_allowed,
            report.overlay_mutation_allowed,
            report.raw_transcript_export_allowed,
            report.full_body_export_allowed,
        ]
    )

