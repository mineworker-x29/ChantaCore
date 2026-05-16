from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal
from uuid import uuid4

from chanta_core.deep_self_introspection.mapping import (
    DEEP_SELF_INTROSPECTION_OCEL_EVENT_TYPES,
    DEEP_SELF_INTROSPECTION_OCEL_OBJECT_TYPES,
    DEEP_SELF_INTROSPECTION_OCEL_RELATION_TYPES,
)
from chanta_core.deep_self_introspection.registry import (
    DEEP_SELF_INTROSPECTION_SEED_SKILL_IDS,
    DeepSelfIntrospectionRegistryService,
)
from chanta_core.observation_digest import DIGESTION_SKILL_IDS, OBSERVATION_SKILL_IDS
from chanta_core.self_awareness.registry import SelfAwarenessRegistryService
from chanta_core.utility.time import utc_now_iso


CapabilityStatus = Literal["implemented", "contract_only", "stub", "blocked", "future_track", "unknown"]
TruthStatus = Literal["passed", "warning", "failed", "blocked"]


@dataclass(frozen=True)
class SelfCapabilityRegistryViewRequest:
    layer_filter: str | None = None
    status_filter: str | None = None
    include_contract_only: bool = True
    include_future_track: bool = True
    include_blocked: bool = True
    include_risk_profile: bool = True
    include_gate_contract: bool = True
    include_observability: bool = True
    include_ocel_mapping: bool = True
    max_items: int = 500

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)


@dataclass(frozen=True)
class SelfCapabilityRecord:
    capability_id: str
    skill_id: str | None
    layer: str
    name: str
    description: str
    status: CapabilityStatus
    introduced_in: str | None
    execution_enabled: bool
    materialization_enabled: bool
    canonical_promotion_enabled: bool
    read_only: bool
    candidate_only: bool
    effect_types: list[str]
    risk_profile_ref: str | None
    gate_contract_ref: str | None
    observability_ref: str | None
    ocel_object_types: list[str]
    ocel_event_types: list[str]
    ocel_relation_types: list[str]
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "capability_id": self.capability_id,
            "skill_id": self.skill_id,
            "layer": self.layer,
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "introduced_in": self.introduced_in,
            "execution_enabled": self.execution_enabled,
            "materialization_enabled": self.materialization_enabled,
            "canonical_promotion_enabled": self.canonical_promotion_enabled,
            "read_only": self.read_only,
            "candidate_only": self.candidate_only,
            "effect_types": list(self.effect_types),
            "risk_profile_ref": self.risk_profile_ref,
            "gate_contract_ref": self.gate_contract_ref,
            "observability_ref": self.observability_ref,
            "ocel_object_types": list(self.ocel_object_types),
            "ocel_event_types": list(self.ocel_event_types),
            "ocel_relation_types": list(self.ocel_relation_types),
            "source_refs": [dict(item) for item in self.source_refs],
            "evidence_refs": [dict(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class SelfCapabilityRiskProfileView:
    capability_id: str
    dangerous_capability: bool
    mutates_workspace: bool
    mutates_memory: bool
    mutates_persona: bool
    mutates_overlay: bool
    uses_shell: bool
    uses_network: bool
    uses_mcp: bool
    loads_plugin: bool
    executes_external_harness: bool
    grants_permission: bool
    creates_task: bool
    promotes_candidate: bool
    materializes_candidate: bool
    risk_level: str
    risk_reasons: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "capability_id": self.capability_id,
            "dangerous_capability": self.dangerous_capability,
            "mutates_workspace": self.mutates_workspace,
            "mutates_memory": self.mutates_memory,
            "mutates_persona": self.mutates_persona,
            "mutates_overlay": self.mutates_overlay,
            "uses_shell": self.uses_shell,
            "uses_network": self.uses_network,
            "uses_mcp": self.uses_mcp,
            "loads_plugin": self.loads_plugin,
            "executes_external_harness": self.executes_external_harness,
            "grants_permission": self.grants_permission,
            "creates_task": self.creates_task,
            "promotes_candidate": self.promotes_candidate,
            "materializes_candidate": self.materializes_candidate,
            "risk_level": self.risk_level,
            "risk_reasons": list(self.risk_reasons),
        }


@dataclass(frozen=True)
class SelfCapabilityGateView:
    capability_id: str
    requires_explicit_invocation: bool
    requires_review: bool
    requires_read_only_gate: bool
    requires_execution_envelope: bool
    deny_by_default: bool
    unsupported_if_write_shell_network: bool
    permission_grant_allowed: bool
    gate_status: str

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)


