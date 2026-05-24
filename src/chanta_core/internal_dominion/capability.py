from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from chanta_core.utility.time import utc_now_iso

from chanta_core.internal_dominion.inventory import RuntimeInventoryReportService
from chanta_core.internal_dominion.mapping import (
    DOMINION_EFFECT_TYPES,
    DOMINION_OCEL_EVENT_TYPES,
    DOMINION_OCEL_OBJECT_TYPES,
    DOMINION_OCEL_RELATION_TYPES,
)


CAPABILITY_OBSERVATION_VERSION = "v0.23.2"
CAPABILITY_OBSERVATION_VERSION_NAME = "Capability Observation & Digestion for Dominion"
CAPABILITY_OBSERVATION_TRACK = "Internal Dominion Foundation"
CAPABILITY_OBSERVATION_LAYER = "internal_dominion"
CAPABILITY_OBSERVATION_SUBJECT = "capability_observation_digestion"
CAPABILITY_OBSERVATION_STATE = "dominion_capability_candidates_digested"
CAPABILITY_OBSERVATION_NEXT_STEP = "v0.23.3 Control Request & Action Candidate"

CAPABILITY_SOURCE_TYPES = {"declared_descriptor", "operator_input", "static_registry", "fixture", "unknown"}
READ_VERBS = {"observe", "list", "describe", "inspect", "status", "get", "read"}
MUTATING_VERBS = {"trigger", "start", "run", "update", "create", "assign", "approve", "reject", "prepare", "validate"}
DESTRUCTIVE_VERBS = {"delete", "remove", "destroy"}
STOP_VERBS = {"stop", "cancel"}
SECRET_KEYS = {"credential_value", "token", "secret", "password", "api_key", "private_key", "raw_secret"}


def _now() -> str:
    return utc_now_iso()


def _clean_ref(value: dict[str, Any] | None) -> dict[str, Any]:
    if not value:
        return {}
    return {str(key): item for key, item in value.items() if str(key).lower() not in SECRET_KEYS}


def _choice(value: Any, allowed: set[str], fallback: str = "unknown") -> str:
    text = str(value or fallback)
    return text if text in allowed else fallback


def _text(value: Any, fallback: str) -> str:
    text = str(value or "").strip()
    return text or fallback


@dataclass(frozen=True)
class DominionCapabilityObservationRequest:
    inventory_report_id: str | None = None
    runtime_ids: list[str] = field(default_factory=list)
    provider_ref_ids: list[str] = field(default_factory=list)
    source_type: str = "declared_descriptor"
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    include_read_only: bool = True
    include_mutating: bool = True
    include_production_impacting: bool = True
    include_unknown: bool = True
    max_capabilities: int = 1000
    strictness: str = "standard"

    def to_dict(self) -> dict[str, Any]:
        return {
            "inventory_report_id": self.inventory_report_id,
            "runtime_ids": list(self.runtime_ids),
            "provider_ref_ids": list(self.provider_ref_ids),
            "source_type": _choice(self.source_type, CAPABILITY_SOURCE_TYPES, "declared_descriptor"),
            "source_refs": [_clean_ref(item) for item in self.source_refs[: self.max_capabilities]],
            "include_read_only": self.include_read_only,
            "include_mutating": self.include_mutating,
            "include_production_impacting": self.include_production_impacting,
            "include_unknown": self.include_unknown,
            "max_capabilities": self.max_capabilities,
            "strictness": self.strictness,
        }


