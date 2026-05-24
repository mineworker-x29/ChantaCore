from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from chanta_core.utility.time import utc_now_iso

from chanta_core.internal_dominion.mapping import (
    DOMINION_EFFECT_TYPES,
    DOMINION_OCEL_EVENT_TYPES,
    DOMINION_OCEL_OBJECT_TYPES,
    DOMINION_OCEL_RELATION_TYPES,
)


RUNTIME_INVENTORY_VERSION = "v0.23.1"
RUNTIME_INVENTORY_VERSION_NAME = "Runtime / Agent / System Inventory"
RUNTIME_INVENTORY_TRACK = "Internal Dominion Foundation"
RUNTIME_INVENTORY_LAYER = "internal_dominion"
RUNTIME_INVENTORY_SUBJECT = "runtime_agent_system_inventory"
RUNTIME_INVENTORY_STATE = "dominion_runtime_inventory_declared"
RUNTIME_INVENTORY_NEXT_STEP = "v0.23.2 Capability Observation & Digestion for Dominion"

INVENTORY_SOURCE_TYPES = {"declared_manifest", "operator_input", "static_registry", "fixture", "unknown"}
PROVIDER_TYPES = {
    "local_runtime",
    "rpa_runtime",
    "agent_runtime",
    "workflow_engine",
    "browser_automation",
    "enterprise_api",
    "database_or_etl",
    "custom_system",
    "unknown",
}
AGENT_TYPES = {"coding_agent", "workflow_agent", "browser_agent", "chat_agent", "custom_agent", "unknown"}
TOOL_TYPES = {"rpa_tool", "cli_tool", "api_tool", "browser_tool", "workflow_tool", "database_tool", "unknown"}
SYSTEM_TYPES = {
    "business_app",
    "erp",
    "mes",
    "groupware",
    "ticketing",
    "document",
    "data_platform",
    "workflow",
    "unknown",
}
CONTROL_SURFACE_TYPES = {
    "cli",
    "api",
    "sdk",
    "control_room",
    "queue",
    "scheduler",
    "agent_endpoint",
    "browser_session",
    "webhook",
    "database_connection",
    "workflow_console",
    "manual_only",
    "unknown",
}
ENVIRONMENTS = {"local", "dev", "test", "staging", "production", "sandbox", "unknown"}
SECRET_KEYS = {
    "credential_value",
    "token",
    "secret",
    "password",
    "api_key",
    "private_key",
    "raw_secret",
    "raw_content",
    "private_full_path",
    "full_path",
}


def _now() -> str:
    return utc_now_iso()


def _safe_text(value: Any, fallback: str) -> str:
    text = str(value or "").strip()
    return text or fallback


def _normalize_choice(value: Any, allowed: set[str], fallback: str = "unknown") -> str:
    text = str(value or fallback).strip()
    return text if text in allowed else fallback


def _sanitize_ref(value: dict[str, Any] | None) -> dict[str, Any]:
    if not value:
        return {}
    sanitized: dict[str, Any] = {}
    for key, item in value.items():
        key_text = str(key)
        if key_text.lower() in SECRET_KEYS:
            continue
        if isinstance(item, dict):
            sanitized[key_text] = _sanitize_ref(item)
        elif isinstance(item, list):
            sanitized[key_text] = [
                _sanitize_ref(entry) if isinstance(entry, dict) else entry
                for entry in item
                if str(entry).strip()
            ]
        else:
            sanitized[key_text] = item
    return sanitized


@dataclass(frozen=True)
class DominionRuntimeInventoryRequest:
    source_type: str = "declared_manifest"
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    include_local_runtime: bool = True
    include_rpa_runtime: bool = True
    include_agent_runtime: bool = True
    include_workflow_engine: bool = True
    include_enterprise_api: bool = True
    include_business_system: bool = True
    include_unknown: bool = True
    max_items: int = 500
    strictness: str = "standard"

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_type": _normalize_choice(self.source_type, INVENTORY_SOURCE_TYPES),
            "source_refs": [_sanitize_ref(item) for item in self.source_refs[: self.max_items]],
            "include_local_runtime": self.include_local_runtime,
            "include_rpa_runtime": self.include_rpa_runtime,
            "include_agent_runtime": self.include_agent_runtime,
            "include_workflow_engine": self.include_workflow_engine,
            "include_enterprise_api": self.include_enterprise_api,
            "include_business_system": self.include_business_system,
            "include_unknown": self.include_unknown,
            "max_items": self.max_items,
            "strictness": self.strictness,
        }