@dataclass(frozen=True)
class SelfCapabilityObservabilityView:
    capability_id: str
    ocel_visible: bool
    pig_visible: bool
    ocpx_visible: bool
    workbench_visible: bool
    audit_visible: bool
    envelope_visible: bool
    observability_status: str
    missing_surfaces: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "capability_id": self.capability_id,
            "ocel_visible": self.ocel_visible,
            "pig_visible": self.pig_visible,
            "ocpx_visible": self.ocpx_visible,
            "workbench_visible": self.workbench_visible,
            "audit_visible": self.audit_visible,
            "envelope_visible": self.envelope_visible,
            "observability_status": self.observability_status,
            "missing_surfaces": list(self.missing_surfaces),
        }


@dataclass(frozen=True)
class SelfCapabilityTruthFinding:
    finding_id: str
    severity: str
    finding_type: str
    capability_id: str | None
    skill_id: str | None
    message: str
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "severity": self.severity,
            "finding_type": self.finding_type,
            "capability_id": self.capability_id,
            "skill_id": self.skill_id,
            "message": self.message,
            "evidence_refs": [dict(item) for item in self.evidence_refs],
            "withdrawal_condition": self.withdrawal_condition,
        }


@dataclass(frozen=True)
class SelfCapabilityRegistrySnapshot:
    snapshot_id: str
    created_at: str
    request: SelfCapabilityRegistryViewRequest
    records: list[SelfCapabilityRecord]
    risk_views: list[SelfCapabilityRiskProfileView]
    gate_views: list[SelfCapabilityGateView]
    observability_views: list[SelfCapabilityObservabilityView]
    total_count: int
    implemented_count: int
    contract_only_count: int
    stub_count: int
    blocked_count: int
    future_track_count: int
    dangerous_capability_count: int
    execution_enabled_count: int
    materialization_enabled_count: int
    canonical_promotion_enabled_count: int
    limitations: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id,
            "created_at": self.created_at,
            "request": self.request.to_dict(),
            "records": [item.to_dict() for item in self.records],
            "risk_views": [item.to_dict() for item in self.risk_views],
            "gate_views": [item.to_dict() for item in self.gate_views],
            "observability_views": [item.to_dict() for item in self.observability_views],
            "total_count": self.total_count,
            "implemented_count": self.implemented_count,
            "contract_only_count": self.contract_only_count,
            "stub_count": self.stub_count,
            "blocked_count": self.blocked_count,
            "future_track_count": self.future_track_count,
            "dangerous_capability_count": self.dangerous_capability_count,
            "execution_enabled_count": self.execution_enabled_count,
            "materialization_enabled_count": self.materialization_enabled_count,
            "canonical_promotion_enabled_count": self.canonical_promotion_enabled_count,
            "limitations": list(self.limitations),
        }


@dataclass(frozen=True)
class SelfCapabilityTruthReport:
    report_id: str
    snapshot_id: str
    created_at: str
    status: TruthStatus
    findings: list[SelfCapabilityTruthFinding]
    registry_truth_summary: dict[str, Any]
    unsafe_claims_detected: int
    dangerous_capabilities_detected: int
    missing_observability_count: int
    missing_gate_count: int
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
            "registry_truth_summary": dict(self.registry_truth_summary),
            "unsafe_claims_detected": self.unsafe_claims_detected,
            "dangerous_capabilities_detected": self.dangerous_capabilities_detected,
            "missing_observability_count": self.missing_observability_count,
            "missing_gate_count": self.missing_gate_count,
            "limitations": list(self.limitations),
            "withdrawal_conditions": list(self.withdrawal_conditions),
            "validity_horizon": self.validity_horizon,
            "review_status": self.review_status,
            "canonical_promotion_enabled": self.canonical_promotion_enabled,
            "promoted": self.promoted,
        }


