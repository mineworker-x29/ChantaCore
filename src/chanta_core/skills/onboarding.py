from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from chanta_core.ocel.models import OCELEvent, OCELObject, OCELRecord, OCELRelation
from chanta_core.ocel.store import OCELStore
from chanta_core.skills.ids import (
    new_internal_skill_descriptor_id,
    new_internal_skill_gate_contract_id,
    new_internal_skill_input_contract_id,
    new_internal_skill_observability_contract_id,
    new_internal_skill_onboarding_finding_id,
    new_internal_skill_onboarding_result_id,
    new_internal_skill_onboarding_review_id,
    new_internal_skill_output_contract_id,
    new_internal_skill_risk_profile_id,
)
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso
from chanta_core.observation_digest import (
    DIGESTION_SKILL_IDS,
    OBSERVATION_DIGESTION_EVENT_ACTIVITIES,
    OBSERVATION_DIGESTION_OBJECT_TYPES,
    OBSERVATION_DIGESTION_RELATIONS,
    OBSERVATION_DIGESTION_SKILL_IDS,
    OBSERVATION_SKILL_IDS,
)


ALLOWED_RISK_CLASSES = {"read_only", "low", "medium", "high", "write", "shell", "network", "mcp", "plugin"}
ALLOWED_CAPABILITY_CATEGORIES = {
    "runtime_status",
    "workbench",
    "audit",
    "promotion",
    "workspace_read",
    "read_only",
    "observation",
    "digestion",
    "write",
    "shell",
    "network",
    "mcp",
    "plugin",
}
BLOCKED_RISK_CLASSES = {"write", "shell", "network", "mcp", "plugin"}
BLOCKED_CAPABILITY_CATEGORIES = {"write", "shell", "network", "mcp", "plugin"}
DEFAULT_READ_ONLY_CANDIDATE_SKILL_IDS = [
    "skill:personal_runtime_status",
    "skill:workbench_status",
    "skill:execution_audit",
    "skill:promotion_candidate_list",
    "skill:workspace_summary_from_file",
    *OBSERVATION_DIGESTION_SKILL_IDS,
]
DEFAULT_OCEL_OBJECT_TYPES = [
    "internal_skill_descriptor",
    "internal_skill_input_contract",
    "internal_skill_output_contract",
    "internal_skill_risk_profile",
    "internal_skill_gate_contract",
    "internal_skill_observability_contract",
    "internal_skill_onboarding_review",
    "internal_skill_onboarding_finding",
    "internal_skill_onboarding_result",
]
DEFAULT_OCEL_EVENT_ACTIVITIES = [
    "internal_skill_descriptor_registered",
    "internal_skill_input_contract_registered",
    "internal_skill_output_contract_registered",
    "internal_skill_risk_profile_registered",
    "internal_skill_gate_contract_registered",
    "internal_skill_observability_contract_registered",
    "internal_skill_onboarding_review_requested",
    "internal_skill_onboarding_finding_recorded",
    "internal_skill_onboarding_result_recorded",
]
DEFAULT_REQUIRED_RELATIONS = [
    "input_contract_belongs_to_descriptor",
    "output_contract_belongs_to_descriptor",
    "risk_profile_belongs_to_descriptor",
    "gate_contract_belongs_to_descriptor",
    "observability_contract_belongs_to_descriptor",
    "onboarding_review_reviews_descriptor",
    "onboarding_result_summarizes_review",
    "onboarding_finding_belongs_to_descriptor",
]


@dataclass(frozen=True)
class InternalSkillDescriptor:
    descriptor_id: str
    skill_id: str
    skill_name: str
    description: str
    capability_category: str
    risk_class: str
    invocation_modes: list[str]
    supported: bool
    enabled_by_default: bool
    owner_module: str
    created_at: str
    descriptor_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "descriptor_id": self.descriptor_id,
            "skill_id": self.skill_id,
            "skill_name": self.skill_name,
            "description": self.description,
            "capability_category": self.capability_category,
            "risk_class": self.risk_class,
            "invocation_modes": list(self.invocation_modes),
            "supported": self.supported,
            "enabled_by_default": self.enabled_by_default,
            "owner_module": self.owner_module,
            "created_at": self.created_at,
            "descriptor_attrs": dict(self.descriptor_attrs),
        }


@dataclass(frozen=True)
class InternalSkillInputContract:
    input_contract_id: str
    skill_id: str
    required_fields: list[str]
    optional_fields: list[str]
    field_types: dict[str, str]
    validation_rules: list[str]
    redacted_fields: list[str]
    created_at: str
    input_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "input_contract_id": self.input_contract_id,
            "skill_id": self.skill_id,
            "required_fields": list(self.required_fields),
            "optional_fields": list(self.optional_fields),
            "field_types": dict(self.field_types),
            "validation_rules": list(self.validation_rules),
            "redacted_fields": list(self.redacted_fields),
            "created_at": self.created_at,
            "input_attrs": dict(self.input_attrs),
        }