@dataclass(frozen=True)
class DominionInventorySource:
    source_id: str
    source_type: str
    source_ref: dict[str, Any]
    trusted_level: str = "unknown"
    raw_content_included: bool = False
    credential_values_included: bool = False
    private_full_paths_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_id": self.source_id,
            "source_type": self.source_type,
            "source_ref": _sanitize_ref(self.source_ref),
            "trusted_level": self.trusted_level,
            "raw_content_included": self.raw_content_included,
            "credential_values_included": self.credential_values_included,
            "private_full_paths_included": self.private_full_paths_included,
            "evidence_refs": [_sanitize_ref(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class ExternalProviderRef:
    provider_ref_id: str
    provider_name: str
    provider_type: str
    vendor_name: str | None = None
    adapter_status: str = "none"
    internal_core_dependency: bool = False
    provider_specific_logic_in_core: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"evidence_refs": [_sanitize_ref(item) for item in self.evidence_refs]}


@dataclass(frozen=True)
class ExternalRuntimeRef:
    runtime_id: str
    runtime_name: str
    runtime_type: str
    provider_ref_id: str | None = None
    environment: str = "unknown"
    runtime_status: str = "declared"
    owner_team: str | None = None
    control_surface_refs: list[dict[str, Any]] = field(default_factory=list)
    credential_boundary_ref: dict[str, Any] | None = None
    risk_class: str = "unknown"
    production_impacting: bool = False
    dispatch_enabled: bool = False
    runtime_touched: bool = False
    provider_api_call_performed: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {
            "control_surface_refs": [_sanitize_ref(item) for item in self.control_surface_refs],
            "credential_boundary_ref": _sanitize_ref(self.credential_boundary_ref or {}),
            "evidence_refs": [_sanitize_ref(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class ExternalAgentRef:
    agent_id: str
    agent_name: str
    agent_type: str
    runtime_id: str | None = None
    provider_ref_id: str | None = None
    environment: str = "unknown"
    agent_status: str = "declared"
    control_surface_refs: list[dict[str, Any]] = field(default_factory=list)
    dispatch_enabled: bool = False
    runtime_touched: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"control_surface_refs": [_sanitize_ref(item) for item in self.control_surface_refs]}


@dataclass(frozen=True)
class ExternalToolRef:
    tool_id: str
    tool_name: str
    tool_type: str
    runtime_id: str | None = None
    provider_ref_id: str | None = None
    environment: str = "unknown"
    tool_status: str = "declared"
    control_surface_refs: list[dict[str, Any]] = field(default_factory=list)
    dispatch_enabled: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"control_surface_refs": [_sanitize_ref(item) for item in self.control_surface_refs]}


@dataclass(frozen=True)
class ExternalSystemRef:
    system_id: str
    system_name: str
    system_type: str
    provider_ref_id: str | None = None
    environment: str = "unknown"
    system_status: str = "declared"
    control_surface_refs: list[dict[str, Any]] = field(default_factory=list)
    business_object_types: list[str] = field(default_factory=list)
    production_impacting: bool = False
    dispatch_enabled: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"control_surface_refs": [_sanitize_ref(item) for item in self.control_surface_refs]}


@dataclass(frozen=True)
class ExternalControlSurfaceRef:
    control_surface_id: str
    surface_type: str
    runtime_id: str | None = None
    provider_ref_id: str | None = None
    endpoint_ref: dict[str, Any] | None = None
    credential_boundary_ref: dict[str, Any] | None = None
    read_only_supported: bool = True
    dispatch_supported: bool = False
    status_tracking_supported: bool = False
    output_fetch_supported: bool = False
    cancel_or_stop_supported: bool = False
    dispatch_enabled_v0_23_1: bool = False
    provider_api_call_enabled_v0_23_1: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {
            "endpoint_ref": _sanitize_ref(self.endpoint_ref or {}),
            "credential_boundary_ref": _sanitize_ref(self.credential_boundary_ref or {}),
            "evidence_refs": [_sanitize_ref(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class CredentialBoundaryDescriptor:
    credential_boundary_id: str
    credential_type: str = "none"
    credential_value_stored: bool = False
    credential_value_output: bool = False
    credential_required_for_future_preflight: bool = False
    vault_or_secret_ref_only: bool = True
    redaction_required: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"evidence_refs": [_sanitize_ref(item) for item in self.evidence_refs]}


@dataclass(frozen=True)
class EnvironmentBoundaryDescriptor:
    environment_boundary_id: str
    runtime_id: str
    environment: str
    production_impacting: bool
    requires_human_gate_for_dispatch: bool
    requires_strong_gate_for_mutation: bool
    allowed_in_v0_23_1: bool = False
    dispatch_allowed_in_v0_23_1: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"evidence_refs": [_sanitize_ref(item) for item in self.evidence_refs]}


@dataclass(frozen=True)
class RuntimeInventoryFinding:
    finding_id: str
    severity: str
    finding_type: str
    message: str
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
            "runtime_ref": _sanitize_ref(self.runtime_ref or {}),
            "provider_ref": _sanitize_ref(self.provider_ref or {}),
            "evidence_refs": [_sanitize_ref(item) for item in self.evidence_refs],
            "withdrawal_condition": self.withdrawal_condition,
        }


@dataclass(frozen=True)
class RuntimeInventorySnapshot:
    snapshot_id: str
    created_at: str
    sources: list[DominionInventorySource]
    providers: list[ExternalProviderRef]
    runtimes: list[ExternalRuntimeRef]
    agents: list[ExternalAgentRef]
    tools: list[ExternalToolRef]
    systems: list[ExternalSystemRef]
    control_surfaces: list[ExternalControlSurfaceRef]
    credential_boundaries: list[CredentialBoundaryDescriptor]
    environment_boundaries: list[EnvironmentBoundaryDescriptor]
    findings: list[RuntimeInventoryFinding]
    inventory_status: str
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
            "providers": [item.to_dict() for item in self.providers],
            "runtimes": [item.to_dict() for item in self.runtimes],
            "agents": [item.to_dict() for item in self.agents],
            "tools": [item.to_dict() for item in self.tools],
            "systems": [item.to_dict() for item in self.systems],
            "control_surfaces": [item.to_dict() for item in self.control_surfaces],
            "credential_boundaries": [item.to_dict() for item in self.credential_boundaries],
            "environment_boundaries": [item.to_dict() for item in self.environment_boundaries],
            "findings": [item.to_dict() for item in self.findings],
            "inventory_status": self.inventory_status,
            "dispatch_enabled": self.dispatch_enabled,
            "external_runtime_touched": self.external_runtime_touched,
            "provider_api_call_performed": self.provider_api_call_performed,
            "credential_exposed": self.credential_exposed,
            "raw_secret_output": self.raw_secret_output,
        }