class SelfCapabilityRegistrySourceService:
    def __init__(
        self,
        *,
        self_awareness_registry: SelfAwarenessRegistryService | None = None,
        deep_self_registry: DeepSelfIntrospectionRegistryService | None = None,
        external_candidate_records: list[SelfCapabilityRecord] | None = None,
    ) -> None:
        self.self_awareness_registry = self_awareness_registry or SelfAwarenessRegistryService()
        self.deep_self_registry = deep_self_registry or DeepSelfIntrospectionRegistryService()
        self.external_candidate_records = external_candidate_records or []

    def load_registry_records(self) -> list[SelfCapabilityRecord]:
        return [
            *self._self_awareness_records(),
            *self._deep_self_records(),
            *self._observation_digestion_records(),
            *[self._external_candidate_record(item) for item in self.external_candidate_records],
        ]

    def _self_awareness_records(self) -> list[SelfCapabilityRecord]:
        records: list[SelfCapabilityRecord] = []
        for contract in self.self_awareness_registry.list_contracts():
            capability_id = contract.capability.capability_id
            records.append(
                SelfCapabilityRecord(
                    capability_id=capability_id,
                    skill_id=contract.skill_id,
                    layer="self_awareness",
                    name=contract.capability.capability_name,
                    description=contract.description,
                    status=_normalize_status(contract.implementation_status),
                    introduced_in=contract.contract_attrs.get("contract_version"),
                    execution_enabled=contract.execution_enabled,
                    materialization_enabled=False,
                    canonical_promotion_enabled=contract.contract_attrs.get("canonical_promotion_enabled", False),
                    read_only=contract.risk_profile.read_only,
                    candidate_only=contract.capability.output_kind.endswith("candidate")
                    or "candidate" in contract.capability.output_kind,
                    effect_types=[contract.effect_type],
                    risk_profile_ref=f"risk:{capability_id}",
                    gate_contract_ref=contract.gate_contract.gate_id,
                    observability_ref=contract.observability_contract.observability_id,
                    ocel_object_types=contract.observability_contract.ocel_object_types,
                    ocel_event_types=contract.observability_contract.ocel_event_types,
                    ocel_relation_types=contract.observability_contract.ocel_relation_types,
                    source_refs=[{"source": "self_awareness_registry", "skill_id": contract.skill_id}],
                    evidence_refs=[{"contract_version": contract.contract_attrs.get("contract_version")}],
                )
            )
        return records

    def _deep_self_records(self) -> list[SelfCapabilityRecord]:
        records: list[SelfCapabilityRecord] = []
        implemented = {
            "skill:deep_self_capability_registry_view",
            "skill:deep_self_capability_truth_check",
        }
        skill_ids = [
            "skill:deep_self_capability_registry_view",
            "skill:deep_self_capability_truth_check",
            *[
                skill_id
                for skill_id in DEEP_SELF_INTROSPECTION_SEED_SKILL_IDS
                if skill_id != "skill:deep_self_capability_registry_view"
            ],
        ]
        for skill_id in skill_ids:
            suffix = skill_id.removeprefix("skill:")
            status: CapabilityStatus = "implemented" if skill_id in implemented else "contract_only"
            records.append(
                SelfCapabilityRecord(
                    capability_id=f"deep_self_capability:{suffix}",
                    skill_id=skill_id,
                    layer="deep_self_introspection",
                    name=suffix.replace("_", " "),
                    description=(
                        "Read-only capability registry awareness view."
                        if skill_id == "skill:deep_self_capability_registry_view"
                        else "Read-only capability truth check."
                        if skill_id == "skill:deep_self_capability_truth_check"
                        else "Contract-only deep self-introspection seed skill."
                    ),
                    status=status,
                    introduced_in="v0.21.1" if skill_id in implemented else "v0.21.0",
                    execution_enabled=False,
                    materialization_enabled=False,
                    canonical_promotion_enabled=False,
                    read_only=True,
                    candidate_only=False,
                    effect_types=["read_only_observation", "state_candidate_created"] if skill_id in implemented else ["contract_only"],
                    risk_profile_ref=f"risk:deep_self_capability:{suffix}",
                    gate_contract_ref=f"gate:{suffix}" if skill_id in implemented else None,
                    observability_ref=f"observability:{suffix}",
                    ocel_object_types=DEEP_SELF_INTROSPECTION_OCEL_OBJECT_TYPES,
                    ocel_event_types=DEEP_SELF_INTROSPECTION_OCEL_EVENT_TYPES,
                    ocel_relation_types=DEEP_SELF_INTROSPECTION_OCEL_RELATION_TYPES,
                    source_refs=[{"source": "deep_self_introspection_registry", "skill_id": skill_id}],
                    evidence_refs=[{"introduced_in": "v0.21.1" if skill_id in implemented else "v0.21.0"}],
                )
            )
        return records

    def _observation_digestion_records(self) -> list[SelfCapabilityRecord]:
        records: list[SelfCapabilityRecord] = []
        for skill_id in [*OBSERVATION_SKILL_IDS, *DIGESTION_SKILL_IDS]:
            layer = "internal_observation" if skill_id in OBSERVATION_SKILL_IDS else "internal_digestion"
            suffix = skill_id.removeprefix("skill:")
            records.append(
                SelfCapabilityRecord(
                    capability_id=f"{layer}_capability:{suffix}",
                    skill_id=skill_id,
                    layer=layer,
                    name=suffix.replace("_", " "),
                    description="Observation/Digestion read-only registry capability.",
                    status="implemented",
                    introduced_in="v0.19.x",
                    execution_enabled=False,
                    materialization_enabled=False,
                    canonical_promotion_enabled=False,
                    read_only=True,
                    candidate_only="candidate" in suffix,
                    effect_types=["read_only_observation"],
                    risk_profile_ref=f"risk:{layer}:{suffix}",
                    gate_contract_ref=f"gate:{layer}:{suffix}",
                    observability_ref=f"observability:{layer}:{suffix}",
                    ocel_object_types=["skill_contract", "capability_record"],
                    ocel_event_types=["deep_self_capability_registry_snapshot_created"],
                    ocel_relation_types=["contains_capability", "describes_skill_contract"],
                    source_refs=[{"source": "observation_digest_skill_ids", "skill_id": skill_id}],
                    evidence_refs=[{"introduced_in": "v0.19.x"}],
                )
            )
        return records

    def _external_candidate_record(self, record: SelfCapabilityRecord) -> SelfCapabilityRecord:
        return SelfCapabilityRecord(
            **{
                **record.to_dict(),
                "layer": record.layer or "external_candidate",
                "status": "future_track",
                "execution_enabled": False,
                "materialization_enabled": False,
                "canonical_promotion_enabled": False,
                "read_only": True,
                "ocel_object_types": record.ocel_object_types or ["external_candidate_capability"],
                "ocel_event_types": record.ocel_event_types or ["deep_self_capability_registry_snapshot_created"],
                "ocel_relation_types": record.ocel_relation_types or ["contains_capability"],
            }
        )