@dataclass(frozen=True)
class InternalSkillOutputContract:
    output_contract_id: str
    skill_id: str
    output_kind: str
    required_fields: list[str]
    preview_fields: list[str]
    sensitive_fields: list[str]
    max_preview_chars: int
    full_output_allowed: bool
    created_at: str
    output_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "output_contract_id": self.output_contract_id,
            "skill_id": self.skill_id,
            "output_kind": self.output_kind,
            "required_fields": list(self.required_fields),
            "preview_fields": list(self.preview_fields),
            "sensitive_fields": list(self.sensitive_fields),
            "max_preview_chars": self.max_preview_chars,
            "full_output_allowed": self.full_output_allowed,
            "created_at": self.created_at,
            "output_attrs": dict(self.output_attrs),
        }


@dataclass(frozen=True)
class InternalSkillRiskProfile:
    risk_profile_id: str
    skill_id: str
    risk_class: str
    reversible: bool
    read_only: bool
    touches_filesystem: bool
    touches_network: bool
    touches_shell: bool
    touches_private_context: bool
    requires_review: bool
    requires_permission: bool
    created_at: str
    risk_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "risk_profile_id": self.risk_profile_id,
            "skill_id": self.skill_id,
            "risk_class": self.risk_class,
            "reversible": self.reversible,
            "read_only": self.read_only,
            "touches_filesystem": self.touches_filesystem,
            "touches_network": self.touches_network,
            "touches_shell": self.touches_shell,
            "touches_private_context": self.touches_private_context,
            "requires_review": self.requires_review,
            "requires_permission": self.requires_permission,
            "created_at": self.created_at,
            "risk_attrs": dict(self.risk_attrs),
        }


@dataclass(frozen=True)
class InternalSkillGateContract:
    gate_contract_id: str
    skill_id: str
    gate_required: bool
    gate_kind: str
    supported_gate_policy_ids: list[str]
    deny_if_gate_missing: bool
    deny_if_permission_missing: bool
    deny_if_workspace_boundary_unknown: bool
    created_at: str
    gate_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "gate_contract_id": self.gate_contract_id,
            "skill_id": self.skill_id,
            "gate_required": self.gate_required,
            "gate_kind": self.gate_kind,
            "supported_gate_policy_ids": list(self.supported_gate_policy_ids),
            "deny_if_gate_missing": self.deny_if_gate_missing,
            "deny_if_permission_missing": self.deny_if_permission_missing,
            "deny_if_workspace_boundary_unknown": self.deny_if_workspace_boundary_unknown,
            "created_at": self.created_at,
            "gate_attrs": dict(self.gate_attrs),
        }


@dataclass(frozen=True)
class InternalSkillObservabilityContract:
    observability_contract_id: str
    skill_id: str
    ocel_object_types: list[str]
    ocel_event_activities: list[str]
    required_relations: list[str]
    envelope_required: bool
    audit_visible: bool
    workbench_visible: bool
    pig_report_keys: list[str]
    ocpx_projection_keys: list[str]
    created_at: str
    observability_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "observability_contract_id": self.observability_contract_id,
            "skill_id": self.skill_id,
            "ocel_object_types": list(self.ocel_object_types),
            "ocel_event_activities": list(self.ocel_event_activities),
            "required_relations": list(self.required_relations),
            "envelope_required": self.envelope_required,
            "audit_visible": self.audit_visible,
            "workbench_visible": self.workbench_visible,
            "pig_report_keys": list(self.pig_report_keys),
            "ocpx_projection_keys": list(self.ocpx_projection_keys),
            "created_at": self.created_at,
            "observability_attrs": dict(self.observability_attrs),
        }


@dataclass(frozen=True)
class InternalSkillOnboardingReview:
    review_id: str
    skill_id: str
    descriptor_id: str
    status: str
    reviewer_type: str | None
    reviewer_id: str | None
    reason: str | None
    created_at: str
    review_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "review_id": self.review_id,
            "skill_id": self.skill_id,
            "descriptor_id": self.descriptor_id,
            "status": self.status,
            "reviewer_type": self.reviewer_type,
            "reviewer_id": self.reviewer_id,
            "reason": self.reason,
            "created_at": self.created_at,
            "review_attrs": dict(self.review_attrs),
        }


