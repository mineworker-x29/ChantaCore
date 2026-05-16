from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal
from uuid import uuid4

from chanta_core.ocel.store import OCELStore
from chanta_core.self_awareness.conformance import SelfAwarenessConformanceService
from chanta_core.self_awareness.registry import SelfAwarenessRegistryService
from chanta_core.self_awareness.reports import SelfAwarenessReportService
from chanta_core.utility.time import utc_now_iso


WorkbenchSection = Literal[
    "overview",
    "registry",
    "coverage",
    "candidates",
    "verification",
    "audit",
    "risks",
    "timeline",
    "pig",
    "ocpx",
]
CoverageStatus = Literal["not_started", "contract_only", "stub", "implemented", "blocked"]
FindingSeverity = Literal["info", "warning", "error", "critical"]
WorkbenchStatus = Literal["ok", "warning", "violation"]


@dataclass(frozen=True)
class SelfAwarenessWorkbenchRequest:
    root_id: str | None = None
    section: WorkbenchSection = "overview"
    include_registry: bool = True
    include_coverage: bool = True
    include_candidates: bool = True
    include_verification: bool = True
    include_recent_envelopes: bool = True
    include_safety: bool = True
    include_pig: bool = True
    include_ocpx: bool = True
    max_recent_items: int = 20

    def normalized(self) -> SelfAwarenessWorkbenchRequest:
        allowed = {
            "overview",
            "registry",
            "coverage",
            "candidates",
            "verification",
            "audit",
            "risks",
            "timeline",
            "pig",
            "ocpx",
        }
        section = self.section if self.section in allowed else "overview"
        return SelfAwarenessWorkbenchRequest(
            root_id=self.root_id,
            section=section,  # type: ignore[arg-type]
            include_registry=self.include_registry,
            include_coverage=self.include_coverage,
            include_candidates=self.include_candidates,
            include_verification=self.include_verification,
            include_recent_envelopes=self.include_recent_envelopes,
            include_safety=self.include_safety,
            include_pig=self.include_pig,
            include_ocpx=self.include_ocpx,
            max_recent_items=max(0, min(int(self.max_recent_items), 100)),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "root_id": self.root_id,
            "section": self.section,
            "include_registry": self.include_registry,
            "include_coverage": self.include_coverage,
            "include_candidates": self.include_candidates,
            "include_verification": self.include_verification,
            "include_recent_envelopes": self.include_recent_envelopes,
            "include_safety": self.include_safety,
            "include_pig": self.include_pig,
            "include_ocpx": self.include_ocpx,
            "max_recent_items": self.max_recent_items,
        }


@dataclass(frozen=True)
class SelfAwarenessCoverageRow:
    version: str
    capability: str
    skill_id: str | None
    status: CoverageStatus
    execution_enabled: bool
    materialization_enabled: bool
    canonical_promotion_enabled: bool
    effect_types: list[str]
    safety_notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "capability": self.capability,
            "skill_id": self.skill_id,
            "status": self.status,
            "execution_enabled": self.execution_enabled,
            "materialization_enabled": self.materialization_enabled,
            "canonical_promotion_enabled": self.canonical_promotion_enabled,
            "effect_types": list(self.effect_types),
            "safety_notes": list(self.safety_notes),
        }


@dataclass(frozen=True)
class SelfAwarenessSafetyBoundaryStatus:
    write_enabled_count: int = 0
    shell_enabled_count: int = 0
    network_enabled_count: int = 0
    mcp_enabled_count: int = 0
    plugin_enabled_count: int = 0
    external_harness_enabled_count: int = 0
    memory_mutation_enabled_count: int = 0
    persona_mutation_enabled_count: int = 0
    overlay_mutation_enabled_count: int = 0
    canonical_promotion_enabled_count: int = 0
    materialization_enabled_count: int = 0
    read_only_invocation_enabled_count: int = 0
    dangerous_execution_enabled_count: int = 0
    dangerous_capability_count: int = 0
    status: WorkbenchStatus = "ok"

    def to_dict(self) -> dict[str, Any]:
        return {
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
            "materialization_enabled_count": self.materialization_enabled_count,
            "read_only_invocation_enabled_count": self.read_only_invocation_enabled_count,
            "dangerous_execution_enabled_count": self.dangerous_execution_enabled_count,
            "dangerous_capability_count": self.dangerous_capability_count,
            "status": self.status,
        }


