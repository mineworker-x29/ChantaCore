from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import json
import re
import time
from typing import Any

from chanta_core.internal_provider.contract import (
    INTERNAL_PROVIDER_OCEL_EVENT_TYPES,
    INTERNAL_PROVIDER_OCEL_OBJECT_TYPES,
    INTERNAL_PROVIDER_OCEL_RELATION_TYPES,
)
from chanta_core.internal_provider.registry import (
    InternalProviderRegistryReportService,
)
from chanta_core.internal_provider.repository_file_provider import (
    RepositoryFileProviderSkillService,
)


PROCESS_INSPECTION_PROVIDER_VERSION = "v0.24.4"
PROCESS_INSPECTION_PROVIDER_VERSION_NAME = "OCEL / PIG / OCPX Inspection Provider"
PROCESS_INSPECTION_PROVIDER_KOREAN_NAME = "OCEL·PIG·OCPX 검사 Provider"
PROCESS_INSPECTION_PROVIDER_LAYER = "internal_provider"
PROCESS_INSPECTION_PROVIDER_STATE = "process_intelligence_state_inspected"
PROCESS_INSPECTION_PROVIDER_NEXT_STEP = "v0.24.5 Local Runtime Command Candidate Provider"
OCEL_INSPECTION_PROVIDER_ID = "ocel_inspection_provider"
PIG_INSPECTION_PROVIDER_ID = "pig_inspection_provider"
OCPX_PROJECTION_PROVIDER_ID = "ocpx_projection_provider"

PROCESS_INSPECTION_OBJECT_TYPES = [
    "process_inspection_provider_policy",
    "process_inspection_scope",
    "ocel_inspection_request",
    "ocel_type_catalog",
    "ocel_event_type_descriptor",
    "ocel_object_type_descriptor",
    "ocel_relation_type_descriptor",
    "ocel_recent_event_view",
    "ocel_object_trace_request",
    "ocel_object_trace_view",
    "pig_inspection_request",
    "pig_report_index",
    "pig_report_view",
    "pig_inspection_report",
    "ocpx_inspection_request",
    "ocpx_projection_index",
    "ocpx_projection_view",
    "ocpx_inspection_report",
    "process_state_inspection_finding",
    "process_state_inspection_report",
    "internal_provider_registry",
    "internal_provider_capability_surface",
    "execution_envelope",
    "pig_report",
    "ocpx_projection",
]

PROCESS_INSPECTION_EVENT_TYPES = [
    "process_state_inspection_requested",
    "process_inspection_policy_created",
    "process_inspection_scope_created",
    "ocel_type_catalog_created",
    "ocel_recent_events_inspected",
    "ocel_object_trace_inspected",
    "pig_report_index_created",
    "pig_report_view_created",
    "pig_inspection_report_created",
    "ocpx_projection_index_created",
    "ocpx_projection_view_created",
    "ocpx_inspection_report_created",
    "process_state_inspection_report_created",
    "process_state_inspection_warning_created",
    "process_state_inspection_blocked",
]

PROCESS_INSPECTION_RELATION_TYPES = [
    "uses_ocel_inspection_provider",
    "uses_pig_inspection_provider",
    "uses_ocpx_projection_provider",
    "uses_internal_provider_registry",
    "applies_process_inspection_policy",
    "observes_ocel_event_type",
    "observes_ocel_object_type",
    "observes_ocel_relation_type",
    "observes_recent_ocel_event",
    "observes_object_centric_trace",
    "views_pig_report",
    "views_ocpx_projection",
    "sanitizes_event_payload_preview",
    "sanitizes_pig_report_view",
    "sanitizes_ocpx_projection_view",
    "redacts_secret_like_content",
    "not_ocel_mutated",
    "not_pig_mutated",
    "not_ocpx_mutated",
    "not_projection_recomputed",
    "not_graph_recomputed",
    "not_local_command_executed",
    "not_external_runtime_touched",
    "prevents_credential_exposure",
    "prepares_local_runtime_command_candidate_provider",
    "defers_local_runtime_candidate_to_v0_24_5",
    "defers_local_runtime_execution_to_later_v0_24",
    "defers_general_agent_usability_to_v0_25",
    "visible_in_workbench_future",
    "recorded_in_envelope",
    "derived_from_internal_provider_registry",
]

PROCESS_INSPECTION_EFFECT_TYPES = [
    "read_only_observation",
    "process_state_inspected",
    "ocel_type_catalog_observed",
    "ocel_recent_events_observed",
    "ocel_object_trace_observed",
    "pig_report_viewed",
    "ocpx_projection_viewed",
    "state_candidate_created",
]

PROCESS_INSPECTION_FORBIDDEN_EFFECT_TYPES = [
    "ocel_event_appended",
    "ocel_event_written",
    "ocel_object_mutated",
    "ocel_relation_mutated",
    "pig_graph_mutated",
    "pig_graph_recomputed",
    "ocpx_projection_mutated",
    "ocpx_projection_recomputed",
    "event_log_migration_performed",
    "raw_event_payload_output",
    "raw_secret_output",
    "local_command_candidate_created",
    "local_command_executed",
    "bounded_local_command_executed",
    "unrestricted_shell_executed",
    "network_accessed",
    "package_installed",
    "destructive_command_executed",
    "external_runtime_touched",
    "external_control_dispatched",
    "credential_exposed",
    "external_provider_called",
]


def _utc_now() -> str:
    return datetime.fromtimestamp(time.time(), timezone.utc).isoformat().replace("+00:00", "Z")


def _model_dict(value: Any) -> dict[str, Any]:
    return asdict(value)


def _safe_id(value: str | None) -> str:
    text = value or "none"
    return re.sub(r"[^a-zA-Z0-9_.:-]+", "_", text)[:120] or "none"


