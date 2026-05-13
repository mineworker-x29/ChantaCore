from __future__ import annotations

import hashlib
import json
import re
import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from uuid import uuid4

from chanta_core.observation_digest import (
    DigestionService,
    ExternalSkillAdapterCandidate,
    ExternalSkillAssimilationCandidate,
    ExternalSkillSourceDescriptor,
    ExternalSkillStaticProfile,
)
from chanta_core.ocel.models import OCELEvent, OCELObject, OCELRecord, OCELRelation
from chanta_core.ocel.store import OCELStore
from chanta_core.skills.ids import (
    new_external_skill_declared_capability_id,
    new_external_skill_instruction_profile_id,
    new_external_skill_manifest_profile_id,
    new_external_skill_resource_inventory_id,
    new_external_skill_static_digestion_finding_id,
    new_external_skill_static_digestion_report_id,
    new_external_skill_static_risk_profile_id,
)
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso
from chanta_core.workspace import (
    WorkspacePathViolationError,
    WorkspaceReadRootError,
    resolve_workspace_path,
)


MARKDOWN_SUFFIXES = {".md", ".markdown"}
MANIFEST_NAMES = {
    "manifest.json",
    "plugin.json",
    "package.json",
    "skill.json",
    "skill.yaml",
    "skill.yml",
    "manifest.yaml",
    "manifest.yml",
    "skill.toml",
    "manifest.toml",
    "pyproject.toml",
}
MANIFEST_SUFFIXES = {".json", ".yaml", ".yml", ".toml"}
SCRIPT_SUFFIXES = {".py", ".js", ".ts", ".mjs", ".sh", ".ps1", ".bat", ".cmd"}
ASSET_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".mp3", ".wav", ".mp4", ".mov"}
PRIVATE_PATH_TERMS = {"private", "sensitive", "confidential", "restricted"}
READ_TERMS = {"read", "search", "summarize", "inspect", "parse", "inventory", "scan"}
SHELL_TERMS = {"shell", "command", "bash", "powershell", "terminal", "process spawn"}
NETWORK_TERMS = {"network", "http", "https", "url", "web", "request", "api"}
WRITE_TERMS = {"write", "edit", "patch", "apply", "delete", "create file", "modify"}
MCP_TERMS = {"mcp", "server"}
PLUGIN_TERMS = {"plugin", "extension"}
EXTERNAL_RUN_TERMS = {"harness", "external execution", "execute external", "script execution"}


@dataclass(frozen=True)
class ExternalSkillResourceInventory:
    inventory_id: str
    source_descriptor_id: str
    source_root_ref: str | None
    resource_count: int
    markdown_files: list[str]
    manifest_files: list[str]
    script_files: list[str]
    reference_files: list[str]
    asset_files: list[str]
    agent_config_files: list[str]
    mcp_config_files: list[str]
    unknown_files: list[str]
    denied_files: list[str]
    private: bool
    sensitive: bool
    created_at: str
    inventory_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "inventory_id": self.inventory_id,
            "source_descriptor_id": self.source_descriptor_id,
            "source_root_ref": self.source_root_ref,
            "resource_count": self.resource_count,
            "markdown_files": list(self.markdown_files),
            "manifest_files": list(self.manifest_files),
            "script_files": list(self.script_files),
            "reference_files": list(self.reference_files),
            "asset_files": list(self.asset_files),
            "agent_config_files": list(self.agent_config_files),
            "mcp_config_files": list(self.mcp_config_files),
            "unknown_files": list(self.unknown_files),
            "denied_files": list(self.denied_files),
            "private": self.private,
            "sensitive": self.sensitive,
            "created_at": self.created_at,
            "inventory_attrs": dict(self.inventory_attrs),
        }


@dataclass(frozen=True)
class ExternalSkillManifestProfile:
    manifest_profile_id: str
    source_descriptor_id: str
    manifest_ref: str | None
    manifest_kind: str
    parsed_name: str | None
    parsed_description: str | None
    parsed_version: str | None
    parsed_author: str | None
    declared_tools: list[str]
    declared_permissions: list[str]
    declared_inputs: list[str]
    declared_outputs: list[str]
    declared_runtime_requirements: list[str]
    parse_status: str
    confidence: float
    created_at: str
    manifest_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "confidence", _clamp_confidence(self.confidence))

    def to_dict(self) -> dict[str, Any]:
        return {
            "manifest_profile_id": self.manifest_profile_id,
            "source_descriptor_id": self.source_descriptor_id,
            "manifest_ref": self.manifest_ref,
            "manifest_kind": self.manifest_kind,
            "parsed_name": self.parsed_name,
            "parsed_description": self.parsed_description,
            "parsed_version": self.parsed_version,
            "parsed_author": self.parsed_author,
            "declared_tools": list(self.declared_tools),
            "declared_permissions": list(self.declared_permissions),
            "declared_inputs": list(self.declared_inputs),
            "declared_outputs": list(self.declared_outputs),
            "declared_runtime_requirements": list(self.declared_runtime_requirements),
            "parse_status": self.parse_status,
            "confidence": self.confidence,
            "created_at": self.created_at,
            "manifest_attrs": dict(self.manifest_attrs),
        }


@dataclass(frozen=True)
class ExternalSkillInstructionProfile:
    instruction_profile_id: str
    source_descriptor_id: str
    instruction_ref: str | None
    instruction_kind: str
    title: str | None
    instruction_preview: str | None
    declared_behavior: list[str]
    declared_constraints: list[str]
    declared_tools: list[str]
    declared_outputs: list[str]
    max_preview_chars: int
    full_body_stored: bool
    confidence: float
    created_at: str
    instruction_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "confidence", _clamp_confidence(self.confidence))

    def to_dict(self) -> dict[str, Any]:
        return {
            "instruction_profile_id": self.instruction_profile_id,
            "source_descriptor_id": self.source_descriptor_id,
            "instruction_ref": self.instruction_ref,
            "instruction_kind": self.instruction_kind,
            "title": self.title,
            "instruction_preview": self.instruction_preview,
            "declared_behavior": list(self.declared_behavior),
            "declared_constraints": list(self.declared_constraints),
            "declared_tools": list(self.declared_tools),
            "declared_outputs": list(self.declared_outputs),
            "max_preview_chars": self.max_preview_chars,
            "full_body_stored": self.full_body_stored,
            "confidence": self.confidence,
            "created_at": self.created_at,
            "instruction_attrs": dict(self.instruction_attrs),
        }