@dataclass(frozen=True)
class SelfAwarenessCandidateQueueView:
    plan_candidate_count: int = 0
    todo_candidate_count: int = 0
    no_action_candidate_count: int = 0
    needs_more_input_candidate_count: int = 0
    summary_candidate_count: int = 0
    project_structure_candidate_count: int = 0
    verification_report_count: int = 0
    pending_review_count: int = 0
    promoted_count: int = 0
    materialized_count: int = 0
    recent_candidate_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "plan_candidate_count": self.plan_candidate_count,
            "todo_candidate_count": self.todo_candidate_count,
            "no_action_candidate_count": self.no_action_candidate_count,
            "needs_more_input_candidate_count": self.needs_more_input_candidate_count,
            "summary_candidate_count": self.summary_candidate_count,
            "project_structure_candidate_count": self.project_structure_candidate_count,
            "verification_report_count": self.verification_report_count,
            "pending_review_count": self.pending_review_count,
            "promoted_count": self.promoted_count,
            "materialized_count": self.materialized_count,
            "recent_candidate_refs": [dict(item) for item in self.recent_candidate_refs],
        }


@dataclass(frozen=True)
class SelfAwarenessVerificationQueueView:
    total_reports: int = 0
    passed_count: int = 0
    warning_count: int = 0
    failed_count: int = 0
    blocked_count: int = 0
    recent_report_refs: list[dict[str, Any]] = field(default_factory=list)
    open_findings: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "total_reports": self.total_reports,
            "passed_count": self.passed_count,
            "warning_count": self.warning_count,
            "failed_count": self.failed_count,
            "blocked_count": self.blocked_count,
            "recent_report_refs": [dict(item) for item in self.recent_report_refs],
            "open_findings": [dict(item) for item in self.open_findings],
        }


@dataclass(frozen=True)
class SelfAwarenessEnvelopeView:
    envelope_id: str
    skill_id: str | None
    event_type: str
    effect_types: list[str]
    blocked: bool
    created_at: str
    summary: str
    object_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "envelope_id": self.envelope_id,
            "skill_id": self.skill_id,
            "event_type": self.event_type,
            "effect_types": list(self.effect_types),
            "blocked": self.blocked,
            "created_at": self.created_at,
            "summary": self.summary,
            "object_refs": [dict(item) for item in self.object_refs],
        }


@dataclass(frozen=True)
class SelfAwarenessWorkbenchFinding:
    finding_id: str
    severity: FindingSeverity
    finding_type: str
    message: str
    source_ref: dict[str, Any] | None = None
    recommended_followup: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "severity": self.severity,
            "finding_type": self.finding_type,
            "message": self.message,
            "source_ref": dict(self.source_ref) if self.source_ref else None,
            "recommended_followup": self.recommended_followup,
        }