@dataclass
class ProcessInspectionProviderPolicy:
    policy_id: str = "process_inspection_provider_policy:v0.24.4"
    version: str = PROCESS_INSPECTION_PROVIDER_VERSION
    provider_ids: list[str] = field(default_factory=lambda: [
        OCEL_INSPECTION_PROVIDER_ID,
        PIG_INSPECTION_PROVIDER_ID,
        OCPX_PROJECTION_PROVIDER_ID,
    ])
    read_only: bool = True
    ocel_mutation_enabled: bool = False
    pig_mutation_enabled: bool = False
    ocpx_mutation_enabled: bool = False
    event_append_enabled: bool = False
    projection_recompute_enabled: bool = False
    graph_recompute_enabled: bool = False
    raw_payload_output_enabled: bool = False
    secret_redaction_required: bool = True
    private_path_sanitization_required: bool = True
    max_recent_events_default: int = 200
    max_trace_events_default: int = 500
    max_report_chars_default: int = 40000
    max_projection_chars_default: int = 40000
    local_command_execution_enabled: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class ProcessInspectionScope:
    scope_id: str
    max_recent_events: int
    max_trace_events: int
    max_report_chars: int
    max_projection_chars: int
    include_ocel: bool = True
    include_pig: bool = True
    include_ocpx: bool = True
    include_recent_events: bool = True
    include_object_traces: bool = True
    include_reports: bool = True
    include_projections: bool = True
    allowed_versions: list[str] = field(default_factory=lambda: ["v0.24.0", "v0.24.1", "v0.24.2", "v0.24.3", "v0.24.4"])
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    strictness: str = "standard"

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class OCELInspectionRequest:
    request_id: str
    include_event_types: bool = True
    include_object_types: bool = True
    include_relation_types: bool = True
    include_recent_events: bool = True
    recent_event_limit: int | None = None
    event_type_filter: list[str] = field(default_factory=list)
    object_type_filter: list[str] = field(default_factory=list)
    include_payload_preview: bool = False
    include_raw_payload: bool = False
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    strictness: str = "standard"

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class OCELEventTypeDescriptor:
    event_type_id: str
    event_type: str
    display_name: str | None
    version_introduced: str | None
    source_layer: str | None
    observed_count: int | None
    last_observed_at: str | None
    schema_ref: dict[str, Any] | None
    payload_schema_available: bool
    raw_payload_output: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class OCELObjectTypeDescriptor:
    object_type_id: str
    object_type: str
    display_name: str | None
    version_introduced: str | None
    source_layer: str | None
    observed_count: int | None
    last_observed_at: str | None
    schema_ref: dict[str, Any] | None
    raw_payload_output: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class OCELRelationTypeDescriptor:
    relation_type_id: str
    relation_type: str
    source_object_type: str | None
    target_object_type: str | None
    event_type: str | None
    observed_count: int | None
    schema_ref: dict[str, Any] | None
    raw_payload_output: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class OCELTypeCatalog:
    catalog_id: str
    version: str
    event_types: list[OCELEventTypeDescriptor]
    object_types: list[OCELObjectTypeDescriptor]
    relation_types: list[OCELRelationTypeDescriptor]
    event_type_count: int
    object_type_count: int
    relation_type_count: int
    catalog_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            **_model_dict(self),
            "event_types": [item.to_dict() for item in self.event_types],
            "object_types": [item.to_dict() for item in self.object_types],
            "relation_types": [item.to_dict() for item in self.relation_types],
        }


@dataclass
class OCELRecentEventView:
    view_id: str
    events: list[dict[str, Any]]
    event_count: int
    limit_applied: int
    truncated: bool
    payload_preview_included: bool
    raw_payload_included: bool = False
    redaction_applied: bool = False
    redaction_count: int = 0
    credential_exposed: bool = False
    raw_secret_output: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class OCELObjectTraceRequest:
    object_id: str | None = None
    object_type: str | None = None
    max_events: int | None = None
    include_related_objects: bool = True
    include_event_payload_preview: bool = False
    include_raw_payload: bool = False
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    strictness: str = "standard"

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class OCELObjectTraceView:
    trace_id: str
    object_id: str | None
    object_type: str | None
    events: list[dict[str, Any]]
    related_objects: list[dict[str, Any]]
    event_count: int
    related_object_count: int
    truncated: bool
    raw_payload_included: bool = False
    redaction_applied: bool = False
    credential_exposed: bool = False
    raw_secret_output: bool = False
    trace_status: str = "missing"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class PIGInspectionRequest:
    request_id: str
    report_ids: list[str] = field(default_factory=list)
    include_index: bool = True
    include_report_summary: bool = True
    include_report_body: bool = False
    include_raw_report: bool = False
    max_report_chars: int | None = None
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    strictness: str = "standard"

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class PIGReportIndex:
    index_id: str
    reports: list[dict[str, Any]]
    report_count: int
    index_status: str
    raw_report_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class PIGReportView:
    view_id: str
    report_id: str
    version: str | None
    layer: str | None
    subject: str | None
    summary: dict[str, Any]
    body_excerpt: str | None
    raw_report_included: bool = False
    truncated: bool = False
    redaction_applied: bool = False
    credential_exposed: bool = False
    raw_secret_output: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class PIGInspectionReport:
    report_id: str
    version: str
    created_at: str
    request: PIGInspectionRequest
    index: PIGReportIndex | None
    report_views: list[PIGReportView]
    findings: list["ProcessStateInspectionFinding"]
    report_status: str
    raw_report_output: bool = False
    credential_exposed: bool = False
    raw_secret_output: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            **_model_dict(self),
            "request": self.request.to_dict(),
            "index": self.index.to_dict() if self.index else None,
            "report_views": [item.to_dict() for item in self.report_views],
            "findings": [item.to_dict() for item in self.findings],
        }


@dataclass
class OCPXInspectionRequest:
    request_id: str
    projection_ids: list[str] = field(default_factory=list)
    include_index: bool = True
    include_projection_summary: bool = True
    include_projection_body: bool = False
    include_raw_projection: bool = False
    max_projection_chars: int | None = None
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    strictness: str = "standard"

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class OCPXProjectionIndex:
    index_id: str
    projections: list[dict[str, Any]]
    projection_count: int
    index_status: str
    raw_projection_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class OCPXProjectionView:
    view_id: str
    projection_id: str
    version: str | None
    state: str | None
    source_read_models: list[str]
    target_read_models: list[str]
    effect_types: list[str]
    summary: dict[str, Any]
    body_excerpt: str | None
    raw_projection_included: bool = False
    truncated: bool = False
    redaction_applied: bool = False
    credential_exposed: bool = False
    raw_secret_output: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class OCPXInspectionReport:
    report_id: str
    version: str
    created_at: str
    request: OCPXInspectionRequest
    index: OCPXProjectionIndex | None
    projection_views: list[OCPXProjectionView]
    findings: list["ProcessStateInspectionFinding"]
    report_status: str
    raw_projection_output: bool = False
    credential_exposed: bool = False
    raw_secret_output: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            **_model_dict(self),
            "request": self.request.to_dict(),
            "index": self.index.to_dict() if self.index else None,
            "projection_views": [item.to_dict() for item in self.projection_views],
            "findings": [item.to_dict() for item in self.findings],
        }