@dataclass(frozen=True)
class InternalSkillOnboardingFinding:
    finding_id: str
    skill_id: str
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
class InternalSkillOnboardingResult:
    result_id: str
    skill_id: str
    descriptor_id: str
    review_id: str
    status: str
    accepted: bool
    enabled: bool
    finding_ids: list[str]
    summary: str
    created_at: str
    result_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "result_id": self.result_id,
            "skill_id": self.skill_id,
            "descriptor_id": self.descriptor_id,
            "review_id": self.review_id,
            "status": self.status,
            "accepted": self.accepted,
            "enabled": self.enabled,
            "finding_ids": list(self.finding_ids),
            "summary": self.summary,
            "created_at": self.created_at,
            "result_attrs": dict(self.result_attrs),
        }


class InternalSkillOnboardingService:
    def __init__(
        self,
        *,
        trace_service: TraceService | None = None,
        ocel_store: OCELStore | None = None,
    ) -> None:
        if trace_service is not None:
            self.trace_service = trace_service
        elif ocel_store is not None:
            self.trace_service = TraceService(ocel_store=ocel_store)
        else:
            self.trace_service = TraceService()
        self.descriptors: dict[str, InternalSkillDescriptor] = {}
        self.last_descriptor: InternalSkillDescriptor | None = None
        self.last_input_contract: InternalSkillInputContract | None = None
        self.last_output_contract: InternalSkillOutputContract | None = None
        self.last_risk_profile: InternalSkillRiskProfile | None = None
        self.last_gate_contract: InternalSkillGateContract | None = None
        self.last_observability_contract: InternalSkillObservabilityContract | None = None
        self.last_review: InternalSkillOnboardingReview | None = None
        self.last_findings: list[InternalSkillOnboardingFinding] = []
        self.last_result: InternalSkillOnboardingResult | None = None

    def create_descriptor(
        self,
        *,
        skill_id: str,
        skill_name: str,
        description: str,
        capability_category: str,
        risk_class: str = "read_only",
        invocation_modes: list[str] | None = None,
        supported: bool = True,
        enabled_by_default: bool = False,
        owner_module: str = "chanta_core.skills",
        descriptor_attrs: dict[str, Any] | None = None,
    ) -> InternalSkillDescriptor:
        descriptor = InternalSkillDescriptor(
            descriptor_id=new_internal_skill_descriptor_id(),
            skill_id=skill_id,
            skill_name=skill_name,
            description=description,
            capability_category=capability_category,
            risk_class=risk_class,
            invocation_modes=list(invocation_modes or ["explicit_cli", "explicit_api"]),
            supported=supported,
            enabled_by_default=enabled_by_default,
            owner_module=owner_module,
            created_at=utc_now_iso(),
            descriptor_attrs={
                "onboarding_contract_only": True,
                "runtime_registered": False,
                "skills_executed": False,
                **dict(descriptor_attrs or {}),
            },
        )
        self.descriptors[descriptor.skill_id] = descriptor
        self.last_descriptor = descriptor
        self._record(
            "internal_skill_descriptor_registered",
            objects=[_object("internal_skill_descriptor", descriptor.descriptor_id, descriptor.to_dict())],
            links=[("internal_skill_descriptor_object", descriptor.descriptor_id)],
            object_links=[],
            attrs={"skill_id": skill_id, "capability_category": capability_category},
        )
        return descriptor

    def create_input_contract(
        self,
        *,
        skill_id: str,
        required_fields: list[str] | None = None,
        optional_fields: list[str] | None = None,
        field_types: dict[str, str] | None = None,
        validation_rules: list[str] | None = None,
        redacted_fields: list[str] | None = None,
        input_attrs: dict[str, Any] | None = None,
    ) -> InternalSkillInputContract:
        contract = InternalSkillInputContract(
            input_contract_id=new_internal_skill_input_contract_id(),
            skill_id=skill_id,
            required_fields=list(required_fields or []),
            optional_fields=list(optional_fields or []),
            field_types=dict(field_types or {}),
            validation_rules=list(validation_rules or []),
            redacted_fields=list(redacted_fields or []),
            created_at=utc_now_iso(),
            input_attrs=dict(input_attrs or {}),
        )
        self.last_input_contract = contract
        self._record_contract("internal_skill_input_contract_registered", "internal_skill_input_contract", contract.input_contract_id, contract.to_dict())
        return contract

    def create_output_contract(
        self,
        *,
        skill_id: str,
        output_kind: str = "diagnostic",
        required_fields: list[str] | None = None,
        preview_fields: list[str] | None = None,
        sensitive_fields: list[str] | None = None,
        max_preview_chars: int = 2000,
        full_output_allowed: bool = False,
        output_attrs: dict[str, Any] | None = None,
    ) -> InternalSkillOutputContract:
        contract = InternalSkillOutputContract(
            output_contract_id=new_internal_skill_output_contract_id(),
            skill_id=skill_id,
            output_kind=output_kind,
            required_fields=list(required_fields or ["status", "summary"]),
            preview_fields=list(preview_fields or ["status", "summary"]),
            sensitive_fields=list(sensitive_fields or []),
            max_preview_chars=max_preview_chars,
            full_output_allowed=full_output_allowed,
            created_at=utc_now_iso(),
            output_attrs=dict(output_attrs or {}),
        )
        self.last_output_contract = contract
        self._record_contract("internal_skill_output_contract_registered", "internal_skill_output_contract", contract.output_contract_id, contract.to_dict())
        return contract

    def create_risk_profile(
        self,
        *,
        skill_id: str,
        risk_class: str = "read_only",
        reversible: bool = True,
        read_only: bool = True,
        touches_filesystem: bool = False,
        touches_network: bool = False,
        touches_shell: bool = False,
        touches_private_context: bool = False,
        requires_review: bool = True,
        requires_permission: bool = False,
        risk_attrs: dict[str, Any] | None = None,
    ) -> InternalSkillRiskProfile:
        profile = InternalSkillRiskProfile(
            risk_profile_id=new_internal_skill_risk_profile_id(),
            skill_id=skill_id,
            risk_class=risk_class,
            reversible=reversible,
            read_only=read_only,
            touches_filesystem=touches_filesystem,
            touches_network=touches_network,
            touches_shell=touches_shell,
            touches_private_context=touches_private_context,
            requires_review=requires_review,
            requires_permission=requires_permission,
            created_at=utc_now_iso(),
            risk_attrs=dict(risk_attrs or {}),
        )
        self.last_risk_profile = profile
        self._record_contract("internal_skill_risk_profile_registered", "internal_skill_risk_profile", profile.risk_profile_id, profile.to_dict())
        return profile

    def create_gate_contract(
        self,
        *,
        skill_id: str,
        gate_required: bool = True,
        gate_kind: str = "read_only_execution_gate",
        supported_gate_policy_ids: list[str] | None = None,
        deny_if_gate_missing: bool = True,
        deny_if_permission_missing: bool = False,
        deny_if_workspace_boundary_unknown: bool = True,
        gate_attrs: dict[str, Any] | None = None,
    ) -> InternalSkillGateContract:
        contract = InternalSkillGateContract(
            gate_contract_id=new_internal_skill_gate_contract_id(),
            skill_id=skill_id,
            gate_required=gate_required,
            gate_kind=gate_kind,
            supported_gate_policy_ids=list(supported_gate_policy_ids or ["read_only_execution_gate"]),
            deny_if_gate_missing=deny_if_gate_missing,
            deny_if_permission_missing=deny_if_permission_missing,
            deny_if_workspace_boundary_unknown=deny_if_workspace_boundary_unknown,
            created_at=utc_now_iso(),
            gate_attrs=dict(gate_attrs or {}),
        )
        self.last_gate_contract = contract
        self._record_contract("internal_skill_gate_contract_registered", "internal_skill_gate_contract", contract.gate_contract_id, contract.to_dict())
        return contract

    def create_observability_contract(
        self,
        *,
        skill_id: str,
        ocel_object_types: list[str] | None = None,
        ocel_event_activities: list[str] | None = None,
        required_relations: list[str] | None = None,
        envelope_required: bool = True,
        audit_visible: bool = True,
        workbench_visible: bool = True,
        pig_report_keys: list[str] | None = None,
        ocpx_projection_keys: list[str] | None = None,
        observability_attrs: dict[str, Any] | None = None,
    ) -> InternalSkillObservabilityContract:
        contract = InternalSkillObservabilityContract(
            observability_contract_id=new_internal_skill_observability_contract_id(),
            skill_id=skill_id,
            ocel_object_types=list(DEFAULT_OCEL_OBJECT_TYPES if ocel_object_types is None else ocel_object_types),
            ocel_event_activities=list(DEFAULT_OCEL_EVENT_ACTIVITIES if ocel_event_activities is None else ocel_event_activities),
            required_relations=list(DEFAULT_REQUIRED_RELATIONS if required_relations is None else required_relations),
            envelope_required=envelope_required,
            audit_visible=audit_visible,
            workbench_visible=workbench_visible,
            pig_report_keys=list(
                [
                    "internal_skill_descriptor_count",
                    "internal_skill_onboarding_result_count",
                    "internal_skill_onboarding_accepted_count",
                ]
                if pig_report_keys is None
                else pig_report_keys
            ),
            ocpx_projection_keys=list(
                ["internal_skill_onboarding_by_capability_category", "internal_skill_onboarding_by_risk_class"]
                if ocpx_projection_keys is None
                else ocpx_projection_keys
            ),
            created_at=utc_now_iso(),
            observability_attrs=dict(observability_attrs or {}),
        )
        self.last_observability_contract = contract
        self._record_contract("internal_skill_observability_contract_registered", "internal_skill_observability_contract", contract.observability_contract_id, contract.to_dict())
        return contract

    def validate_onboarding(
        self,
        *,
        descriptor: InternalSkillDescriptor,
        input_contract: InternalSkillInputContract | None = None,
        output_contract: InternalSkillOutputContract | None = None,
        risk_profile: InternalSkillRiskProfile | None = None,
        gate_contract: InternalSkillGateContract | None = None,
        observability_contract: InternalSkillObservabilityContract | None = None,
        reviewer_type: str | None = None,
        reviewer_id: str | None = None,
    ) -> InternalSkillOnboardingResult:
        self.last_findings = []
        review = self.record_review(
            skill_id=descriptor.skill_id,
            descriptor_id=descriptor.descriptor_id,
            status="requested",
            reviewer_type=reviewer_type,
            reviewer_id=reviewer_id,
            reason="Internal skill onboarding contract validation.",
        )
        findings: list[InternalSkillOnboardingFinding] = []

        def add(finding_type: str, severity: str, message: str, subject_ref: str | None = None) -> None:
            findings.append(
                self.record_finding(
                    skill_id=descriptor.skill_id,
                    finding_type=finding_type,
                    status="failed",
                    severity=severity,
                    message=message,
                    subject_ref=subject_ref or descriptor.descriptor_id,
                    finding_attrs={"descriptor_id": descriptor.descriptor_id},
                )
            )

        if not descriptor.skill_id:
            add("missing_skill_id", "high", "Internal skill descriptor must include a skill_id.")
        if not input_contract:
            add("missing_input_contract", "high", "Internal skill onboarding requires an input contract.")
        if not output_contract:
            add("missing_output_contract", "high", "Internal skill onboarding requires an output contract.")
        if not risk_profile:
            add("missing_risk_profile", "high", "Internal skill onboarding requires a risk profile.")
        if not gate_contract:
            add("missing_gate_contract", "high", "Internal skill onboarding requires a gate contract.")
        if not observability_contract:
            add("missing_observability_contract", "high", "Internal skill onboarding requires an observability contract.")
        if descriptor.risk_class not in ALLOWED_RISK_CLASSES:
            add("invalid_risk_class", "high", "Risk class is not supported by the onboarding contract.", descriptor.risk_class)
        if descriptor.capability_category not in ALLOWED_CAPABILITY_CATEGORIES:
            add("invalid_capability_category", "high", "Capability category is not supported by the onboarding contract.", descriptor.capability_category)

        blocked = descriptor.risk_class in BLOCKED_RISK_CLASSES or descriptor.capability_category in BLOCKED_CAPABILITY_CATEGORIES
        if risk_profile:
            blocked = blocked or risk_profile.risk_class in BLOCKED_RISK_CLASSES
            blocked = blocked or not risk_profile.read_only
            blocked = blocked or risk_profile.touches_network or risk_profile.touches_shell
        if blocked:
            add("unsafe_category_blocked", "critical", "write/shell/network/MCP/plugin skill categories are blocked in v0.18.6.", descriptor.skill_id)

        if observability_contract:
            if not observability_contract.envelope_required:
                add("missing_envelope_support", "high", "Execution envelope support is mandatory for internal skill onboarding.", observability_contract.observability_contract_id)
            if not observability_contract.ocel_object_types or not observability_contract.ocel_event_activities or not observability_contract.required_relations:
                add("missing_ocel_mapping", "high", "OCEL object/event/relation mappings are mandatory.", observability_contract.observability_contract_id)
            if not observability_contract.pig_report_keys:
                add("missing_pig_report_mapping", "high", "PIG report keys are mandatory.", observability_contract.observability_contract_id)
            if not observability_contract.ocpx_projection_keys:
                add("missing_ocpx_projection_mapping", "high", "OCPX projection keys are mandatory.", observability_contract.observability_contract_id)
            if not observability_contract.audit_visible or not observability_contract.workbench_visible:
                add("missing_operator_visibility", "medium", "Audit and workbench visibility must be declared.", observability_contract.observability_contract_id)

        status = "accepted"
        accepted = True
        if findings:
            accepted = False
            status = "blocked" if any(f.severity == "critical" for f in findings) else "needs_fix"
        result = self.record_result(
            skill_id=descriptor.skill_id,
            descriptor_id=descriptor.descriptor_id,
            review_id=review.review_id,
            status=status,
            accepted=accepted,
            enabled=False,
            findings=findings,
            summary=_onboarding_summary(status=status, skill_id=descriptor.skill_id, finding_count=len(findings)),
            result_attrs={
                "input_contract_id": input_contract.input_contract_id if input_contract else None,
                "output_contract_id": output_contract.output_contract_id if output_contract else None,
                "risk_profile_id": risk_profile.risk_profile_id if risk_profile else None,
                "gate_contract_id": gate_contract.gate_contract_id if gate_contract else None,
                "observability_contract_id": observability_contract.observability_contract_id if observability_contract else None,
                "runtime_registered": False,
                "skills_executed": False,
                "permission_grants_created": False,
                "enabled_by_default_requested": descriptor.enabled_by_default,
            },
        )
        return result

    def record_finding(
        self,
        *,
        skill_id: str,
        finding_type: str,
        status: str,
        severity: str,
        message: str,
        subject_ref: str | None = None,
        finding_attrs: dict[str, Any] | None = None,
    ) -> InternalSkillOnboardingFinding:
        finding = InternalSkillOnboardingFinding(
            finding_id=new_internal_skill_onboarding_finding_id(),
            skill_id=skill_id,
            finding_type=finding_type,
            status=status,
            severity=severity,
            message=message,
            subject_ref=subject_ref,
            created_at=utc_now_iso(),
            finding_attrs={
                "skills_executed": False,
                "permission_grants_created": False,
                **dict(finding_attrs or {}),
            },
        )
        self.last_findings.append(finding)
        self._record(
            "internal_skill_onboarding_finding_recorded",
            objects=[_object("internal_skill_onboarding_finding", finding.finding_id, finding.to_dict())],
            links=[("internal_skill_onboarding_finding_object", finding.finding_id)],
            object_links=[],
            attrs={"skill_id": skill_id, "finding_type": finding_type, "severity": severity},
        )
        return finding

    def record_review(
        self,
        *,
        skill_id: str,
        descriptor_id: str,
        status: str,
        reviewer_type: str | None = None,
        reviewer_id: str | None = None,
        reason: str | None = None,
        review_attrs: dict[str, Any] | None = None,
    ) -> InternalSkillOnboardingReview:
        review = InternalSkillOnboardingReview(
            review_id=new_internal_skill_onboarding_review_id(),
            skill_id=skill_id,
            descriptor_id=descriptor_id,
            status=status,
            reviewer_type=reviewer_type,
            reviewer_id=reviewer_id,
            reason=reason,
            created_at=utc_now_iso(),
            review_attrs={
                "diagnostic_only": True,
                "skills_executed": False,
                "permission_grants_created": False,
                **dict(review_attrs or {}),
            },
        )
        self.last_review = review
        self._record(
            "internal_skill_onboarding_review_requested",
            objects=[_object("internal_skill_onboarding_review", review.review_id, review.to_dict())],
            links=[
                ("internal_skill_onboarding_review_object", review.review_id),
                ("internal_skill_descriptor_object", descriptor_id),
            ],
            object_links=[(review.review_id, descriptor_id, "onboarding_review_reviews_descriptor")],
            attrs={"skill_id": skill_id, "status": status},
        )
        return review

    def record_result(
        self,
        *,
        skill_id: str,
        descriptor_id: str,
        review_id: str,
        status: str,
        accepted: bool,
        enabled: bool,
        findings: list[InternalSkillOnboardingFinding],
        summary: str,
        result_attrs: dict[str, Any] | None = None,
    ) -> InternalSkillOnboardingResult:
        result = InternalSkillOnboardingResult(
            result_id=new_internal_skill_onboarding_result_id(),
            skill_id=skill_id,
            descriptor_id=descriptor_id,
            review_id=review_id,
            status=status,
            accepted=accepted,
            enabled=enabled,
            finding_ids=[finding.finding_id for finding in findings],
            summary=summary,
            created_at=utc_now_iso(),
            result_attrs={
                "diagnostic_only": True,
                "runtime_registered": False,
                "skills_executed": False,
                "permission_grants_created": False,
                "tool_dispatcher_mutated": False,
                "skill_executor_mutated": False,
                "llm_called": False,
                "shell_execution_used": False,
                "network_access_used": False,
                "mcp_connection_used": False,
                "plugin_loaded": False,
                **dict(result_attrs or {}),
            },
        )
        self.last_result = result
        links = [
            ("internal_skill_onboarding_result_object", result.result_id),
            ("internal_skill_descriptor_object", descriptor_id),
            ("internal_skill_onboarding_review_object", review_id),
        ] + [("internal_skill_onboarding_finding_object", finding.finding_id) for finding in findings]
        object_links = [
            (result.result_id, review_id, "onboarding_result_summarizes_review"),
            (result.result_id, descriptor_id, "onboarding_result_summarizes_descriptor"),
        ] + [(finding.finding_id, descriptor_id, "onboarding_finding_belongs_to_descriptor") for finding in findings]
        self._record(
            "internal_skill_onboarding_result_recorded",
            objects=[_object("internal_skill_onboarding_result", result.result_id, result.to_dict())],
            links=links,
            object_links=object_links,
            attrs={"skill_id": skill_id, "status": status, "accepted": accepted, "enabled": enabled},
        )
        status_event = {
            "accepted": "internal_skill_onboarding_accepted",
            "rejected": "internal_skill_onboarding_rejected",
            "needs_fix": "internal_skill_onboarding_needs_fix",
            "blocked": "internal_skill_onboarding_blocked",
        }.get(status)
        if status_event:
            self._record(
                status_event,
                objects=[_object("internal_skill_onboarding_result", result.result_id, result.to_dict())],
                links=[
                    ("internal_skill_onboarding_result_object", result.result_id),
                    ("internal_skill_descriptor_object", descriptor_id),
                ],
                object_links=[(result.result_id, descriptor_id, "onboarding_result_summarizes_descriptor")],
                attrs={"skill_id": skill_id, "status": status},
            )
        return result

    def render_onboarding_summary(self, result: InternalSkillOnboardingResult) -> str:
        lines = [
            "Internal Skill Onboarding",
            f"status={result.status}",
            f"accepted={str(result.accepted).lower()}",
            f"enabled={str(result.enabled).lower()}",
            f"skill_id={result.skill_id}",
            f"descriptor_id={result.descriptor_id}",
            f"review_id={result.review_id}",
            f"finding_count={len(result.finding_ids)}",
            "skills_executed=false",
            "runtime_registered=false",
            "permission_grants_created=false",
            "tool_dispatcher_mutated=false",
            "skill_executor_mutated=false",
            f"summary={result.summary}",
        ]
        if self.last_findings:
            lines.append(f"first_finding_type={self.last_findings[0].finding_type}")
        return "\n".join(lines)

    def create_read_only_skill_contract_bundle(self, *, skill_id: str) -> dict[str, Any]:
        descriptor = self.create_descriptor(
            skill_id=skill_id,
            skill_name=skill_id.removeprefix("skill:").replace("_", " ").title(),
            description="Candidate read-only internal skill contract descriptor.",
            capability_category=_default_category(skill_id),
            risk_class="read_only",
            supported=True,
            enabled_by_default=False,
            owner_module="chanta_core.skills",
        )
        input_contract = self.create_input_contract(
            skill_id=skill_id,
            required_fields=_default_required_fields(skill_id),
            optional_fields=["limit", "show_paths", "format_hint", "runtime", "vendor_hint"],
            field_types={
                "root_path": "str",
                "relative_path": "str",
                "limit": "int",
                "show_paths": "bool",
                "format_hint": "str",
                "runtime": "str",
                "vendor_hint": "str",
            },
            validation_rules=["explicit_input_only", "no_ambient_context", "redact_path_like_values"],
            redacted_fields=["root_path"],
        )
        output_contract = self.create_output_contract(skill_id=skill_id)
        filesystem_read_skill_ids = {
            "skill:workspace_summary_from_file",
            "skill:agent_observation_source_inspect",
            "skill:agent_trace_observe",
            "skill:external_skill_source_inspect",
            "skill:external_skill_static_digest",
        }
        risk_profile = self.create_risk_profile(
            skill_id=skill_id,
            read_only=True,
            touches_filesystem=skill_id in filesystem_read_skill_ids,
        )
        gate_contract = self.create_gate_contract(skill_id=skill_id)
        observability_kwargs = {}
        if skill_id in OBSERVATION_DIGESTION_SKILL_IDS:
            observability_kwargs = {
                "ocel_object_types": OBSERVATION_DIGESTION_OBJECT_TYPES,
                "ocel_event_activities": OBSERVATION_DIGESTION_EVENT_ACTIVITIES,
                "required_relations": OBSERVATION_DIGESTION_RELATIONS,
                "pig_report_keys": [
                    "agent_observation_source_count",
                    "external_skill_assimilation_candidate_count",
                    "observation_digestion_result_count",
                ],
                "ocpx_projection_keys": [
                    "observed_event_by_activity",
                    "external_candidate_by_risk_class",
                ],
            }
        observability_contract = self.create_observability_contract(skill_id=skill_id, **observability_kwargs)
        return {
            "descriptor": descriptor,
            "input_contract": input_contract,
            "output_contract": output_contract,
            "risk_profile": risk_profile,
            "gate_contract": gate_contract,
            "observability_contract": observability_contract,
        }

    def default_read_only_descriptor_candidates(self) -> list[InternalSkillDescriptor]:
        return [
            self.create_descriptor(
                skill_id=skill_id,
                skill_name=skill_id.removeprefix("skill:").replace("_", " ").title(),
                description="Candidate descriptor for future read-only internal skill pack.",
                capability_category=_default_category(skill_id),
                risk_class="read_only",
                enabled_by_default=False,
            )
            for skill_id in DEFAULT_READ_ONLY_CANDIDATE_SKILL_IDS
        ]

    def _record_contract(self, activity: str, object_type: str, object_id: str, attrs: dict[str, Any]) -> None:
        skill_id = str(attrs.get("skill_id") or "")
        descriptor = self.descriptors.get(skill_id)
        relation_by_object_type = {
            "internal_skill_input_contract": "input_contract_belongs_to_descriptor",
            "internal_skill_output_contract": "output_contract_belongs_to_descriptor",
            "internal_skill_risk_profile": "risk_profile_belongs_to_descriptor",
            "internal_skill_gate_contract": "gate_contract_belongs_to_descriptor",
            "internal_skill_observability_contract": "observability_contract_belongs_to_descriptor",
        }
        object_links = []
        links = [(f"{object_type}_object", object_id)]
        if descriptor:
            links.append(("internal_skill_descriptor_object", descriptor.descriptor_id))
            object_links.append((object_id, descriptor.descriptor_id, relation_by_object_type[object_type]))
        self._record(
            activity,
            objects=[_object(object_type, object_id, attrs)],
            links=links,
            object_links=object_links,
            attrs={"skill_id": skill_id},
        )

    def _record(
        self,
        activity: str,
        *,
        objects: list[OCELObject],
        links: list[tuple[str, str]],
        object_links: list[tuple[str, str, str]],
        attrs: dict[str, Any],
    ) -> None:
        event = OCELEvent(
            event_id=f"evt:{uuid4()}",
            event_activity=activity,
            event_timestamp=utc_now_iso(),
            event_attrs={
                **attrs,
                "runtime_event_type": activity,
                "source_runtime": "chanta_core",
                "internal_skill_onboarding": True,
                "diagnostic_only": True,
                "skills_executed": False,
                "runtime_registered": False,
                "permission_grants_created": False,
                "tool_dispatcher_mutated": False,
                "skill_executor_mutated": False,
                "llm_called": False,
                "shell_execution_used": False,
                "network_access_used": False,
                "mcp_connection_used": False,
                "plugin_loaded": False,
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
        self.trace_service.record_session_ocel_record(OCELRecord(event=event, objects=objects, relations=relations))


def descriptor_from_dict(value: dict[str, Any]) -> InternalSkillDescriptor:
    return InternalSkillDescriptor(
        descriptor_id=str(value.get("descriptor_id") or new_internal_skill_descriptor_id()),
        skill_id=str(value.get("skill_id") or ""),
        skill_name=str(value.get("skill_name") or value.get("skill_id") or ""),
        description=str(value.get("description") or ""),
        capability_category=str(value.get("capability_category") or "read_only"),
        risk_class=str(value.get("risk_class") or "read_only"),
        invocation_modes=[str(item) for item in value.get("invocation_modes") or []],
        supported=bool(value.get("supported", True)),
        enabled_by_default=bool(value.get("enabled_by_default", False)),
        owner_module=str(value.get("owner_module") or "chanta_core.skills"),
        created_at=str(value.get("created_at") or utc_now_iso()),
        descriptor_attrs=dict(value.get("descriptor_attrs") or {}),
    )


def descriptor_from_json(raw: str) -> InternalSkillDescriptor:
    loaded = json.loads(raw)
    if not isinstance(loaded, dict):
        raise ValueError("descriptor JSON must be an object")
    descriptor_value = loaded.get("descriptor", loaded)
    if not isinstance(descriptor_value, dict):
        raise ValueError("descriptor JSON must contain an object descriptor")
    return descriptor_from_dict(descriptor_value)


def _default_category(skill_id: str) -> str:
    if skill_id in OBSERVATION_SKILL_IDS:
        return "observation"
    if skill_id in DIGESTION_SKILL_IDS:
        return "digestion"
    if "workbench" in skill_id:
        return "workbench"
    if "audit" in skill_id:
        return "audit"
    if "promotion" in skill_id:
        return "promotion"
    if "workspace" in skill_id:
        return "workspace_read"
    if "runtime" in skill_id:
        return "runtime_status"
    return "read_only"


def _default_required_fields(skill_id: str) -> list[str]:
    if skill_id == "skill:workspace_summary_from_file":
        return ["root_path", "relative_path"]
    if skill_id in {
        "skill:agent_observation_source_inspect",
        "skill:agent_trace_observe",
        "skill:external_skill_source_inspect",
        "skill:external_skill_static_digest",
    }:
        return ["root_path", "relative_path"]
    return []


def _onboarding_summary(*, status: str, skill_id: str, finding_count: int) -> str:
    return f"{status}: skill_id={skill_id}; findings={finding_count}; enabled=false."


def _object(object_type: str, object_id: str, attrs: dict[str, Any]) -> OCELObject:
    return OCELObject(
        object_id=object_id,
        object_type=object_type,
        object_attrs={
            "object_key": object_id,
            "display_name": object_id,
            **attrs,
        },
    )
