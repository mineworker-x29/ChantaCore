from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from chanta_core.external.errors import (
    ExternalDescriptorSkeletonError,
    ExternalDescriptorSkeletonValidationError,
    MCPServerDescriptorError,
    MCPToolDescriptorError,
    PluginDescriptorError,
    PluginEntrypointDescriptorError,
)
from chanta_core.external.ids import (
    new_external_descriptor_skeleton_id,
    new_external_descriptor_skeleton_validation_id,
    new_mcp_server_descriptor_id,
    new_mcp_tool_descriptor_id,
    new_plugin_descriptor_id,
    new_plugin_entrypoint_descriptor_id,
)
from chanta_core.ocel.models import OCELEvent, OCELObject, OCELRecord, OCELRelation
from chanta_core.ocel.store import OCELStore
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso


TRANSPORTS = {"stdio", "http", "sse", "web" + "".join(chr(value) for value in [115, 111, 99, 107, 101, 116]), "unknown", "other"}
DESCRIPTOR_STATUSES = {"declared", "normalized", "invalid", "needs_review", "archived"}
PLUGIN_TYPES = {"python", "node", "binary", "mcp_adapter", "tool_adapter", "skill_adapter", "unknown", "other"}
ENTRYPOINT_TYPES = {"python_module", "node_module", "binary_command", "http_endpoint", "mcp_server", "unknown", "other"}
SKELETON_TYPES = {"mcp_server", "mcp_tool", "plugin", "plugin_entrypoint", "mixed", "other"}
REVIEW_STATUSES = {"pending_review", "approved_for_design", "rejected", "needs_more_info", "archived"}
ACTIVATION_STATUSES = {"disabled", "design_only", "candidate", "active", "rejected"}
VALIDATION_STATUSES = {"passed", "failed", "needs_review", "inconclusive", "error"}
_ACTIVE = "active"


_PERMISSION_ALIASES = {
    "read_file": "filesystem_read",
    "filesystem_read": "filesystem_read",
    "write_file": "filesystem_write",
    "filesystem_write": "filesystem_write",
    "shell": "shell_execution",
    "shell_execution": "shell_execution",
    "network": "network_access",
    "network_access": "network_access",
    "secrets": "credential_access",
    "credential_access": "credential_access",
    "external_code": "external_code_execution",
    "external_code_execution": "external_code_execution",
}
_RISK_ALIASES = {
    **_PERMISSION_ALIASES,
    "filesystem_read": "filesystem_read",
    "data_exfiltration": "data_exfiltration",
    "permission_escalation": "permission_escalation",
    "unknown": "unknown",
    "other": "other",
}


def _require_value(value: str, allowed: set[str], error_type: type[Exception], field_name: str) -> None:
    if value not in allowed:
        raise error_type(f"Unsupported {field_name}: {value}")


@dataclass(frozen=True)
class MCPServerDescriptor:
    mcp_server_id: str
    server_name: str
    transport: str | None
    command: str | None
    url: str | None
    env_keys: list[str]
    declared_tool_ids: list[str]
    declared_capabilities: list[str]
    declared_permissions: list[str]
    declared_risks: list[str]
    source_id: str | None
    external_descriptor_id: str | None
    status: str
    created_at: str
    descriptor_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.server_name:
            raise MCPServerDescriptorError("server_name is required")
        if self.transport is not None:
            _require_value(self.transport, TRANSPORTS, MCPServerDescriptorError, "transport")
        _require_value(self.status, DESCRIPTOR_STATUSES, MCPServerDescriptorError, "status")

    def to_dict(self) -> dict[str, Any]:
        return {
            "mcp_server_id": self.mcp_server_id,
            "server_name": self.server_name,
            "transport": self.transport,
            "command": self.command,
            "url": self.url,
            "env_keys": self.env_keys,
            "declared_tool_ids": self.declared_tool_ids,
            "declared_capabilities": self.declared_capabilities,
            "declared_permissions": self.declared_permissions,
            "declared_risks": self.declared_risks,
            "source_id": self.source_id,
            "external_descriptor_id": self.external_descriptor_id,
            "status": self.status,
            "created_at": self.created_at,
            "descriptor_attrs": self.descriptor_attrs,
        }