@dataclass(frozen=True)
class SelfAwarenessWorkbenchSnapshot:
    snapshot_id: str
    created_at: str
    root_id: str | None
    coverage: list[SelfAwarenessCoverageRow]
    safety_boundary: SelfAwarenessSafetyBoundaryStatus
    candidate_queue: SelfAwarenessCandidateQueueView
    verification_queue: SelfAwarenessVerificationQueueView
    recent_envelopes: list[SelfAwarenessEnvelopeView]
    pig_status: dict[str, Any]
    ocpx_status: dict[str, Any]
    findings: list[SelfAwarenessWorkbenchFinding]
    limitations: list[str]
    read_only: bool = True
    mutation_performed: bool = False

    @property
    def status(self) -> WorkbenchStatus:
        return determine_workbench_status(self.findings, self.safety_boundary, self.candidate_queue)

    def to_dict(self) -> dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id,
            "created_at": self.created_at,
            "root_id": self.root_id,
            "status": self.status,
            "coverage": [item.to_dict() for item in self.coverage],
            "safety_boundary": self.safety_boundary.to_dict(),
            "candidate_queue": self.candidate_queue.to_dict(),
            "verification_queue": self.verification_queue.to_dict(),
            "recent_envelopes": [item.to_dict() for item in self.recent_envelopes],
            "pig_status": dict(self.pig_status),
            "ocpx_status": dict(self.ocpx_status),
            "findings": [item.to_dict() for item in self.findings],
            "limitations": list(self.limitations),
            "read_only": self.read_only,
            "mutation_performed": self.mutation_performed,
        }


class SelfAwarenessCoverageService:
    def __init__(self, registry_service: SelfAwarenessRegistryService | None = None) -> None:
        self.registry_service = registry_service or SelfAwarenessRegistryService()

    def build_coverage(self) -> list[SelfAwarenessCoverageRow]:
        rows: list[SelfAwarenessCoverageRow] = []
        for contract in self.registry_service.list_contracts():
            rows.append(
                SelfAwarenessCoverageRow(
                    version=str(contract.contract_attrs.get("contract_version") or "v0.20.0"),
                    capability=contract.capability.capability_name,
                    skill_id=contract.skill_id,
                    status=_coverage_status(contract.implementation_status),
                    execution_enabled=contract.execution_enabled,
                    materialization_enabled=bool(contract.contract_attrs.get("materialized", False)),
                    canonical_promotion_enabled=bool(
                        contract.contract_attrs.get("canonical_promotion_enabled", False)
                    ),
                    effect_types=[contract.effect_type],
                    safety_notes=_safety_notes(contract),
                )
            )
        return rows


class SelfAwarenessSafetyBoundaryService:
    def __init__(
        self,
        registry_service: SelfAwarenessRegistryService | None = None,
        conformance_service: SelfAwarenessConformanceService | None = None,
    ) -> None:
        self.registry_service = registry_service or SelfAwarenessRegistryService()
        self.conformance_service = conformance_service or SelfAwarenessConformanceService(self.registry_service)

    def inspect_safety_boundary(
        self,
        *,
        candidate_queue: SelfAwarenessCandidateQueueView | None = None,
    ) -> SelfAwarenessSafetyBoundaryStatus:
        report = self.conformance_service.run_conformance()
        materialized_count = candidate_queue.materialized_count if candidate_queue else 0
        status = _boundary_status(
            dangerous=report.dangerous_capability_count,
            write=report.workspace_mutation_count,
            shell=report.shell_usage_count,
            network=report.network_usage_count,
            mcp=report.mcp_usage_count,
            plugin=report.plugin_loading_count,
            external=report.external_harness_execution_count,
            memory=report.memory_mutation_count,
            persona=report.persona_mutation_count,
            overlay=report.overlay_mutation_count,
            promotion=report.canonical_mutation_enabled_count,
            materialized=materialized_count,
        )
        return SelfAwarenessSafetyBoundaryStatus(
            write_enabled_count=report.workspace_mutation_count,
            shell_enabled_count=report.shell_usage_count,
            network_enabled_count=report.network_usage_count,
            mcp_enabled_count=report.mcp_usage_count,
            plugin_enabled_count=report.plugin_loading_count,
            external_harness_enabled_count=report.external_harness_execution_count,
            memory_mutation_enabled_count=report.memory_mutation_count,
            persona_mutation_enabled_count=report.persona_mutation_count,
            overlay_mutation_enabled_count=report.overlay_mutation_count,
            canonical_promotion_enabled_count=report.canonical_mutation_enabled_count,
            materialization_enabled_count=materialized_count,
            read_only_invocation_enabled_count=sum(
                1 for item in self.registry_service.list_contracts() if item.gate_contract.allow_skill_execution
            ),
            dangerous_execution_enabled_count=sum(
                1
                for item in self.registry_service.list_contracts()
                if item.execution_enabled and item.risk_profile.dangerous_capability
            ),
            dangerous_capability_count=report.dangerous_capability_count,
            status=status,
        )


