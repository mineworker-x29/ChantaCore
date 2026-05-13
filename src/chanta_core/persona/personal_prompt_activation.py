from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from chanta_core.ocel.models import OCELEvent, OCELObject, OCELRecord, OCELRelation
from chanta_core.ocel.store import OCELStore
from chanta_core.persona.errors import PersonalPromptActivationError
from chanta_core.persona.ids import (
    new_personal_prompt_activation_block_id,
    new_personal_prompt_activation_config_id,
    new_personal_prompt_activation_finding_id,
    new_personal_prompt_activation_request_id,
    new_personal_prompt_activation_result_id,
)
from chanta_core.persona.personal_conformance import PersonalConformanceResult
from chanta_core.persona.personal_mode_binding import (
    NO_CAPABILITY_GRANT_STATEMENT,
    RUNTIME_CAPABILITY_OVERRIDE_STATEMENT,
    PersonalModeBindingService,
    PersonalModeSelection,
    PersonalRuntimeBinding,
    PersonalRuntimeCapabilityBinding,
)
from chanta_core.persona.personal_mode_loadout import (
    PersonalModeLoadout,
    PersonalModeLoadoutService,
)
from chanta_core.persona.personal_overlay import (
    DEFAULT_PERSONAL_DIRECTORY_ENV_KEY,
    PersonalOverlayLoadResult,
    PersonalOverlayLoaderService,
)
from chanta_core.persona.personal_smoke_test import (
    PersonalRuntimeSmokeTestService,
    PersonalSmokeTestResult,
)
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso


@dataclass(frozen=True)
class PersonalPromptActivationConfig:
    config_id: str
    personal_directory_configured: bool
    selected_mode_name: str | None
    selected_profile_name: str | None
    runtime_kind: str | None
    activation_source: str | None
    max_chars: int
    require_conformance_pass: bool
    require_smoke_pass: bool
    private: bool
    status: str
    created_at: str
    config_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.max_chars < 0:
            raise PersonalPromptActivationError("max_chars must be non-negative")

    def to_dict(self) -> dict[str, Any]:
        return {
            "config_id": self.config_id,
            "personal_directory_configured": self.personal_directory_configured,
            "selected_mode_name": self.selected_mode_name,
            "selected_profile_name": self.selected_profile_name,
            "runtime_kind": self.runtime_kind,
            "activation_source": self.activation_source,
            "max_chars": self.max_chars,
            "require_conformance_pass": self.require_conformance_pass,
            "require_smoke_pass": self.require_smoke_pass,
            "private": self.private,
            "status": self.status,
            "created_at": self.created_at,
            "config_attrs": dict(self.config_attrs),
        }


@dataclass(frozen=True)
class PersonalPromptActivationRequest:
    request_id: str
    config_id: str | None
    session_id: str | None
    turn_id: str | None
    selected_mode_name: str | None
    selected_profile_name: str | None
    runtime_kind: str | None
    requested_by: str | None
    created_at: str
    request_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "config_id": self.config_id,
            "session_id": self.session_id,
            "turn_id": self.turn_id,
            "selected_mode_name": self.selected_mode_name,
            "selected_profile_name": self.selected_profile_name,
            "runtime_kind": self.runtime_kind,
            "requested_by": self.requested_by,
            "created_at": self.created_at,
            "request_attrs": dict(self.request_attrs),
        }


@dataclass(frozen=True)
class PersonalPromptActivationBlock:
    block_id: str
    request_id: str
    block_type: str
    title: str | None
    content: str
    source_kind: str | None
    source_ref: str | None
    private: bool
    safe_for_prompt: bool
    total_chars: int
    created_at: str
    block_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "block_id": self.block_id,
            "request_id": self.request_id,
            "block_type": self.block_type,
            "title": self.title,
            "content": self.content,
            "source_kind": self.source_kind,
            "source_ref": self.source_ref,
            "private": self.private,
            "safe_for_prompt": self.safe_for_prompt,
            "total_chars": self.total_chars,
            "created_at": self.created_at,
            "block_attrs": dict(self.block_attrs),
        }


