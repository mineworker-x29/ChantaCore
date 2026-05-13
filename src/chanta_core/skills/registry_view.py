from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from chanta_core.observation_digest import DIGESTION_SKILL_IDS, OBSERVATION_SKILL_IDS
from chanta_core.observation_digest.models import (
    ExternalSkillAdapterCandidate,
    ExternalSkillAssimilationCandidate,
)
from chanta_core.ocel.models import OCELEvent, OCELObject, OCELRecord, OCELRelation
from chanta_core.ocel.store import OCELStore
from chanta_core.skills.ids import (
    new_skill_registry_entry_id,
    new_skill_registry_filter_id,
    new_skill_registry_finding_id,
    new_skill_registry_result_id,
    new_skill_registry_view_id,
)
from chanta_core.skills.onboarding import InternalSkillOnboardingService
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso


SKILL_LAYERS = {
    "core_process_intelligence",
    "internal_observation",
    "internal_digestion",
    "basic_foundation",
    "external_candidate",
    "external_adapted",
    "blocked",
    "unknown",
}
SKILL_ORIGINS = {
    "chantacore_builtin",
    "chantacore_internal",
    "external_static_digest",
    "external_behavior_observation",
    "external_adapter_candidate",
    "manual_candidate",
    "test_fixture",
    "unknown",
}
SKILL_REGISTRY_STATUSES = {
    "draft",
    "candidate",
    "pending_review",
    "accepted",
    "enabled",
    "disabled",
    "blocked",
    "deprecated",
    "needs_fix",
    "unknown",
}


@dataclass(frozen=True)
class SkillRegistryView:
    registry_view_id: str
    view_name: str
    total_skill_count: int
    enabled_skill_count: int
    disabled_skill_count: int
    candidate_skill_count: int
    blocked_skill_count: int
    observation_skill_count: int
    digestion_skill_count: int
    external_candidate_count: int
    created_at: str
    view_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "registry_view_id": self.registry_view_id,
            "view_name": self.view_name,
            "total_skill_count": self.total_skill_count,
            "enabled_skill_count": self.enabled_skill_count,
            "disabled_skill_count": self.disabled_skill_count,
            "candidate_skill_count": self.candidate_skill_count,
            "blocked_skill_count": self.blocked_skill_count,
            "observation_skill_count": self.observation_skill_count,
            "digestion_skill_count": self.digestion_skill_count,
            "external_candidate_count": self.external_candidate_count,
            "created_at": self.created_at,
            "view_attrs": dict(self.view_attrs),
        }


@dataclass(frozen=True)
class SkillRegistryEntry:
    registry_entry_id: str
    registry_view_id: str
    skill_id: str
    skill_name: str
    description: str
    skill_layer: str
    skill_origin: str
    capability_category: str
    risk_class: str
    status: str
    enabled: bool
    execution_enabled: bool
    proposal_enabled: bool
    review_required: bool
    gate_required: bool
    envelope_required: bool
    audit_visible: bool
    workbench_visible: bool
    ocel_observable: bool
    pig_visible: bool
    source_ref: str | None
    created_at: str
    entry_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "registry_entry_id": self.registry_entry_id,
            "registry_view_id": self.registry_view_id,
            "skill_id": self.skill_id,
            "skill_name": self.skill_name,
            "description": self.description,
            "skill_layer": self.skill_layer,
            "skill_origin": self.skill_origin,
            "capability_category": self.capability_category,
            "risk_class": self.risk_class,
            "status": self.status,
            "enabled": self.enabled,
            "execution_enabled": self.execution_enabled,
            "proposal_enabled": self.proposal_enabled,
            "review_required": self.review_required,
            "gate_required": self.gate_required,
            "envelope_required": self.envelope_required,
            "audit_visible": self.audit_visible,
            "workbench_visible": self.workbench_visible,
            "ocel_observable": self.ocel_observable,
            "pig_visible": self.pig_visible,
            "source_ref": self.source_ref,
            "created_at": self.created_at,
            "entry_attrs": dict(self.entry_attrs),
        }