@dataclass(frozen=True)
class RuntimeInventoryReport:
    report_id: str
    version: str
    created_at: str
    request: DominionRuntimeInventoryRequest
    snapshot: RuntimeInventorySnapshot
    provider_count: int
    runtime_count: int
    agent_count: int
    tool_count: int
    system_count: int
    control_surface_count: int
    production_runtime_count: int
    credential_sensitive_count: int
    unknown_count: int
    finding_count: int
    report_status: str
    next_required_step: str = RUNTIME_INVENTORY_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = "Valid until declared inventory, provider registry, or company system landscape changes."

    def to_dict(self) -> dict[str, Any]:
        return {
            "report_id": self.report_id,
            "version": self.version,
            "created_at": self.created_at,
            "request": self.request.to_dict(),
            "snapshot": self.snapshot.to_dict(),
            "provider_count": self.provider_count,
            "runtime_count": self.runtime_count,
            "agent_count": self.agent_count,
            "tool_count": self.tool_count,
            "system_count": self.system_count,
            "control_surface_count": self.control_surface_count,
            "production_runtime_count": self.production_runtime_count,
            "credential_sensitive_count": self.credential_sensitive_count,
            "unknown_count": self.unknown_count,
            "finding_count": self.finding_count,
            "report_status": self.report_status,
            "next_required_step": self.next_required_step,
            "limitations": list(self.limitations),
            "withdrawal_conditions": list(self.withdrawal_conditions),
            "validity_horizon": self.validity_horizon,
        }


class DominionInventorySourceService:
    def load_sources(self, request: DominionRuntimeInventoryRequest) -> list[DominionInventorySource]:
        source_type = _normalize_choice(request.source_type, INVENTORY_SOURCE_TYPES)
        source_refs = request.source_refs or [_default_inventory_manifest()]
        return [
            DominionInventorySource(
                source_id=f"dominion_inventory_source:{index + 1}",
                source_type=source_type,
                source_ref=_sanitize_ref(source_ref),
                trusted_level=str(source_ref.get("trusted_level", "unknown")),
                raw_content_included=False,
                credential_values_included=False,
                private_full_paths_included=False,
                evidence_refs=[{"source_type": source_type, "sanitized": True}],
            )
            for index, source_ref in enumerate(source_refs[: request.max_items])
        ]


class DominionInventoryParser:
    def parse_sources(self, sources: list[DominionInventorySource]) -> list[dict[str, Any]]:
        parsed: list[dict[str, Any]] = []
        for source in sources:
            ref = source.to_dict()["source_ref"]
            if isinstance(ref.get("items"), list):
                parsed.extend(item for item in ref["items"] if isinstance(item, dict))
            elif ref:
                parsed.append(ref)
        return parsed


class ExternalProviderNormalizer:
    def normalize_providers(self, parsed_items: list[dict[str, Any]]) -> list[ExternalProviderRef]:
        providers: dict[str, ExternalProviderRef] = {}
        for item in parsed_items:
            provider_ref = item.get("provider") if isinstance(item.get("provider"), dict) else item
            if provider_ref.get("kind") not in {None, "provider"} and "provider_ref_id" not in provider_ref:
                continue
            provider_id = _safe_text(provider_ref.get("provider_ref_id") or provider_ref.get("id"), "provider:unknown")
            providers[provider_id] = ExternalProviderRef(
                provider_ref_id=provider_id,
                provider_name=_safe_text(provider_ref.get("provider_name") or provider_ref.get("name"), provider_id),
                provider_type=_normalize_choice(provider_ref.get("provider_type"), PROVIDER_TYPES),
                vendor_name=provider_ref.get("vendor_name"),
                adapter_status=_safe_text(provider_ref.get("adapter_status"), "none"),
                internal_core_dependency=bool(provider_ref.get("internal_core_dependency", False)),
                provider_specific_logic_in_core=bool(provider_ref.get("provider_specific_logic_in_core", False)),
                evidence_refs=[{"declared": True, "provider_api_call_performed": False}],
            )
        return list(providers.values())