@dataclass(frozen=True)
class ExternalSkillDeclaredCapability:
    declared_capability_id: str
    source_descriptor_id: str
    static_profile_id: str | None
    capability_name: str
    capability_category: str
    declared_actions: list[str]
    declared_objects: list[str]
    declared_inputs: list[str]
    declared_outputs: list[str]
    declared_side_effects: list[str]
    declared_risk_class: str
    confidence: float
    created_at: str
    capability_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "confidence", _clamp_confidence(self.confidence))

    def to_dict(self) -> dict[str, Any]:
        return {
            "declared_capability_id": self.declared_capability_id,
            "source_descriptor_id": self.source_descriptor_id,
            "static_profile_id": self.static_profile_id,
            "capability_name": self.capability_name,
            "capability_category": self.capability_category,
            "declared_actions": list(self.declared_actions),
            "declared_objects": list(self.declared_objects),
            "declared_inputs": list(self.declared_inputs),
            "declared_outputs": list(self.declared_outputs),
            "declared_side_effects": list(self.declared_side_effects),
            "declared_risk_class": self.declared_risk_class,
            "confidence": self.confidence,
            "created_at": self.created_at,
            "capability_attrs": dict(self.capability_attrs),
        }


@dataclass(frozen=True)
class ExternalSkillStaticRiskProfile:
    static_risk_profile_id: str
    source_descriptor_id: str
    risk_class: str
    declared_read_only: bool
    declared_write: bool
    declared_shell: bool
    declared_network: bool
    declared_mcp: bool
    declared_plugin: bool
    declared_external_execution: bool
    declared_private_context_access: bool
    risk_evidence_refs: list[str]
    requires_review: bool
    execution_allowed_by_default: bool
    created_at: str
    risk_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "static_risk_profile_id": self.static_risk_profile_id,
            "source_descriptor_id": self.source_descriptor_id,
            "risk_class": self.risk_class,
            "declared_read_only": self.declared_read_only,
            "declared_write": self.declared_write,
            "declared_shell": self.declared_shell,
            "declared_network": self.declared_network,
            "declared_mcp": self.declared_mcp,
            "declared_plugin": self.declared_plugin,
            "declared_external_execution": self.declared_external_execution,
            "declared_private_context_access": self.declared_private_context_access,
            "risk_evidence_refs": list(self.risk_evidence_refs),
            "requires_review": self.requires_review,
            "execution_allowed_by_default": self.execution_allowed_by_default,
            "created_at": self.created_at,
            "risk_attrs": dict(self.risk_attrs),
        }


@dataclass(frozen=True)
class ExternalSkillStaticDigestionReport:
    report_id: str
    source_descriptor_id: str
    inventory_id: str | None
    manifest_profile_ids: list[str]
    instruction_profile_ids: list[str]
    declared_capability_ids: list[str]
    static_risk_profile_id: str | None
    static_profile_id: str | None
    assimilation_candidate_id: str | None
    adapter_candidate_ids: list[str]
    finding_ids: list[str]
    status: str
    summary: str
    created_at: str
    report_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "report_id": self.report_id,
            "source_descriptor_id": self.source_descriptor_id,
            "inventory_id": self.inventory_id,
            "manifest_profile_ids": list(self.manifest_profile_ids),
            "instruction_profile_ids": list(self.instruction_profile_ids),
            "declared_capability_ids": list(self.declared_capability_ids),
            "static_risk_profile_id": self.static_risk_profile_id,
            "static_profile_id": self.static_profile_id,
            "assimilation_candidate_id": self.assimilation_candidate_id,
            "adapter_candidate_ids": list(self.adapter_candidate_ids),
            "finding_ids": list(self.finding_ids),
            "status": self.status,
            "summary": self.summary,
            "created_at": self.created_at,
            "report_attrs": dict(self.report_attrs),
        }


@dataclass(frozen=True)
class ExternalSkillStaticDigestionFinding:
    finding_id: str
    source_descriptor_id: str | None
    subject_ref: str | None
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
            "source_descriptor_id": self.source_descriptor_id,
            "subject_ref": self.subject_ref,
            "finding_type": self.finding_type,
            "status": self.status,
            "severity": self.severity,
            "message": self.message,
            "evidence_ref": self.evidence_ref,
            "created_at": self.created_at,
            "finding_attrs": dict(self.finding_attrs),
        }