@dataclass
class ProcessStateInspectionFinding:
    finding_id: str
    severity: str
    finding_type: str
    message: str
    subject_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class ProcessStateInspectionReport:
    report_id: str
    version: str
    created_at: str
    policy: ProcessInspectionProviderPolicy
    scope: ProcessInspectionScope
    ocel_type_catalog: OCELTypeCatalog | None
    ocel_recent_event_view: OCELRecentEventView | None
    ocel_trace_views: list[OCELObjectTraceView]
    pig_inspection_report: PIGInspectionReport | None
    ocpx_inspection_report: OCPXInspectionReport | None
    findings: list[ProcessStateInspectionFinding]
    report_status: str
    ready_for_v0_24_5: bool
    ready_for_v0_25: bool
    ocel_inspection_performed: bool
    pig_inspection_performed: bool
    ocpx_inspection_performed: bool
    event_log_mutation_performed: bool = False
    projection_mutation_performed: bool = False
    graph_recompute_performed: bool = False
    local_command_executed: bool = False
    external_provider_adapter_implemented: bool = False
    credential_exposed: bool = False
    raw_secret_output: bool = False
    raw_payload_output: bool = False
    llm_judge_used: bool = False
    next_required_step: str = PROCESS_INSPECTION_PROVIDER_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = (
        "Valid until OCEL/PIG/OCPX state, inspection policy, or provider policy changes."
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            **_model_dict(self),
            "policy": self.policy.to_dict(),
            "scope": self.scope.to_dict(),
            "ocel_type_catalog": self.ocel_type_catalog.to_dict() if self.ocel_type_catalog else None,
            "ocel_recent_event_view": self.ocel_recent_event_view.to_dict() if self.ocel_recent_event_view else None,
            "ocel_trace_views": [item.to_dict() for item in self.ocel_trace_views],
            "pig_inspection_report": self.pig_inspection_report.to_dict() if self.pig_inspection_report else None,
            "ocpx_inspection_report": self.ocpx_inspection_report.to_dict() if self.ocpx_inspection_report else None,
            "findings": [item.to_dict() for item in self.findings],
        }


class ProcessStateSanitizationService:
    _SECRET_PATTERNS = [
        re.compile(r"(?i)([a-z0-9_.-]*(password|passwd|secret|token|api[_-]?key|credential)[a-z0-9_.-]*)(\s*[:=]\s*)([^\s,'\"]+)"),
        re.compile(r"(?i)(bearer\s+)[a-z0-9._~+/=-]{12,}"),
        re.compile(r"(?i)(sk-|ghp_|xox[baprs]-)[a-z0-9_-]{8,}"),
    ]

    def redact_secret_like_content(self, text: str) -> tuple[str, int]:
        redaction_count = 0
        redacted = text
        for pattern in self._SECRET_PATTERNS:
            def replace(match: re.Match[str]) -> str:
                if len(match.groups()) >= 4:
                    return f"{match.group(1)}{match.group(3)}[REDACTED]"
                return f"{match.group(1)}[REDACTED]"

            redacted, count = pattern.subn(replace, redacted)
            redaction_count += count
        return redacted, redaction_count

    def sanitize_event_payload_preview(self, payload: Any) -> tuple[dict[str, Any], int]:
        if payload is None:
            return {}, 0
        if isinstance(payload, str):
            redacted, count = self.redact_secret_like_content(payload[:2000])
            return {"preview": redacted}, count
        if isinstance(payload, dict):
            sanitized: dict[str, Any] = {}
            total = 0
            for key, value in payload.items():
                if re.search(r"(?i)(password|passwd|secret|token|api[_-]?key|credential)", str(key)) and value:
                    sanitized[str(key)] = "[REDACTED]"
                    total += 1
                    continue
                text = json.dumps(value, ensure_ascii=False, default=str)
                redacted, count = self.redact_secret_like_content(text[:500])
                sanitized[str(key)] = redacted if count else value
                total += count
            return sanitized, total
        text = json.dumps(payload, ensure_ascii=False, default=str)
        redacted, count = self.redact_secret_like_content(text[:2000])
        return {"preview": redacted}, count

    def sanitize_report_excerpt(self, text: str, max_chars: int) -> tuple[str, bool, int]:
        excerpt = text[:max_chars]
        redacted, count = self.redact_secret_like_content(excerpt)
        return redacted, len(text) > max_chars, count

    def sanitize_projection_excerpt(self, text: str, max_chars: int) -> tuple[str, bool, int]:
        return self.sanitize_report_excerpt(text, max_chars)


class ProcessInspectionProviderContractSourceService:
    def __init__(
        self,
        ocel_events: list[dict[str, Any]] | None = None,
        pig_reports: list[dict[str, Any]] | None = None,
        ocpx_projections: list[dict[str, Any]] | None = None,
    ) -> None:
        self.ocel_events = ocel_events or []
        self.pig_reports = pig_reports or []
        self.ocpx_projections = ocpx_projections or []

    def load_internal_provider_contract(self) -> dict[str, Any]:
        return {"version": "v0.24.0", "provider_contract_available": True}

    def load_provider_registry(self) -> Any:
        return InternalProviderRegistryReportService().build_report().registry

    def _surface(self, provider_id: str) -> Any | None:
        registry = self.load_provider_registry()
        return next(
            (
                item for item in registry.capability_surfaces
                if item.provider_id.endswith(provider_id) or item.provider_type == provider_id
            ),
            None,
        )

    def load_ocel_provider_surface(self) -> Any | None:
        return self._surface(OCEL_INSPECTION_PROVIDER_ID)

    def load_pig_provider_surface(self) -> Any | None:
        return self._surface(PIG_INSPECTION_PROVIDER_ID)

    def load_ocpx_provider_surface(self) -> Any | None:
        return self._surface(OCPX_PROJECTION_PROVIDER_ID)


class ProcessInspectionProviderSkillService:
    def list_skill_contracts(self) -> list[dict[str, Any]]:
        skills = {item["skill_id"]: dict(item) for item in RepositoryFileProviderSkillService().list_skill_contracts()}
        for skill_id, scope in {
            "skill:ocel_inspection_provider_view": "implemented/read-only/bounded-inspection-only",
            "skill:pig_inspection_provider_view": "implemented/read-only/bounded-inspection-only",
            "skill:ocpx_projection_provider_view": "implemented/read-only/bounded-inspection-only",
        }.items():
            if skill_id in skills:
                skills[skill_id]["status"] = "implemented"
                skills[skill_id]["scope"] = scope
                skills[skill_id]["read_only"] = True
                skills[skill_id]["provider_invocation_enabled"] = True
                skills[skill_id]["external_provider_invocation_enabled"] = False
                skills[skill_id]["local_command_execution_enabled"] = False
        return list(skills.values())

    def build_skill_statuses(self) -> dict[str, str]:
        return {item["skill_id"]: item.get("status", "unknown") for item in self.list_skill_contracts()}