class ExternalRuntimeNormalizer:
    def normalize_runtimes(
        self,
        parsed_items: list[dict[str, Any]],
        providers: list[ExternalProviderRef],
    ) -> list[ExternalRuntimeRef]:
        provider_ids = {item.provider_ref_id for item in providers}
        runtimes: list[ExternalRuntimeRef] = []
        for item in parsed_items:
            runtime_ref = item.get("runtime") if isinstance(item.get("runtime"), dict) else item
            if runtime_ref.get("kind") != "runtime" and "runtime_type" not in runtime_ref:
                continue
            runtime_id = _safe_text(runtime_ref.get("runtime_id") or runtime_ref.get("id"), f"runtime:{len(runtimes) + 1}")
            environment = _normalize_choice(runtime_ref.get("environment"), ENVIRONMENTS)
            provider_id = runtime_ref.get("provider_ref_id")
            runtimes.append(
                ExternalRuntimeRef(
                    runtime_id=runtime_id,
                    runtime_name=_safe_text(runtime_ref.get("runtime_name") or runtime_ref.get("name"), runtime_id),
                    runtime_type=_normalize_choice(runtime_ref.get("runtime_type"), PROVIDER_TYPES),
                    provider_ref_id=provider_id if provider_id in provider_ids else provider_id,
                    environment=environment,
                    runtime_status=_safe_text(runtime_ref.get("runtime_status"), "declared"),
                    owner_team=runtime_ref.get("owner_team"),
                    control_surface_refs=_sanitize_control_refs(runtime_ref.get("control_surface_refs")),
                    credential_boundary_ref=_sanitize_ref(runtime_ref.get("credential_boundary_ref")),
                    risk_class=_safe_text(runtime_ref.get("risk_class"), "production_impacting" if environment == "production" else "unknown"),
                    production_impacting=environment == "production" or bool(runtime_ref.get("production_impacting", False)),
                    dispatch_enabled=bool(runtime_ref.get("dispatch_enabled", False)),
                    runtime_touched=False,
                    provider_api_call_performed=False,
                    evidence_refs=[{"declared": True, "external_runtime_touched": False}],
                )
            )
        return runtimes


class ExternalAgentToolSystemNormalizer:
    def normalize_agents_tools_systems(
        self,
        parsed_items: list[dict[str, Any]],
        providers: list[ExternalProviderRef],
        runtimes: list[ExternalRuntimeRef],
    ) -> tuple[list[ExternalAgentRef], list[ExternalToolRef], list[ExternalSystemRef]]:
        agents: list[ExternalAgentRef] = []
        tools: list[ExternalToolRef] = []
        systems: list[ExternalSystemRef] = []
        for item in parsed_items:
            kind = str(item.get("kind", ""))
            if kind == "agent" or "agent_id" in item:
                agents.append(
                    ExternalAgentRef(
                        agent_id=_safe_text(item.get("agent_id") or item.get("id"), f"agent:{len(agents) + 1}"),
                        agent_name=_safe_text(item.get("agent_name") or item.get("name"), "declared agent"),
                        agent_type=_normalize_choice(item.get("agent_type"), AGENT_TYPES),
                        runtime_id=item.get("runtime_id"),
                        provider_ref_id=item.get("provider_ref_id"),
                        environment=_normalize_choice(item.get("environment"), ENVIRONMENTS),
                        agent_status=_safe_text(item.get("agent_status"), "declared"),
                        control_surface_refs=_sanitize_control_refs(item.get("control_surface_refs")),
                        dispatch_enabled=bool(item.get("dispatch_enabled", False)),
                        runtime_touched=False,
                    )
                )
            if kind == "tool" or "tool_id" in item:
                tools.append(
                    ExternalToolRef(
                        tool_id=_safe_text(item.get("tool_id") or item.get("id"), f"tool:{len(tools) + 1}"),
                        tool_name=_safe_text(item.get("tool_name") or item.get("name"), "declared tool"),
                        tool_type=_normalize_choice(item.get("tool_type"), TOOL_TYPES),
                        runtime_id=item.get("runtime_id"),
                        provider_ref_id=item.get("provider_ref_id"),
                        environment=_normalize_choice(item.get("environment"), ENVIRONMENTS),
                        tool_status=_safe_text(item.get("tool_status"), "declared"),
                        control_surface_refs=_sanitize_control_refs(item.get("control_surface_refs")),
                        dispatch_enabled=bool(item.get("dispatch_enabled", False)),
                    )
                )
            if kind == "system" or "system_id" in item:
                environment = _normalize_choice(item.get("environment"), ENVIRONMENTS)
                systems.append(
                    ExternalSystemRef(
                        system_id=_safe_text(item.get("system_id") or item.get("id"), f"system:{len(systems) + 1}"),
                        system_name=_safe_text(item.get("system_name") or item.get("name"), "declared system"),
                        system_type=_normalize_choice(item.get("system_type"), SYSTEM_TYPES),
                        provider_ref_id=item.get("provider_ref_id"),
                        environment=environment,
                        system_status=_safe_text(item.get("system_status"), "declared"),
                        control_surface_refs=_sanitize_control_refs(item.get("control_surface_refs")),
                        business_object_types=[str(value) for value in item.get("business_object_types", [])],
                        production_impacting=environment == "production" or bool(item.get("production_impacting", False)),
                        dispatch_enabled=bool(item.get("dispatch_enabled", False)),
                    )
                )
        return agents, tools, systems