class ExternalSkillStaticDigestionService:
    def __init__(
        self,
        *,
        digestion_service: DigestionService | None = None,
        trace_service: TraceService | None = None,
        ocel_store: OCELStore | None = None,
    ) -> None:
        if trace_service is not None:
            self.trace_service = trace_service
        elif ocel_store is not None:
            self.trace_service = TraceService(ocel_store=ocel_store)
        else:
            self.trace_service = TraceService()
        self.digestion_service = digestion_service or DigestionService(trace_service=self.trace_service)
        self.last_inventory: ExternalSkillResourceInventory | None = None
        self.last_manifest_profiles: list[ExternalSkillManifestProfile] = []
        self.last_instruction_profiles: list[ExternalSkillInstructionProfile] = []
        self.last_declared_capabilities: list[ExternalSkillDeclaredCapability] = []
        self.last_risk_profile: ExternalSkillStaticRiskProfile | None = None
        self.last_report: ExternalSkillStaticDigestionReport | None = None
        self.last_findings: list[ExternalSkillStaticDigestionFinding] = []
        self.last_candidate: ExternalSkillAssimilationCandidate | None = None
        self.last_adapter_hints: list[ExternalSkillAdapterCandidate] = []

    def inspect_resource_inventory(
        self,
        *,
        root_path: str,
        relative_path: str,
        source_descriptor: ExternalSkillSourceDescriptor | None = None,
    ) -> ExternalSkillResourceInventory:
        descriptor_id = source_descriptor.source_descriptor_id if source_descriptor else ""
        markdown_files: list[str] = []
        manifest_files: list[str] = []
        script_files: list[str] = []
        reference_files: list[str] = []
        asset_files: list[str] = []
        agent_config_files: list[str] = []
        mcp_config_files: list[str] = []
        unknown_files: list[str] = []
        denied_files: list[str] = []
        status = "completed"
        try:
            target = resolve_workspace_path(root_path, relative_path)
        except (WorkspacePathViolationError, WorkspaceReadRootError) as error:
            status = "blocked"
            self.record_finding(
                source_descriptor_id=descriptor_id or None,
                subject_ref=relative_path,
                finding_type="workspace_boundary_violation",
                status="blocked",
                severity="high",
                message=str(error),
                evidence_ref="path_validation",
            )
            target = None
        if target is not None and not target.exists():
            status = "missing"
            self.record_finding(
                source_descriptor_id=descriptor_id or None,
                subject_ref=_redacted_ref(relative_path),
                finding_type="source_missing",
                status="warning",
                severity="medium",
                message="External skill source path was not found.",
                evidence_ref="path_validation",
            )
        files = _iter_source_files(target) if target is not None and target.exists() else []
        for path in files:
            ref = _redacted_ref(_relative_ref(path, target if target and target.is_dir() else path.parent))
            if _is_private_ref(ref):
                denied_files.append(ref)
                continue
            categories = _classify_resource(path)
            if "markdown" in categories:
                markdown_files.append(ref)
            if "manifest" in categories:
                manifest_files.append(ref)
            if "script" in categories:
                script_files.append(ref)
            if "reference" in categories:
                reference_files.append(ref)
            if "asset" in categories:
                asset_files.append(ref)
            if "agent_config" in categories:
                agent_config_files.append(ref)
            if "mcp_config" in categories:
                mcp_config_files.append(ref)
            if categories == {"unknown"}:
                unknown_files.append(ref)
        if script_files:
            self.record_finding(
                source_descriptor_id=descriptor_id or None,
                subject_ref=descriptor_id or _redacted_ref(relative_path),
                finding_type="script_present",
                status="review_required",
                severity="medium",
                message="Script files were inventoried but not executed.",
                evidence_ref="resource_inventory",
            )
        private = bool(denied_files) or _is_private_ref(relative_path)
        inventory = ExternalSkillResourceInventory(
            inventory_id=new_external_skill_resource_inventory_id(),
            source_descriptor_id=descriptor_id,
            source_root_ref=_redacted_ref(relative_path) if status != "blocked" else None,
            resource_count=len(files),
            markdown_files=markdown_files,
            manifest_files=manifest_files,
            script_files=script_files,
            reference_files=reference_files,
            asset_files=asset_files,
            agent_config_files=agent_config_files,
            mcp_config_files=mcp_config_files,
            unknown_files=unknown_files,
            denied_files=denied_files,
            private=private,
            sensitive=private,
            created_at=utc_now_iso(),
            inventory_attrs={
                "status": status,
                "read_only": True,
                "script_execution_used": False,
                "external_harness_execution_used": False,
                "full_raw_body_stored": False,
            },
        )
        self.last_inventory = inventory
        self._record_model(
            "external_skill_resource_inventory_created",
            "external_skill_resource_inventory",
            inventory.inventory_id,
            inventory,
            links=[("external_skill_source_descriptor_object", descriptor_id)] if descriptor_id else None,
            object_links=[(inventory.inventory_id, descriptor_id, "resource_inventory_belongs_to_source_descriptor")]
            if descriptor_id
            else None,
        )
        return inventory

    def parse_skill_md_frontmatter(
        self,
        *,
        root_path: str,
        relative_path: str,
        source_descriptor: ExternalSkillSourceDescriptor,
    ) -> ExternalSkillManifestProfile:
        target = self._resolve_instruction_path(root_path, relative_path)
        raw = _safe_read_preview(target, max_chars=12000) if target and target.exists() else ""
        frontmatter = _extract_frontmatter(raw)
        data = _parse_simple_mapping(frontmatter) if frontmatter else {}
        status = "parsed" if data else "no_frontmatter" if raw else "missing"
        profile = self._manifest_profile_from_mapping(
            source_descriptor=source_descriptor,
            manifest_ref=_redacted_ref(_relative_ref(target, target.parent)) if target else None,
            manifest_kind="skill_md_frontmatter",
            data=data,
            parse_status=status,
            confidence=0.8 if data else 0.35 if raw else 0.0,
        )
        return profile

    def parse_generic_manifest(
        self,
        *,
        root_path: str,
        relative_path: str,
        manifest_ref: str,
        source_descriptor: ExternalSkillSourceDescriptor,
    ) -> ExternalSkillManifestProfile:
        target = _resolve_child(root_path, relative_path, manifest_ref)
        if target is None or not target.exists() or not target.is_file():
            return self._manifest_profile_from_mapping(
                source_descriptor=source_descriptor,
                manifest_ref=_redacted_ref(manifest_ref),
                manifest_kind="unknown",
                data={},
                parse_status="missing",
                confidence=0.0,
            )
        raw = _safe_read_preview(target, max_chars=20000)
        kind = _manifest_kind(target)
        try:
            data = _parse_manifest_text(raw, kind)
            status = "parsed"
            confidence = 0.75 if data else 0.35
        except (ValueError, json.JSONDecodeError, tomllib.TOMLDecodeError) as error:
            data = {}
            status = "failed"
            confidence = 0.0
            self.record_finding(
                source_descriptor_id=source_descriptor.source_descriptor_id,
                subject_ref=_redacted_ref(manifest_ref),
                finding_type="manifest_parse_failed",
                status="warning",
                severity="medium",
                message=f"Manifest parse failed safely: {error}",
                evidence_ref=_redacted_ref(manifest_ref),
            )
        return self._manifest_profile_from_mapping(
            source_descriptor=source_descriptor,
            manifest_ref=_redacted_ref(manifest_ref),
            manifest_kind=kind,
            data=data,
            parse_status=status,
            confidence=confidence,
        )

    def parse_instruction_profile(
        self,
        *,
        root_path: str,
        relative_path: str,
        source_descriptor: ExternalSkillSourceDescriptor,
        max_preview_chars: int = 800,
    ) -> ExternalSkillInstructionProfile:
        target = self._resolve_instruction_path(root_path, relative_path)
        raw = _safe_read_preview(target, max_chars=max(2000, max_preview_chars * 4)) if target and target.exists() else ""
        title = _first_markdown_title(raw)
        profile = ExternalSkillInstructionProfile(
            instruction_profile_id=new_external_skill_instruction_profile_id(),
            source_descriptor_id=source_descriptor.source_descriptor_id,
            instruction_ref=_redacted_ref(_relative_ref(target, target.parent)) if target else None,
            instruction_kind="skill_md" if target and target.name == "SKILL.md" else "markdown",
            title=title,
            instruction_preview=_preview_text(raw, max_preview_chars) if raw else None,
            declared_behavior=_matching_lines(raw, ["behavior", "does", "capability", "can "], max_items=8),
            declared_constraints=_matching_lines(raw, ["do not", "must not", "constraint", "boundary"], max_items=8),
            declared_tools=_extract_terms(raw, READ_TERMS | SHELL_TERMS | NETWORK_TERMS | MCP_TERMS | PLUGIN_TERMS),
            declared_outputs=_extract_list_like(raw, ["outputs", "returns", "result"]),
            max_preview_chars=max_preview_chars,
            full_body_stored=False,
            confidence=0.75 if raw else 0.0,
            created_at=utc_now_iso(),
            instruction_attrs={
                "content_hash": _hash_text(raw) if raw else None,
                "read_only": True,
                "full_raw_body_stored": False,
            },
        )
        self.last_instruction_profiles.append(profile)
        self._record_model(
            "external_skill_instruction_profile_created",
            "external_skill_instruction_profile",
            profile.instruction_profile_id,
            profile,
            links=[("external_skill_source_descriptor_object", source_descriptor.source_descriptor_id)],
            object_links=[
                (
                    profile.instruction_profile_id,
                    source_descriptor.source_descriptor_id,
                    "instruction_profile_derived_from_source_descriptor",
                )
            ],
        )
        return profile

    def extract_declared_capabilities(
        self,
        *,
        source_descriptor: ExternalSkillSourceDescriptor,
        manifest_profiles: list[ExternalSkillManifestProfile] | None = None,
        instruction_profiles: list[ExternalSkillInstructionProfile] | None = None,
        static_profile: ExternalSkillStaticProfile | None = None,
    ) -> list[ExternalSkillDeclaredCapability]:
        manifest_profiles = list(manifest_profiles or [])
        instruction_profiles = list(instruction_profiles or [])
        static_text = (
            [static_profile.declared_description or "", static_profile.instruction_preview or ""]
            if static_profile is not None
            else []
        )
        combined_text = " ".join(
            [
                *(profile.parsed_description or "" for profile in manifest_profiles),
                *(profile.instruction_preview or "" for profile in instruction_profiles),
                *static_text,
            ]
        )
        actions = _extract_terms(combined_text, READ_TERMS | WRITE_TERMS | SHELL_TERMS | NETWORK_TERMS | MCP_TERMS | PLUGIN_TERMS)
        inputs = _unique(
            [
                *(item for profile in manifest_profiles for item in profile.declared_inputs),
                *(static_profile.declared_inputs if static_profile else []),
            ]
        )
        outputs = _unique(
            [
                *(item for profile in manifest_profiles for item in profile.declared_outputs),
                *(item for profile in instruction_profiles for item in profile.declared_outputs),
                *(static_profile.declared_outputs if static_profile else []),
            ]
        )
        if not actions:
            actions = ["inspect"] if manifest_profiles or instruction_profiles else ["unknown"]
        risk_class = "read_only"
        side_effects: list[str] = []
        if any(action in WRITE_TERMS for action in actions):
            risk_class = "high"
            side_effects.append("write_declared")
        if any(action in SHELL_TERMS for action in actions):
            risk_class = "high"
            side_effects.append("shell_declared")
        if any(action in NETWORK_TERMS for action in actions):
            risk_class = "high"
            side_effects.append("network_declared")
        if any(action in MCP_TERMS for action in actions):
            risk_class = "high"
            side_effects.append("mcp_declared")
        if any(action in PLUGIN_TERMS for action in actions):
            risk_class = "high"
            side_effects.append("plugin_declared")
        capability = ExternalSkillDeclaredCapability(
            declared_capability_id=new_external_skill_declared_capability_id(),
            source_descriptor_id=source_descriptor.source_descriptor_id,
            static_profile_id=static_profile.static_profile_id if static_profile else None,
            capability_name=(static_profile.declared_name if static_profile else None) or "external_static_capability",
            capability_category="read_only" if risk_class == "read_only" else "external_risky_static",
            declared_actions=actions,
            declared_objects=["external_skill_source"],
            declared_inputs=inputs,
            declared_outputs=outputs,
            declared_side_effects=side_effects,
            declared_risk_class=risk_class,
            confidence=0.75 if combined_text else 0.35,
            created_at=utc_now_iso(),
            capability_attrs={
                "read_only_analysis": True,
                "execution_enabled": False,
                "canonical_import_enabled": False,
            },
        )
        self.last_declared_capabilities.append(capability)
        self._record_model(
            "external_skill_declared_capability_created",
            "external_skill_declared_capability",
            capability.declared_capability_id,
            capability,
            links=[("external_skill_source_descriptor_object", source_descriptor.source_descriptor_id)],
            object_links=[
                (
                    capability.declared_capability_id,
                    source_descriptor.source_descriptor_id,
                    "declared_capability_derived_from_source_descriptor",
                )
            ],
        )
        return [capability]

    def infer_static_risk_profile(
        self,
        *,
        source_descriptor: ExternalSkillSourceDescriptor,
        inventory: ExternalSkillResourceInventory | None = None,
        manifest_profiles: list[ExternalSkillManifestProfile] | None = None,
        instruction_profiles: list[ExternalSkillInstructionProfile] | None = None,
        declared_capabilities: list[ExternalSkillDeclaredCapability] | None = None,
    ) -> ExternalSkillStaticRiskProfile:
        manifest_profiles = list(manifest_profiles or [])
        instruction_profiles = list(instruction_profiles or [])
        declared_capabilities = list(declared_capabilities or [])
        text = " ".join(
            [
                *(profile.parsed_description or "" for profile in manifest_profiles),
                *(" ".join(profile.declared_permissions) for profile in manifest_profiles),
                *(profile.instruction_preview or "" for profile in instruction_profiles),
                *(" ".join(cap.declared_actions + cap.declared_side_effects) for cap in declared_capabilities),
            ]
        ).lower()
        declared_shell = bool(inventory and inventory.script_files) or _contains_any(text, SHELL_TERMS)
        declared_network = _contains_any(text, NETWORK_TERMS)
        declared_write = _contains_any(text, WRITE_TERMS)
        declared_mcp = bool(inventory and inventory.mcp_config_files) or _contains_any(text, MCP_TERMS)
        declared_plugin = _contains_any(text, PLUGIN_TERMS)
        declared_external = _contains_any(text, EXTERNAL_RUN_TERMS)
        declared_private = _contains_any(text, PRIVATE_PATH_TERMS)
        declared_read_only = _contains_any(text, READ_TERMS) and not any(
            [declared_shell, declared_network, declared_write, declared_mcp, declared_plugin, declared_external]
        )
        evidence_refs: list[str] = []
        for label, enabled, severity in [
            ("shell_declared", declared_shell, "high"),
            ("network_declared", declared_network, "high"),
            ("write_declared", declared_write, "high"),
            ("mcp_declared", declared_mcp, "high"),
            ("plugin_declared", declared_plugin, "high"),
            ("external_execution_declared", declared_external, "high"),
            ("private_context_risk", declared_private, "high"),
        ]:
            if enabled:
                evidence_refs.append(label)
                self.record_finding(
                    source_descriptor_id=source_descriptor.source_descriptor_id,
                    subject_ref=source_descriptor.source_descriptor_id,
                    finding_type=label,
                    status="review_required",
                    severity=severity,
                    message=f"Static digestion detected {label.replace('_', ' ')}.",
                    evidence_ref=label,
                )
        if any([declared_shell, declared_network, declared_write, declared_mcp, declared_plugin, declared_external, declared_private]):
            risk_class = "high"
        elif inventory and inventory.script_files:
            risk_class = "medium"
        elif declared_read_only:
            risk_class = "read_only"
        else:
            risk_class = "unknown"
        profile = ExternalSkillStaticRiskProfile(
            static_risk_profile_id=new_external_skill_static_risk_profile_id(),
            source_descriptor_id=source_descriptor.source_descriptor_id,
            risk_class=risk_class,
            declared_read_only=declared_read_only,
            declared_write=declared_write,
            declared_shell=declared_shell,
            declared_network=declared_network,
            declared_mcp=declared_mcp,
            declared_plugin=declared_plugin,
            declared_external_execution=declared_external,
            declared_private_context_access=declared_private,
            risk_evidence_refs=evidence_refs,
            requires_review=True,
            execution_allowed_by_default=False,
            created_at=utc_now_iso(),
            risk_attrs={
                "read_only_analysis": True,
                "candidate_only": True,
                "script_execution_used": False,
                "external_harness_execution_used": False,
            },
        )
        self.last_risk_profile = profile
        self._record_model(
            "external_skill_static_risk_profile_created",
            "external_skill_static_risk_profile",
            profile.static_risk_profile_id,
            profile,
            links=[("external_skill_source_descriptor_object", source_descriptor.source_descriptor_id)],
            object_links=[
                (
                    profile.static_risk_profile_id,
                    source_descriptor.source_descriptor_id,
                    "static_risk_profile_derived_from_source_descriptor",
                )
            ],
        )
        return profile

    def create_static_digestion_report(
        self,
        *,
        root_path: str,
        relative_path: str,
        vendor_hint: str | None = None,
        create_candidate: bool = True,
        create_adapter_hints: bool = True,
    ) -> ExternalSkillStaticDigestionReport:
        self.last_manifest_profiles = []
        self.last_instruction_profiles = []
        self.last_declared_capabilities = []
        self.last_adapter_hints = []
        descriptor = self.digestion_service.inspect_external_skill_source(
            root_path=root_path,
            relative_path=relative_path,
            vendor_hint=vendor_hint,
        )
        inventory = self.inspect_resource_inventory(
            root_path=root_path,
            relative_path=relative_path,
            source_descriptor=descriptor,
        )
        skill_profile = self.parse_skill_md_frontmatter(
            root_path=root_path,
            relative_path=relative_path,
            source_descriptor=descriptor,
        )
        manifest_profiles = [skill_profile]
        for manifest_ref in inventory.manifest_files:
            if manifest_ref == "SKILL.md":
                continue
            manifest_profiles.append(
                self.parse_generic_manifest(
                    root_path=root_path,
                    relative_path=relative_path,
                    manifest_ref=manifest_ref,
                    source_descriptor=descriptor,
                )
            )
        instruction = self.parse_instruction_profile(
            root_path=root_path,
            relative_path=relative_path,
            source_descriptor=descriptor,
        )
        static_profile = self.digestion_service.create_static_profile(
            source_descriptor=descriptor,
            root_path=root_path,
            relative_path=relative_path,
        )
        capabilities = self.extract_declared_capabilities(
            source_descriptor=descriptor,
            manifest_profiles=manifest_profiles,
            instruction_profiles=[instruction],
            static_profile=static_profile,
        )
        risk = self.infer_static_risk_profile(
            source_descriptor=descriptor,
            inventory=inventory,
            manifest_profiles=manifest_profiles,
            instruction_profiles=[instruction],
            declared_capabilities=capabilities,
        )
        candidate = (
            self.create_assimilation_candidate_from_report(static_profile=static_profile, risk_profile=risk)
            if create_candidate
            else None
        )
        adapters = self.create_adapter_hints_from_report(candidate=candidate) if create_adapter_hints and candidate else []
        status = "blocked" if inventory.inventory_attrs.get("status") == "blocked" else "completed_with_findings" if self.last_findings else "completed"
        report = ExternalSkillStaticDigestionReport(
            report_id=new_external_skill_static_digestion_report_id(),
            source_descriptor_id=descriptor.source_descriptor_id,
            inventory_id=inventory.inventory_id,
            manifest_profile_ids=[profile.manifest_profile_id for profile in manifest_profiles],
            instruction_profile_ids=[instruction.instruction_profile_id],
            declared_capability_ids=[cap.declared_capability_id for cap in capabilities],
            static_risk_profile_id=risk.static_risk_profile_id,
            static_profile_id=static_profile.static_profile_id,
            assimilation_candidate_id=candidate.candidate_id if candidate else None,
            adapter_candidate_ids=[adapter.adapter_candidate_id for adapter in adapters],
            finding_ids=[finding.finding_id for finding in self.last_findings],
            status=status,
            summary=(
                "External skill static digestion completed: "
                f"resources={inventory.resource_count}, manifests={len(manifest_profiles)}, "
                f"capabilities={len(capabilities)}, risk={risk.risk_class}."
            ),
            created_at=utc_now_iso(),
            report_attrs={
                "read_only": True,
                "canonical_import_enabled": False,
                "execution_enabled": False,
                "script_execution_used": False,
                "external_harness_execution_used": False,
                "full_raw_body_stored": False,
            },
        )
        self.last_report = report
        self._record_model(
            "external_skill_static_digestion_report_created",
            "external_skill_static_digestion_report",
            report.report_id,
            report,
            links=[("external_skill_source_descriptor_object", descriptor.source_descriptor_id)],
            object_links=[
                (report.report_id, descriptor.source_descriptor_id, "static_digestion_report_summarizes_source_descriptor"),
                (report.report_id, inventory.inventory_id, "static_digestion_report_includes_inventory"),
                (report.report_id, risk.static_risk_profile_id, "static_digestion_report_includes_static_risk_profile"),
            ],
        )
        return report

    def create_static_profile_from_report(
        self,
        report: ExternalSkillStaticDigestionReport | None = None,
    ) -> ExternalSkillStaticProfile | None:
        _ = report
        return self.digestion_service.last_static_profile

    def create_assimilation_candidate_from_report(
        self,
        report: ExternalSkillStaticDigestionReport | None = None,
        *,
        static_profile: ExternalSkillStaticProfile | None = None,
        risk_profile: ExternalSkillStaticRiskProfile | None = None,
    ) -> ExternalSkillAssimilationCandidate | None:
        _ = report
        profile = static_profile or self.digestion_service.last_static_profile
        if profile is None:
            return None
        candidate = self.digestion_service.create_assimilation_candidate(
            static_profile=profile,
            source_runtime="external_static_digest",
        )
        if risk_profile is not None:
            candidate = ExternalSkillAssimilationCandidate(
                **{
                    **candidate.to_dict(),
                    "risk_class": risk_profile.risk_class,
                    "candidate_attrs": {
                        **candidate.candidate_attrs,
                        "static_risk_profile_id": risk_profile.static_risk_profile_id,
                    },
                }
            )
        self.last_candidate = candidate
        return candidate

    def create_adapter_hints_from_report(
        self,
        report: ExternalSkillStaticDigestionReport | None = None,
        *,
        candidate: ExternalSkillAssimilationCandidate | None = None,
    ) -> list[ExternalSkillAdapterCandidate]:
        _ = report
        selected = candidate or self.last_candidate
        if selected is None:
            return []
        adapter = self.digestion_service.create_adapter_candidate(candidate=selected)
        self.last_adapter_hints = [adapter]
        return [adapter]

    def record_finding(
        self,
        *,
        source_descriptor_id: str | None,
        subject_ref: str | None,
        finding_type: str,
        status: str,
        severity: str,
        message: str,
        evidence_ref: str | None = None,
        finding_attrs: dict[str, Any] | None = None,
    ) -> ExternalSkillStaticDigestionFinding:
        finding = ExternalSkillStaticDigestionFinding(
            finding_id=new_external_skill_static_digestion_finding_id(),
            source_descriptor_id=source_descriptor_id,
            subject_ref=subject_ref,
            finding_type=finding_type,
            status=status,
            severity=severity,
            message=message,
            evidence_ref=evidence_ref,
            created_at=utc_now_iso(),
            finding_attrs={
                "read_only": True,
                "execution_enabled": False,
                **dict(finding_attrs or {}),
            },
        )
        self.last_findings.append(finding)
        self._record_model(
            "external_skill_static_digestion_finding_recorded",
            "external_skill_static_digestion_finding",
            finding.finding_id,
            finding,
        )
        return finding

    def render_static_digestion_cli(self, value: Any | None = None) -> str:
        item = value or self.last_report or self.last_risk_profile or self.last_inventory
        if item is None:
            return "External Skill Static Digestion: unavailable"
        data = item.to_dict() if hasattr(item, "to_dict") else dict(item)
        report = data if "report_id" in data else (self.last_report.to_dict() if self.last_report else {})
        inventory = self.last_inventory
        risk = self.last_risk_profile
        lines = ["External Skill Static Digestion"]
        for key in ["status", "report_id", "source_descriptor_id", "static_profile_id", "assimilation_candidate_id", "summary"]:
            if report.get(key) is not None:
                lines.append(f"{key}={report[key]}")
        if inventory is not None:
            lines.append(f"resource_count={inventory.resource_count}")
            lines.append(f"markdown_count={len(inventory.markdown_files)}")
            lines.append(f"manifest_count={len(inventory.manifest_files)}")
            lines.append(f"script_count={len(inventory.script_files)}")
            lines.append(f"reference_count={len(inventory.reference_files)}")
            lines.append(f"asset_count={len(inventory.asset_files)}")
        lines.append(f"instruction_profile_count={len(self.last_instruction_profiles)}")
        lines.append(f"declared_capability_count={len(self.last_declared_capabilities)}")
        if risk is not None:
            lines.append(f"risk_class={risk.risk_class}")
            lines.append(f"execution_allowed_by_default={str(risk.execution_allowed_by_default).lower()}")
        lines.append(f"finding_count={len(self.last_findings)}")
        lines.append("read_only=true")
        lines.append("full_raw_body_stored=false")
        lines.append("canonical_import_enabled=false")
        lines.append("execution_enabled=false")
        lines.append("script_execution_used=false")
        lines.append("external_harness_execution_used=false")
        return "\n".join(lines)

    def _resolve_instruction_path(self, root_path: str, relative_path: str) -> Path | None:
        try:
            target = resolve_workspace_path(root_path, relative_path)
        except (WorkspacePathViolationError, WorkspaceReadRootError) as error:
            self.record_finding(
                source_descriptor_id=None,
                subject_ref=relative_path,
                finding_type="workspace_boundary_violation",
                status="blocked",
                severity="high",
                message=str(error),
                evidence_ref="path_validation",
            )
            return None
        if target.is_dir():
            skill_file = target / "SKILL.md"
            return skill_file if skill_file.exists() else None
        return target

    def _manifest_profile_from_mapping(
        self,
        *,
        source_descriptor: ExternalSkillSourceDescriptor,
        manifest_ref: str | None,
        manifest_kind: str,
        data: dict[str, Any],
        parse_status: str,
        confidence: float,
    ) -> ExternalSkillManifestProfile:
        profile = ExternalSkillManifestProfile(
            manifest_profile_id=new_external_skill_manifest_profile_id(),
            source_descriptor_id=source_descriptor.source_descriptor_id,
            manifest_ref=manifest_ref,
            manifest_kind=manifest_kind,
            parsed_name=_first_string(data, ["name", "title", "id"]),
            parsed_description=_first_string(data, ["description", "summary"]),
            parsed_version=_first_string(data, ["version"]),
            parsed_author=_first_string(data, ["author", "maintainer"]),
            declared_tools=_list_value(data, ["tools", "tool", "commands"]),
            declared_permissions=_list_value(data, ["permissions", "permission", "capabilities"]),
            declared_inputs=_list_value(data, ["inputs", "input", "parameters"]),
            declared_outputs=_list_value(data, ["outputs", "output", "returns"]),
            declared_runtime_requirements=_list_value(data, ["runtime", "runtime_requirements", "requires"]),
            parse_status=parse_status,
            confidence=confidence,
            created_at=utc_now_iso(),
            manifest_attrs={
                "read_only": True,
                "full_raw_body_stored": False,
                "content_hash": _hash_text(json.dumps(data, sort_keys=True)) if data else None,
            },
        )
        self.last_manifest_profiles.append(profile)
        self._record_model(
            "external_skill_manifest_profile_created",
            "external_skill_manifest_profile",
            profile.manifest_profile_id,
            profile,
            links=[("external_skill_source_descriptor_object", source_descriptor.source_descriptor_id)],
            object_links=[
                (
                    profile.manifest_profile_id,
                    source_descriptor.source_descriptor_id,
                    "manifest_profile_derived_from_source_descriptor",
                )
            ],
        )
        return profile

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
        event_id = f"event:{uuid4()}"
        objects = [OCELObject(object_id=object_id, object_type=object_type, object_attrs=model.to_dict())]
        relations = [
            OCELRelation.event_object(event_id=event_id, object_id=object_id, qualifier=f"{object_type}_object")
        ]
        for _, linked_object_id in links or []:
            relations.append(
                OCELRelation.event_object(
                    event_id=event_id,
                    object_id=linked_object_id,
                    qualifier="related_object",
                )
            )
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
                    event_attrs={"source": "external_skill_static_digestion", "read_only": True},
                ),
                objects=objects,
                relations=relations,
            )
        )