@dataclass(frozen=True)
class CapabilityObservationSource:
    source_id: str
    source_type: str
    source_ref: dict[str, Any]
    trusted_level: str = "unknown"
    raw_descriptor_included: bool = False
    credential_values_included: bool = False
    private_full_paths_included: bool = False
    provider_api_call_performed: bool = False
    external_runtime_touched: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {
            "source_ref": _clean_ref(self.source_ref),
            "evidence_refs": [_clean_ref(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class ExternalCapabilityDescriptor:
    descriptor_id: str
    capability_name: str
    capability_type: str
    provider_ref_id: str | None = None
    runtime_id: str | None = None
    agent_id: str | None = None
    tool_id: str | None = None
    system_id: str | None = None
    control_surface_id: str | None = None
    description: str | None = None
    declared_action_verbs: list[str] = field(default_factory=list)
    declared_input_schema_ref: dict[str, Any] | None = None
    declared_output_schema_ref: dict[str, Any] | None = None
    environment: str = "unknown"
    maturity: str = "declared"
    dispatch_supported: bool = False
    dispatch_enabled_v0_23_2: bool = False
    provider_api_call_performed: bool = False
    external_runtime_touched: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {
            "declared_input_schema_ref": _clean_ref(self.declared_input_schema_ref),
            "declared_output_schema_ref": _clean_ref(self.declared_output_schema_ref),
            "evidence_refs": [_clean_ref(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class DominionActionVerbDescriptor:
    verb_id: str
    raw_verb: str
    normalized_verb: str
    verb_category: str
    risk_class: str
    requires_control_request: bool
    requires_control_plan: bool
    requires_preflight: bool
    requires_human_gate: bool
    requires_strong_gate: bool
    forbidden_in_current_track: bool
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)


@dataclass(frozen=True)
class CapabilitySchemaDescriptor:
    schema_id: str
    capability_descriptor_id: str
    schema_kind: str
    schema_available: bool
    schema_source: str
    required_fields: list[str] = field(default_factory=list)
    optional_fields: list[str] = field(default_factory=list)
    sensitive_fields: list[str] = field(default_factory=list)
    business_object_refs: list[dict[str, Any]] = field(default_factory=list)
    raw_schema_included: bool = False
    credential_fields_present: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {
            "business_object_refs": [_clean_ref(item) for item in self.business_object_refs],
            "evidence_refs": [_clean_ref(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class CapabilityBoundaryDescriptor:
    boundary_id: str
    capability_descriptor_id: str
    environment: str
    production_impacting: bool
    credential_sensitive: bool
    mutating: bool
    destructive: bool
    external_system_touch_required: bool
    status_tracking_required: bool
    outcome_record_required: bool
    cancel_or_stop_required: bool
    idempotency_key_required: bool
    rate_limit_required: bool
    allowed_in_v0_23_2: bool = True
    dispatch_allowed_in_v0_23_2: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"evidence_refs": [_clean_ref(item) for item in self.evidence_refs]}


@dataclass(frozen=True)
class CapabilityRiskProfile:
    risk_profile_id: str
    capability_descriptor_id: str
    risk_class: str
    risk_reasons: list[str]
    requires_human_gate: bool
    requires_strong_human_gate: bool
    requires_preflight: bool
    requires_status_tracking: bool
    requires_outcome_record: bool
    forbidden_until_provider_adapter: bool
    forbidden_until_preflight: bool
    dispatch_enabled: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"evidence_refs": [_clean_ref(item) for item in self.evidence_refs]}


@dataclass(frozen=True)
class CapabilityDigestionRule:
    rule_id: str
    rule_name: str
    category: str
    description: str
    enabled: bool = True
    severity_if_failed: str = "warning"

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)


@dataclass(frozen=True)
class CapabilityDigestionResult:
    result_id: str
    descriptor_id: str
    normalized_name: str
    normalized_capability_type: str
    action_verbs: list[DominionActionVerbDescriptor]
    input_schema: CapabilitySchemaDescriptor | None
    output_schema: CapabilitySchemaDescriptor | None
    boundary: CapabilityBoundaryDescriptor
    risk_profile: CapabilityRiskProfile
    digestion_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "result_id": self.result_id,
            "descriptor_id": self.descriptor_id,
            "normalized_name": self.normalized_name,
            "normalized_capability_type": self.normalized_capability_type,
            "action_verbs": [item.to_dict() for item in self.action_verbs],
            "input_schema": self.input_schema.to_dict() if self.input_schema else None,
            "output_schema": self.output_schema.to_dict() if self.output_schema else None,
            "boundary": self.boundary.to_dict(),
            "risk_profile": self.risk_profile.to_dict(),
            "digestion_status": self.digestion_status,
            "evidence_refs": [_clean_ref(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class ExternalCapabilityCandidate:
    candidate_id: str
    descriptor_id: str
    provider_ref_id: str | None
    runtime_id: str | None
    capability_name: str
    normalized_capability_type: str
    action_verbs: list[DominionActionVerbDescriptor]
    input_schema_ref: dict[str, Any] | None
    output_schema_ref: dict[str, Any] | None
    boundary_ref: dict[str, Any]
    risk_profile_ref: dict[str, Any]
    maturity: str = "digested_candidate"
    candidate_status: str = "candidate_only"
    control_request_created: bool = False
    control_plan_created: bool = False
    preflight_checked: bool = False
    human_gate_opened: bool = False
    dispatch_enabled: bool = False
    dispatched: bool = False
    provider_api_call_performed: bool = False
    external_runtime_touched: bool = False
    credential_exposed: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {
            "action_verbs": [item.to_dict() for item in self.action_verbs],
            "input_schema_ref": _clean_ref(self.input_schema_ref),
            "output_schema_ref": _clean_ref(self.output_schema_ref),
            "boundary_ref": _clean_ref(self.boundary_ref),
            "risk_profile_ref": _clean_ref(self.risk_profile_ref),
            "evidence_refs": [_clean_ref(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class CapabilityObservationFinding:
    finding_id: str
    severity: str
    finding_type: str
    message: str
    capability_ref: dict[str, Any] | None = None
    runtime_ref: dict[str, Any] | None = None
    provider_ref: dict[str, Any] | None = None
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    withdrawal_condition: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "severity": self.severity,
            "finding_type": self.finding_type,
            "message": self.message,
            "capability_ref": _clean_ref(self.capability_ref),
            "runtime_ref": _clean_ref(self.runtime_ref),
            "provider_ref": _clean_ref(self.provider_ref),
            "evidence_refs": [_clean_ref(item) for item in self.evidence_refs],
            "withdrawal_condition": self.withdrawal_condition,
        }


@dataclass(frozen=True)
class CapabilityObservationDigestSnapshot:
    snapshot_id: str
    created_at: str
    sources: list[CapabilityObservationSource]
    descriptors: list[ExternalCapabilityDescriptor]
    digestion_results: list[CapabilityDigestionResult]
    candidates: list[ExternalCapabilityCandidate]
    findings: list[CapabilityObservationFinding]
    snapshot_status: str
    dispatch_enabled: bool = False
    external_runtime_touched: bool = False
    provider_api_call_performed: bool = False
    credential_exposed: bool = False
    raw_secret_output: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id,
            "created_at": self.created_at,
            "sources": [item.to_dict() for item in self.sources],
            "descriptors": [item.to_dict() for item in self.descriptors],
            "digestion_results": [item.to_dict() for item in self.digestion_results],
            "candidates": [item.to_dict() for item in self.candidates],
            "findings": [item.to_dict() for item in self.findings],
            "snapshot_status": self.snapshot_status,
            "dispatch_enabled": self.dispatch_enabled,
            "external_runtime_touched": self.external_runtime_touched,
            "provider_api_call_performed": self.provider_api_call_performed,
            "credential_exposed": self.credential_exposed,
            "raw_secret_output": self.raw_secret_output,
        }


@dataclass(frozen=True)
class CapabilityObservationDigestReport:
    report_id: str
    version: str
    created_at: str
    request: DominionCapabilityObservationRequest
    snapshot: CapabilityObservationDigestSnapshot
    descriptor_count: int
    candidate_count: int
    read_only_count: int
    mutating_count: int
    production_impacting_count: int
    credential_sensitive_count: int
    destructive_count: int
    unknown_count: int
    finding_count: int
    report_status: str
    next_required_step: str = CAPABILITY_OBSERVATION_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = "Valid until declared capability descriptors, inventory, provider registry, or company system landscape changes."

    def to_dict(self) -> dict[str, Any]:
        return {
            "report_id": self.report_id,
            "version": self.version,
            "created_at": self.created_at,
            "request": self.request.to_dict(),
            "snapshot": self.snapshot.to_dict(),
            "descriptor_count": self.descriptor_count,
            "candidate_count": self.candidate_count,
            "read_only_count": self.read_only_count,
            "mutating_count": self.mutating_count,
            "production_impacting_count": self.production_impacting_count,
            "credential_sensitive_count": self.credential_sensitive_count,
            "destructive_count": self.destructive_count,
            "unknown_count": self.unknown_count,
            "finding_count": self.finding_count,
            "report_status": self.report_status,
            "next_required_step": self.next_required_step,
            "limitations": list(self.limitations),
            "withdrawal_conditions": list(self.withdrawal_conditions),
            "validity_horizon": self.validity_horizon,
        }


class CapabilityObservationSourceService:
    def load_sources(self, request: DominionCapabilityObservationRequest) -> list[CapabilityObservationSource]:
        refs = request.source_refs or [_default_capability_manifest()]
        source_type = _choice(request.source_type, CAPABILITY_SOURCE_TYPES, "declared_descriptor")
        return [
            CapabilityObservationSource(
                source_id=f"capability_observation_source:{index + 1}",
                source_type=source_type,
                source_ref=_clean_ref(ref),
                trusted_level=str(ref.get("trusted_level", "unknown")),
                evidence_refs=[{"sanitized": True, "provider_api_call_performed": False}],
            )
            for index, ref in enumerate(refs[: request.max_capabilities])
        ]


class CapabilityDescriptorParser:
    def parse_sources(self, sources: list[CapabilityObservationSource]) -> list[dict[str, Any]]:
        parsed: list[dict[str, Any]] = []
        for source in sources:
            ref = source.to_dict()["source_ref"]
            if isinstance(ref.get("items"), list):
                parsed.extend(item for item in ref["items"] if isinstance(item, dict))
            elif ref:
                parsed.append(ref)
        return parsed


class ExternalCapabilityNormalizer:
    def normalize_descriptors(
        self,
        parsed_items: list[dict[str, Any]],
        inventory: Any,
    ) -> list[ExternalCapabilityDescriptor]:
        descriptors: list[ExternalCapabilityDescriptor] = []
        for item in parsed_items:
            if item.get("kind") not in {"capability", None} and "descriptor_id" not in item:
                continue
            descriptor_id = _text(item.get("descriptor_id") or item.get("id"), f"capability_descriptor:{len(descriptors) + 1}")
            descriptors.append(
                ExternalCapabilityDescriptor(
                    descriptor_id=descriptor_id,
                    capability_name=_text(item.get("capability_name") or item.get("name"), descriptor_id),
                    capability_type=_text(item.get("capability_type"), "unknown"),
                    provider_ref_id=item.get("provider_ref_id"),
                    runtime_id=item.get("runtime_id"),
                    agent_id=item.get("agent_id"),
                    tool_id=item.get("tool_id"),
                    system_id=item.get("system_id"),
                    control_surface_id=item.get("control_surface_id"),
                    description=item.get("description"),
                    declared_action_verbs=[str(verb) for verb in item.get("declared_action_verbs", [])],
                    declared_input_schema_ref=_clean_ref(item.get("declared_input_schema_ref")),
                    declared_output_schema_ref=_clean_ref(item.get("declared_output_schema_ref")),
                    environment=_text(item.get("environment"), "unknown"),
                    maturity=_text(item.get("maturity"), "declared"),
                    dispatch_supported=bool(item.get("dispatch_supported", False)),
                    dispatch_enabled_v0_23_2=bool(item.get("dispatch_enabled_v0_23_2", False)),
                    provider_api_call_performed=False,
                    external_runtime_touched=False,
                    evidence_refs=[{"declared_descriptor": True}],
                )
            )
        return descriptors


class ActionVerbNormalizer:
    def normalize_verbs(self, descriptor: ExternalCapabilityDescriptor) -> list[DominionActionVerbDescriptor]:
        verbs = descriptor.declared_action_verbs or ["unknown"]
        return [_normalize_verb(verb, descriptor.environment) for verb in verbs]


class CapabilitySchemaService:
    def build_input_schema(self, descriptor: ExternalCapabilityDescriptor) -> CapabilitySchemaDescriptor:
        return _schema(descriptor, "input", descriptor.declared_input_schema_ref)

    def build_output_schema(self, descriptor: ExternalCapabilityDescriptor) -> CapabilitySchemaDescriptor:
        return _schema(descriptor, "output", descriptor.declared_output_schema_ref)


class CapabilityBoundaryService:
    def build_boundary(
        self,
        descriptor: ExternalCapabilityDescriptor,
        action_verbs: list[DominionActionVerbDescriptor],
    ) -> CapabilityBoundaryDescriptor:
        risks = {verb.risk_class for verb in action_verbs}
        return CapabilityBoundaryDescriptor(
            boundary_id=f"capability_boundary:{descriptor.descriptor_id}",
            capability_descriptor_id=descriptor.descriptor_id,
            environment=descriptor.environment,
            production_impacting=descriptor.environment == "production" or "production_impacting" in risks,
            credential_sensitive="credential_sensitive" in risks or any("credential" in str(ref).lower() for ref in [descriptor.declared_input_schema_ref]),
            mutating=any(verb.verb_category in {"trigger", "mutate", "approve", "stop"} for verb in action_verbs),
            destructive="destructive" in risks,
            external_system_touch_required=descriptor.dispatch_supported,
            status_tracking_required=descriptor.dispatch_supported,
            outcome_record_required=True,
            cancel_or_stop_required=any(verb.verb_category == "stop" for verb in action_verbs),
            idempotency_key_required=descriptor.dispatch_supported,
            rate_limit_required=descriptor.dispatch_supported,
            dispatch_allowed_in_v0_23_2=False,
            evidence_refs=[{"risk_classes": sorted(risks)}],
        )


class CapabilityRiskClassifier:
    def classify(
        self,
        descriptor: ExternalCapabilityDescriptor,
        action_verbs: list[DominionActionVerbDescriptor],
        boundary: CapabilityBoundaryDescriptor,
    ) -> CapabilityRiskProfile:
        risk_class = _highest_risk([verb.risk_class for verb in action_verbs], boundary)
        return CapabilityRiskProfile(
            risk_profile_id=f"capability_risk:{descriptor.descriptor_id}",
            capability_descriptor_id=descriptor.descriptor_id,
            risk_class=risk_class,
            risk_reasons=[risk_class, f"environment:{descriptor.environment}"],
            requires_human_gate=risk_class not in {"read_only", "low"},
            requires_strong_human_gate=risk_class in {"production_impacting", "destructive", "credential_sensitive"},
            requires_preflight=risk_class != "read_only",
            requires_status_tracking=boundary.status_tracking_required,
            requires_outcome_record=True,
            forbidden_until_provider_adapter=descriptor.dispatch_supported,
            forbidden_until_preflight=risk_class != "read_only",
            dispatch_enabled=False,
            evidence_refs=[{"classified": True}],
        )


class CapabilityDigestionRuleRegistry:
    def list_rules(self) -> list[CapabilityDigestionRule]:
        return [
            CapabilityDigestionRule("rule:verb_normalization", "Verb normalization", "verb_normalization", "Normalize provider verbs."),
            CapabilityDigestionRule("rule:schema", "Schema metadata", "schema", "Create schema descriptors without raw schema output."),
            CapabilityDigestionRule("rule:risk", "Risk classification", "risk", "Classify before control planning."),
            CapabilityDigestionRule("rule:boundary", "Boundary classification", "boundary", "Keep dispatch disabled."),
        ]


class CapabilityDigestionService:
    def __init__(self) -> None:
        self.verb_normalizer = ActionVerbNormalizer()
        self.schema_service = CapabilitySchemaService()
        self.boundary_service = CapabilityBoundaryService()
        self.risk_classifier = CapabilityRiskClassifier()

    def digest(self, descriptor: ExternalCapabilityDescriptor) -> CapabilityDigestionResult:
        verbs = self.verb_normalizer.normalize_verbs(descriptor)
        input_schema = self.schema_service.build_input_schema(descriptor)
        output_schema = self.schema_service.build_output_schema(descriptor)
        boundary = self.boundary_service.build_boundary(descriptor, verbs)
        risk = self.risk_classifier.classify(descriptor, verbs, boundary)
        status = "warning" if descriptor.capability_type == "unknown" or any(v.risk_class == "unknown" for v in verbs) else "digested"
        if risk.risk_class in {"destructive", "credential_sensitive"}:
            status = "warning"
        return CapabilityDigestionResult(
            result_id=f"capability_digestion_result:{descriptor.descriptor_id}",
            descriptor_id=descriptor.descriptor_id,
            normalized_name=descriptor.capability_name.strip().lower().replace(" ", "_"),
            normalized_capability_type=descriptor.capability_type,
            action_verbs=verbs,
            input_schema=input_schema,
            output_schema=output_schema,
            boundary=boundary,
            risk_profile=risk,
            digestion_status=status,
            evidence_refs=[{"rules_applied": True}],
        )


class ExternalCapabilityCandidateService:
    def build_candidates(self, digestion_results: list[CapabilityDigestionResult]) -> list[ExternalCapabilityCandidate]:
        return [
            ExternalCapabilityCandidate(
                candidate_id=f"external_capability_candidate:{result.descriptor_id}",
                descriptor_id=result.descriptor_id,
                provider_ref_id=None,
                runtime_id=None,
                capability_name=result.normalized_name,
                normalized_capability_type=result.normalized_capability_type,
                action_verbs=result.action_verbs,
                input_schema_ref={"schema_id": result.input_schema.schema_id} if result.input_schema else None,
                output_schema_ref={"schema_id": result.output_schema.schema_id} if result.output_schema else None,
                boundary_ref={"boundary_id": result.boundary.boundary_id},
                risk_profile_ref={"risk_profile_id": result.risk_profile.risk_profile_id, "risk_class": result.risk_profile.risk_class},
                evidence_refs=[{"candidate_only": True}],
            )
            for result in digestion_results
        ]


class CapabilityObservationFindingService:
    def build_findings(
        self,
        sources: list[CapabilityObservationSource],
        descriptors: list[ExternalCapabilityDescriptor],
        digestion_results: list[CapabilityDigestionResult],
        candidates: list[ExternalCapabilityCandidate],
    ) -> list[CapabilityObservationFinding]:
        findings: list[CapabilityObservationFinding] = []
        if not descriptors:
            findings.append(_finding("critical", "missing_runtime_inventory"))
        for source in sources:
            if source.credential_values_included:
                findings.append(_finding("critical", "credential_value_exposure"))
        for descriptor, result in zip(descriptors, digestion_results):
            if descriptor.capability_type == "unknown":
                findings.append(_finding("warning", "unknown_capability_type", capability_ref=descriptor.to_dict()))
            if descriptor.dispatch_enabled_v0_23_2:
                findings.append(_finding("error", "dispatch_enabled_too_early", capability_ref=descriptor.to_dict()))
            if descriptor.provider_api_call_performed:
                findings.append(_finding("critical", "provider_api_call_performed", capability_ref=descriptor.to_dict()))
            if descriptor.external_runtime_touched:
                findings.append(_finding("critical", "external_runtime_touched", capability_ref=descriptor.to_dict()))
            lowered = " ".join([descriptor.capability_name, descriptor.description or ""]).lower()
            if "self_execution" in lowered:
                findings.append(_finding("error", "self_execution_legacy_detected", capability_ref=descriptor.to_dict()))
            if "growthkernel dependency" in lowered or "requires growthkernel" in lowered:
                findings.append(_finding("error", "growthkernel_dependency_detected", capability_ref=descriptor.to_dict()))
            if "vendor hardcoding" in lowered:
                findings.append(_finding("error", "vendor_hardcoding_detected", capability_ref=descriptor.to_dict()))
            for verb in result.action_verbs:
                if verb.risk_class == "unknown":
                    findings.append(_finding("warning", "unknown_action_verb", capability_ref=descriptor.to_dict()))
            if result.input_schema and not result.input_schema.schema_available:
                findings.append(_finding("warning", "input_schema_missing", capability_ref=descriptor.to_dict()))
            if result.output_schema and not result.output_schema.schema_available:
                findings.append(_finding("warning", "output_schema_missing", capability_ref=descriptor.to_dict()))
            if result.input_schema and result.input_schema.credential_fields_present:
                findings.append(_finding("warning", "credential_field_detected", capability_ref=descriptor.to_dict()))
            if result.boundary.production_impacting:
                findings.append(_finding("warning", "production_impacting_capability", capability_ref=descriptor.to_dict()))
            if result.boundary.destructive:
                findings.append(_finding("warning", "destructive_capability", capability_ref=descriptor.to_dict()))
            if result.boundary.status_tracking_required:
                findings.append(_finding("warning", "status_tracking_missing", capability_ref=descriptor.to_dict()))
            if result.boundary.outcome_record_required:
                findings.append(_finding("warning", "outcome_mapping_missing", capability_ref=descriptor.to_dict()))
            if result.risk_profile.forbidden_until_provider_adapter:
                findings.append(_finding("warning", "provider_adapter_required", capability_ref=descriptor.to_dict()))
        if not findings:
            findings.append(_finding("info", "ok"))
        return findings


class CapabilityObservationDigestReportService:
    def __init__(self) -> None:
        self.source_service = CapabilityObservationSourceService()
        self.parser = CapabilityDescriptorParser()
        self.normalizer = ExternalCapabilityNormalizer()
        self.digestion = CapabilityDigestionService()
        self.candidate_service = ExternalCapabilityCandidateService()
        self.finding_service = CapabilityObservationFindingService()
        self.inventory_reports = RuntimeInventoryReportService()

    def build_report(
        self,
        request: DominionCapabilityObservationRequest | None = None,
    ) -> CapabilityObservationDigestReport:
        request = request or DominionCapabilityObservationRequest()
        inventory = self.inventory_reports.build_report()
        sources = self.source_service.load_sources(request)
        parsed = self.parser.parse_sources(sources)
        descriptors = self.normalizer.normalize_descriptors(parsed, inventory)
        results = [self.digestion.digest(descriptor) for descriptor in descriptors]
        candidates = self.candidate_service.build_candidates(results)
        findings = self.finding_service.build_findings(sources, descriptors, results, candidates)
        snapshot = CapabilityObservationDigestSnapshot(
            snapshot_id="capability_observation_digest_snapshot:v0.23.2",
            created_at=_now(),
            sources=sources,
            descriptors=descriptors,
            digestion_results=results,
            candidates=candidates,
            findings=findings,
            snapshot_status=_status(findings),
        )
        risk_classes = [result.risk_profile.risk_class for result in results]
        return CapabilityObservationDigestReport(
            report_id="capability_observation_digest_report:v0.23.2",
            version=CAPABILITY_OBSERVATION_VERSION,
            created_at=snapshot.created_at,
            request=request,
            snapshot=snapshot,
            descriptor_count=len(descriptors),
            candidate_count=len(candidates),
            read_only_count=risk_classes.count("read_only"),
            mutating_count=sum(1 for result in results if result.boundary.mutating),
            production_impacting_count=sum(1 for result in results if result.boundary.production_impacting),
            credential_sensitive_count=risk_classes.count("credential_sensitive"),
            destructive_count=risk_classes.count("destructive"),
            unknown_count=risk_classes.count("unknown") + sum(1 for item in descriptors if item.capability_type == "unknown"),
            finding_count=len(findings),
            report_status="passed" if snapshot.snapshot_status == "observed" else snapshot.snapshot_status,
            limitations=[
                "Capability observation uses declared/static descriptors only.",
                "Capability candidates are not control requests and do not dispatch.",
            ],
            withdrawal_conditions=[
                "Withdraw if provider API discovery, runtime touch, dispatch, control request creation, or credential output is introduced.",
                "Withdraw if v0.23.x is described as Self-Execution Safety.",
            ],
        )

    def build_pig_report(self) -> dict[str, Any]:
        report = self.build_report()
        snapshot = report.snapshot
        return {
            "version": CAPABILITY_OBSERVATION_VERSION,
            "layer": CAPABILITY_OBSERVATION_LAYER,
            "subject": CAPABILITY_OBSERVATION_SUBJECT,
            "principles": [
                "capability observation is not provider API discovery",
                "capability digestion is not execution",
                "capability candidate is not control request",
                "capability candidate is not dispatch",
                "every capability must be risk-classified before control planning",
            ],
            "safety_boundary": {
                "dispatch_enabled": snapshot.dispatch_enabled,
                "control_request_created": False,
                "control_plan_created": False,
                "external_runtime_touched": snapshot.external_runtime_touched,
                "provider_api_call_performed": snapshot.provider_api_call_performed,
                "credential_exposed": snapshot.credential_exposed,
                "raw_secret_output": snapshot.raw_secret_output,
                "network_enabled": False,
                "mcp_enabled": False,
                "plugin_enabled": False,
                "shell_enabled": False,
            },
            "counts": _counts(report),
            "next_step": CAPABILITY_OBSERVATION_NEXT_STEP,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": CAPABILITY_OBSERVATION_STATE,
            "version": CAPABILITY_OBSERVATION_VERSION,
            "source_read_models": [
                "InternalDominionContractState",
                "DominionRuntimeInventoryState",
                "ExternalProviderRefState",
                "ExternalRuntimeRefState",
                "ExternalAgentRefState",
                "ExternalToolRefState",
                "ExternalSystemRefState",
                "ExternalControlSurfaceRefState",
            ],
            "target_read_models": [
                "ExternalCapabilityDescriptorState",
                "ExternalCapabilityCandidateState",
                "CapabilityRiskProfileState",
                "CapabilityBoundaryState",
                "CapabilitySchemaState",
            ],
            "effect_types": list(DOMINION_EFFECT_TYPES),
            "object_coverage": list(DOMINION_OCEL_OBJECT_TYPES),
            "event_coverage": list(DOMINION_OCEL_EVENT_TYPES),
            "relation_coverage": list(DOMINION_OCEL_RELATION_TYPES),
            "canonical_store": "ocel",
        }

    def render_report_cli(self, report: CapabilityObservationDigestReport | None = None) -> str:
        report = report or self.build_report()
        snapshot = report.snapshot
        return "\n".join(
            [
                "Dominion Capability Observation & Digestion",
                f"version={report.version}",
                f"layer={CAPABILITY_OBSERVATION_LAYER}",
                f"status={report.report_status}",
                f"descriptor_count={report.descriptor_count}",
                f"candidate_count={report.candidate_count}",
                f"read_only_count={report.read_only_count}",
                f"mutating_count={report.mutating_count}",
                f"production_impacting_count={report.production_impacting_count}",
                f"credential_sensitive_count={report.credential_sensitive_count}",
                f"destructive_count={report.destructive_count}",
                f"unknown_count={report.unknown_count}",
                f"finding_count={report.finding_count}",
                f"dispatch_enabled={str(snapshot.dispatch_enabled).lower()}",
                f"external_runtime_touched={str(snapshot.external_runtime_touched).lower()}",
                f"provider_api_call_performed={str(snapshot.provider_api_call_performed).lower()}",
                f"credential_exposed={str(snapshot.credential_exposed).lower()}",
                f"next_required_step={report.next_required_step}",
                "raw_descriptor_printed=False",
                "raw_secrets_printed=False",
                "private_full_paths_printed=False",
            ]
        )

    def render_collection_cli(self, section: str, report: CapabilityObservationDigestReport | None = None) -> str:
        report = report or self.build_report()
        items = {
            "candidates": report.snapshot.candidates,
            "descriptors": report.snapshot.descriptors,
            "risks": [item.risk_profile for item in report.snapshot.digestion_results],
            "findings": report.snapshot.findings,
        }[section]
        lines = [self.render_report_cli(report)]
        for item in items:
            payload = item.to_dict()
            item_id = payload.get("candidate_id") or payload.get("descriptor_id") or payload.get("risk_profile_id") or payload.get("finding_id")
            lines.append(f"- id={item_id}")
        return "\n".join(lines)


class DominionCapabilityObservationDigestService:
    def __init__(self, report_service: CapabilityObservationDigestReportService | None = None) -> None:
        self.report_service = report_service or CapabilityObservationDigestReportService()

    def observe_and_digest(
        self,
        request: DominionCapabilityObservationRequest | None = None,
    ) -> CapabilityObservationDigestReport:
        return self.report_service.build_report(request)


def _normalize_verb(raw_verb: str, environment: str = "unknown") -> DominionActionVerbDescriptor:
    normalized = str(raw_verb or "unknown").strip().lower() or "unknown"
    if normalized in READ_VERBS:
        category, risk = "inspect", "read_only"
    elif normalized in {"prepare", "validate"}:
        category, risk = "prepare", "low"
    elif normalized in STOP_VERBS:
        category, risk = "stop", "high"
    elif normalized in DESTRUCTIVE_VERBS:
        category, risk = "mutate", "destructive"
    elif normalized in MUTATING_VERBS:
        category, risk = ("trigger" if normalized in {"trigger", "start", "run"} else "mutate"), "high"
    else:
        category, risk = "unknown", "unknown"
    if environment == "production" and risk in {"high", "medium"}:
        risk = "production_impacting"
    requires_future_controls = risk != "read_only"
    return DominionActionVerbDescriptor(
        verb_id=f"dominion_action_verb:{normalized}",
        raw_verb=raw_verb,
        normalized_verb=normalized,
        verb_category=category,
        risk_class=risk,
        requires_control_request=True,
        requires_control_plan=requires_future_controls,
        requires_preflight=requires_future_controls,
        requires_human_gate=requires_future_controls,
        requires_strong_gate=risk in {"production_impacting", "destructive", "credential_sensitive"},
        forbidden_in_current_track=requires_future_controls,
        notes=["candidate_only", "no_dispatch"],
    )


def _schema(
    descriptor: ExternalCapabilityDescriptor,
    schema_kind: str,
    schema_ref: dict[str, Any] | None,
) -> CapabilitySchemaDescriptor:
    ref = _clean_ref(schema_ref)
    required = [str(item) for item in ref.get("required_fields", [])] if ref else []
    optional = [str(item) for item in ref.get("optional_fields", [])] if ref else []
    sensitive = [field for field in [*required, *optional] if "credential" in field.lower() or "token" in field.lower()]
    return CapabilitySchemaDescriptor(
        schema_id=f"capability_schema:{descriptor.descriptor_id}:{schema_kind}",
        capability_descriptor_id=descriptor.descriptor_id,
        schema_kind=schema_kind,
        schema_available=bool(ref),
        schema_source=str(ref.get("schema_source", "declared_descriptor" if ref else "unavailable")),
        required_fields=required,
        optional_fields=optional,
        sensitive_fields=sensitive,
        business_object_refs=[_clean_ref(item) for item in ref.get("business_object_refs", [])] if ref else [],
        credential_fields_present=bool(sensitive),
        evidence_refs=[{"metadata_only": True}],
    )


def _highest_risk(risks: list[str], boundary: CapabilityBoundaryDescriptor) -> str:
    if boundary.credential_sensitive:
        return "credential_sensitive"
    for risk in ["destructive", "production_impacting", "high", "medium", "low", "read_only", "unknown"]:
        if risk in risks:
            return risk
    return "unknown"


def _finding(
    severity: str,
    finding_type: str,
    *,
    capability_ref: dict[str, Any] | None = None,
) -> CapabilityObservationFinding:
    return CapabilityObservationFinding(
        finding_id=f"capability_observation_finding:{finding_type}",
        severity=severity,
        finding_type=finding_type,
        message=finding_type.replace("_", " "),
        capability_ref=capability_ref,
        evidence_refs=[{"policy": "v0.23.2_static_capability_observation"}],
        withdrawal_condition="Withdraw this finding if sanitized descriptor evidence changes.",
    )


def _status(findings: list[CapabilityObservationFinding]) -> str:
    severities = {item.severity for item in findings}
    if "critical" in severities:
        return "blocked"
    if "error" in severities:
        return "failed"
    if "warning" in severities:
        return "warning"
    return "observed"


def _counts(report: CapabilityObservationDigestReport) -> dict[str, int]:
    return {
        "descriptor_count": report.descriptor_count,
        "candidate_count": report.candidate_count,
        "read_only_count": report.read_only_count,
        "mutating_count": report.mutating_count,
        "production_impacting_count": report.production_impacting_count,
        "credential_sensitive_count": report.credential_sensitive_count,
        "destructive_count": report.destructive_count,
        "unknown_count": report.unknown_count,
        "finding_count": report.finding_count,
    }


def _default_capability_manifest() -> dict[str, Any]:
    return {
        "kind": "manifest",
        "items": [
            {
                "kind": "capability",
                "descriptor_id": "capability_descriptor:declared_status",
                "capability_name": "Declared status observation",
                "capability_type": "status_observation",
                "provider_ref_id": "provider:declared-local-runtime",
                "runtime_id": "runtime:declared-local",
                "control_surface_id": "surface:manual-only",
                "declared_action_verbs": ["observe", "status"],
                "declared_input_schema_ref": {"required_fields": [], "optional_fields": ["target_ref"]},
                "declared_output_schema_ref": {"required_fields": ["status"], "optional_fields": []},
                "environment": "local",
                "maturity": "declared",
                "dispatch_supported": False,
            }
        ],
    }