@dataclass(frozen=True)
class SkillRegistryFilter:
    registry_filter_id: str
    registry_view_id: str
    skill_layer: str | None
    skill_origin: str | None
    capability_category: str | None
    risk_class: str | None
    status: str | None
    enabled: bool | None
    execution_enabled: bool | None
    ocel_observable: bool | None
    limit: int | None
    created_at: str
    filter_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "registry_filter_id": self.registry_filter_id,
            "registry_view_id": self.registry_view_id,
            "skill_layer": self.skill_layer,
            "skill_origin": self.skill_origin,
            "capability_category": self.capability_category,
            "risk_class": self.risk_class,
            "status": self.status,
            "enabled": self.enabled,
            "execution_enabled": self.execution_enabled,
            "ocel_observable": self.ocel_observable,
            "limit": self.limit,
            "created_at": self.created_at,
            "filter_attrs": dict(self.filter_attrs),
        }


@dataclass(frozen=True)
class SkillRegistryFinding:
    finding_id: str
    registry_view_id: str
    skill_id: str | None
    finding_type: str
    status: str
    severity: str
    message: str
    subject_ref: str | None
    created_at: str
    finding_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "registry_view_id": self.registry_view_id,
            "skill_id": self.skill_id,
            "finding_type": self.finding_type,
            "status": self.status,
            "severity": self.severity,
            "message": self.message,
            "subject_ref": self.subject_ref,
            "created_at": self.created_at,
            "finding_attrs": dict(self.finding_attrs),
        }


@dataclass(frozen=True)
class SkillRegistryResult:
    registry_result_id: str
    registry_view_id: str
    command_name: str
    status: str
    entry_ids: list[str]
    finding_ids: list[str]
    summary: str
    created_at: str
    result_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "registry_result_id": self.registry_result_id,
            "registry_view_id": self.registry_view_id,
            "command_name": self.command_name,
            "status": self.status,
            "entry_ids": list(self.entry_ids),
            "finding_ids": list(self.finding_ids),
            "summary": self.summary,
            "created_at": self.created_at,
            "result_attrs": dict(self.result_attrs),
        }