class ControlSurfaceNormalizer:
    def normalize_control_surfaces(
        self,
        parsed_items: list[dict[str, Any]],
        providers: list[ExternalProviderRef],
        runtimes: list[ExternalRuntimeRef],
    ) -> list[ExternalControlSurfaceRef]:
        surfaces: list[ExternalControlSurfaceRef] = []
        for item in parsed_items:
            surface_items = item.get("control_surfaces")
            if isinstance(surface_items, list):
                candidates = [entry for entry in surface_items if isinstance(entry, dict)]
            elif item.get("kind") == "control_surface" or "control_surface_id" in item:
                candidates = [item]
            else:
                candidates = []
            for surface in candidates:
                surfaces.append(
                    ExternalControlSurfaceRef(
                        control_surface_id=_safe_text(
                            surface.get("control_surface_id") or surface.get("id"),
                            f"control_surface:{len(surfaces) + 1}",
                        ),
                        surface_type=_normalize_choice(surface.get("surface_type"), CONTROL_SURFACE_TYPES),
                        runtime_id=surface.get("runtime_id") or item.get("runtime_id"),
                        provider_ref_id=surface.get("provider_ref_id") or item.get("provider_ref_id"),
                        endpoint_ref=_sanitize_ref(surface.get("endpoint_ref")),
                        credential_boundary_ref=_sanitize_ref(surface.get("credential_boundary_ref")),
                        read_only_supported=bool(surface.get("read_only_supported", True)),
                        dispatch_supported=bool(surface.get("dispatch_supported", False)),
                        status_tracking_supported=bool(surface.get("status_tracking_supported", False)),
                        output_fetch_supported=bool(surface.get("output_fetch_supported", False)),
                        cancel_or_stop_supported=bool(surface.get("cancel_or_stop_supported", False)),
                        dispatch_enabled_v0_23_1=bool(surface.get("dispatch_enabled_v0_23_1", False)),
                        provider_api_call_enabled_v0_23_1=bool(
                            surface.get("provider_api_call_enabled_v0_23_1", False)
                        ),
                    )
                )
        return surfaces


class CredentialBoundaryService:
    def build_credential_boundaries(self, parsed_items: list[dict[str, Any]]) -> list[CredentialBoundaryDescriptor]:
        boundaries: dict[str, CredentialBoundaryDescriptor] = {}
        for item in parsed_items:
            boundary = item.get("credential_boundary") if isinstance(item.get("credential_boundary"), dict) else None
            if boundary is None and "credential_boundary_id" in item:
                boundary = item
            if not boundary:
                continue
            boundary_id = _safe_text(boundary.get("credential_boundary_id") or boundary.get("id"), "credential:none")
            boundaries[boundary_id] = CredentialBoundaryDescriptor(
                credential_boundary_id=boundary_id,
                credential_type=_safe_text(boundary.get("credential_type"), "none"),
                credential_value_stored=False,
                credential_value_output=False,
                credential_required_for_future_preflight=bool(
                    boundary.get("credential_required_for_future_preflight", False)
                ),
                vault_or_secret_ref_only=True,
                redaction_required=True,
                evidence_refs=[{"sanitized": True}],
            )
        return list(boundaries.values())


class EnvironmentBoundaryService:
    def build_environment_boundaries(self, runtimes: list[ExternalRuntimeRef]) -> list[EnvironmentBoundaryDescriptor]:
        return [
            EnvironmentBoundaryDescriptor(
                environment_boundary_id=f"environment_boundary:{runtime.runtime_id}",
                runtime_id=runtime.runtime_id,
                environment=runtime.environment,
                production_impacting=runtime.production_impacting,
                requires_human_gate_for_dispatch=runtime.production_impacting,
                requires_strong_gate_for_mutation=runtime.production_impacting,
                allowed_in_v0_23_1=False,
                dispatch_allowed_in_v0_23_1=False,
                evidence_refs=[{"runtime_status": runtime.runtime_status}],
            )
            for runtime in runtimes
        ]


class RuntimeInventoryPolicyService:
    def evaluate_policy(
        self,
        providers: list[ExternalProviderRef],
        runtimes: list[ExternalRuntimeRef],
        control_surfaces: list[ExternalControlSurfaceRef],
        credential_boundaries: list[CredentialBoundaryDescriptor],
        parsed_items: list[dict[str, Any]] | None = None,
    ) -> list[RuntimeInventoryFinding]:
        findings: list[RuntimeInventoryFinding] = []
        parsed_items = parsed_items or []
        boundary_ids = {item.credential_boundary_id for item in credential_boundaries}
        for provider in providers:
            if provider.provider_specific_logic_in_core or provider.internal_core_dependency:
                findings.append(_finding("error", "provider_specific_logic_in_core", provider_ref=provider.to_dict()))
            if provider.vendor_name:
                findings.append(_finding("warning", "vendor_hardcoding_detected", provider_ref=provider.to_dict()))
            if "growthkernel" in provider.provider_name.lower():
                findings.append(_finding("error", "growthkernel_dependency_detected", provider_ref=provider.to_dict()))
        seen_runtime_ids: set[str] = set()
        for runtime in runtimes:
            if runtime.runtime_id in seen_runtime_ids:
                findings.append(_finding("warning", "duplicate_runtime", runtime_ref=runtime.to_dict()))
            seen_runtime_ids.add(runtime.runtime_id)
            if runtime.runtime_type == "unknown":
                findings.append(_finding("warning", "unknown_runtime_type", runtime_ref=runtime.to_dict()))
            if runtime.environment == "unknown":
                findings.append(_finding("warning", "unknown_environment", runtime_ref=runtime.to_dict()))
            if runtime.production_impacting:
                findings.append(_finding("warning", "production_runtime_declared", runtime_ref=runtime.to_dict()))
            boundary_ref = runtime.credential_boundary_ref or {}
            boundary_id = boundary_ref.get("credential_boundary_id")
            if not boundary_id or boundary_id not in boundary_ids:
                findings.append(_finding("warning", "credential_boundary_missing", runtime_ref=runtime.to_dict()))
            if runtime.dispatch_enabled:
                findings.append(_finding("error", "dispatch_enabled_too_early", runtime_ref=runtime.to_dict()))
            if runtime.provider_api_call_performed:
                findings.append(_finding("critical", "provider_api_call_enabled_too_early", runtime_ref=runtime.to_dict()))
        for surface in control_surfaces:
            if surface.dispatch_enabled_v0_23_1:
                findings.append(_finding("error", "dispatch_enabled_too_early"))
            if surface.provider_api_call_enabled_v0_23_1:
                findings.append(_finding("critical", "provider_api_call_enabled_too_early"))
            if not surface.status_tracking_supported:
                findings.append(_finding("warning", "status_tracking_missing"))
            if not surface.output_fetch_supported:
                findings.append(_finding("warning", "outcome_mapping_missing"))
        for item in parsed_items:
            lowered = " ".join(f"{key}={value}" for key, value in item.items()).lower()
            if any(secret_key in item for secret_key in SECRET_KEYS):
                findings.append(_finding("critical", "credential_value_exposure_risk"))
            if "self_execution" in lowered or "self-execution safety" in lowered:
                findings.append(_finding("error", "self_execution_legacy_detected"))
            if "growthkernel dependency" in lowered or "requires growthkernel" in lowered:
                findings.append(_finding("error", "growthkernel_dependency_detected"))
            if "provider direct run" in lowered or "dispatch without gate" in lowered:
                findings.append(_finding("error", "provider_specific_logic_in_core"))
        if not findings:
            findings.append(_finding("info", "ok", message="Declared inventory passed v0.23.1 static policy checks."))
        return findings