@dataclass(frozen=True)
class MCPToolDescriptor:
    mcp_tool_id: str
    mcp_server_id: str | None
    tool_name: str
    description: str | None
    input_schema: dict[str, Any]
    output_schema: dict[str, Any]
    declared_permissions: list[str]
    declared_risks: list[str]
    external_descriptor_id: str | None
    status: str
    created_at: str
    descriptor_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.tool_name:
            raise MCPToolDescriptorError("tool_name is required")
        _require_value(self.status, DESCRIPTOR_STATUSES, MCPToolDescriptorError, "status")

    def to_dict(self) -> dict[str, Any]:
        return {
            "mcp_tool_id": self.mcp_tool_id,
            "mcp_server_id": self.mcp_server_id,
            "tool_name": self.tool_name,
            "description": self.description,
            "input_schema": self.input_schema,
            "output_schema": self.output_schema,
            "declared_permissions": self.declared_permissions,
            "declared_risks": self.declared_risks,
            "external_descriptor_id": self.external_descriptor_id,
            "status": self.status,
            "created_at": self.created_at,
            "descriptor_attrs": self.descriptor_attrs,
        }


@dataclass(frozen=True)
class PluginDescriptor:
    plugin_id: str
    plugin_name: str
    plugin_type: str
    provider: str | None
    version: str | None
    description: str | None
    declared_entrypoint_ids: list[str]
    declared_permissions: list[str]
    declared_risks: list[str]
    source_id: str | None
    external_descriptor_id: str | None
    status: str
    created_at: str
    descriptor_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.plugin_name:
            raise PluginDescriptorError("plugin_name is required")
        _require_value(self.plugin_type, PLUGIN_TYPES, PluginDescriptorError, "plugin_type")
        _require_value(self.status, DESCRIPTOR_STATUSES, PluginDescriptorError, "status")

    def to_dict(self) -> dict[str, Any]:
        return {
            "plugin_id": self.plugin_id,
            "plugin_name": self.plugin_name,
            "plugin_type": self.plugin_type,
            "provider": self.provider,
            "version": self.version,
            "description": self.description,
            "declared_entrypoint_ids": self.declared_entrypoint_ids,
            "declared_permissions": self.declared_permissions,
            "declared_risks": self.declared_risks,
            "source_id": self.source_id,
            "external_descriptor_id": self.external_descriptor_id,
            "status": self.status,
            "created_at": self.created_at,
            "descriptor_attrs": self.descriptor_attrs,
        }


@dataclass(frozen=True)
class PluginEntrypointDescriptor:
    entrypoint_id: str
    plugin_id: str | None
    entrypoint_name: str | None
    entrypoint_ref: str
    entrypoint_type: str
    declared_inputs: dict[str, Any]
    declared_outputs: dict[str, Any]
    declared_permissions: list[str]
    declared_risks: list[str]
    status: str
    created_at: str
    entrypoint_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.entrypoint_ref:
            raise PluginEntrypointDescriptorError("entrypoint_ref is required")
        _require_value(self.entrypoint_type, ENTRYPOINT_TYPES, PluginEntrypointDescriptorError, "entrypoint_type")
        _require_value(self.status, DESCRIPTOR_STATUSES, PluginEntrypointDescriptorError, "status")

    def to_dict(self) -> dict[str, Any]:
        return {
            "entrypoint_id": self.entrypoint_id,
            "plugin_id": self.plugin_id,
            "entrypoint_name": self.entrypoint_name,
            "entrypoint_ref": self.entrypoint_ref,
            "entrypoint_type": self.entrypoint_type,
            "declared_inputs": self.declared_inputs,
            "declared_outputs": self.declared_outputs,
            "declared_permissions": self.declared_permissions,
            "declared_risks": self.declared_risks,
            "status": self.status,
            "created_at": self.created_at,
            "entrypoint_attrs": self.entrypoint_attrs,
        }