class SkillRegistryViewService:
    def __init__(
        self,
        *,
        onboarding_service: InternalSkillOnboardingService | None = None,
        trace_service: TraceService | None = None,
        ocel_store: OCELStore | None = None,
    ) -> None:
        self.onboarding_service = onboarding_service or InternalSkillOnboardingService()
        if trace_service is not None:
            self.trace_service = trace_service
        elif ocel_store is not None:
            self.trace_service = TraceService(ocel_store=ocel_store)
        else:
            self.trace_service = TraceService()
        self.last_view: SkillRegistryView | None = None
        self.last_entries: list[SkillRegistryEntry] = []
        self.last_filter: SkillRegistryFilter | None = None
        self.last_findings: list[SkillRegistryFinding] = []
        self.last_result: SkillRegistryResult | None = None

    def build_registry_view(
        self,
        *,
        view_name: str = "observation_digest_skill_registry",
        external_candidates: list[ExternalSkillAssimilationCandidate] | None = None,
        adapter_candidates: list[ExternalSkillAdapterCandidate] | None = None,
    ) -> SkillRegistryView:
        view_id = new_skill_registry_view_id()
        self.last_findings = []
        entries = [
            *self.collect_internal_skill_entries(registry_view_id=view_id),
            *self.collect_external_candidate_entries(
                registry_view_id=view_id,
                external_candidates=external_candidates or [],
                adapter_candidates=adapter_candidates or [],
            ),
        ]
        view = SkillRegistryView(
            registry_view_id=view_id,
            view_name=view_name,
            total_skill_count=len(entries),
            enabled_skill_count=sum(1 for item in entries if item.enabled),
            disabled_skill_count=sum(1 for item in entries if not item.enabled),
            candidate_skill_count=sum(1 for item in entries if item.status in {"candidate", "pending_review"}),
            blocked_skill_count=sum(1 for item in entries if item.status == "blocked" or item.skill_layer == "blocked"),
            observation_skill_count=sum(1 for item in entries if item.skill_layer == "internal_observation"),
            digestion_skill_count=sum(1 for item in entries if item.skill_layer == "internal_digestion"),
            external_candidate_count=sum(1 for item in entries if item.skill_layer in {"external_candidate", "external_adapted"}),
            created_at=utc_now_iso(),
            view_attrs={
                "read_only": True,
                "skills_executed": False,
                "skills_enabled": False,
                "dynamic_registration_used": False,
                "permission_grants_created": False,
            },
        )
        self.last_view = view
        self.last_entries = entries
        self._record_model("skill_registry_view_created", "skill_registry_view", view.registry_view_id, view)
        for entry in entries:
            self.record_entry(entry)
        for entry in entries:
            self._check_entry_contract(entry)
        return view

    def collect_internal_skill_entries(self, *, registry_view_id: str) -> list[SkillRegistryEntry]:
        return [
            *self.collect_observation_skill_entries(registry_view_id=registry_view_id),
            *self.collect_digestion_skill_entries(registry_view_id=registry_view_id),
        ]

    def collect_observation_skill_entries(self, *, registry_view_id: str) -> list[SkillRegistryEntry]:
        return [
            self._entry_from_skill_id(
                registry_view_id=registry_view_id,
                skill_id=skill_id,
                skill_layer="internal_observation",
                skill_origin="chantacore_internal",
            )
            for skill_id in OBSERVATION_SKILL_IDS
        ]

    def collect_digestion_skill_entries(self, *, registry_view_id: str) -> list[SkillRegistryEntry]:
        return [
            self._entry_from_skill_id(
                registry_view_id=registry_view_id,
                skill_id=skill_id,
                skill_layer="internal_digestion",
                skill_origin="chantacore_internal",
            )
            for skill_id in DIGESTION_SKILL_IDS
        ]

    def collect_external_candidate_entries(
        self,
        *,
        registry_view_id: str,
        external_candidates: list[ExternalSkillAssimilationCandidate],
        adapter_candidates: list[ExternalSkillAdapterCandidate],
    ) -> list[SkillRegistryEntry]:
        entries = [
            SkillRegistryEntry(
                registry_entry_id=new_skill_registry_entry_id(),
                registry_view_id=registry_view_id,
                skill_id=item.proposed_chantacore_skill_id,
                skill_name=_name_from_skill_id(item.proposed_chantacore_skill_id),
                description="Review-only external capability candidate.",
                skill_layer="external_candidate",
                skill_origin=_candidate_origin(item),
                capability_category="digestion",
                risk_class=item.risk_class,
                status=item.review_status or "pending_review",
                enabled=False,
                execution_enabled=False,
                proposal_enabled=False,
                review_required=True,
                gate_required=True,
                envelope_required=True,
                audit_visible=True,
                workbench_visible=True,
                ocel_observable=True,
                pig_visible=True,
                source_ref=item.source_skill_ref,
                created_at=utc_now_iso(),
                entry_attrs={
                    "candidate_id": item.candidate_id,
                    "canonical_import_enabled": False,
                    "runtime_registered": False,
                    "read_only": True,
                },
            )
            for item in external_candidates
        ]
        entries.extend(
            SkillRegistryEntry(
                registry_entry_id=new_skill_registry_entry_id(),
                registry_view_id=registry_view_id,
                skill_id=item.target_skill_id,
                skill_name=_name_from_skill_id(item.target_skill_id),
                description="Review-only adapter candidate.",
                skill_layer="external_adapted",
                skill_origin="external_adapter_candidate",
                capability_category="digestion",
                risk_class="unknown",
                status="pending_review",
                enabled=False,
                execution_enabled=False,
                proposal_enabled=False,
                review_required=True,
                gate_required=True,
                envelope_required=True,
                audit_visible=True,
                workbench_visible=True,
                ocel_observable=True,
                pig_visible=True,
                source_ref=item.source_skill_ref,
                created_at=utc_now_iso(),
                entry_attrs={
                    "adapter_candidate_id": item.adapter_candidate_id,
                    "requires_review": item.requires_review,
                    "runtime_registered": False,
                    "read_only": True,
                },
            )
            for item in adapter_candidates
        )
        return entries

    def apply_filter(
        self,
        entries: list[SkillRegistryEntry] | None = None,
        *,
        skill_layer: str | None = None,
        skill_origin: str | None = None,
        capability_category: str | None = None,
        risk_class: str | None = None,
        status: str | None = None,
        enabled: bool | None = None,
        execution_enabled: bool | None = None,
        ocel_observable: bool | None = None,
        limit: int | None = None,
    ) -> list[SkillRegistryEntry]:
        source_entries = list(entries if entries is not None else self.last_entries)
        registry_view_id = self.last_view.registry_view_id if self.last_view else ""
        registry_filter = SkillRegistryFilter(
            registry_filter_id=new_skill_registry_filter_id(),
            registry_view_id=registry_view_id,
            skill_layer=skill_layer,
            skill_origin=skill_origin,
            capability_category=capability_category,
            risk_class=risk_class,
            status=status,
            enabled=enabled,
            execution_enabled=execution_enabled,
            ocel_observable=ocel_observable,
            limit=limit,
            created_at=utc_now_iso(),
            filter_attrs={"read_only": True},
        )
        filtered = [
            item
            for item in source_entries
            if _matches(item.skill_layer, skill_layer)
            and _matches(item.skill_origin, skill_origin)
            and _matches(item.capability_category, capability_category)
            and _matches(item.risk_class, risk_class)
            and _matches(item.status, status)
            and _matches_bool(item.enabled, enabled)
            and _matches_bool(item.execution_enabled, execution_enabled)
            and _matches_bool(item.ocel_observable, ocel_observable)
        ]
        if limit is not None:
            filtered = filtered[: max(0, limit)]
        self.last_filter = registry_filter
        self._record_model(
            "skill_registry_filter_applied",
            "skill_registry_filter",
            registry_filter.registry_filter_id,
            registry_filter,
            links=[("skill_registry_view_object", registry_view_id)],
            object_links=[(registry_filter.registry_filter_id, registry_view_id, "registry_filter_applies_to_registry_view")],
        )
        return filtered

    def record_entry(self, entry: SkillRegistryEntry) -> SkillRegistryEntry:
        self._record_model(
            "skill_registry_entry_recorded",
            "skill_registry_entry",
            entry.registry_entry_id,
            entry,
            links=[("skill_registry_view_object", entry.registry_view_id)],
            object_links=[(entry.registry_entry_id, entry.registry_view_id, "registry_entry_belongs_to_registry_view")],
        )
        return entry

    def record_finding(
        self,
        *,
        registry_view_id: str,
        skill_id: str | None,
        finding_type: str,
        status: str,
        severity: str,
        message: str,
        subject_ref: str | None = None,
        finding_attrs: dict[str, Any] | None = None,
    ) -> SkillRegistryFinding:
        finding = SkillRegistryFinding(
            finding_id=new_skill_registry_finding_id(),
            registry_view_id=registry_view_id,
            skill_id=skill_id,
            finding_type=finding_type,
            status=status,
            severity=severity,
            message=message,
            subject_ref=subject_ref,
            created_at=utc_now_iso(),
            finding_attrs={"read_only": True, **dict(finding_attrs or {})},
        )
        self.last_findings.append(finding)
        self._record_model(
            "skill_registry_finding_recorded",
            "skill_registry_finding",
            finding.finding_id,
            finding,
            links=[("skill_registry_view_object", registry_view_id)],
            object_links=[(finding.finding_id, registry_view_id, "registry_finding_belongs_to_registry_view")],
        )
        return finding

    def record_result(
        self,
        *,
        command_name: str,
        entries: list[SkillRegistryEntry],
        status: str = "completed",
        summary: str | None = None,
    ) -> SkillRegistryResult:
        registry_view_id = self.last_view.registry_view_id if self.last_view else ""
        result = SkillRegistryResult(
            registry_result_id=new_skill_registry_result_id(),
            registry_view_id=registry_view_id,
            command_name=command_name,
            status=status,
            entry_ids=[item.registry_entry_id for item in entries],
            finding_ids=[item.finding_id for item in self.last_findings],
            summary=summary or f"Registry view returned {len(entries)} entries.",
            created_at=utc_now_iso(),
            result_attrs={
                "read_only": True,
                "skills_executed": False,
                "skills_enabled": False,
                "permission_grants_created": False,
            },
        )
        self.last_result = result
        self._record_model(
            "skill_registry_result_recorded",
            "skill_registry_result",
            result.registry_result_id,
            result,
            links=[("skill_registry_view_object", registry_view_id)]
            + [("skill_registry_entry_object", item.registry_entry_id) for item in entries],
            object_links=[(result.registry_result_id, registry_view_id, "registry_result_summarizes_registry_view")]
            + [
                (result.registry_result_id, item.registry_entry_id, "registry_result_includes_registry_entry")
                for item in entries
            ],
        )
        return result

    def render_registry_table(self, entries: list[SkillRegistryEntry] | None = None) -> str:
        items = list(entries if entries is not None else self.last_entries)
        lines = ["Skill Registry View"]
        lines.append("skill_id | layer | origin | risk | status | enabled | execution")
        for item in items:
            lines.append(
                " | ".join(
                    [
                        item.skill_id,
                        item.skill_layer,
                        item.skill_origin,
                        item.risk_class,
                        item.status,
                        str(item.enabled).lower(),
                        str(item.execution_enabled).lower(),
                    ]
                )
            )
        lines.append("read_only=true")
        lines.append("skills_executed=false")
        lines.append("skills_enabled=false")
        self._record_rendered("table", len(items))
        return "\n".join(lines)

    def render_registry_detail(self, skill_id: str) -> str:
        matches = [item for item in self.last_entries if item.skill_id == skill_id]
        if not matches:
            return f"Skill Registry Detail\nstatus=not_found\nskill_id={skill_id}\nread_only=true"
        item = matches[0]
        data = item.to_dict()
        lines = ["Skill Registry Detail"]
        for key in [
            "skill_id",
            "skill_name",
            "skill_layer",
            "skill_origin",
            "capability_category",
            "risk_class",
            "status",
            "enabled",
            "execution_enabled",
            "gate_required",
            "envelope_required",
            "ocel_observable",
            "pig_visible",
        ]:
            lines.append(f"{key}={data[key]}")
        lines.append("read_only=true")
        self._record_rendered("detail", 1)
        return "\n".join(lines)

    def render_registry_risk_view(self, entries: list[SkillRegistryEntry] | None = None) -> str:
        grouped = _group_counts(entries if entries is not None else self.last_entries, "risk_class")
        lines = ["Skill Registry Risk"]
        lines.extend(f"{key}={value}" for key, value in sorted(grouped.items()))
        lines.append("read_only=true")
        self._record_rendered("risk", sum(grouped.values()))
        return "\n".join(lines)

    def render_registry_observability_view(self, entries: list[SkillRegistryEntry] | None = None) -> str:
        items = list(entries if entries is not None else self.last_entries)
        lines = ["Skill Registry Observability"]
        for item in items:
            lines.append(
                f"{item.skill_id} ocel_observable={str(item.ocel_observable).lower()} "
                f"pig_visible={str(item.pig_visible).lower()}"
            )
        lines.append("read_only=true")
        self._record_rendered("observability", len(items))
        return "\n".join(lines)

    def render_registry_findings(self, findings: list[SkillRegistryFinding] | None = None) -> str:
        items = list(findings if findings is not None else self.last_findings)
        lines = ["Skill Registry Findings"]
        for item in items:
            lines.append(f"{item.finding_type} skill_id={item.skill_id} severity={item.severity} status={item.status}")
        lines.append("read_only=true")
        self._record_rendered("findings", len(items))
        return "\n".join(lines)

    def _entry_from_skill_id(
        self,
        *,
        registry_view_id: str,
        skill_id: str,
        skill_layer: str,
        skill_origin: str,
    ) -> SkillRegistryEntry:
        bundle = self.onboarding_service.create_read_only_skill_contract_bundle(skill_id=skill_id)
        descriptor = bundle["descriptor"]
        risk_profile = bundle["risk_profile"]
        gate_contract = bundle["gate_contract"]
        observability_contract = bundle["observability_contract"]
        return SkillRegistryEntry(
            registry_entry_id=new_skill_registry_entry_id(),
            registry_view_id=registry_view_id,
            skill_id=descriptor.skill_id,
            skill_name=descriptor.skill_name,
            description=descriptor.description,
            skill_layer=skill_layer,
            skill_origin=skill_origin,
            capability_category=descriptor.capability_category,
            risk_class=descriptor.risk_class,
            status="candidate",
            enabled=False,
            execution_enabled=False,
            proposal_enabled=True,
            review_required=risk_profile.requires_review,
            gate_required=gate_contract.gate_required,
            envelope_required=observability_contract.envelope_required,
            audit_visible=observability_contract.audit_visible,
            workbench_visible=observability_contract.workbench_visible,
            ocel_observable=bool(observability_contract.ocel_object_types and observability_contract.ocel_event_activities),
            pig_visible=bool(observability_contract.pig_report_keys),
            source_ref=descriptor.owner_module,
            created_at=utc_now_iso(),
            entry_attrs={
                "descriptor_id": descriptor.descriptor_id,
                "gate_contract_id": gate_contract.gate_contract_id,
                "observability_contract_id": observability_contract.observability_contract_id,
                "read_only": True,
            },
        )

    def _check_entry_contract(self, entry: SkillRegistryEntry) -> None:
        if not entry.gate_required or not entry.envelope_required:
            self.record_finding(
                registry_view_id=entry.registry_view_id,
                skill_id=entry.skill_id,
                finding_type="missing_contract",
                status="needs_fix",
                severity="high",
                message="Registry entry is missing required gate or envelope contract.",
                subject_ref=entry.registry_entry_id,
            )
        if entry.enabled and (not entry.gate_required or not entry.envelope_required):
            self.record_finding(
                registry_view_id=entry.registry_view_id,
                skill_id=entry.skill_id,
                finding_type="unsafe_enabled",
                status="blocked",
                severity="high",
                message="Enabled skill lacks required read-only gate or envelope contract.",
                subject_ref=entry.registry_entry_id,
            )
        if entry.skill_layer in {"external_candidate", "external_adapted"} and entry.execution_enabled:
            self.record_finding(
                registry_view_id=entry.registry_view_id,
                skill_id=entry.skill_id,
                finding_type="unsafe_external_candidate",
                status="blocked",
                severity="high",
                message="External candidates must remain non-executable.",
                subject_ref=entry.registry_entry_id,
            )

    def _record_model(
        self,
        activity: str,
        object_type: str,
        object_id: str,
        model: Any,
        *,
        links: list[tuple[str, str]] | None = None,
        object_links: list[tuple[str, str, str]] | None = None,
    ) -> None:
        _record(
            self.trace_service,
            activity,
            objects=[_object(object_type, object_id, model.to_dict())],
            links=[(f"{object_type}_object", object_id), *(links or [])],
            object_links=object_links or [],
        )

    def _record_rendered(self, render_kind: str, entry_count: int) -> None:
        if self.last_view is None:
            return
        event = OCELEvent(
            event_id=f"evt:{uuid4()}",
            event_activity="skill_registry_rendered",
            event_timestamp=utc_now_iso(),
            event_attrs={
                "render_kind": render_kind,
                "entry_count": entry_count,
                "read_only": True,
                "skills_executed": False,
                "skills_enabled": False,
            },
        )
        relation = OCELRelation.event_object(
            event_id=event.event_id,
            object_id=self.last_view.registry_view_id,
            qualifier="skill_registry_view_object",
        )
        self.trace_service.record_session_ocel_record(OCELRecord(event=event, objects=[], relations=[relation]))