class SelfAwarenessCandidateQueueService:
    def __init__(self, *, ocel_store: OCELStore | Any | None = None) -> None:
        self.ocel_store = ocel_store

    def build_candidate_queue_view(self, max_recent_items: int = 20) -> SelfAwarenessCandidateQueueView:
        refs = self._candidate_refs()
        counts = _count_by_ref_type(refs)
        promoted_count = sum(1 for item in refs if item.get("promoted") is True)
        materialized_count = sum(1 for item in refs if item.get("materialized") is True)
        return SelfAwarenessCandidateQueueView(
            plan_candidate_count=counts.get("plan_candidate", 0),
            todo_candidate_count=counts.get("todo_candidate", 0),
            no_action_candidate_count=counts.get("no_action_candidate", 0),
            needs_more_input_candidate_count=counts.get("needs_more_input_candidate", 0),
            summary_candidate_count=counts.get("summary_candidate", 0),
            project_structure_candidate_count=counts.get("project_structure_candidate", 0),
            verification_report_count=counts.get("surface_verification_report", 0),
            pending_review_count=sum(1 for item in refs if item.get("review_status") == "candidate_only"),
            promoted_count=promoted_count,
            materialized_count=materialized_count,
            recent_candidate_refs=refs[:max_recent_items],
        )

    def _candidate_refs(self) -> list[dict[str, Any]]:
        if self.ocel_store is None:
            return []
        refs: list[dict[str, Any]] = []
        for object_type in [
            "plan_candidate",
            "todo_candidate",
            "no_action_candidate",
            "needs_more_input_candidate",
            "summary_candidate",
            "project_structure_candidate",
            "surface_verification_report",
        ]:
            try:
                rows = self.ocel_store.fetch_objects_by_type(object_type)
            except Exception:
                rows = []
            for row in rows:
                attrs = _attrs(row)
                refs.append(
                    {
                        "ref_type": object_type,
                        "ref_id": _safe_id(str(row.get("object_id") or attrs.get("candidate_id") or object_type)),
                        "review_status": str(attrs.get("review_status") or "candidate_only"),
                        "promoted": bool(attrs.get("promoted", False)),
                        "materialized": bool(attrs.get("materialized", False)),
                    }
                )
        return refs


class SelfAwarenessVerificationQueueService:
    def __init__(self, *, ocel_store: OCELStore | Any | None = None) -> None:
        self.ocel_store = ocel_store

    def build_verification_queue_view(self, max_recent_items: int = 20) -> SelfAwarenessVerificationQueueView:
        refs = self._report_refs(max_recent_items=max_recent_items)
        passed = sum(1 for item in refs if item.get("status") == "passed")
        warning = sum(1 for item in refs if item.get("status") == "warning")
        failed = sum(1 for item in refs if item.get("status") == "failed")
        blocked = sum(1 for item in refs if item.get("status") == "blocked")
        findings = [
            {
                "ref_type": "verification_finding",
                "ref_id": item.get("ref_id"),
                "severity": item.get("status"),
                "summary": "verification report requires operator review",
            }
            for item in refs
            if item.get("status") in {"warning", "failed", "blocked"}
        ][:max_recent_items]
        return SelfAwarenessVerificationQueueView(
            total_reports=len(refs),
            passed_count=passed,
            warning_count=warning,
            failed_count=failed,
            blocked_count=blocked,
            recent_report_refs=refs,
            open_findings=findings,
        )

    def _report_refs(self, *, max_recent_items: int) -> list[dict[str, Any]]:
        if self.ocel_store is None:
            return []
        try:
            rows = self.ocel_store.fetch_objects_by_type("surface_verification_report")
        except Exception:
            rows = []
        refs: list[dict[str, Any]] = []
        for row in rows[:max_recent_items]:
            attrs = _attrs(row)
            status = str(attrs.get("status") or attrs.get("report_status") or "passed")
            refs.append(
                {
                    "ref_type": "surface_verification_report",
                    "ref_id": _safe_id(str(row.get("object_id") or attrs.get("report_id") or "surface_verification_report")),
                    "status": _safe_status(status),
                }
            )
        return refs