class SelfCapabilityRiskViewService:
    def build_risk_views(self, records: list[SelfCapabilityRecord]) -> list[SelfCapabilityRiskProfileView]:
        return [_risk_view_from_record(record) for record in records]


class SelfCapabilityGateViewService:
    def build_gate_views(self, records: list[SelfCapabilityRecord]) -> list[SelfCapabilityGateView]:
        views: list[SelfCapabilityGateView] = []
        for record in records:
            has_gate = bool(record.gate_contract_ref)
            unsupported = record.execution_enabled or not record.read_only
            views.append(
                SelfCapabilityGateView(
                    capability_id=record.capability_id,
                    requires_explicit_invocation=record.status == "implemented",
                    requires_review=record.candidate_only or record.status in {"contract_only", "future_track", "stub", "blocked"},
                    requires_read_only_gate=record.status == "implemented",
                    requires_execution_envelope=record.status == "implemented",
                    deny_by_default=record.status != "implemented",
                    unsupported_if_write_shell_network=unsupported,
                    permission_grant_allowed=False,
                    gate_status="violation" if record.status == "implemented" and not has_gate else "ok",
                )
            )
        return views


class SelfCapabilityObservabilityViewService:
    def build_observability_views(self, records: list[SelfCapabilityRecord]) -> list[SelfCapabilityObservabilityView]:
        views: list[SelfCapabilityObservabilityView] = []
        for record in records:
            flags = {
                "ocel": bool(record.ocel_object_types and record.ocel_event_types and record.ocel_relation_types),
                "pig": True,
                "ocpx": True,
                "workbench": True,
                "audit": True,
                "envelope": bool(record.gate_contract_ref) or record.status != "implemented",
            }
            missing = [name for name, value in flags.items() if not value]
            views.append(
                SelfCapabilityObservabilityView(
                    capability_id=record.capability_id,
                    ocel_visible=flags["ocel"],
                    pig_visible=flags["pig"],
                    ocpx_visible=flags["ocpx"],
                    workbench_visible=flags["workbench"],
                    audit_visible=flags["audit"],
                    envelope_visible=flags["envelope"],
                    observability_status="complete" if not missing else "partial" if flags["ocel"] else "missing",
                    missing_surfaces=missing,
                )
            )
        return views