@dataclass(frozen=True)
class PersonalPromptActivationResult:
    result_id: str
    request_id: str
    status: str
    activation_scope: str
    attached_block_ids: list[str]
    total_chars: int
    truncated: bool
    denied: bool
    finding_ids: list[str]
    created_at: str
    result_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.activation_scope not in {"prompt_context_only", "none"}:
            raise PersonalPromptActivationError("activation_scope must be prompt_context_only or none")

    def to_dict(self) -> dict[str, Any]:
        return {
            "result_id": self.result_id,
            "request_id": self.request_id,
            "status": self.status,
            "activation_scope": self.activation_scope,
            "attached_block_ids": list(self.attached_block_ids),
            "total_chars": self.total_chars,
            "truncated": self.truncated,
            "denied": self.denied,
            "finding_ids": list(self.finding_ids),
            "created_at": self.created_at,
            "result_attrs": dict(self.result_attrs),
        }


@dataclass(frozen=True)
class PersonalPromptActivationFinding:
    finding_id: str
    request_id: str | None
    result_id: str | None
    finding_type: str
    status: str
    severity: str | None
    message: str
    subject_ref: str | None
    created_at: str
    finding_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "request_id": self.request_id,
            "result_id": self.result_id,
            "finding_type": self.finding_type,
            "status": self.status,
            "severity": self.severity,
            "message": self.message,
            "subject_ref": self.subject_ref,
            "created_at": self.created_at,
            "finding_attrs": dict(self.finding_attrs),
        }