class RuntimeInventorySnapshotService:
    def __init__(
        self,
        *,
        source_service: DominionInventorySourceService | None = None,
        parser: DominionInventoryParser | None = None,
        provider_normalizer: ExternalProviderNormalizer | None = None,
        runtime_normalizer: ExternalRuntimeNormalizer | None = None,
        agent_tool_system_normalizer: ExternalAgentToolSystemNormalizer | None = None,
        control_surface_normalizer: ControlSurfaceNormalizer | None = None,
        credential_boundary_service: CredentialBoundaryService | None = None,
        environment_boundary_service: EnvironmentBoundaryService | None = None,
        policy_service: RuntimeInventoryPolicyService | None = None,
    ) -> None:
        self.source_service = source_service or DominionInventorySourceService()
        self.parser = parser or DominionInventoryParser()
        self.provider_normalizer = provider_normalizer or ExternalProviderNormalizer()
        self.runtime_normalizer = runtime_normalizer or ExternalRuntimeNormalizer()
        self.agent_tool_system_normalizer = agent_tool_system_normalizer or ExternalAgentToolSystemNormalizer()
        self.control_surface_normalizer = control_surface_normalizer or ControlSurfaceNormalizer()
        self.credential_boundary_service = credential_boundary_service or CredentialBoundaryService()
        self.environment_boundary_service = environment_boundary_service or EnvironmentBoundaryService()
        self.policy_service = policy_service or RuntimeInventoryPolicyService()

    def build_snapshot(self, request: DominionRuntimeInventoryRequest) -> RuntimeInventorySnapshot:
        sources = self.source_service.load_sources(request)
        parsed_items = self.parser.parse_sources(sources)
        providers = self.provider_normalizer.normalize_providers(parsed_items)
        runtimes = self.runtime_normalizer.normalize_runtimes(parsed_items, providers)
        agents, tools, systems = self.agent_tool_system_normalizer.normalize_agents_tools_systems(
            parsed_items,
            providers,
            runtimes,
        )
        surfaces = self.control_surface_normalizer.normalize_control_surfaces(parsed_items, providers, runtimes)
        credentials = self.credential_boundary_service.build_credential_boundaries(parsed_items)
        environments = self.environment_boundary_service.build_environment_boundaries(runtimes)
        findings = self.policy_service.evaluate_policy(providers, runtimes, surfaces, credentials, parsed_items)
        return RuntimeInventorySnapshot(
            snapshot_id="runtime_inventory_snapshot:v0.23.1",
            created_at=_now(),
            sources=sources,
            providers=providers,
            runtimes=runtimes,
            agents=agents,
            tools=tools,
            systems=systems,
            control_surfaces=surfaces,
            credential_boundaries=credentials,
            environment_boundaries=environments,
            findings=findings,
            inventory_status=_status_from_findings(findings),
            dispatch_enabled=False,
            external_runtime_touched=False,
            provider_api_call_performed=False,
            credential_exposed=any(item.finding_type == "credential_value_exposure_risk" for item in findings),
            raw_secret_output=False,
        )