class SelfAwarenessEnvelopeAuditService:
    def __init__(self, *, ocel_store: OCELStore | Any | None = None) -> None:
        self.ocel_store = ocel_store

    def recent_envelopes(self, max_recent_items: int = 20) -> list[SelfAwarenessEnvelopeView]:
        if self.ocel_store is None:
            return []
        try:
            rows = self.ocel_store.fetch_objects_by_type("execution_envelope")
        except Exception:
            rows = []
        views: list[SelfAwarenessEnvelopeView] = []
        for row in rows[:max_recent_items]:
            attrs = _attrs(row)
            envelope_id = _safe_id(str(row.get("object_id") or attrs.get("envelope_id") or "execution_envelope"))
            skill_id = attrs.get("skill_id")
            event_type = str(attrs.get("event_type") or attrs.get("execution_kind") or "execution_envelope")
            blocked = bool(attrs.get("blocked", False) or attrs.get("status") == "blocked")
            views.append(
                SelfAwarenessEnvelopeView(
                    envelope_id=envelope_id,
                    skill_id=str(skill_id) if skill_id else None,
                    event_type=_safe_token(event_type),
                    effect_types=_safe_effects(attrs.get("effect_types")),
                    blocked=blocked,
                    created_at=str(attrs.get("created_at") or attrs.get("started_at") or ""),
                    summary=_sanitize_summary(str(attrs.get("summary") or attrs.get("status") or "envelope observed")),
                    object_refs=_safe_object_refs(attrs.get("object_refs")),
                )
            )
        return views