class PersonalPromptActivationService:
    def __init__(
        self,
        *,
        personal_overlay_loader_service: PersonalOverlayLoaderService | None = None,
        personal_mode_loadout_service: PersonalModeLoadoutService | None = None,
        personal_mode_binding_service: PersonalModeBindingService | None = None,
        personal_conformance_service: Any | None = None,
        personal_smoke_test_service: PersonalRuntimeSmokeTestService | None = None,
        trace_service: TraceService | None = None,
        ocel_store: OCELStore | None = None,
    ) -> None:
        if trace_service is not None:
            self.trace_service = trace_service
        elif ocel_store is not None:
            self.trace_service = TraceService(ocel_store=ocel_store)
        else:
            self.trace_service = TraceService()
        self.personal_overlay_loader_service = (
            personal_overlay_loader_service
            or PersonalOverlayLoaderService(trace_service=self.trace_service)
        )
        self.personal_mode_loadout_service = (
            personal_mode_loadout_service
            or PersonalModeLoadoutService(trace_service=self.trace_service)
        )
        self.personal_mode_binding_service = (
            personal_mode_binding_service
            or PersonalModeBindingService(trace_service=self.trace_service)
        )
        self.personal_conformance_service = personal_conformance_service
        self.personal_smoke_test_service = (
            personal_smoke_test_service
            or PersonalRuntimeSmokeTestService(trace_service=self.trace_service)
        )
        self.last_config: PersonalPromptActivationConfig | None = None
        self.last_request: PersonalPromptActivationRequest | None = None
        self.last_blocks: list[PersonalPromptActivationBlock] = []
        self.last_findings: list[PersonalPromptActivationFinding] = []
        self.last_result: PersonalPromptActivationResult | None = None

    def load_activation_config(
        self,
        *,
        env_mode_key: str = "CHANTA_PERSONAL_MODE",
        env_profile_key: str = "CHANTA_PERSONAL_PROFILE",
        env_runtime_kind_key: str = "CHANTA_PERSONAL_RUNTIME_KIND",
        env_directory_key: str = DEFAULT_PERSONAL_DIRECTORY_ENV_KEY,
        max_chars: int = 8000,
        require_conformance_pass: bool = False,
        require_smoke_pass: bool = False,
    ) -> PersonalPromptActivationConfig:
        directory_configured = bool(os.environ.get(env_directory_key))
        selected_mode = _clean_env(os.environ.get(env_mode_key))
        selected_profile = _clean_env(os.environ.get(env_profile_key))
        runtime_kind = _clean_env(os.environ.get(env_runtime_kind_key))
        has_activation_input = bool(selected_mode or selected_profile or runtime_kind)
        status = "active" if directory_configured and has_activation_input else "inactive"
        if has_activation_input and not directory_configured:
            status = "missing_config"
        config = PersonalPromptActivationConfig(
            config_id=new_personal_prompt_activation_config_id(),
            personal_directory_configured=directory_configured,
            selected_mode_name=selected_mode,
            selected_profile_name=selected_profile,
            runtime_kind=runtime_kind,
            activation_source="env" if has_activation_input else None,
            max_chars=max_chars,
            require_conformance_pass=require_conformance_pass,
            require_smoke_pass=require_smoke_pass,
            private=True,
            status=status,
            created_at=utc_now_iso(),
            config_attrs={
                "env_mode_key": env_mode_key,
                "env_profile_key": env_profile_key,
                "env_runtime_kind_key": env_runtime_kind_key,
                "env_directory_key": env_directory_key,
                "nl_mode_switch": False,
                "mode_auto_selected": False,
                "source_bodies_loaded": False,
                "capability_grants_created": False,
            },
        )
        self.last_config = config
        self._record(
            "personal_prompt_activation_config_loaded",
            objects=[_object("personal_prompt_activation_config", config.config_id, config.to_dict())],
            links=[("activation_config_object", config.config_id)],
            object_links=[],
            attrs={"status": config.status, "activation_source": config.activation_source or ""},
        )
        return config

    def create_activation_request(
        self,
        *,
        config: PersonalPromptActivationConfig | None = None,
        session_id: str | None = None,
        turn_id: str | None = None,
        selected_mode_name: str | None = None,
        selected_profile_name: str | None = None,
        runtime_kind: str | None = None,
        requested_by: str | None = None,
    ) -> PersonalPromptActivationRequest:
        request = PersonalPromptActivationRequest(
            request_id=new_personal_prompt_activation_request_id(),
            config_id=config.config_id if config else None,
            session_id=session_id,
            turn_id=turn_id,
            selected_mode_name=selected_mode_name or (config.selected_mode_name if config else None),
            selected_profile_name=selected_profile_name or (config.selected_profile_name if config else None),
            runtime_kind=runtime_kind or (config.runtime_kind if config else None),
            requested_by=requested_by,
            created_at=utc_now_iso(),
            request_attrs={
                "nl_mode_switch": False,
                "explicit_activation_only": True,
                "prompt_context_only": True,
            },
        )
        self.last_request = request
        self._record(
            "personal_prompt_activation_requested",
            objects=[_object("personal_prompt_activation_request", request.request_id, request.to_dict())],
            links=[("activation_request_object", request.request_id)]
            + ([("activation_config_object", request.config_id)] if request.config_id else []),
            object_links=(
                [(request.request_id, request.config_id, "uses_activation_config")]
                if request.config_id
                else []
            ),
            attrs={"requested_by": requested_by or "", "runtime_kind": request.runtime_kind or ""},
        )
        return request

    def build_mode_loadout_block(
        self,
        *,
        request: PersonalPromptActivationRequest,
        loadout: PersonalModeLoadout,
    ) -> PersonalPromptActivationBlock:
        content = "\n\n".join(
            block
            for block in [
                "Personal Mode Prompt Activation: loadout",
                loadout.identity_block,
                loadout.role_block,
                loadout.capability_boundary_block,
                loadout.safety_boundary_block,
                loadout.privacy_boundary_block or "",
                RUNTIME_CAPABILITY_OVERRIDE_STATEMENT,
            ]
            if block
        )
        return self._block(
            request=request,
            block_type="personal_mode_loadout",
            title="Personal Mode Loadout",
            content=content,
            source_kind="personal_mode_loadout",
            source_ref=loadout.loadout_id,
            safe_for_prompt=True,
            block_attrs={
                "source_bodies_loaded": False,
                "capability_grants_created": False,
            },
        )

    def build_runtime_binding_block(
        self,
        *,
        request: PersonalPromptActivationRequest,
        selection: PersonalModeSelection | None,
        runtime_binding: PersonalRuntimeBinding | None,
        capability_bindings: list[PersonalRuntimeCapabilityBinding] | None = None,
    ) -> PersonalPromptActivationBlock:
        lines = [
            "Personal Mode Prompt Activation: runtime binding",
            f"- selected_mode: {selection.selected_mode_name if selection else request.selected_mode_name or 'unspecified'}",
            f"- runtime_kind: {runtime_binding.runtime_kind if runtime_binding else request.runtime_kind or 'unspecified'}",
            f"- context_ingress: {runtime_binding.context_ingress if runtime_binding else 'not_bound'}",
            f"- {NO_CAPABILITY_GRANT_STATEMENT}",
            f"- {RUNTIME_CAPABILITY_OVERRIDE_STATEMENT}",
            "- runtime_capabilities:",
        ]
        for binding in capability_bindings or []:
            lines.append(
                "  - "
                f"{binding.capability_name}: {binding.availability}; "
                f"can_execute_now={binding.can_execute_now}; "
                f"requires_permission={binding.requires_permission}; "
                f"requires_review={binding.requires_review}"
            )
        if not capability_bindings:
            lines.append("  - no runtime capability bindings supplied")
        return self._block(
            request=request,
            block_type="personal_runtime_binding",
            title="Personal Runtime Binding",
            content="\n".join(lines),
            source_kind="personal_runtime_binding",
            source_ref=runtime_binding.binding_id if runtime_binding else None,
            safe_for_prompt=True,
            block_attrs={
                "capability_grants_created": False,
                "runtime_mutated": False,
            },
        )

    def build_overlay_projection_blocks(
        self,
        *,
        request: PersonalPromptActivationRequest,
        overlay_load_result: PersonalOverlayLoadResult | None,
    ) -> list[PersonalPromptActivationBlock]:
        if overlay_load_result is None or overlay_load_result.denied:
            return []
        blocks: list[PersonalPromptActivationBlock] = []
        for rendered in overlay_load_result.rendered_blocks:
            content = str(rendered.get("content") or "")
            if not content:
                continue
            blocks.append(
                self._block(
                    request=request,
                    block_type="personal_overlay_projection",
                    title="Personal Overlay Projection",
                    content=content,
                    source_kind="personal_overlay_load_result",
                    source_ref=overlay_load_result.result_id,
                    safe_for_prompt=True,
                    block_attrs={
                        "projection_ref_id": rendered.get("projection_ref_id"),
                        "source_bodies_loaded": False,
                        "excluded_roots_loaded": False,
                    },
                )
            )
        return blocks

    def build_conformance_summary_block(
        self,
        *,
        request: PersonalPromptActivationRequest,
        conformance_result: PersonalConformanceResult | None = None,
    ) -> PersonalPromptActivationBlock | None:
        if conformance_result is None:
            return None
        return self._block(
            request=request,
            block_type="personal_conformance_summary",
            title="Personal Conformance Summary",
            content=(
                "Personal Conformance summary: "
                f"status={conformance_result.status}; score={conformance_result.score}; "
                "private details omitted."
            ),
            source_kind="personal_conformance_result",
            source_ref=conformance_result.result_id,
            safe_for_prompt=True,
        )

    def build_smoke_summary_block(
        self,
        *,
        request: PersonalPromptActivationRequest,
        smoke_result: PersonalSmokeTestResult | None = None,
    ) -> PersonalPromptActivationBlock | None:
        if smoke_result is None:
            return None
        return self._block(
            request=request,
            block_type="personal_smoke_summary",
            title="Personal Runtime Smoke Test Summary",
            content=(
                "Personal Runtime Smoke Test summary: "
                f"status={smoke_result.status}; score={smoke_result.score}; "
                "deterministic check only."
            ),
            source_kind="personal_smoke_test_result",
            source_ref=smoke_result.result_id,
            safe_for_prompt=True,
        )

    def activate_for_prompt_context(
        self,
        *,
        session_id: str | None = None,
        turn_id: str | None = None,
        selected_mode_name: str | None = None,
        selected_profile_name: str | None = None,
        runtime_kind: str | None = None,
        explicit_loadout: PersonalModeLoadout | None = None,
        explicit_runtime_binding: PersonalRuntimeBinding | None = None,
        explicit_overlay_load_result: PersonalOverlayLoadResult | None = None,
        explicit_selection: PersonalModeSelection | None = None,
        explicit_capability_bindings: list[PersonalRuntimeCapabilityBinding] | None = None,
        conformance_result: PersonalConformanceResult | None = None,
        smoke_result: PersonalSmokeTestResult | None = None,
        max_chars: int | None = None,
        require_conformance_pass: bool = False,
        require_smoke_pass: bool = False,
    ) -> PersonalPromptActivationResult:
        config = self.load_activation_config(
            max_chars=max_chars or 8000,
            require_conformance_pass=require_conformance_pass,
            require_smoke_pass=require_smoke_pass,
        )
        request = self.create_activation_request(
            config=config,
            session_id=session_id,
            turn_id=turn_id,
            selected_mode_name=selected_mode_name,
            selected_profile_name=selected_profile_name,
            runtime_kind=runtime_kind,
            requested_by="explicit_runtime_input" if any(
                [selected_mode_name, selected_profile_name, runtime_kind, explicit_loadout]
            ) else config.activation_source,
        )
        findings: list[PersonalPromptActivationFinding] = []
        blocks: list[PersonalPromptActivationBlock] = []
        if not config.personal_directory_configured and explicit_loadout is None:
            findings.append(
                self._finding(
                    request=request,
                    finding_type="missing_personal_directory",
                    status="skipped",
                    severity="medium",
                    message="No Personal Directory is configured and no explicit loadout was supplied.",
                    subject_ref=None,
                )
            )
            return self._result(
                request=request,
                status="missing_config",
                activation_scope="none",
                blocks=[],
                findings=findings,
                denied=False,
                truncated=False,
            )
        if request.selected_mode_name is None and explicit_loadout is None:
            findings.append(
                self._finding(
                    request=request,
                    finding_type="missing_selected_mode",
                    status="skipped",
                    severity="medium",
                    message="No selected Personal Mode was provided by env or explicit input.",
                    subject_ref=None,
                )
            )
            return self._result(
                request=request,
                status="skipped",
                activation_scope="none",
                blocks=[],
                findings=findings,
                denied=False,
                truncated=False,
            )
        if explicit_loadout is None:
            findings.append(
                self._finding(
                    request=request,
                    finding_type="mode_loadout_not_found",
                    status="warning",
                    severity="medium",
                    message="Selected Personal Mode was configured, but no resolved loadout was supplied.",
                    subject_ref=request.selected_mode_name,
                )
            )
        else:
            blocks.append(self.build_mode_loadout_block(request=request, loadout=explicit_loadout))
        if explicit_runtime_binding is not None or request.runtime_kind:
            blocks.append(
                self.build_runtime_binding_block(
                    request=request,
                    selection=explicit_selection,
                    runtime_binding=explicit_runtime_binding,
                    capability_bindings=explicit_capability_bindings,
                )
            )
        blocks.extend(
            self.build_overlay_projection_blocks(
                request=request,
                overlay_load_result=explicit_overlay_load_result,
            )
        )
        conformance_block = self.build_conformance_summary_block(
            request=request,
            conformance_result=conformance_result,
        )
        if conformance_block:
            blocks.append(conformance_block)
        smoke_block = self.build_smoke_summary_block(request=request, smoke_result=smoke_result)
        if smoke_block:
            blocks.append(smoke_block)
        if explicit_overlay_load_result is not None and explicit_overlay_load_result.denied:
            findings.append(
                self._finding(
                    request=request,
                    finding_type="unsafe_overlay_projection",
                    status="failed",
                    severity="high",
                    message="Personal Overlay projection was denied by its boundary loader.",
                    subject_ref=explicit_overlay_load_result.result_id,
                )
            )
        if require_conformance_pass and conformance_result and conformance_result.status != "passed":
            findings.append(
                self._finding(
                    request=request,
                    finding_type="conformance_failed",
                    status="failed",
                    severity="high",
                    message="Personal Conformance did not pass and activation requires a pass.",
                    subject_ref=conformance_result.result_id,
                )
            )
        if require_smoke_pass and smoke_result and smoke_result.status != "passed":
            findings.append(
                self._finding(
                    request=request,
                    finding_type="smoke_failed",
                    status="failed",
                    severity="high",
                    message="Personal Runtime Smoke Test did not pass and activation requires a pass.",
                    subject_ref=smoke_result.result_id,
                )
            )
        if explicit_loadout and not explicit_loadout.capability_boundary_block.strip():
            findings.append(
                self._finding(
                    request=request,
                    finding_type="capability_boundary_missing",
                    status="failed",
                    severity="high",
                    message="Personal Mode Loadout has no capability boundary block.",
                    subject_ref=explicit_loadout.loadout_id,
                )
            )
        unsafe = [finding for finding in findings if finding.status in {"failed", "error"}]
        if unsafe:
            return self._result(
                request=request,
                status="denied",
                activation_scope="none",
                blocks=[],
                findings=findings,
                denied=True,
                truncated=False,
            )
        bounded_blocks, truncated = _bound_blocks(blocks, max_chars=max_chars or config.max_chars)
        if truncated:
            findings.append(
                self._finding(
                    request=request,
                    finding_type="prompt_block_too_large",
                    status="warning",
                    severity="medium",
                    message="Personal Mode Prompt Activation blocks were truncated to max_chars.",
                    subject_ref=None,
                )
            )
        if not bounded_blocks:
            return self._result(
                request=request,
                status="skipped" if findings else "missing_config",
                activation_scope="none",
                blocks=[],
                findings=findings,
                denied=False,
                truncated=truncated,
            )
        status = "needs_review" if any(finding.status == "warning" for finding in findings) else "attached"
        return self._result(
            request=request,
            status=status,
            activation_scope="prompt_context_only",
            blocks=bounded_blocks,
            findings=findings,
            denied=False,
            truncated=truncated,
        )

    def render_activation_blocks(
        self,
        *,
        result: PersonalPromptActivationResult,
        blocks: list[PersonalPromptActivationBlock] | None = None,
    ) -> str:
        if result.activation_scope != "prompt_context_only" or result.denied:
            return ""
        rendered_blocks = blocks if blocks is not None else self.last_blocks
        allowed = [block for block in rendered_blocks if block.block_id in result.attached_block_ids]
        if not allowed:
            return ""
        body = "\n\n".join(
            f"[{block.block_type}]\n{block.content}" for block in allowed if block.safe_for_prompt
        )
        if not body:
            return ""
        return (
            "Personal Mode Prompt Activation:\n"
            "Activation scope: prompt_context_only. "
            "This block does not grant capabilities or execute tools.\n"
            f"{RUNTIME_CAPABILITY_OVERRIDE_STATEMENT}\n\n"
            f"{body}"
        )

    def render_activation_diagnostics(
        self,
        *,
        result: PersonalPromptActivationResult | None = None,
    ) -> str:
        active_result = result or self.last_result
        request = self.last_request
        if active_result is None:
            return "Personal Prompt Activation Diagnostics: unavailable"
        attrs = active_result.result_attrs
        lines = [
            "Personal Prompt Activation Diagnostics",
            f"selected_mode={attrs.get('selected_mode') or (request.selected_mode_name if request else 'unspecified') or 'unspecified'}",
            f"matched_loadout={attrs.get('matched_loadout') or 'none'}",
            f"activation_status={active_result.status}",
            f"activation_scope={active_result.activation_scope}",
            f"activation_attached={str(bool(attrs.get('activation_attached'))).lower()}",
            f"activation_skipped={str(bool(attrs.get('activation_skipped'))).lower()}",
            f"activation_denied={str(bool(attrs.get('activation_denied'))).lower()}",
            f"total_activation_chars={active_result.total_chars}",
            f"truncated={str(active_result.truncated).lower()}",
            "capability_grants_created=false",
            "tool_execution_used=false",
            "source_bodies_loaded=false",
        ]
        return "\n".join(lines)

    def _block(
        self,
        *,
        request: PersonalPromptActivationRequest,
        block_type: str,
        title: str | None,
        content: str,
        source_kind: str | None,
        source_ref: str | None,
        safe_for_prompt: bool,
        block_attrs: dict[str, Any] | None = None,
    ) -> PersonalPromptActivationBlock:
        block = PersonalPromptActivationBlock(
            block_id=new_personal_prompt_activation_block_id(),
            request_id=request.request_id,
            block_type=block_type,
            title=title,
            content=content,
            source_kind=source_kind,
            source_ref=source_ref,
            private=True,
            safe_for_prompt=safe_for_prompt,
            total_chars=len(content),
            created_at=utc_now_iso(),
            block_attrs={
                "source_bodies_loaded": False,
                "excluded_roots_loaded": False,
                "capability_grants_created": False,
                **dict(block_attrs or {}),
            },
        )
        self._record(
            "personal_prompt_activation_block_created",
            objects=[_object("personal_prompt_activation_block", block.block_id, block.to_dict())],
            links=[
                ("activation_block_object", block.block_id),
                ("activation_request_object", request.request_id),
            ],
            object_links=[(block.block_id, request.request_id, "belongs_to_activation_request")]
            + ([(block.block_id, source_ref, f"references_{source_kind}")] if source_ref and source_kind else []),
            attrs={"block_type": block.block_type, "safe_for_prompt": block.safe_for_prompt},
        )
        return block

    def _finding(
        self,
        *,
        request: PersonalPromptActivationRequest,
        finding_type: str,
        status: str,
        severity: str | None,
        message: str,
        subject_ref: str | None,
    ) -> PersonalPromptActivationFinding:
        finding = PersonalPromptActivationFinding(
            finding_id=new_personal_prompt_activation_finding_id(),
            request_id=request.request_id,
            result_id=None,
            finding_type=finding_type,
            status=status,
            severity=severity,
            message=message,
            subject_ref=subject_ref,
            created_at=utc_now_iso(),
            finding_attrs={"prompt_context_only": True},
        )
        self._record(
            "personal_prompt_activation_finding_recorded",
            objects=[_object("personal_prompt_activation_finding", finding.finding_id, finding.to_dict())],
            links=[
                ("activation_finding_object", finding.finding_id),
                ("activation_request_object", request.request_id),
            ],
            object_links=[(finding.finding_id, request.request_id, "belongs_to_activation_request")],
            attrs={"finding_type": finding.finding_type, "status": finding.status},
        )
        return finding

    def _result(
        self,
        *,
        request: PersonalPromptActivationRequest,
        status: str,
        activation_scope: str,
        blocks: list[PersonalPromptActivationBlock],
        findings: list[PersonalPromptActivationFinding],
        denied: bool,
        truncated: bool,
    ) -> PersonalPromptActivationResult:
        result = PersonalPromptActivationResult(
            result_id=new_personal_prompt_activation_result_id(),
            request_id=request.request_id,
            status=status,
            activation_scope=activation_scope,
            attached_block_ids=[block.block_id for block in blocks],
            total_chars=sum(block.total_chars for block in blocks),
            truncated=truncated,
            denied=denied,
            finding_ids=[finding.finding_id for finding in findings],
            created_at=utc_now_iso(),
            result_attrs={
                "selected_mode": request.selected_mode_name,
                "matched_loadout": _matched_loadout_ref(blocks),
                "activation_attached": activation_scope == "prompt_context_only" and not denied,
                "activation_skipped": activation_scope == "none" and not denied,
                "activation_denied": denied,
                "total_activation_chars": sum(block.total_chars for block in blocks),
                "truncation_status": "truncated" if truncated else "not_truncated",
                "runtime_capability_activation": False,
                "capability_grants_created": False,
                "tool_execution_used": False,
                "model_call_used": False,
                "shell_execution_used": False,
                "network_access_used": False,
                "mcp_connection_used": False,
                "plugin_loading_used": False,
                "line_delimited_prompt_activation_store_created": False,
                "nl_mode_switch": False,
                "source_bodies_loaded": False,
            },
        )
        self.last_blocks = list(blocks)
        self.last_findings = list(findings)
        self.last_result = result
        event_activity = (
            "personal_prompt_activation_denied"
            if denied
            else "personal_prompt_activation_attached"
            if activation_scope == "prompt_context_only"
            else "personal_prompt_activation_skipped"
        )
        objects = [_object("personal_prompt_activation_result", result.result_id, result.to_dict())]
        links = [
            ("activation_result_object", result.result_id),
            ("activation_request_object", request.request_id),
        ]
        object_links = [(result.result_id, request.request_id, "belongs_to_activation_request")]
        for block in blocks:
            links.append(("activation_block_object", block.block_id))
            object_links.append((result.result_id, block.block_id, "includes_activation_block"))
        for finding in findings:
            links.append(("activation_finding_object", finding.finding_id))
            object_links.append((finding.finding_id, result.result_id, "belongs_to_activation_result"))
        self._record(
            event_activity,
            objects=objects,
            links=links,
            object_links=object_links,
            attrs={"status": result.status, "activation_scope": result.activation_scope},
        )
        return result

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
                "personal_prompt_activation": True,
                "prompt_context_only": True,
                "runtime_capability_activation": False,
                "capability_grants_created": False,
                "tool_execution_used": False,
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


def _bound_blocks(
    blocks: list[PersonalPromptActivationBlock],
    *,
    max_chars: int,
) -> tuple[list[PersonalPromptActivationBlock], bool]:
    bounded: list[PersonalPromptActivationBlock] = []
    total = 0
    truncated = False
    for block in blocks:
        remaining = max_chars - total
        if remaining <= 0:
            truncated = True
            break
        content = block.content if len(block.content) <= remaining else block.content[:remaining]
        if len(content) < len(block.content):
            truncated = True
        bounded.append(
            PersonalPromptActivationBlock(
                **{**block.to_dict(), "content": content, "total_chars": len(content)}
            )
        )
        total += len(content)
    return bounded, truncated


def _clean_env(value: str | None) -> str | None:
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None


def _matched_loadout_ref(blocks: list[PersonalPromptActivationBlock]) -> str | None:
    for block in blocks:
        if block.block_type == "personal_mode_loadout":
            return block.source_ref
    return None


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