def _iter_source_files(target: Path | None, max_files: int = 500) -> list[Path]:
    if target is None:
        return []
    if target.is_file():
        return [target]
    files: list[Path] = []
    for path in sorted(target.rglob("*"), key=lambda item: str(item).lower()):
        if path.is_file():
            files.append(path)
        if len(files) >= max_files:
            break
    return files


def _classify_resource(path: Path) -> set[str]:
    name = path.name.lower()
    suffix = path.suffix.lower()
    parts = {part.lower() for part in path.parts}
    categories: set[str] = set()
    if suffix in MARKDOWN_SUFFIXES:
        categories.add("markdown")
    if name == "skill.md" or name in MANIFEST_NAMES or suffix in MANIFEST_SUFFIXES:
        categories.add("manifest")
    if suffix in SCRIPT_SUFFIXES:
        categories.add("script")
    if {"reference", "references", "docs", "doc"} & parts:
        categories.add("reference")
    if suffix in ASSET_SUFFIXES or {"asset", "assets", "images"} & parts:
        categories.add("asset")
    if name in {"agents.md", "agent.json", "agents.json", "codex.json"} or ".agents" in parts:
        categories.add("agent_config")
    if "mcp" in name or "mcp" in parts:
        categories.add("mcp_config")
    return categories or {"unknown"}