class RuntimeInventoryReportService:
    def __init__(self, snapshot_service: RuntimeInventorySnapshotService | None = None) -> None:
        self.snapshot_service = snapshot_service or RuntimeInventorySnapshotService()

    def build_report(self, request: DominionRuntimeInventoryRequest | None = None) -> RuntimeInventoryReport:
        request = request or DominionRuntimeInventoryRequest()
        snapshot = self.snapshot_service.build_snapshot(request)
        credential_sensitive_count = sum(
            1 for item in snapshot.credential_boundaries if item.credential_type not in {"none", "unknown"}
        )
        unknown_count = sum(
            1 for item in [*snapshot.providers, *snapshot.runtimes] if "unknown" in item.to_dict().values()
        )
        return RuntimeInventoryReport(
            report_id="runtime_inventory_report:v0.23.1",
            version=RUNTIME_INVENTORY_VERSION,
            created_at=snapshot.created_at,
            request=request,
            snapshot=snapshot,
            provider_count=len(snapshot.providers),
            runtime_count=len(snapshot.runtimes),
            agent_count=len(snapshot.agents),
            tool_count=len(snapshot.tools),
            system_count=len(snapshot.systems),
            control_surface_count=len(snapshot.control_surfaces),
            production_runtime_count=sum(1 for item in snapshot.runtimes if item.production_impacting),
            credential_sensitive_count=credential_sensitive_count,
            unknown_count=unknown_count,
            finding_count=len(snapshot.findings),
            report_status="passed" if snapshot.inventory_status == "declared" else snapshot.inventory_status,
            limitations=[
                "Inventory is declared/static/operator-provided only.",
                "No provider API discovery, external runtime touch, dispatch, credential materialization, network, MCP, plugin, shell, or local command execution is enabled.",
                "Vendor systems are future external provider skills or provider adapters.",
            ],
            withdrawal_conditions=[
                "Withdraw if provider API calls or external runtime touch are introduced.",
                "Withdraw if credential values are stored or output.",
                "Withdraw if v0.23.x is re-described as Self-Execution Safety.",
            ],
        )

    def build_pig_report(self, request: DominionRuntimeInventoryRequest | None = None) -> dict[str, Any]:
        report = self.build_report(request)
        snapshot = report.snapshot
        return {
            "version": RUNTIME_INVENTORY_VERSION,
            "layer": RUNTIME_INVENTORY_LAYER,
            "subject": RUNTIME_INVENTORY_SUBJECT,
            "track": RUNTIME_INVENTORY_TRACK,
            "version_name": RUNTIME_INVENTORY_VERSION_NAME,
            "principles": [
                "inventory is not dispatch",
                "inventory is not provider API discovery",
                "inventory is not runtime touch",
                "inventory is not credential materialization",
            ],
            "counts": _report_counts(report),
            "safety_boundary": {
                "dispatch_enabled": snapshot.dispatch_enabled,
                "external_runtime_touched": snapshot.external_runtime_touched,
                "provider_api_call_performed": snapshot.provider_api_call_performed,
                "credential_exposed": snapshot.credential_exposed,
                "raw_secret_output": snapshot.raw_secret_output,
                "network_enabled": False,
                "mcp_enabled": False,
                "plugin_enabled": False,
                "shell_enabled": False,
            },
            "next_step": RUNTIME_INVENTORY_NEXT_STEP,
            "canonical_store": "ocel",
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": RUNTIME_INVENTORY_STATE,
            "version": RUNTIME_INVENTORY_VERSION,
            "layer": RUNTIME_INVENTORY_LAYER,
            "source_read_models": [
                "InternalDominionContractState",
                "DominionProviderInterfaceState",
                "InternalSkillTaxonomyState",
                "DominionMigrationState",
            ],
            "target_read_models": [
                "DominionRuntimeInventoryState",
                "ExternalProviderRefState",
                "ExternalRuntimeRefState",
                "ExternalAgentRefState",
                "ExternalToolRefState",
                "ExternalSystemRefState",
                "ExternalControlSurfaceRefState",
                "CredentialBoundaryState",
                "EnvironmentBoundaryState",
            ],
            "effect_types": list(DOMINION_EFFECT_TYPES),
            "object_coverage": list(DOMINION_OCEL_OBJECT_TYPES),
            "event_coverage": list(DOMINION_OCEL_EVENT_TYPES),
            "relation_coverage": list(DOMINION_OCEL_RELATION_TYPES),
            "canonical_store": "ocel",
        }

    def render_report_cli(self, report: RuntimeInventoryReport | None = None) -> str:
        report = report or self.build_report()
        snapshot = report.snapshot
        return "\n".join(
            [
                "Dominion Runtime / Agent / System Inventory",
                f"version={report.version}",
                f"version_name={RUNTIME_INVENTORY_VERSION_NAME}",
                f"track={RUNTIME_INVENTORY_TRACK}",
                f"layer={RUNTIME_INVENTORY_LAYER}",
                f"status={report.report_status}",
                f"provider_count={report.provider_count}",
                f"runtime_count={report.runtime_count}",
                f"agent_count={report.agent_count}",
                f"tool_count={report.tool_count}",
                f"system_count={report.system_count}",
                f"control_surface_count={report.control_surface_count}",
                f"production_runtime_count={report.production_runtime_count}",
                f"credential_sensitive_count={report.credential_sensitive_count}",
                f"unknown_count={report.unknown_count}",
                f"finding_count={report.finding_count}",
                f"dispatch_enabled={str(snapshot.dispatch_enabled).lower()}",
                f"external_runtime_touched={str(snapshot.external_runtime_touched).lower()}",
                f"provider_api_call_performed={str(snapshot.provider_api_call_performed).lower()}",
                f"credential_exposed={str(snapshot.credential_exposed).lower()}",
                f"raw_secret_output={str(snapshot.raw_secret_output).lower()}",
                "GrowthKernel=future_consumer_not_dependency",
                "vendor adapters=future_external_provider_skills",
                "self_execution=v0.24 Local Runtime Provider",
                f"next_required_step={report.next_required_step}",
                "raw_secrets_printed=False",
                "private_full_paths_printed=False",
            ]
        )

    def render_collection_cli(self, section: str, report: RuntimeInventoryReport | None = None) -> str:
        report = report or self.build_report()
        snapshot = report.snapshot
        items = {
            "providers": snapshot.providers,
            "runtimes": snapshot.runtimes,
            "systems": snapshot.systems,
            "control-surfaces": snapshot.control_surfaces,
            "findings": snapshot.findings,
        }[section]
        lines = [
            f"Dominion Inventory {section}",
            f"version={RUNTIME_INVENTORY_VERSION}",
            f"layer={RUNTIME_INVENTORY_LAYER}",
            f"status={report.report_status}",
            f"provider_count={report.provider_count}",
            f"runtime_count={report.runtime_count}",
            f"agent_count={report.agent_count}",
            f"tool_count={report.tool_count}",
            f"system_count={report.system_count}",
            f"production_runtime_count={report.production_runtime_count}",
            f"credential_sensitive_count={report.credential_sensitive_count}",
            "dispatch_enabled=false",
            "external_runtime_touched=false",
            "provider_api_call_performed=false",
            "credential_exposed=false",
            f"next_required_step={report.next_required_step}",
        ]
        for item in items:
            payload = item.to_dict()
            primary = (
                payload.get("provider_ref_id")
                or payload.get("runtime_id")
                or payload.get("system_id")
                or payload.get("control_surface_id")
                or payload.get("finding_id")
            )
            status = payload.get("runtime_status") or payload.get("system_status") or payload.get("severity") or "declared"
            lines.append(f"- id={primary} status={status}")
        lines.extend(["raw_secrets_printed=False", "private_full_paths_printed=False"])
        return "\n".join(lines)