def _record(
    trace_service: TraceService,
    activity: str,
    *,
    objects: list[OCELObject],
    links: list[tuple[str, str]],
    object_links: list[tuple[str, str, str]],
) -> None:
    event = OCELEvent(
        event_id=f"evt:{uuid4()}",
        event_activity=activity,
        event_timestamp=utc_now_iso(),
        event_attrs={
            "source_runtime": "chanta_core",
            "runtime_event_type": activity,
            "read_only": True,
            "skills_executed": False,
            "skills_enabled": False,
            "dynamic_registration_used": False,
            "permission_grants_created": False,
        },
    )
    relations = [
        OCELRelation.event_object(event_id=event.event_id, object_id=object_id, qualifier=qualifier)
        for qualifier, object_id in links
        if object_id
    ]
    relations.extend(
        OCELRelation.object_object(source_object_id=source_id, target_object_id=target_id, qualifier=qualifier)
        for source_id, target_id, qualifier in object_links
        if source_id and target_id
    )
    trace_service.record_session_ocel_record(OCELRecord(event=event, objects=objects, relations=relations))


def _object(object_type: str, object_id: str, attrs: dict[str, Any]) -> OCELObject:
    return OCELObject(
        object_id=object_id,
        object_type=object_type,
        object_attrs={"object_key": object_id, "display_name": object_id, **attrs},
    )


def _matches(value: str, expected: str | None) -> bool:
    return expected is None or value == expected


def _matches_bool(value: bool, expected: bool | None) -> bool:
    return expected is None or value is expected


def _name_from_skill_id(skill_id: str) -> str:
    return skill_id.removeprefix("skill:").replace("_", " ").title()


def _candidate_origin(item: ExternalSkillAssimilationCandidate) -> str:
    if item.behavior_fingerprint_id:
        return "external_behavior_observation"
    if item.static_profile_id:
        return "external_static_digest"
    return "manual_candidate"


def _group_counts(entries: list[SkillRegistryEntry], attr_name: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in entries:
        key = str(getattr(item, attr_name) or "unknown")
        counts[key] = counts.get(key, 0) + 1
    return counts