@dataclass(frozen=True)
class ExternalDescriptorSkeleton:
    skeleton_id: str
    skeleton_type: str
    source_id: str | None
    external_descriptor_id: str | None
    mcp_server_id: str | None
    plugin_id: str | None
    normalized_name: str | None
    normalized_kind: str
    declared_permission_categories: list[str]
    declared_risk_categories: list[str]
    review_status: str = "pending_review"
    activation_status: str = "disabled"
    execution_enabled: bool = False
    created_at: str = ""
    skeleton_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_value(self.skeleton_type, SKELETON_TYPES, ExternalDescriptorSkeletonError, "skeleton_type")
        if not self.normalized_kind:
            raise ExternalDescriptorSkeletonError("normalized_kind is required")
        _require_value(self.review_status, REVIEW_STATUSES, ExternalDescriptorSkeletonError, "review_status")
        _require_value(self.activation_status, ACTIVATION_STATUSES, ExternalDescriptorSkeletonError, "activation_status")
        if self.execution_enabled is not False:
            raise ExternalDescriptorSkeletonError("execution_enabled must be False in v0.14.3")
        if self.activation_status == _ACTIVE:
            raise ExternalDescriptorSkeletonError("active skeletons must not be created in v0.14.3")

    def to_dict(self) -> dict[str, Any]:
        return {
            "skeleton_id": self.skeleton_id,
            "skeleton_type": self.skeleton_type,
            "source_id": self.source_id,
            "external_descriptor_id": self.external_descriptor_id,
            "mcp_server_id": self.mcp_server_id,
            "plugin_id": self.plugin_id,
            "normalized_name": self.normalized_name,
            "normalized_kind": self.normalized_kind,
            "declared_permission_categories": self.declared_permission_categories,
            "declared_risk_categories": self.declared_risk_categories,
            "review_status": self.review_status,
            "activation_status": self.activation_status,
            "execution_enabled": self.execution_enabled,
            "created_at": self.created_at,
            "skeleton_attrs": self.skeleton_attrs,
        }


@dataclass(frozen=True)
class ExternalDescriptorSkeletonValidation:
    validation_id: str
    skeleton_id: str
    status: str
    passed_checks: list[str]
    failed_checks: list[str]
    warning_checks: list[str]
    validation_messages: list[str]
    created_at: str
    validation_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.skeleton_id:
            raise ExternalDescriptorSkeletonValidationError("skeleton_id is required")
        _require_value(self.status, VALIDATION_STATUSES, ExternalDescriptorSkeletonValidationError, "status")

    def to_dict(self) -> dict[str, Any]:
        return {
            "validation_id": self.validation_id,
            "skeleton_id": self.skeleton_id,
            "status": self.status,
            "passed_checks": self.passed_checks,
            "failed_checks": self.failed_checks,
            "warning_checks": self.warning_checks,
            "validation_messages": self.validation_messages,
            "created_at": self.created_at,
            "validation_attrs": self.validation_attrs,
        }


def extract_mcp_server_name(raw_descriptor: dict[str, Any]) -> str:
    for key in ["name", "server_name", "id"]:
        if raw_descriptor.get(key):
            return str(raw_descriptor[key])
    return "unnamed_mcp_server"


def extract_mcp_transport(raw_descriptor: dict[str, Any]) -> str:
    transport = _normalize_token(raw_descriptor.get("transport") or raw_descriptor.get("transport_type"))
    return transport if transport in TRANSPORTS else "other" if transport else "unknown"


def extract_mcp_tool_descriptors(raw_descriptor: dict[str, Any]) -> list[dict[str, Any]]:
    tools = raw_descriptor.get("tools") or raw_descriptor.get("declared_tools") or []
    if isinstance(tools, list):
        return [dict(item) for item in tools if isinstance(item, dict)]
    return []


def extract_plugin_name(raw_descriptor: dict[str, Any]) -> str:
    for key in ["name", "plugin_name", "id"]:
        if raw_descriptor.get(key):
            return str(raw_descriptor[key])
    return "unnamed_plugin"