class ProcessInspectionPolicyService:
    def build_policy(self) -> ProcessInspectionProviderPolicy:
        return ProcessInspectionProviderPolicy(
            evidence_refs=[{"type": "policy", "id": "process_inspection_provider_policy:v0.24.4"}]
        )


class ProcessInspectionScopeService:
    def build_scope(self, scope: ProcessInspectionScope | None = None) -> ProcessInspectionScope:
        policy = ProcessInspectionPolicyService().build_policy()
        return scope or ProcessInspectionScope(
            scope_id="process_inspection_scope:v0.24.4:default",
            max_recent_events=policy.max_recent_events_default,
            max_trace_events=policy.max_trace_events_default,
            max_report_chars=policy.max_report_chars_default,
            max_projection_chars=policy.max_projection_chars_default,
            source_refs=[{"type": "internal_provider_registry", "version": "v0.24.1"}],
        )


class OCELTypeCatalogService:
    def __init__(self, source_service: ProcessInspectionProviderContractSourceService | None = None) -> None:
        self.source_service = source_service or ProcessInspectionProviderContractSourceService()

    def list_event_types(self) -> list[OCELEventTypeDescriptor]:
        event_counts: dict[str, int] = {}
        last_observed: dict[str, str] = {}
        for event in self.source_service.ocel_events:
            event_type = str(event.get("event_type") or event.get("event_activity") or "unknown")
            event_counts[event_type] = event_counts.get(event_type, 0) + 1
            if event.get("event_timestamp"):
                last_observed[event_type] = str(event["event_timestamp"])
        types = sorted(set(INTERNAL_PROVIDER_OCEL_EVENT_TYPES) | set(event_counts))
        return [
            OCELEventTypeDescriptor(
                event_type_id=f"ocel_event_type:{_safe_id(item)}",
                event_type=item,
                display_name=item.replace("_", " ").title(),
                version_introduced=None,
                source_layer="internal_provider" if item in INTERNAL_PROVIDER_OCEL_EVENT_TYPES else "observed_ocel",
                observed_count=event_counts.get(item),
                last_observed_at=last_observed.get(item),
                schema_ref={"type": "ocel_event_schema", "event_type": item},
                payload_schema_available=item in INTERNAL_PROVIDER_OCEL_EVENT_TYPES,
                evidence_refs=[{"type": "ocel_event_type", "id": item}],
            )
            for item in types
        ]

    def list_object_types(self) -> list[OCELObjectTypeDescriptor]:
        object_counts: dict[str, int] = {}
        for event in self.source_service.ocel_events:
            for obj in event.get("related_objects", []) if isinstance(event.get("related_objects"), list) else []:
                object_type = str(obj.get("object_type") or "unknown") if isinstance(obj, dict) else "unknown"
                object_counts[object_type] = object_counts.get(object_type, 0) + 1
        types = sorted(set(INTERNAL_PROVIDER_OCEL_OBJECT_TYPES) | set(object_counts))
        return [
            OCELObjectTypeDescriptor(
                object_type_id=f"ocel_object_type:{_safe_id(item)}",
                object_type=item,
                display_name=item.replace("_", " ").title(),
                version_introduced=None,
                source_layer="internal_provider" if item in INTERNAL_PROVIDER_OCEL_OBJECT_TYPES else "observed_ocel",
                observed_count=object_counts.get(item),
                last_observed_at=None,
                schema_ref={"type": "ocel_object_schema", "object_type": item},
                evidence_refs=[{"type": "ocel_object_type", "id": item}],
            )
            for item in types
        ]

    def list_relation_types(self) -> list[OCELRelationTypeDescriptor]:
        relation_counts: dict[str, int] = {}
        for event in self.source_service.ocel_events:
            for obj in event.get("related_objects", []) if isinstance(event.get("related_objects"), list) else []:
                qualifier = str(obj.get("qualifier") or "related") if isinstance(obj, dict) else "related"
                relation_counts[qualifier] = relation_counts.get(qualifier, 0) + 1
        types = sorted(set(INTERNAL_PROVIDER_OCEL_RELATION_TYPES) | set(relation_counts))
        return [
            OCELRelationTypeDescriptor(
                relation_type_id=f"ocel_relation_type:{_safe_id(item)}",
                relation_type=item,
                source_object_type=None,
                target_object_type=None,
                event_type=None,
                observed_count=relation_counts.get(item),
                schema_ref={"type": "ocel_relation_schema", "relation_type": item},
                evidence_refs=[{"type": "ocel_relation_type", "id": item}],
            )
            for item in types
        ]

    def build_catalog(self) -> OCELTypeCatalog:
        event_types = self.list_event_types()
        object_types = self.list_object_types()
        relation_types = self.list_relation_types()
        status = "observed" if event_types and object_types and relation_types else "missing"
        return OCELTypeCatalog(
            catalog_id="ocel_type_catalog:v0.24.4",
            version=PROCESS_INSPECTION_PROVIDER_VERSION,
            event_types=event_types,
            object_types=object_types,
            relation_types=relation_types,
            event_type_count=len(event_types),
            object_type_count=len(object_types),
            relation_type_count=len(relation_types),
            catalog_status=status,
            evidence_refs=[{"type": "ocel_mapping", "source": "internal_provider_constants"}],
        )


class OCELRecentEventInspectionService:
    def __init__(
        self,
        source_service: ProcessInspectionProviderContractSourceService | None = None,
        sanitizer: ProcessStateSanitizationService | None = None,
    ) -> None:
        self.source_service = source_service or ProcessInspectionProviderContractSourceService()
        self.sanitizer = sanitizer or ProcessStateSanitizationService()

    def inspect_recent_events(self, request: OCELInspectionRequest, policy: ProcessInspectionProviderPolicy) -> OCELRecentEventView:
        limit = min(request.recent_event_limit or policy.max_recent_events_default, policy.max_recent_events_default)
        selected = self.source_service.ocel_events[:limit]
        rendered: list[dict[str, Any]] = []
        redactions = 0
        for event in selected:
            item = {
                "event_id": event.get("event_id"),
                "event_type": event.get("event_type") or event.get("event_activity"),
                "event_timestamp": event.get("event_timestamp"),
            }
            if request.include_payload_preview:
                preview, count = self.sanitizer.sanitize_event_payload_preview(event.get("event_attrs") or event.get("payload"))
                item["payload_preview"] = preview
                redactions += count
            rendered.append(item)
        return OCELRecentEventView(
            view_id="ocel_recent_event_view:v0.24.4",
            events=rendered,
            event_count=len(rendered),
            limit_applied=limit,
            truncated=len(self.source_service.ocel_events) > limit,
            payload_preview_included=request.include_payload_preview,
            redaction_applied=redactions > 0,
            redaction_count=redactions,
            evidence_refs=[{"type": "ocel_recent_events", "bounded": True}],
        )