class SelfAwarenessWorkbenchService:
    def __init__(
        self,
        *,
        registry_service: SelfAwarenessRegistryService | None = None,
        report_service: SelfAwarenessReportService | None = None,
        ocel_store: OCELStore | Any | None = None,
    ) -> None:
        self.registry_service = registry_service or SelfAwarenessRegistryService()
        self.report_service = report_service or SelfAwarenessReportService(registry_service=self.registry_service)
        self.ocel_store = ocel_store
        self.coverage_service = SelfAwarenessCoverageService(self.registry_service)
        self.candidate_queue_service = SelfAwarenessCandidateQueueService(ocel_store=ocel_store)
        self.verification_queue_service = SelfAwarenessVerificationQueueService(ocel_store=ocel_store)
        self.envelope_audit_service = SelfAwarenessEnvelopeAuditService(ocel_store=ocel_store)
        self.safety_boundary_service = SelfAwarenessSafetyBoundaryService(self.registry_service)

    def build_snapshot(self, request: SelfAwarenessWorkbenchRequest | None = None) -> SelfAwarenessWorkbenchSnapshot:
        request = (request or SelfAwarenessWorkbenchRequest()).normalized()
        coverage = self.coverage_service.build_coverage() if request.include_coverage else []
        candidate_queue = (
            self.candidate_queue_service.build_candidate_queue_view(request.max_recent_items)
            if request.include_candidates
            else SelfAwarenessCandidateQueueView()
        )
        verification_queue = (
            self.verification_queue_service.build_verification_queue_view(request.max_recent_items)
            if request.include_verification
            else SelfAwarenessVerificationQueueView()
        )
        safety = (
            self.safety_boundary_service.inspect_safety_boundary(candidate_queue=candidate_queue)
            if request.include_safety
            else SelfAwarenessSafetyBoundaryStatus()
        )
        envelopes = (
            self.envelope_audit_service.recent_envelopes(request.max_recent_items)
            if request.include_recent_envelopes
            else []
        )
        pig_status = _pig_status(self.report_service.build_pig_report()) if request.include_pig else {}
        ocpx_status = _ocpx_status(self.report_service.build_ocpx_projection()) if request.include_ocpx else {}
        findings = self._build_findings(
            coverage=coverage,
            safety=safety,
            candidate_queue=candidate_queue,
            verification_queue=verification_queue,
            pig_status=pig_status,
            ocpx_status=ocpx_status,
        )
        return SelfAwarenessWorkbenchSnapshot(
            snapshot_id=f"self_awareness_workbench_snapshot:{uuid4()}",
            created_at=utc_now_iso(),
            root_id=request.root_id,
            coverage=coverage,
            safety_boundary=safety,
            candidate_queue=candidate_queue,
            verification_queue=verification_queue,
            recent_envelopes=envelopes,
            pig_status=pig_status,
            ocpx_status=ocpx_status,
            findings=findings,
            limitations=[
                "read_only_operator_surface",
                "summary_count_ref_views_only",
                "no_approval_promotion_materialization_or_execution",
                "no_raw_file_content_or_private_full_paths",
            ],
        )

    def render_cli(self, snapshot: SelfAwarenessWorkbenchSnapshot, *, section: str = "overview") -> str:
        coverage = snapshot.coverage
        safety = snapshot.safety_boundary
        candidates = snapshot.candidate_queue
        verification = snapshot.verification_queue
        lines = [
            "Self-Awareness Workbench",
            f"section={section}",
            f"status={snapshot.status}",
            f"read_only={str(snapshot.read_only).lower()}",
            f"mutation_performed={str(snapshot.mutation_performed).lower()}",
            f"coverage_row_count={len(coverage)}",
            f"implemented_coverage_count={sum(1 for item in coverage if item.status == 'implemented')}",
            f"contract_only_coverage_count={sum(1 for item in coverage if item.status == 'contract_only')}",
            f"dangerous_capability_count={safety.dangerous_capability_count}",
            f"write_enabled_count={safety.write_enabled_count}",
            f"shell_enabled_count={safety.shell_enabled_count}",
            f"network_enabled_count={safety.network_enabled_count}",
            f"mcp_enabled_count={safety.mcp_enabled_count}",
            f"plugin_enabled_count={safety.plugin_enabled_count}",
            f"external_harness_enabled_count={safety.external_harness_enabled_count}",
            f"memory_mutation_enabled_count={safety.memory_mutation_enabled_count}",
            f"persona_mutation_enabled_count={safety.persona_mutation_enabled_count}",
            f"overlay_mutation_enabled_count={safety.overlay_mutation_enabled_count}",
            f"plan_candidate_count={candidates.plan_candidate_count}",
            f"todo_candidate_count={candidates.todo_candidate_count}",
            f"no_action_candidate_count={candidates.no_action_candidate_count}",
            f"needs_more_input_candidate_count={candidates.needs_more_input_candidate_count}",
            f"summary_candidate_count={candidates.summary_candidate_count}",
            f"project_structure_candidate_count={candidates.project_structure_candidate_count}",
            f"verification_report_count={candidates.verification_report_count}",
            f"promoted_count={candidates.promoted_count}",
            f"materialized_count={candidates.materialized_count}",
            f"verification_total_reports={verification.total_reports}",
            f"verification_passed_count={verification.passed_count}",
            f"verification_warning_count={verification.warning_count}",
            f"verification_failed_count={verification.failed_count}",
            f"verification_blocked_count={verification.blocked_count}",
            f"recent_envelope_count={len(snapshot.recent_envelopes)}",
            f"pig_state={snapshot.pig_status.get('state', '')}",
            f"ocpx_state={snapshot.ocpx_status.get('state', '')}",
            f"finding_count={len(snapshot.findings)}",
            "approval_enabled=false",
            "promotion_enabled=false",
            "execution_enabled=false",
            "raw_file_content_printed=false",
            "private_full_paths_printed=false",
        ]
        if section == "coverage":
            for item in coverage[:20]:
                lines.append(
                    f"- coverage version={item.version} skill_id={item.skill_id} "
                    f"status={item.status} execution_enabled={str(item.execution_enabled).lower()}"
                )
        elif section == "candidates":
            for item in candidates.recent_candidate_refs[:20]:
                lines.append(f"- candidate ref_type={item.get('ref_type')} ref_id={item.get('ref_id')}")
        elif section == "verification":
            for item in verification.recent_report_refs[:20]:
                lines.append(f"- verification ref_id={item.get('ref_id')} status={item.get('status')}")
        elif section in {"audit", "timeline"}:
            for item in snapshot.recent_envelopes[:20]:
                lines.append(
                    f"- envelope envelope_id={item.envelope_id} skill_id={item.skill_id or ''} "
                    f"blocked={str(item.blocked).lower()} summary={item.summary}"
                )
        elif section == "risks":
            for item in snapshot.findings[:20]:
                lines.append(f"- finding severity={item.severity} type={item.finding_type} message={item.message}")
        return "\n".join(lines)

    def _build_findings(
        self,
        *,
        coverage: list[SelfAwarenessCoverageRow],
        safety: SelfAwarenessSafetyBoundaryStatus,
        candidate_queue: SelfAwarenessCandidateQueueView,
        verification_queue: SelfAwarenessVerificationQueueView,
        pig_status: dict[str, Any],
        ocpx_status: dict[str, Any],
    ) -> list[SelfAwarenessWorkbenchFinding]:
        findings: list[SelfAwarenessWorkbenchFinding] = []
        for row in coverage:
            if row.status in {"not_started", "blocked"}:
                findings.append(
                    _finding(
                        "warning",
                        "coverage_gap",
                        f"{row.capability} is not implemented.",
                        {"ref_type": "coverage_row", "ref_id": row.skill_id or row.capability},
                        "Keep it non-executable unless a later version explicitly scopes it.",
                    )
                )
        if verification_queue.failed_count or verification_queue.blocked_count:
            findings.append(_finding("error", "verification_failed", "Verification queue contains failed or blocked reports."))
        if candidate_queue.promoted_count:
            findings.append(_finding("critical", "unexpected_promotion", "Candidate queue contains promoted candidates."))
        if candidate_queue.materialized_count:
            findings.append(_finding("critical", "unexpected_materialization", "Candidate queue contains materialized candidates."))
        if safety.status == "violation":
            findings.append(_finding("critical", "dangerous_capability_enabled", "A dangerous or mutating capability is visible."))
        if not pig_status:
            findings.append(_finding("warning", "missing_pig_projection", "PIG status is unavailable."))
        if not ocpx_status:
            findings.append(_finding("warning", "missing_ocpx_projection", "OCPX status is unavailable."))
        if not findings:
            findings.append(_finding("info", "ok", "Workbench read model has no warnings or violations."))
        return findings