class DominionRuntimeInventoryService:
    def __init__(self, report_service: RuntimeInventoryReportService | None = None) -> None:
        self.report_service = report_service or RuntimeInventoryReportService()

    def inventory(self, request: DominionRuntimeInventoryRequest | None = None) -> RuntimeInventoryReport:
        return self.report_service.build_report(request)


def _sanitize_control_refs(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [_sanitize_ref(item) for item in value if isinstance(item, dict)]


def _finding(
    severity: str,
    finding_type: str,
    *,
    message: str | None = None,
    runtime_ref: dict[str, Any] | None = None,
    provider_ref: dict[str, Any] | None = None,
) -> RuntimeInventoryFinding:
    return RuntimeInventoryFinding(
        finding_id=f"runtime_inventory_finding:{finding_type}",
        severity=severity,
        finding_type=finding_type,
        message=message or finding_type.replace("_", " "),
        runtime_ref=runtime_ref,
        provider_ref=provider_ref,
        evidence_refs=[{"policy": "v0.23.1_static_inventory"}],
        withdrawal_condition="Withdraw this finding if sanitized declaration evidence changes.",
    )


def _status_from_findings(findings: list[RuntimeInventoryFinding]) -> str:
    severities = {item.severity for item in findings}
    if "critical" in severities:
        return "blocked"
    if "error" in severities:
        return "failed"
    if "warning" in severities:
        return "warning"
    return "declared"


def _report_counts(report: RuntimeInventoryReport) -> dict[str, int]:
    return {
        "provider_count": report.provider_count,
        "runtime_count": report.runtime_count,
        "agent_count": report.agent_count,
        "tool_count": report.tool_count,
        "system_count": report.system_count,
        "control_surface_count": report.control_surface_count,
        "production_runtime_count": report.production_runtime_count,
        "credential_sensitive_count": report.credential_sensitive_count,
        "unknown_count": report.unknown_count,
        "finding_count": report.finding_count,
    }


def _default_inventory_manifest() -> dict[str, Any]:
    return {
        "kind": "manifest",
        "items": [
            {
                "kind": "provider",
                "provider_ref_id": "provider:declared-local-runtime",
                "provider_name": "Declared Local Runtime Provider Ref",
                "provider_type": "local_runtime",
                "adapter_status": "future_adapter",
            },
            {
                "kind": "runtime",
                "runtime_id": "runtime:declared-local",
                "runtime_name": "Declared Local Runtime",
                "runtime_type": "local_runtime",
                "provider_ref_id": "provider:declared-local-runtime",
                "environment": "local",
                "runtime_status": "declared",
                "credential_boundary_ref": {"credential_boundary_id": "credential:none"},
                "control_surface_refs": [{"control_surface_id": "surface:manual-only"}],
            },
            {
                "kind": "control_surface",
                "control_surface_id": "surface:manual-only",
                "surface_type": "manual_only",
                "runtime_id": "runtime:declared-local",
                "provider_ref_id": "provider:declared-local-runtime",
                "read_only_supported": True,
                "dispatch_supported": False,
                "status_tracking_supported": False,
                "output_fetch_supported": False,
                "cancel_or_stop_supported": False,
            },
            {
                "kind": "credential_boundary",
                "credential_boundary_id": "credential:none",
                "credential_type": "none",
            },
        ],
    }