def _safe_read_preview(path: Path | None, max_chars: int) -> str:
    if path is None or not path.exists() or not path.is_file():
        return ""
    data = path.read_bytes()[: max_chars * 4]
    if b"\x00" in data:
        return ""
    return data.decode("utf-8-sig", errors="replace")[:max_chars]


def _extract_frontmatter(text: str) -> str:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return ""
    collected: list[str] = []
    for line in lines[1:]:
        if line.strip() == "---":
            return "\n".join(collected)
        collected.append(line)
    return ""


def _parse_simple_mapping(text: str) -> dict[str, Any]:
    result: dict[str, Any] = {}
    current_key: str | None = None
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("-") and current_key:
            result.setdefault(current_key, []).append(stripped[1:].strip().strip("'\""))
            continue
        if ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        key = key.strip()
        value = value.strip()
        current_key = key
        result[key] = [] if not value else _parse_scalar_or_list(value)
    return result


def _parse_manifest_text(text: str, kind: str) -> dict[str, Any]:
    if kind == "json":
        value = json.loads(text)
    elif kind == "toml":
        value = tomllib.loads(text)
    elif kind == "yaml":
        value = _parse_simple_mapping(text)
    else:
        value = _parse_simple_mapping(text)
    if not isinstance(value, dict):
        raise ValueError("manifest root must be an object")
    return value