def determine_workbench_status(
    findings: list[SelfAwarenessWorkbenchFinding],
    safety: SelfAwarenessSafetyBoundaryStatus,
    candidate_queue: SelfAwarenessCandidateQueueView | None = None,
) -> WorkbenchStatus:
    candidate_queue = candidate_queue or SelfAwarenessCandidateQueueView()
    if safety.status == "violation" or candidate_queue.promoted_count > 0 or candidate_queue.materialized_count > 0:
        return "violation"
    if any(item.severity in {"critical", "error"} for item in findings):
        return "violation"
    if any(item.severity == "warning" for item in findings):
        return "warning"
    return "ok"


def _boundary_status(**counts: int) -> WorkbenchStatus:
    return "violation" if any(value > 0 for value in counts.values()) else "ok"


def _coverage_status(value: str) -> CoverageStatus:
    if value in {"implemented", "contract_only", "stub", "blocked"}:
        return value  # type: ignore[return-value]
    if value in {"not_implemented", "candidate_helper_only"}:
        return "contract_only"
    return "not_started"


def _safety_notes(contract: Any) -> list[str]:
    notes = ["read_only" if contract.risk_profile.read_only else "not_read_only"]
    if contract.implementation_status != "implemented":
        notes.append("non_executable_contract_surface")
    if not contract.execution_enabled:
        notes.append("execution_disabled")
    if not contract.canonical_mutation_enabled:
        notes.append("canonical_promotion_disabled")
    return notes