class SelfCapabilityTruthCheckService:
    def check_truth(
        self,
        snapshot: SelfCapabilityRegistrySnapshot,
        optional_claims: list[dict[str, Any]] | None = None,
    ) -> SelfCapabilityTruthReport:
        findings: list[SelfCapabilityTruthFinding] = []
        records_by_capability = {record.capability_id: record for record in snapshot.records}
        records_by_skill = {record.skill_id: record for record in snapshot.records if record.skill_id}
        gate_by_capability = {view.capability_id: view for view in snapshot.gate_views}
        observability_by_capability = {view.capability_id: view for view in snapshot.observability_views}
        for record in snapshot.records:
            if record.status == "implemented" and not (
                record.ocel_object_types and record.ocel_event_types and record.ocel_relation_types
            ):
                findings.append(_finding("error", "implemented_without_ocel_mapping", record, "Implemented capability lacks OCEL mapping."))
            gate = gate_by_capability.get(record.capability_id)
            if record.status == "implemented" and (gate is None or gate.gate_status != "ok"):
                findings.append(_finding("error", "implemented_without_gate", record, "Implemented capability lacks a valid gate."))
            observability = observability_by_capability.get(record.capability_id)
            if record.status == "implemented" and observability and not observability.envelope_visible:
                findings.append(_finding("error", "implemented_without_envelope", record, "Implemented capability lacks envelope visibility."))
            if record.execution_enabled and record.status in {"contract_only", "stub", "future_track", "blocked"}:
                findings.append(_finding("error", "contract_only_claimed_as_executable", record, "Non-implemented capability is executable."))
            if record.candidate_only and (record.materialization_enabled or record.canonical_promotion_enabled):
                findings.append(_finding("error", "candidate_only_claimed_as_materialized", record, "Candidate-only capability is materialized or promoted."))
        for risk in snapshot.risk_views:
            if risk.dangerous_capability or risk.risk_level == "blocked":
                record = records_by_capability.get(risk.capability_id)
                findings.append(_finding("critical", "dangerous_capability_enabled", record, "Dangerous capability is enabled."))
        for claim in optional_claims or []:
            record = _record_for_claim(claim, records_by_capability, records_by_skill)
            if record is None:
                findings.append(
                    SelfCapabilityTruthFinding(
                        finding_id=f"capability_truth_finding:{uuid4().hex}",
                        severity="warning",
                        finding_type="unknown_capability_claim",
                        capability_id=claim.get("capability_id"),
                        skill_id=claim.get("skill_id"),
                        message="Optional self-claim references an unknown capability.",
                        evidence_refs=[dict(claim)],
                        withdrawal_condition="Withdraw the claim unless registry evidence is added.",
                    )
                )
                continue
            claimed_status = claim.get("claimed_status") or claim.get("status")
            if record.status == "future_track" and claimed_status == "implemented":
                findings.append(_finding("error", "future_track_claimed_as_implemented", record, "Future-track capability was claimed as implemented."))
            if record.status in {"contract_only", "stub"} and claim.get("claimed_execution_enabled"):
                findings.append(_finding("error", "contract_only_claimed_as_executable", record, "Contract-only capability was claimed as executable."))
            if record.candidate_only and (claim.get("claimed_materialized") or claim.get("claimed_promoted")):
                findings.append(_finding("error", "candidate_only_claimed_as_materialized", record, "Candidate-only capability was claimed as materialized."))
            if claim.get("persona_claim") and claim.get("claimed_execution_enabled") and not record.execution_enabled:
                findings.append(_finding("warning", "persona_claim_exceeds_capability_truth", record, "Persona claim exceeds registry truth."))
        missing_observability = sum(1 for view in snapshot.observability_views if view.observability_status != "complete")
        missing_gate = sum(1 for view in snapshot.gate_views if view.gate_status != "ok")
        unsafe_claims = sum(1 for item in findings if item.finding_type != "ok")
        status: TruthStatus = "passed"
        if any(item.severity in {"error", "critical"} for item in findings):
            status = "failed"
        elif findings or missing_observability:
            status = "warning"
        return SelfCapabilityTruthReport(
            report_id=f"self_capability_truth_report:{uuid4().hex}",
            snapshot_id=snapshot.snapshot_id,
            created_at=utc_now_iso(),
            status=status,
            findings=findings
            or [
                SelfCapabilityTruthFinding(
                    finding_id=f"capability_truth_finding:{uuid4().hex}",
                    severity="info",
                    finding_type="ok",
                    capability_id=None,
                    skill_id=None,
                    message="Capability registry truth check passed.",
                    evidence_refs=[{"snapshot_id": snapshot.snapshot_id}],
                    withdrawal_condition=None,
                )
            ],
            registry_truth_summary={
                "total_count": snapshot.total_count,
                "implemented_count": snapshot.implemented_count,
                "contract_only_count": snapshot.contract_only_count,
                "future_track_count": snapshot.future_track_count,
                "dangerous_capability_count": snapshot.dangerous_capability_count,
                "execution_enabled_count": snapshot.execution_enabled_count,
                "materialization_enabled_count": snapshot.materialization_enabled_count,
                "canonical_promotion_enabled_count": snapshot.canonical_promotion_enabled_count,
                "principle": "Capability truth > persona claim",
            },
            unsafe_claims_detected=unsafe_claims,
            dangerous_capabilities_detected=snapshot.dangerous_capability_count,
            missing_observability_count=missing_observability,
            missing_gate_count=missing_gate,
            limitations=[
                "v0.21.1 performs read-only registry truth awareness.",
                "Optional claim checks use claim-safe structured dictionaries only.",
            ],
            withdrawal_conditions=[
                "Withdraw if registry view mutates a registry or enables a skill.",
                "Withdraw if permission grants, mutation, external execution, or LLM judge behavior are added.",
            ],
            validity_horizon="Valid until v0.21.2 Self-Runtime Boundary Awareness changes runtime boundary assumptions.",
        )