class OCELObjectTraceInspectionService:
    def __init__(
        self,
        source_service: ProcessInspectionProviderContractSourceService | None = None,
        sanitizer: ProcessStateSanitizationService | None = None,
    ) -> None:
        self.source_service = source_service or ProcessInspectionProviderContractSourceService()
        self.sanitizer = sanitizer or ProcessStateSanitizationService()

    def inspect_object_trace(self, request: OCELObjectTraceRequest, policy: ProcessInspectionProviderPolicy) -> OCELObjectTraceView:
        max_events = min(request.max_events or policy.max_trace_events_default, policy.max_trace_events_default)
        matched: list[dict[str, Any]] = []
        related_objects: dict[str, dict[str, Any]] = {}
        redacted = False
        for event in self.source_service.ocel_events:
            event_objects = event.get("related_objects", []) if isinstance(event.get("related_objects"), list) else []
            if request.object_id and not any(isinstance(obj, dict) and obj.get("object_id") == request.object_id for obj in event_objects):
                continue
            if request.object_type and not any(isinstance(obj, dict) and obj.get("object_type") == request.object_type for obj in event_objects):
                continue
            item = {
                "event_id": event.get("event_id"),
                "event_type": event.get("event_type") or event.get("event_activity"),
                "event_timestamp": event.get("event_timestamp"),
            }
            if request.include_event_payload_preview:
                preview, count = self.sanitizer.sanitize_event_payload_preview(event.get("event_attrs") or event.get("payload"))
                item["payload_preview"] = preview
                redacted = redacted or count > 0
            matched.append(item)
            for obj in event_objects:
                if isinstance(obj, dict) and obj.get("object_id"):
                    related_objects[str(obj["object_id"])] = {
                        "object_id": obj.get("object_id"),
                        "object_type": obj.get("object_type"),
                    }
            if len(matched) >= max_events:
                break
        status = "observed" if matched else "missing"
        return OCELObjectTraceView(
            trace_id=f"ocel_object_trace_view:{_safe_id(request.object_id or request.object_type)}",
            object_id=request.object_id,
            object_type=request.object_type,
            events=matched,
            related_objects=list(related_objects.values()) if request.include_related_objects else [],
            event_count=len(matched),
            related_object_count=len(related_objects) if request.include_related_objects else 0,
            truncated=len(matched) >= max_events,
            redaction_applied=redacted,
            trace_status=status,
            evidence_refs=[{"type": "ocel_object_trace", "bounded": True}],
        )


class PIGInspectionService:
    def __init__(
        self,
        source_service: ProcessInspectionProviderContractSourceService | None = None,
        sanitizer: ProcessStateSanitizationService | None = None,
    ) -> None:
        self.source_service = source_service or ProcessInspectionProviderContractSourceService()
        self.sanitizer = sanitizer or ProcessStateSanitizationService()

    def list_pig_reports(self, request: PIGInspectionRequest, policy: ProcessInspectionProviderPolicy) -> PIGReportIndex:
        reports = [
            {
                "report_id": item.get("report_id"),
                "version": item.get("version"),
                "layer": item.get("layer"),
                "subject": item.get("subject"),
            }
            for item in self.source_service.pig_reports
        ]
        return PIGReportIndex(
            index_id="pig_report_index:v0.24.4",
            reports=reports,
            report_count=len(reports),
            index_status="observed" if reports else "missing",
            evidence_refs=[{"type": "pig_report_source", "count": len(reports)}],
        )

    def view_pig_report(self, request: PIGInspectionRequest, policy: ProcessInspectionProviderPolicy) -> list[PIGReportView]:
        max_chars = request.max_report_chars or policy.max_report_chars_default
        selected = self.source_service.pig_reports
        if request.report_ids:
            selected = [item for item in selected if str(item.get("report_id")) in set(request.report_ids)]
        views: list[PIGReportView] = []
        for item in selected:
            body = json.dumps(item, ensure_ascii=False, sort_keys=True)
            excerpt, truncated, redactions = self.sanitizer.sanitize_report_excerpt(body, max_chars)
            views.append(
                PIGReportView(
                    view_id=f"pig_report_view:{_safe_id(str(item.get('report_id')))}",
                    report_id=str(item.get("report_id") or "unknown"),
                    version=item.get("version"),
                    layer=item.get("layer"),
                    subject=item.get("subject"),
                    summary={key: item.get(key) for key in ["version", "layer", "subject", "report_status"] if key in item},
                    body_excerpt=excerpt if request.include_report_body else None,
                    truncated=truncated,
                    redaction_applied=redactions > 0,
                    evidence_refs=[{"type": "pig_report", "id": str(item.get("report_id") or "unknown")}],
                )
            )
        return views

    def build_report(self, request: PIGInspectionRequest, policy: ProcessInspectionProviderPolicy) -> PIGInspectionReport:
        index = self.list_pig_reports(request, policy) if request.include_index else None
        views = self.view_pig_report(request, policy) if request.include_report_summary or request.include_report_body else []
        findings = []
        if index and index.report_count == 0:
            findings.append(_finding("warning" if request.strictness != "strict" else "error", "missing_pig_reports", "No existing PIG reports were available.", None))
        if request.include_raw_report:
            findings.append(_finding("critical", "raw_report_output_blocked", "Raw PIG report output is blocked.", None))
        status = _status_from_findings(findings)
        return PIGInspectionReport(
            report_id="pig_inspection_report:v0.24.4",
            version=PROCESS_INSPECTION_PROVIDER_VERSION,
            created_at=_utc_now(),
            request=request,
            index=index,
            report_views=views,
            findings=findings,
            report_status=status,
        )