def _finding(
    severity: FindingSeverity,
    finding_type: str,
    message: str,
    source_ref: dict[str, Any] | None = None,
    recommended_followup: str | None = None,
) -> SelfAwarenessWorkbenchFinding:
    return SelfAwarenessWorkbenchFinding(
        finding_id=f"self_awareness_workbench_finding:{uuid4()}",
        severity=severity,
        finding_type=finding_type,
        message=message,
        source_ref=source_ref,
        recommended_followup=recommended_followup,
    )


def _pig_status(report: dict[str, Any]) -> dict[str, Any]:
    return {
        "state": report.get("state"),
        "version": report.get("version"),
        "workbench": report.get("workbench"),
        "read_only": report.get("read_only"),
        "mutation_performed": report.get("mutation_performed"),
        "dangerous_capability_count": (report.get("safety_boundary_counts") or {}).get("dangerous_capability_count"),
    }


def _ocpx_status(projection: dict[str, Any]) -> dict[str, Any]:
    return {
        "state": projection.get("state"),
        "version": projection.get("version"),
        "canonical_store": projection.get("canonical_store"),
        "read_model_types": list(projection.get("read_model_types") or []),
        "effect_types": list(projection.get("effect_types") or []),
    }


def _count_by_ref_type(refs: list[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in refs:
        key = str(item.get("ref_type") or "unknown")
        counts[key] = counts.get(key, 0) + 1
    return counts


def _attrs(row: dict[str, Any]) -> dict[str, Any]:
    attrs = row.get("object_attrs")
    if isinstance(attrs, dict):
        return attrs
    return {}


def _safe_id(value: str) -> str:
    return value.replace("\\", "/").split("/")[-1][:120]


def _safe_token(value: str) -> str:
    return "".join(ch for ch in value if ch.isalnum() or ch in {"_", "-", ":"})[:120] or "unknown"


def _safe_status(value: str) -> str:
    lowered = value.casefold()
    if lowered in {"passed", "warning", "failed", "blocked"}:
        return lowered
    return "passed"


def _safe_effects(value: Any) -> list[str]:
    if isinstance(value, list):
        return [_safe_token(str(item)) for item in value[:8]]
    if isinstance(value, str) and value:
        return [_safe_token(value)]
    return ["read_only_observation"]


def _safe_object_refs(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    refs: list[dict[str, Any]] = []
    for item in value[:10]:
        if isinstance(item, dict):
            refs.append(
                {
                    "ref_type": _safe_token(str(item.get("ref_type") or item.get("object_type") or "object")),
                    "ref_id": _safe_id(str(item.get("ref_id") or item.get("object_id") or "")),
                }
            )
    return refs


def _sanitize_summary(value: str) -> str:
    text = value.replace("\r", " ").replace("\n", " ")
    text = text.replace("\\", "/")
    tokens = []
    for token in text.split():
        if "/" in token and (":" in token or token.startswith("/")):
            tokens.append("<path-redacted>")
        elif any(secret in token.casefold() for secret in ["secret", "token=", "api_key", "password"]):
            tokens.append("<redacted>")
        else:
            tokens.append(token)
    return " ".join(tokens)[:200]