class SelfCapabilityRegistryAwarenessService:
    def __init__(
        self,
        *,
        source_service: SelfCapabilityRegistrySourceService | None = None,
        risk_service: SelfCapabilityRiskViewService | None = None,
        gate_service: SelfCapabilityGateViewService | None = None,
        observability_service: SelfCapabilityObservabilityViewService | None = None,
        truth_service: SelfCapabilityTruthCheckService | None = None,
    ) -> None:
        self.source_service = source_service or SelfCapabilityRegistrySourceService()
        self.risk_service = risk_service or SelfCapabilityRiskViewService()
        self.gate_service = gate_service or SelfCapabilityGateViewService()
        self.observability_service = observability_service or SelfCapabilityObservabilityViewService()
        self.truth_service = truth_service or SelfCapabilityTruthCheckService()
        self.last_snapshot: SelfCapabilityRegistrySnapshot | None = None
        self.last_truth_report: SelfCapabilityTruthReport | None = None

    def view_registry(self, request: SelfCapabilityRegistryViewRequest | None = None) -> SelfCapabilityRegistrySnapshot:
        request = request or SelfCapabilityRegistryViewRequest()
        records = self._filter_records(self.source_service.load_registry_records(), request)
        risk_views = self.risk_service.build_risk_views(records) if request.include_risk_profile else []
        gate_views = self.gate_service.build_gate_views(records) if request.include_gate_contract else []
        observability_views = (
            self.observability_service.build_observability_views(records) if request.include_observability else []
        )
        snapshot = SelfCapabilityRegistrySnapshot(
            snapshot_id=f"self_capability_registry_snapshot:{uuid4().hex}",
            created_at=utc_now_iso(),
            request=request,
            records=records,
            risk_views=risk_views,
            gate_views=gate_views,
            observability_views=observability_views,
            total_count=len(records),
            implemented_count=sum(1 for item in records if item.status == "implemented"),
            contract_only_count=sum(1 for item in records if item.status == "contract_only"),
            stub_count=sum(1 for item in records if item.status == "stub"),
            blocked_count=sum(1 for item in records if item.status == "blocked"),
            future_track_count=sum(1 for item in records if item.status == "future_track"),
            dangerous_capability_count=sum(1 for item in risk_views if item.dangerous_capability),
            execution_enabled_count=sum(1 for item in records if item.execution_enabled),
            materialization_enabled_count=sum(1 for item in records if item.materialization_enabled),
            canonical_promotion_enabled_count=sum(1 for item in records if item.canonical_promotion_enabled),
            limitations=[
                "Registry snapshot is read-only.",
                "No capability, skill, permission, or adapter enablement occurs.",
            ],
        )
        self.last_snapshot = snapshot
        return snapshot

    def truth_check(
        self,
        request: SelfCapabilityRegistryViewRequest | None = None,
        optional_claims: list[dict[str, Any]] | None = None,
    ) -> SelfCapabilityTruthReport:
        snapshot = self.view_registry(request)
        report = self.truth_service.check_truth(snapshot, optional_claims=optional_claims)
        self.last_truth_report = report
        return report

    def build_pig_report(self) -> dict[str, Any]:
        snapshot = self.last_snapshot or self.view_registry()
        return {
            "version": "v0.21.1",
            "layer": "deep_self_introspection",
            "subject": "capability_registry",
            "definition": "Read-only OCEL-native awareness of actual capability registry truth.",
            "principle": "Capability truth > persona claim",
            "capability_truth": {
                "implemented_count": snapshot.implemented_count,
                "contract_only_count": snapshot.contract_only_count,
                "future_track_count": snapshot.future_track_count,
                "dangerous_capability_count": snapshot.dangerous_capability_count,
                "execution_enabled_count": snapshot.execution_enabled_count,
                "materialization_enabled_count": snapshot.materialization_enabled_count,
                "canonical_promotion_enabled_count": snapshot.canonical_promotion_enabled_count,
            },
            "diagnostics": [
                "future_track capabilities must not be claimed as implemented",
                "contract_only capabilities must not be claimed as executable",
                "candidate-only capabilities must not be claimed as materialized",
            ],
            "canonical_store": "ocel",
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "self_capability_registry_awareness",
            "version": "v0.21.1",
            "layer": "deep_self_introspection",
            "source_read_models": [
                "SelfAwarenessReleaseState",
                "DeepSelfIntrospectionContractState",
            ],
            "target_read_models": [
                "SelfCapabilityRegistryState",
                "SelfCapabilityTruthState",
                "SelfCapabilityRiskState",
                "SelfCapabilityContradictionState",
            ],
            "effect_types": ["read_only_observation", "state_candidate_created"],
            "canonical_store": "ocel",
        }

    def render_cli(self, command: str, snapshot: SelfCapabilityRegistrySnapshot | None = None, report: SelfCapabilityTruthReport | None = None) -> str:
        snapshot = snapshot or self.last_snapshot or self.view_registry()
        report = report or self.last_truth_report
        lines = [
            "Self-Capability Registry Awareness",
            f"command={command}",
            f"registry_truth_status={report.status if report else 'not_checked'}",
            "principle=Capability truth > persona claim",
            f"total_count={snapshot.total_count}",
            f"implemented_count={snapshot.implemented_count}",
            f"contract_only_count={snapshot.contract_only_count}",
            f"stub_count={snapshot.stub_count}",
            f"blocked_count={snapshot.blocked_count}",
            f"future_track_count={snapshot.future_track_count}",
            f"dangerous_capability_count={snapshot.dangerous_capability_count}",
            f"execution_enabled_count={snapshot.execution_enabled_count}",
            f"materialization_enabled_count={snapshot.materialization_enabled_count}",
            f"canonical_promotion_enabled_count={snapshot.canonical_promotion_enabled_count}",
            f"missing_observability_count={report.missing_observability_count if report else sum(1 for item in snapshot.observability_views if item.observability_status != 'complete')}",
            "registry_mutated=False",
            "skill_enabled=False",
            "permission_grant_created=False",
            "raw_file_content_printed=False",
            "private_full_paths_printed=False",
            "raw_secrets_printed=False",
        ]
        return "\n".join(lines)

    def _filter_records(
        self,
        records: list[SelfCapabilityRecord],
        request: SelfCapabilityRegistryViewRequest,
    ) -> list[SelfCapabilityRecord]:
        filtered = records
        if request.layer_filter:
            filtered = [item for item in filtered if item.layer == request.layer_filter]
        if request.status_filter:
            filtered = [item for item in filtered if item.status == request.status_filter]
        if not request.include_contract_only:
            filtered = [item for item in filtered if item.status != "contract_only"]
        if not request.include_future_track:
            filtered = [item for item in filtered if item.status != "future_track"]
        if not request.include_blocked:
            filtered = [item for item in filtered if item.status != "blocked"]
        return filtered[: max(0, request.max_items)]