class OCPXInspectionService:
    def __init__(
        self,
        source_service: ProcessInspectionProviderContractSourceService | None = None,
        sanitizer: ProcessStateSanitizationService | None = None,
    ) -> None:
        self.source_service = source_service or ProcessInspectionProviderContractSourceService()
        self.sanitizer = sanitizer or ProcessStateSanitizationService()

    def list_ocpx_projections(self, request: OCPXInspectionRequest, policy: ProcessInspectionProviderPolicy) -> OCPXProjectionIndex:
        projections = [
            {
                "projection_id": item.get("projection_id") or item.get("view_id") or item.get("state"),
                "version": item.get("version"),
                "state": item.get("state"),
            }
            for item in self.source_service.ocpx_projections
        ]
        return OCPXProjectionIndex(
            index_id="ocpx_projection_index:v0.24.4",
            projections=projections,
            projection_count=len(projections),
            index_status="observed" if projections else "missing",
            evidence_refs=[{"type": "ocpx_projection_source", "count": len(projections)}],
        )

    def view_ocpx_projection(self, request: OCPXInspectionRequest, policy: ProcessInspectionProviderPolicy) -> list[OCPXProjectionView]:
        max_chars = request.max_projection_chars or policy.max_projection_chars_default
        selected = self.source_service.ocpx_projections
        if request.projection_ids:
            selected = [item for item in selected if str(item.get("projection_id") or item.get("view_id") or item.get("state")) in set(request.projection_ids)]
        views: list[OCPXProjectionView] = []
        for item in selected:
            body = json.dumps(item, ensure_ascii=False, sort_keys=True)
            excerpt, truncated, redactions = self.sanitizer.sanitize_projection_excerpt(body, max_chars)
            projection_id = str(item.get("projection_id") or item.get("view_id") or item.get("state") or "unknown")
            views.append(
                OCPXProjectionView(
                    view_id=f"ocpx_projection_view:{_safe_id(projection_id)}",
                    projection_id=projection_id,
                    version=item.get("version"),
                    state=item.get("state"),
                    source_read_models=list(item.get("source_read_models") or []),
                    target_read_models=list(item.get("target_read_models") or []),
                    effect_types=list(item.get("effect_types") or []),
                    summary={key: item.get(key) for key in ["version", "state"] if key in item},
                    body_excerpt=excerpt if request.include_projection_body else None,
                    truncated=truncated,
                    redaction_applied=redactions > 0,
                    evidence_refs=[{"type": "ocpx_projection", "id": projection_id}],
                )
            )
        return views

    def build_report(self, request: OCPXInspectionRequest, policy: ProcessInspectionProviderPolicy) -> OCPXInspectionReport:
        index = self.list_ocpx_projections(request, policy) if request.include_index else None
        views = self.view_ocpx_projection(request, policy) if request.include_projection_summary or request.include_projection_body else []
        findings = []
        if index and index.projection_count == 0:
            findings.append(_finding("warning" if request.strictness != "strict" else "error", "missing_ocpx_projections", "No existing OCPX projections were available.", None))
        if request.include_raw_projection:
            findings.append(_finding("critical", "raw_projection_output_blocked", "Raw OCPX projection output is blocked.", None))
        status = _status_from_findings(findings)
        return OCPXInspectionReport(
            report_id="ocpx_inspection_report:v0.24.4",
            version=PROCESS_INSPECTION_PROVIDER_VERSION,
            created_at=_utc_now(),
            request=request,
            index=index,
            projection_views=views,
            findings=findings,
            report_status=status,
        )


class ProcessStateInspectionFindingService:
    _MARKER_FINDINGS = {
        "missing_ocel_state": ("warning", "missing_ocel_state", "No OCEL state source is available."),
        "missing_ocel_event_type_registry": ("warning", "missing_ocel_event_type_registry", "OCEL event type registry is missing."),
        "missing_ocel_object_type_registry": ("warning", "missing_ocel_object_type_registry", "OCEL object type registry is missing."),
        "missing_ocel_relation_type_registry": ("warning", "missing_ocel_relation_type_registry", "OCEL relation type registry is missing."),
        "missing_pig_reports": ("warning", "missing_pig_reports", "No PIG report source is available."),
        "missing_ocpx_projections": ("warning", "missing_ocpx_projections", "No OCPX projection source is available."),
        "recent_event_limit": ("warning", "recent_event_limit_exceeded", "Recent event view was truncated by policy."),
        "object_trace_limit": ("warning", "object_trace_limit_exceeded", "Object trace view was truncated by policy."),
        "raw_payload_requested": ("error", "raw_payload_requested", "Raw payload was requested and blocked."),
        "raw_payload_output": ("critical", "raw_payload_output_blocked", "Raw payload output is blocked."),
        "raw_report_output": ("critical", "raw_report_output_blocked", "Raw report output is blocked."),
        "raw_projection_output": ("critical", "raw_projection_output_blocked", "Raw projection output is blocked."),
        "credential_exposure": ("critical", "credential_exposure_detected", "Credential exposure is blocked."),
        "raw_secret_output": ("critical", "raw_secret_output_detected", "Raw secret output is blocked."),
        "event_log_mutation": ("critical", "event_log_mutation_attempted", "Event log mutation is blocked."),
        "ocel_event_append": ("critical", "ocel_event_append_attempted", "OCEL event append is blocked."),
        "ocel_object_mutation": ("critical", "ocel_object_mutation_attempted", "OCEL object mutation is blocked."),
        "ocel_relation_mutation": ("critical", "ocel_relation_mutation_attempted", "OCEL relation mutation is blocked."),
        "pig_graph_mutation": ("critical", "pig_graph_mutation_attempted", "PIG graph mutation is blocked."),
        "pig_recompute": ("critical", "pig_recompute_attempted", "PIG recomputation is blocked."),
        "ocpx_projection_mutation": ("critical", "ocpx_projection_mutation_attempted", "OCPX projection mutation is blocked."),
        "ocpx_recompute": ("critical", "ocpx_recompute_attempted", "OCPX recomputation is blocked."),
        "local_command_execution": ("critical", "local_command_execution_attempted", "Local command execution is blocked."),
        "provider_api_call": ("critical", "provider_api_call_performed", "Provider API calls are blocked."),
        "external_runtime_touched": ("critical", "external_runtime_touched", "External runtime touch is blocked."),
        "vendor_hardcoding": ("critical", "vendor_hardcoding_detected", "Vendor-specific runtime logic is blocked."),
        "growthkernel_dependency": ("critical", "growthkernel_dependency_detected", "GrowthKernel active dependency is blocked."),
        "schumpeter_split": ("critical", "schumpeter_split_detected", "Schumpeter split is blocked."),
        "general_agent_usability": ("error", "general_agent_usability_premature", "General Agent UX remains deferred."),
        "llm_judge": ("critical", "llm_judge_detected", "LLM judge use is blocked."),
    }

    def build_findings(
        self,
        catalog: OCELTypeCatalog | None = None,
        recent_events: OCELRecentEventView | None = None,
        traces: list[OCELObjectTraceView] | None = None,
        pig_report: PIGInspectionReport | None = None,
        ocpx_report: OCPXInspectionReport | None = None,
        markers: list[str] | None = None,
    ) -> list[ProcessStateInspectionFinding]:
        findings: list[ProcessStateInspectionFinding] = []
        for marker in markers or []:
            if marker in self._MARKER_FINDINGS:
                severity, finding_type, message = self._MARKER_FINDINGS[marker]
                findings.append(_finding(severity, finding_type, message, None))
        if catalog and catalog.catalog_status == "missing":
            findings.append(_finding("warning", "missing_ocel_state", "No OCEL catalog source is available.", None))
        if recent_events and recent_events.truncated:
            findings.append(_finding("warning", "recent_event_limit_exceeded", "Recent events were truncated by policy.", None))
        for trace in traces or []:
            if trace.truncated:
                findings.append(_finding("warning", "object_trace_limit_exceeded", "Object trace was truncated by policy.", None))
        if pig_report:
            findings.extend(pig_report.findings)
        if ocpx_report:
            findings.extend(ocpx_report.findings)
        if not findings:
            findings.append(_finding("info", "ok", "Process state inspection completed under read-only policy.", None))
        return findings