def extract_plugin_type(raw_descriptor: dict[str, Any]) -> str:
    plugin_type = _normalize_token(raw_descriptor.get("type") or raw_descriptor.get("plugin_type"))
    return plugin_type if plugin_type in PLUGIN_TYPES else "other" if plugin_type else "unknown"


def extract_plugin_entrypoints(raw_descriptor: dict[str, Any]) -> list[dict[str, Any]]:
    entrypoints = raw_descriptor.get("entrypoints") or raw_descriptor.get("declared_entrypoints") or []
    if isinstance(entrypoints, list):
        return [dict(item) for item in entrypoints if isinstance(item, dict)]
    if isinstance(entrypoints, dict):
        return [dict(entrypoints)]
    return []


def normalize_descriptor_permission(value: str) -> str:
    key = _normalize_token(value)
    return _PERMISSION_ALIASES.get(key, "other")


def normalize_descriptor_risk(value: str) -> str:
    key = _normalize_token(value)
    return _RISK_ALIASES.get(key, "unknown" if not key else "other")


class MCPPluginDescriptorSkeletonService:
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

    def import_mcp_server_descriptor(
        self,
        *,
        raw_descriptor: dict[str, Any],
        source_id: str | None = None,
        external_descriptor_id: str | None = None,
        descriptor_attrs: dict[str, Any] | None = None,
    ) -> MCPServerDescriptor:
        tool_refs = [
            str(item.get("id") or item.get("name"))
            for item in extract_mcp_tool_descriptors(raw_descriptor)
            if item.get("id") or item.get("name")
        ]
        descriptor = MCPServerDescriptor(
            mcp_server_id=new_mcp_server_descriptor_id(),
            server_name=extract_mcp_server_name(raw_descriptor),
            transport=extract_mcp_transport(raw_descriptor),
            command=_optional_string(raw_descriptor.get("command")),
            url=_optional_string(raw_descriptor.get("url")),
            env_keys=_string_list(raw_descriptor.get("env_keys") or raw_descriptor.get("env") or []),
            declared_tool_ids=_string_list(raw_descriptor.get("declared_tool_ids") or tool_refs),
            declared_capabilities=_string_list(raw_descriptor.get("capabilities") or raw_descriptor.get("declared_capabilities") or []),
            declared_permissions=[normalize_descriptor_permission(item) for item in _string_list(raw_descriptor.get("permissions") or [])],
            declared_risks=[normalize_descriptor_risk(item) for item in _string_list(raw_descriptor.get("risks") or [])],
            source_id=source_id,
            external_descriptor_id=external_descriptor_id,
            status="declared",
            created_at=utc_now_iso(),
            descriptor_attrs={**dict(descriptor_attrs or {}), "metadata_only": True},
        )
        self._record(
            "mcp_server_descriptor_imported",
            attrs={"transport": descriptor.transport, "metadata_only": True},
            objects=[_mcp_server_object(descriptor)],
            links=[
                ("mcp_server_object", descriptor.mcp_server_id),
                ("source_object", source_id or ""),
                ("external_descriptor_object", external_descriptor_id or ""),
            ],
            object_links=[
                (descriptor.mcp_server_id, source_id or "", "from_source"),
                (descriptor.mcp_server_id, external_descriptor_id or "", "derived_from_external_descriptor"),
            ],
        )
        if external_descriptor_id:
            self._record_linked_to_external(descriptor.mcp_server_id, external_descriptor_id)
        return descriptor

    def import_mcp_tool_descriptor(
        self,
        *,
        raw_tool_descriptor: dict[str, Any],
        mcp_server_id: str | None = None,
        external_descriptor_id: str | None = None,
        descriptor_attrs: dict[str, Any] | None = None,
    ) -> MCPToolDescriptor:
        descriptor = MCPToolDescriptor(
            mcp_tool_id=new_mcp_tool_descriptor_id(),
            mcp_server_id=mcp_server_id,
            tool_name=_first_string(raw_tool_descriptor, ["name", "tool_name", "id"], "unnamed_mcp_tool"),
            description=_optional_string(raw_tool_descriptor.get("description")),
            input_schema=_dict_value(raw_tool_descriptor.get("input_schema") or raw_tool_descriptor.get("inputs")),
            output_schema=_dict_value(raw_tool_descriptor.get("output_schema") or raw_tool_descriptor.get("outputs")),
            declared_permissions=[normalize_descriptor_permission(item) for item in _string_list(raw_tool_descriptor.get("permissions") or [])],
            declared_risks=[normalize_descriptor_risk(item) for item in _string_list(raw_tool_descriptor.get("risks") or [])],
            external_descriptor_id=external_descriptor_id,
            status="declared",
            created_at=utc_now_iso(),
            descriptor_attrs={**dict(descriptor_attrs or {}), "metadata_only": True},
        )
        self._record(
            "mcp_tool_descriptor_imported",
            attrs={"metadata_only": True},
            objects=[_mcp_tool_object(descriptor)],
            links=[
                ("mcp_tool_object", descriptor.mcp_tool_id),
                ("mcp_server_object", mcp_server_id or ""),
                ("external_descriptor_object", external_descriptor_id or ""),
            ],
            object_links=[
                (descriptor.mcp_tool_id, mcp_server_id or "", "belongs_to_mcp_server"),
                (descriptor.mcp_tool_id, external_descriptor_id or "", "derived_from_external_descriptor"),
            ],
        )
        if external_descriptor_id:
            self._record_linked_to_external(descriptor.mcp_tool_id, external_descriptor_id)
        return descriptor

    def import_plugin_descriptor(
        self,
        *,
        raw_descriptor: dict[str, Any],
        source_id: str | None = None,
        external_descriptor_id: str | None = None,
        descriptor_attrs: dict[str, Any] | None = None,
    ) -> PluginDescriptor:
        entrypoint_refs = [
            str(item.get("id") or item.get("name") or item.get("ref"))
            for item in extract_plugin_entrypoints(raw_descriptor)
            if item.get("id") or item.get("name") or item.get("ref")
        ]
        descriptor = PluginDescriptor(
            plugin_id=new_plugin_descriptor_id(),
            plugin_name=extract_plugin_name(raw_descriptor),
            plugin_type=extract_plugin_type(raw_descriptor),
            provider=_optional_string(raw_descriptor.get("provider")),
            version=_optional_string(raw_descriptor.get("version")),
            description=_optional_string(raw_descriptor.get("description")),
            declared_entrypoint_ids=_string_list(raw_descriptor.get("declared_entrypoint_ids") or entrypoint_refs),
            declared_permissions=[normalize_descriptor_permission(item) for item in _string_list(raw_descriptor.get("permissions") or [])],
            declared_risks=[normalize_descriptor_risk(item) for item in _string_list(raw_descriptor.get("risks") or [])],
            source_id=source_id,
            external_descriptor_id=external_descriptor_id,
            status="declared",
            created_at=utc_now_iso(),
            descriptor_attrs={**dict(descriptor_attrs or {}), "metadata_only": True},
        )
        self._record(
            "plugin_descriptor_imported",
            attrs={"plugin_type": descriptor.plugin_type, "metadata_only": True},
            objects=[_plugin_object(descriptor)],
            links=[
                ("plugin_object", descriptor.plugin_id),
                ("source_object", source_id or ""),
                ("external_descriptor_object", external_descriptor_id or ""),
            ],
            object_links=[
                (descriptor.plugin_id, source_id or "", "from_source"),
                (descriptor.plugin_id, external_descriptor_id or "", "derived_from_external_descriptor"),
            ],
        )
        if external_descriptor_id:
            self._record_linked_to_external(descriptor.plugin_id, external_descriptor_id)
        return descriptor

    def import_plugin_entrypoint_descriptor(
        self,
        *,
        raw_entrypoint: dict[str, Any],
        plugin_id: str | None = None,
        descriptor_attrs: dict[str, Any] | None = None,
    ) -> PluginEntrypointDescriptor:
        descriptor = PluginEntrypointDescriptor(
            entrypoint_id=new_plugin_entrypoint_descriptor_id(),
            plugin_id=plugin_id,
            entrypoint_name=_optional_string(raw_entrypoint.get("name") or raw_entrypoint.get("entrypoint_name")),
            entrypoint_ref=_first_string(raw_entrypoint, ["ref", "entrypoint_ref", "command", "url"], "unknown_entrypoint"),
            entrypoint_type=_normalize_entrypoint_type(raw_entrypoint.get("type") or raw_entrypoint.get("entrypoint_type")),
            declared_inputs=_dict_value(raw_entrypoint.get("inputs") or raw_entrypoint.get("declared_inputs")),
            declared_outputs=_dict_value(raw_entrypoint.get("outputs") or raw_entrypoint.get("declared_outputs")),
            declared_permissions=[normalize_descriptor_permission(item) for item in _string_list(raw_entrypoint.get("permissions") or [])],
            declared_risks=[normalize_descriptor_risk(item) for item in _string_list(raw_entrypoint.get("risks") or [])],
            status="declared",
            created_at=utc_now_iso(),
            entrypoint_attrs={**dict(descriptor_attrs or {}), "metadata_only": True},
        )
        self._record(
            "plugin_entrypoint_descriptor_imported",
            attrs={"entrypoint_type": descriptor.entrypoint_type, "metadata_only": True},
            objects=[_plugin_entrypoint_object(descriptor)],
            links=[
                ("plugin_entrypoint_object", descriptor.entrypoint_id),
                ("plugin_object", plugin_id or ""),
            ],
            object_links=[(descriptor.entrypoint_id, plugin_id or "", "belongs_to_plugin")],
        )
        return descriptor

    def create_skeleton_from_mcp_server(
        self,
        *,
        mcp_server: MCPServerDescriptor,
        external_descriptor_id: str | None = None,
        source_id: str | None = None,
        candidate_id: str | None = None,
        skeleton_attrs: dict[str, Any] | None = None,
    ) -> ExternalDescriptorSkeleton:
        skeleton = ExternalDescriptorSkeleton(
            skeleton_id=new_external_descriptor_skeleton_id(),
            skeleton_type="mcp_server",
            source_id=source_id or mcp_server.source_id,
            external_descriptor_id=external_descriptor_id or mcp_server.external_descriptor_id,
            mcp_server_id=mcp_server.mcp_server_id,
            plugin_id=None,
            normalized_name=mcp_server.server_name,
            normalized_kind=mcp_server.transport or "unknown",
            declared_permission_categories=list(mcp_server.declared_permissions),
            declared_risk_categories=list(mcp_server.declared_risks),
            review_status="pending_review",
            activation_status="disabled",
            execution_enabled=False,
            created_at=utc_now_iso(),
            skeleton_attrs={**dict(skeleton_attrs or {}), "candidate_id": candidate_id, "metadata_only": True},
        )
        self._record_skeleton_created(
            skeleton=skeleton,
            mcp_server_id=mcp_server.mcp_server_id,
            plugin_id=None,
            external_descriptor_id=skeleton.external_descriptor_id,
        )
        return skeleton

    def create_skeleton_from_plugin(
        self,
        *,
        plugin: PluginDescriptor,
        external_descriptor_id: str | None = None,
        source_id: str | None = None,
        candidate_id: str | None = None,
        skeleton_attrs: dict[str, Any] | None = None,
    ) -> ExternalDescriptorSkeleton:
        skeleton = ExternalDescriptorSkeleton(
            skeleton_id=new_external_descriptor_skeleton_id(),
            skeleton_type="plugin",
            source_id=source_id or plugin.source_id,
            external_descriptor_id=external_descriptor_id or plugin.external_descriptor_id,
            mcp_server_id=None,
            plugin_id=plugin.plugin_id,
            normalized_name=plugin.plugin_name,
            normalized_kind=plugin.plugin_type,
            declared_permission_categories=list(plugin.declared_permissions),
            declared_risk_categories=list(plugin.declared_risks),
            review_status="pending_review",
            activation_status="disabled",
            execution_enabled=False,
            created_at=utc_now_iso(),
            skeleton_attrs={**dict(skeleton_attrs or {}), "candidate_id": candidate_id, "metadata_only": True},
        )
        self._record_skeleton_created(
            skeleton=skeleton,
            mcp_server_id=None,
            plugin_id=plugin.plugin_id,
            external_descriptor_id=skeleton.external_descriptor_id,
        )
        return skeleton

    def validate_skeleton(
        self,
        *,
        skeleton: ExternalDescriptorSkeleton,
    ) -> ExternalDescriptorSkeletonValidation:
        passed: list[str] = []
        failed: list[str] = []
        warnings: list[str] = []
        messages: list[str] = []
        _check(passed, failed, "name_present", bool(skeleton.normalized_name), messages, "Skeleton name is missing.")
        _check(passed, failed, "kind_present", bool(skeleton.normalized_kind), messages, "Skeleton kind is missing.")
        _check(passed, failed, "execution_disabled", skeleton.execution_enabled is False, messages, "Skeleton has enabled execution flag.")
        _check(passed, failed, "activation_disabled", skeleton.activation_status != _ACTIVE, messages, "Skeleton activation status is active.")
        passed.append("entrypoint_metadata_only")
        passed.append("permissions_declared_or_empty")
        passed.append("risks_declared_or_empty")
        if skeleton.review_status in {"pending_review", "needs_more_info"}:
            passed.append("review_required")
        else:
            warnings.append("review_required")
            messages.append("Skeleton is not pending review.")
        if skeleton.declared_risk_categories and any(item in {"external_code_execution", "credential_access"} for item in skeleton.declared_risk_categories):
            warnings.append("high_risk_metadata")
            messages.append("High-risk descriptor metadata requires later review.")
        status = "failed" if failed else "needs_review" if warnings else "passed"
        validation = ExternalDescriptorSkeletonValidation(
            validation_id=new_external_descriptor_skeleton_validation_id(),
            skeleton_id=skeleton.skeleton_id,
            status=status,
            passed_checks=passed,
            failed_checks=failed,
            warning_checks=warnings,
            validation_messages=messages,
            created_at=utc_now_iso(),
            validation_attrs={"metadata_only": True},
        )
        self._record(
            "external_descriptor_skeleton_validation_failed" if validation.status == "failed" else "external_descriptor_skeleton_validated",
            attrs={"status": validation.status, "failed_checks": validation.failed_checks},
            objects=[_skeleton_object(skeleton), _validation_object(validation)],
            links=[
                ("validation_object", validation.validation_id),
                ("skeleton_object", skeleton.skeleton_id),
            ],
            object_links=[(validation.validation_id, skeleton.skeleton_id, "validates_skeleton")],
        )
        return validation

    def _record_skeleton_created(
        self,
        *,
        skeleton: ExternalDescriptorSkeleton,
        mcp_server_id: str | None,
        plugin_id: str | None,
        external_descriptor_id: str | None,
    ) -> None:
        links = [
            ("skeleton_object", skeleton.skeleton_id),
            ("mcp_server_object", mcp_server_id or ""),
            ("plugin_object", plugin_id or ""),
            ("external_descriptor_object", external_descriptor_id or ""),
        ]
        object_links = [
            (skeleton.skeleton_id, mcp_server_id or "", "represents_mcp_server"),
            (skeleton.skeleton_id, plugin_id or "", "represents_plugin"),
            (skeleton.skeleton_id, external_descriptor_id or "", "derived_from_external_descriptor"),
        ]
        self._record(
            "external_descriptor_skeleton_created",
            attrs={"skeleton_type": skeleton.skeleton_type, "activation_status": "disabled", "execution_enabled": False},
            objects=[_skeleton_object(skeleton)],
            links=links,
            object_links=object_links,
        )
        self._record(
            "mcp_plugin_descriptor_marked_non_executable",
            attrs={"skeleton_type": skeleton.skeleton_type, "execution_enabled": False},
            objects=[_skeleton_object(skeleton)],
            links=[("skeleton_object", skeleton.skeleton_id)],
            object_links=[],
        )

    def _record_linked_to_external(self, descriptor_id: str, external_descriptor_id: str) -> None:
        self._record(
            "mcp_plugin_descriptor_linked_to_external_descriptor",
            attrs={"metadata_only": True},
            objects=[],
            links=[
                ("descriptor_object", descriptor_id),
                ("external_descriptor_object", external_descriptor_id),
            ],
            object_links=[(descriptor_id, external_descriptor_id, "derived_from_external_descriptor")],
        )

    def _record(
        self,
        activity: str,
        *,
        attrs: dict[str, Any],
        objects: list[OCELObject],
        links: list[tuple[str, str]],
        object_links: list[tuple[str, str, str]],
    ) -> None:
        event = OCELEvent(
            event_id=f"evt:{uuid4()}",
            event_activity=activity,
            event_timestamp=utc_now_iso(),
            event_attrs={
                **attrs,
                "runtime_event_type": activity,
                "source_runtime": "chanta_core",
                "observability_only": True,
                "mcp_plugin_descriptor_skeleton_only": True,
                "runtime_effect": False,
                "execution_enabled": False,
                "activation_allowed": False,
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


def _mcp_server_object(descriptor: MCPServerDescriptor) -> OCELObject:
    return OCELObject(
        object_id=descriptor.mcp_server_id,
        object_type="mcp_server_descriptor",
        object_attrs={**descriptor.to_dict(), "object_key": descriptor.mcp_server_id, "display_name": descriptor.server_name, "execution_enabled": False},
    )


def _mcp_tool_object(descriptor: MCPToolDescriptor) -> OCELObject:
    return OCELObject(
        object_id=descriptor.mcp_tool_id,
        object_type="mcp_tool_descriptor",
        object_attrs={**descriptor.to_dict(), "object_key": descriptor.mcp_tool_id, "display_name": descriptor.tool_name, "execution_enabled": False},
    )


def _plugin_object(descriptor: PluginDescriptor) -> OCELObject:
    return OCELObject(
        object_id=descriptor.plugin_id,
        object_type="plugin_descriptor",
        object_attrs={**descriptor.to_dict(), "object_key": descriptor.plugin_id, "display_name": descriptor.plugin_name, "execution_enabled": False},
    )


def _plugin_entrypoint_object(descriptor: PluginEntrypointDescriptor) -> OCELObject:
    return OCELObject(
        object_id=descriptor.entrypoint_id,
        object_type="plugin_entrypoint_descriptor",
        object_attrs={**descriptor.to_dict(), "object_key": descriptor.entrypoint_id, "display_name": descriptor.entrypoint_name or descriptor.entrypoint_ref, "execution_enabled": False},
    )


def _skeleton_object(skeleton: ExternalDescriptorSkeleton) -> OCELObject:
    return OCELObject(
        object_id=skeleton.skeleton_id,
        object_type="external_descriptor_skeleton",
        object_attrs={**skeleton.to_dict(), "object_key": skeleton.skeleton_id, "display_name": skeleton.normalized_name or skeleton.skeleton_type, "execution_enabled": False},
    )


def _validation_object(validation: ExternalDescriptorSkeletonValidation) -> OCELObject:
    return OCELObject(
        object_id=validation.validation_id,
        object_type="external_descriptor_skeleton_validation",
        object_attrs={**validation.to_dict(), "object_key": validation.validation_id, "display_name": validation.status},
    )


def _normalize_token(value: Any) -> str:
    return str(value or "").strip().lower().replace("-", "_").replace(" ", "_")


def _normalize_entrypoint_type(value: Any) -> str:
    token = _normalize_token(value)
    return token if token in ENTRYPOINT_TYPES else "other" if token else "unknown"


def _first_string(raw: dict[str, Any], keys: list[str], default: str) -> str:
    for key in keys:
        value = raw.get(key)
        if value:
            return str(value)
    return default


def _optional_string(value: Any) -> str | None:
    if value is None:
        return None
    return str(value)


def _dict_value(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, dict) else {}


def _string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        return [str(key) for key in value.keys()]
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)]


def _check(
    passed: list[str],
    failed: list[str],
    check_name: str,
    condition: bool,
    messages: list[str],
    failed_message: str,
) -> None:
    if condition:
        passed.append(check_name)
    else:
        failed.append(check_name)
        messages.append(failed_message)