def _manifest_kind(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".json":
        return "json"
    if suffix in {".yaml", ".yml"}:
        return "yaml"
    if suffix == ".toml":
        return "toml"
    if path.name == "SKILL.md":
        return "skill_md_frontmatter"
    return "unknown"


def _parse_scalar_or_list(value: str) -> Any:
    value = value.strip()
    if not value:
        return ""
    if value.startswith("[") and value.endswith("]"):
        body = value[1:-1].strip()
        if not body:
            return []
        return [item.strip().strip("'\"") for item in body.split(",") if item.strip()]
    return value.strip("'\"")


def _first_string(data: dict[str, Any], keys: list[str]) -> str | None:
    for key in keys:
        value = data.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def _list_value(data: dict[str, Any], keys: list[str]) -> list[str]:
    for key in keys:
        if key not in data:
            continue
        value = data[key]
        if isinstance(value, list):
            return [str(item) for item in value if str(item).strip()]
        if isinstance(value, str) and value.strip():
            return [item.strip() for item in re.split(r"[,;]", value) if item.strip()]
        if isinstance(value, dict):
            return [str(key) for key in value.keys()]
    return []


def _extract_list_like(text: str, labels: list[str]) -> list[str]:
    values: list[str] = []
    lowered_labels = {label.lower() for label in labels}
    for line in text.splitlines():
        stripped = line.strip()
        if ":" not in stripped:
            continue
        label, raw = stripped.split(":", 1)
        if label.lower().strip("# -*") in lowered_labels:
            parsed = _parse_scalar_or_list(raw)
            values.extend(parsed if isinstance(parsed, list) else [str(parsed)])
    return _unique(values)


def _extract_terms(text: str, terms: set[str]) -> list[str]:
    lowered = text.lower()
    return sorted({term for term in terms if term in lowered})


def _matching_lines(text: str, terms: list[str], max_items: int) -> list[str]:
    matches: list[str] = []
    lowered_terms = [term.lower() for term in terms]
    for line in text.splitlines():
        stripped = line.strip()
        lowered = stripped.lower()
        if stripped and any(term in lowered for term in lowered_terms):
            matches.append(_preview_text(stripped, 180))
        if len(matches) >= max_items:
            break
    return matches


def _first_markdown_title(text: str) -> str | None:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip() or None
    return None


def _resolve_child(root_path: str, relative_path: str, child_ref: str) -> Path | None:
    try:
        base = resolve_workspace_path(root_path, relative_path)
    except (WorkspacePathViolationError, WorkspaceReadRootError):
        return None
    if base.is_file():
        return base if base.name == child_ref else None
    candidate = (base / child_ref).resolve(strict=False)
    try:
        candidate.relative_to(base.resolve(strict=False))
    except ValueError:
        return None
    return candidate


def _relative_ref(path: Path | None, base: Path | None) -> str:
    if path is None:
        return ""
    if base is None:
        return path.name
    try:
        return str(path.relative_to(base)).replace("\\", "/")
    except ValueError:
        return path.name


def _redacted_ref(value: str) -> str:
    return str(value).replace("\\", "/").strip("/") or "."


def _is_private_ref(value: str) -> bool:
    parts = {part.lower() for part in Path(value).parts}
    lowered = value.lower()
    return bool(parts & PRIVATE_PATH_TERMS) or any(f"/{term}/" in f"/{lowered}/" for term in PRIVATE_PATH_TERMS)


def _contains_any(text: str, terms: set[str]) -> bool:
    lowered = text.lower()
    return any(term in lowered for term in terms)


def _preview_text(text: str, max_chars: int) -> str:
    normalized = " ".join(text.split())
    return normalized[:max_chars]


def _hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        text = str(value).strip()
        key = text.lower()
        if text and key not in seen:
            seen.add(key)
            result.append(text)
    return result


def _clamp_confidence(value: float | int | None) -> float:
    try:
        numeric = float(0.0 if value is None else value)
    except (TypeError, ValueError):
        numeric = 0.0
    return max(0.0, min(1.0, numeric))