class ProcessStateInspectionReportService:
    def __init__(
        self,
        source_service: ProcessInspectionProviderContractSourceService | None = None,
        policy_service: ProcessInspectionPolicyService | None = None,
        scope_service: ProcessInspectionScopeService | None = None,
        sanitizer: ProcessStateSanitizationService | None = None,
        finding_service: ProcessStateInspectionFindingService | None = None,
    ) -> None:
        self.source_service = source_service or ProcessInspectionProviderContractSourceService()
        self.policy_service = policy_service or ProcessInspectionPolicyService()
        self.scope_service = scope_service or ProcessInspectionScopeService()
        self.sanitizer = sanitizer or ProcessStateSanitizationService()
        self.finding_service = finding_service or ProcessStateInspectionFindingService()

    def build_report(
        self,
        scope: ProcessInspectionScope | None = None,
        ocel_request: OCELInspectionRequest | None = None,
        trace_requests: list[OCELObjectTraceRequest] | None = None,
        pig_request: PIGInspectionRequest | None = None,
        ocpx_request: OCPXInspectionRequest | None = None,
        markers: list[str] | None = None,
    ) -> ProcessStateInspectionReport:
        policy = self.policy_service.build_policy()
        scope = self.scope_service.build_scope(scope)
        catalog = OCELTypeCatalogService(self.source_service).build_catalog() if scope.include_ocel else None
        ocel_request = ocel_request or OCELInspectionRequest(request_id="ocel_inspection_request:v0.24.4")
        recent = OCELRecentEventInspectionService(self.source_service, self.sanitizer).inspect_recent_events(ocel_request, policy) if scope.include_recent_events else None
        traces = [
            OCELObjectTraceInspectionService(self.source_service, self.sanitizer).inspect_object_trace(request, policy)
            for request in (trace_requests or [])
        ]
        pig_request = pig_request or PIGInspectionRequest(request_id="pig_inspection_request:v0.24.4")
        pig_report = PIGInspectionService(self.source_service, self.sanitizer).build_report(pig_request, policy) if scope.include_pig else None
        ocpx_request = ocpx_request or OCPXInspectionRequest(request_id="ocpx_inspection_request:v0.24.4")
        ocpx_report = OCPXInspectionService(self.source_service, self.sanitizer).build_report(ocpx_request, policy) if scope.include_ocpx else None
        findings = self.finding_service.build_findings(catalog, recent, traces, pig_report, ocpx_report, markers)
        if ocel_request.include_raw_payload:
            findings.append(_finding("error", "raw_payload_requested", "Raw OCEL payload output was requested and blocked.", None))
            findings.append(_finding("critical", "raw_payload_output_blocked", "Raw OCEL payload output is blocked.", None))
        for provider_id, loader in {
            OCEL_INSPECTION_PROVIDER_ID: self.source_service.load_ocel_provider_surface,
            PIG_INSPECTION_PROVIDER_ID: self.source_service.load_pig_provider_surface,
            OCPX_PROJECTION_PROVIDER_ID: self.source_service.load_ocpx_provider_surface,
        }.items():
            if loader() is None:
                findings.append(_finding("error" if scope.strictness == "strict" else "warning", "missing_ocel_state", f"Provider surface missing: {provider_id}.", None))
        status = _status_from_findings(findings)
        return ProcessStateInspectionReport(
            report_id="process_state_inspection_report:v0.24.4",
            version=PROCESS_INSPECTION_PROVIDER_VERSION,
            created_at=_utc_now(),
            policy=policy,
            scope=scope,
            ocel_type_catalog=catalog,
            ocel_recent_event_view=recent,
            ocel_trace_views=traces,
            pig_inspection_report=pig_report,
            ocpx_inspection_report=ocpx_report,
            findings=findings,
            report_status=status,
            ready_for_v0_24_5=status in {"passed", "warning"},
            ready_for_v0_25=False,
            ocel_inspection_performed=catalog is not None or recent is not None or bool(traces),
            pig_inspection_performed=pig_report is not None,
            ocpx_inspection_performed=ocpx_report is not None,
            limitations=[
                "Inspection is read-only and bounded; missing process state sources are represented as findings.",
                "Raw payload, raw report, and raw projection output are disabled by default.",
            ],
            withdrawal_conditions=[
                "Withdraw if OCEL/PIG/OCPX mutation, graph/projection recomputation, raw payload/secret output, local command execution, external adapter calls, private material, or LLM judge behavior appears.",
            ],
        )

    def build_pig_report(self) -> dict[str, Any]:
        return {
            "version": PROCESS_INSPECTION_PROVIDER_VERSION,
            "layer": PROCESS_INSPECTION_PROVIDER_LAYER,
            "subject": "ocel_pig_ocpx_inspection_provider",
            "principles": [
                "process inspection is read-only",
                "OCEL inspection is not event log mutation",
                "PIG inspection is not graph recomputation",
                "OCPX inspection is not projection mutation",
                "recent event view is bounded",
                "object trace view is bounded",
                "payloads must be sanitized before output",
            ],
            "safety_boundary": {
                "ocel_inspection_performed": "conditional",
                "pig_inspection_performed": "conditional",
                "ocpx_inspection_performed": "conditional",
                "event_log_mutation_performed": False,
                "projection_mutation_performed": False,
                "graph_recompute_performed": False,
                "local_command_executed": False,
                "external_runtime_touched": False,
                "provider_api_call_performed": False,
                "credential_exposed": False,
                "raw_secret_output": False,
                "raw_payload_output": False,
                "external_provider_adapter_implemented": False,
                "schumpeter_split_introduced": False,
                "llm_judge_enabled": False,
            },
            "next_step": PROCESS_INSPECTION_PROVIDER_NEXT_STEP,
            "roadmap": {
                "v0.24": "Internal Provider / Local Runtime Provider",
                "v0.25": "General Agent Usability & Tool Routing",
                "v0.26": "Workspace Agent Workbench",
                "v0.27": "Memory Candidate & Continuity",
                "v0.28": "Public Alpha / Schumpeter Split Preparation",
                "v0.29+": "External Skill / External Provider Adapters",
            },
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": PROCESS_INSPECTION_PROVIDER_STATE,
            "version": PROCESS_INSPECTION_PROVIDER_VERSION,
            "source_read_models": [
                "InternalProviderRegistryState",
                "InternalProviderCapabilitySurfaceState",
                "WorkspaceReadProviderState",
                "RepositorySearchProviderState",
                "FileReadProviderState",
                "InternalDominionReleaseState",
            ],
            "target_read_models": [
                "OCELInspectionProviderState",
                "OCELTypeCatalogState",
                "OCELRecentEventViewState",
                "OCELObjectTraceViewState",
                "PIGInspectionProviderState",
                "OCPXInspectionProviderState",
                "ProcessStateInspectionState",
                "V024ReadinessState",
            ],
            "effect_types": list(PROCESS_INSPECTION_EFFECT_TYPES),
        }

    def render_report_cli(self, report: ProcessStateInspectionReport, section: str = "report", provider: str = "process_inspection_provider") -> str:
        common = [
            f"version={report.version}",
            f"provider={provider}",
            "read_only=true",
            f"report_status={report.report_status}",
            f"ocel_inspection_performed={str(report.ocel_inspection_performed).lower()}",
            f"pig_inspection_performed={str(report.pig_inspection_performed).lower()}",
            f"ocpx_inspection_performed={str(report.ocpx_inspection_performed).lower()}",
            f"event_log_mutation_performed={str(report.event_log_mutation_performed).lower()}",
            f"projection_mutation_performed={str(report.projection_mutation_performed).lower()}",
            f"graph_recompute_performed={str(report.graph_recompute_performed).lower()}",
            f"local_command_executed={str(report.local_command_executed).lower()}",
            "external_runtime_touched=false",
            f"credential_exposed={str(report.credential_exposed).lower()}",
            f"raw_secret_output={str(report.raw_secret_output).lower()}",
            f"raw_payload_output={str(report.raw_payload_output).lower()}",
            f"ready_for_v0_24_5={str(report.ready_for_v0_24_5).lower()}",
            f"ready_for_v0_25={str(report.ready_for_v0_25).lower()}",
            f"next_required_step={report.next_required_step}",
        ]
        if section == "ocel_types" and report.ocel_type_catalog:
            return "\n".join(["Process OCEL Type Catalog", *common, f"event_type_count={report.ocel_type_catalog.event_type_count}", f"object_type_count={report.ocel_type_catalog.object_type_count}", f"relation_type_count={report.ocel_type_catalog.relation_type_count}"])
        if section == "ocel_events" and report.ocel_recent_event_view:
            lines = [f"- {item.get('event_id')}:{item.get('event_type')}" for item in report.ocel_recent_event_view.events[:20]]
            return "\n".join(["Process OCEL Recent Events", *common, f"event_count={report.ocel_recent_event_view.event_count}", *lines])
        if section == "ocel_trace":
            trace = report.ocel_trace_views[0] if report.ocel_trace_views else None
            return "\n".join(["Process OCEL Object Trace", *common, f"event_count={(trace.event_count if trace else 0)}", f"trace_status={(trace.trace_status if trace else 'missing')}"])
        if section == "pig_list":
            index = report.pig_inspection_report.index if report.pig_inspection_report else None
            return "\n".join(["Process PIG Report Index", *common, f"report_count={(index.report_count if index else 0)}"])
        if section == "pig_view":
            views = report.pig_inspection_report.report_views if report.pig_inspection_report else []
            return "\n".join(["Process PIG Report View", *common, *[f"- {item.report_id}:{item.subject}" for item in views[:20]]])
        if section == "ocpx_list":
            index = report.ocpx_inspection_report.index if report.ocpx_inspection_report else None
            return "\n".join(["Process OCPX Projection Index", *common, f"projection_count={(index.projection_count if index else 0)}"])
        if section == "ocpx_view":
            views = report.ocpx_inspection_report.projection_views if report.ocpx_inspection_report else []
            return "\n".join(["Process OCPX Projection View", *common, *[f"- {item.projection_id}:{item.state}" for item in views[:20]]])
        if section == "findings":
            return "\n".join(["Process State Inspection Findings", *common, *[f"- {item.severity}:{item.finding_type}:{item.message}" for item in report.findings]])
        return "\n".join(["Process State Inspection Report", *common, f"finding_count={len(report.findings)}"])


class ProcessStateInspectionProviderService:
    def __init__(self, report_service: ProcessStateInspectionReportService | None = None) -> None:
        self.report_service = report_service or ProcessStateInspectionReportService()

    def inspect_process_state(self, scope: ProcessInspectionScope | None = None) -> ProcessStateInspectionReport:
        return self.report_service.build_report(scope)


def _finding(
    severity: str,
    finding_type: str,
    message: str,
    subject_ref: dict[str, Any] | None,
) -> ProcessStateInspectionFinding:
    return ProcessStateInspectionFinding(
        finding_id=f"process_state_inspection_finding:{finding_type}",
        severity=severity,
        finding_type=finding_type,
        message=message,
        subject_ref=subject_ref,
        evidence_refs=[{"type": "process_state_inspection", "version": PROCESS_INSPECTION_PROVIDER_VERSION}],
        withdrawal_condition="Withdraw if the boundary condition is no longer true.",
    )


def _status_from_findings(findings: list[ProcessStateInspectionFinding]) -> str:
    if any(item.severity == "critical" for item in findings):
        return "blocked"
    if any(item.severity == "error" for item in findings):
        return "failed"
    if any(item.severity == "warning" for item in findings):
        return "warning"
    return "passed"