def _normalize_status(status: str) -> CapabilityStatus:
    if status in {"implemented", "contract_only", "stub", "blocked", "future_track"}:
        return status  # type: ignore[return-value]
    return "unknown"


def _risk_view_from_record(record: SelfCapabilityRecord) -> SelfCapabilityRiskProfileView:
    dangerous = record.execution_enabled or record.materialization_enabled or record.canonical_promotion_enabled
    reasons = []
    if record.execution_enabled:
        reasons.append("execution_enabled")
    if record.materialization_enabled:
        reasons.append("materialization_enabled")
    if record.canonical_promotion_enabled:
        reasons.append("canonical_promotion_enabled")
    return SelfCapabilityRiskProfileView(
        capability_id=record.capability_id,
        dangerous_capability=dangerous,
        mutates_workspace=False,
        mutates_memory=False,
        mutates_persona=False,
        mutates_overlay=False,
        uses_shell=False,
        uses_network=False,
        uses_mcp=False,
        loads_plugin=False,
        executes_external_harness=False,
        grants_permission=False,
        creates_task=False,
        promotes_candidate=record.canonical_promotion_enabled,
        materializes_candidate=record.materialization_enabled,
        risk_level="blocked" if dangerous else "none",
        risk_reasons=reasons,
    )


def _record_for_claim(
    claim: dict[str, Any],
    records_by_capability: dict[str, SelfCapabilityRecord],
    records_by_skill: dict[str, SelfCapabilityRecord],
) -> SelfCapabilityRecord | None:
    capability_id = claim.get("capability_id")
    skill_id = claim.get("skill_id")
    if capability_id in records_by_capability:
        return records_by_capability[capability_id]
    if skill_id in records_by_skill:
        return records_by_skill[skill_id]
    return None


def _finding(
    severity: str,
    finding_type: str,
    record: SelfCapabilityRecord | None,
    message: str,
) -> SelfCapabilityTruthFinding:
    return SelfCapabilityTruthFinding(
        finding_id=f"capability_truth_finding:{uuid4().hex}",
        severity=severity,
        finding_type=finding_type,
        capability_id=record.capability_id if record else None,
        skill_id=record.skill_id if record else None,
        message=message,
        evidence_refs=record.evidence_refs if record else [],
        withdrawal_condition="Withdraw unsafe capability claim unless registry evidence is corrected.",
    )
