from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from chanta_core.ocel.models import OCELEvent, OCELObject, OCELRecord, OCELRelation
from chanta_core.ocel.store import OCELStore
from chanta_core.persona.errors import PersonalModeBindingError
from chanta_core.persona.ids import (
    new_personal_mode_activation_request_id,
    new_personal_mode_activation_result_id,
    new_personal_mode_selection_id,
    new_personal_runtime_binding_id,
    new_personal_runtime_capability_binding_id,
)
from chanta_core.persona.personal_mode_loadout import (
    PersonalModeLoadout,
    PersonalModeProfile,
)
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso


NO_CAPABILITY_GRANT_STATEMENT = "This binding does not grant new runtime capabilities."
RUNTIME_CAPABILITY_OVERRIDE_STATEMENT = (
    "Runtime capability profile overrides personal/persona claims."
)

DEFAULT_CONTEXT_INGRESS_BY_RUNTIME_KIND = {
    "external_chat": "manual_handoff",
    "local_chat_runtime": "session_context_projection",
    "codex_like_local_repo": "manual_handoff",
    "local_runtime": "local_runtime_context",
    "review_runtime": "session_context_projection",
    "manual_handoff": "manual_handoff",
    "test_runtime": "none",
    "other": "other",
}


@dataclass(frozen=True)
class PersonalModeSelection:
    selection_id: str
    core_profile_id: str | None
    mode_profile_id: str
    loadout_id: str | None
    selected_mode_name: str
    selected_mode_type: str
    selection_source: str | None
    session_id: str | None
    turn_id: str | None
    status: str
    private: bool
    created_at: str
    selection_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "selection_id": self.selection_id,
            "core_profile_id": self.core_profile_id,
            "mode_profile_id": self.mode_profile_id,
            "loadout_id": self.loadout_id,
            "selected_mode_name": self.selected_mode_name,
            "selected_mode_type": self.selected_mode_type,
            "selection_source": self.selection_source,
            "session_id": self.session_id,
            "turn_id": self.turn_id,
            "status": self.status,
            "private": self.private,
            "created_at": self.created_at,
            "selection_attrs": dict(self.selection_attrs),
        }


@dataclass(frozen=True)
class PersonalRuntimeBinding:
    binding_id: str
    selection_id: str | None
    core_profile_id: str | None
    mode_profile_id: str
    loadout_id: str | None
    runtime_kind: str
    runtime_path: str | None
    context_ingress: str
    capability_profile_ref: str | None
    status: str
    private: bool
    created_at: str
    binding_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "binding_id": self.binding_id,
            "selection_id": self.selection_id,
            "core_profile_id": self.core_profile_id,
            "mode_profile_id": self.mode_profile_id,
            "loadout_id": self.loadout_id,
            "runtime_kind": self.runtime_kind,
            "runtime_path": self.runtime_path,
            "context_ingress": self.context_ingress,
            "capability_profile_ref": self.capability_profile_ref,
            "status": self.status,
            "private": self.private,
            "created_at": self.created_at,
            "binding_attrs": dict(self.binding_attrs),
        }


@dataclass(frozen=True)
class PersonalRuntimeCapabilityBinding:
    runtime_capability_binding_id: str
    runtime_binding_id: str
    capability_name: str
    capability_category: str
    availability: str
    can_execute_now: bool
    requires_permission: bool
    requires_review: bool
    source_kind: str | None
    source_ref: str | None
    created_at: str
    binding_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "runtime_capability_binding_id": self.runtime_capability_binding_id,
            "runtime_binding_id": self.runtime_binding_id,
            "capability_name": self.capability_name,
            "capability_category": self.capability_category,
            "availability": self.availability,
            "can_execute_now": self.can_execute_now,
            "requires_permission": self.requires_permission,
            "requires_review": self.requires_review,
            "source_kind": self.source_kind,
            "source_ref": self.source_ref,
            "created_at": self.created_at,
            "binding_attrs": dict(self.binding_attrs),
        }


@dataclass(frozen=True)
class PersonalModeActivationRequest:
    request_id: str
    mode_profile_id: str
    loadout_id: str | None
    runtime_kind: str
    requested_by: str | None
    session_id: str | None
    turn_id: str | None
    reason: str | None
    created_at: str
    request_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "mode_profile_id": self.mode_profile_id,
            "loadout_id": self.loadout_id,
            "runtime_kind": self.runtime_kind,
            "requested_by": self.requested_by,
            "session_id": self.session_id,
            "turn_id": self.turn_id,
            "reason": self.reason,
            "created_at": self.created_at,
            "request_attrs": dict(self.request_attrs),
        }


@dataclass(frozen=True)
class PersonalModeActivationResult:
    result_id: str
    request_id: str
    selection_id: str | None
    runtime_binding_id: str | None
    status: str
    activated: bool
    activation_scope: str
    capability_boundary_summary: str | None
    denied_reason: str | None
    finding_ids: list[str]
    created_at: str
    result_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "result_id": self.result_id,
            "request_id": self.request_id,
            "selection_id": self.selection_id,
            "runtime_binding_id": self.runtime_binding_id,
            "status": self.status,
            "activated": self.activated,
            "activation_scope": self.activation_scope,
            "capability_boundary_summary": self.capability_boundary_summary,
            "denied_reason": self.denied_reason,
            "finding_ids": list(self.finding_ids),
            "created_at": self.created_at,
            "result_attrs": dict(self.result_attrs),
        }


class PersonalModeBindingService:
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

    def select_mode(
        self,
        *,
        mode_profile: PersonalModeProfile,
        loadout: PersonalModeLoadout | None = None,
        core_profile_id: str | None = None,
        selection_source: str | None = None,
        session_id: str | None = None,
        turn_id: str | None = None,
        private: bool | None = None,
        selection_attrs: dict[str, Any] | None = None,
    ) -> PersonalModeSelection:
        if loadout and loadout.mode_profile_id != mode_profile.mode_profile_id:
            raise PersonalModeBindingError("loadout does not match mode_profile")
        resolved_core_profile_id = core_profile_id or mode_profile.core_profile_id
        selection = PersonalModeSelection(
            selection_id=new_personal_mode_selection_id(),
            core_profile_id=resolved_core_profile_id,
            mode_profile_id=mode_profile.mode_profile_id,
            loadout_id=loadout.loadout_id if loadout else None,
            selected_mode_name=mode_profile.mode_name,
            selected_mode_type=mode_profile.mode_type,
            selection_source=selection_source,
            session_id=session_id,
            turn_id=turn_id,
            status="selected",
            private=mode_profile.private if private is None else private,
            created_at=utc_now_iso(),
            selection_attrs={
                "automatic_prompt_classifier_used": False,
                **dict(selection_attrs or {}),
            },
        )
        self._record(
            "personal_mode_selected",
            objects=[_object("personal_mode_selection", selection.selection_id, selection.to_dict())],
            links=[
                ("mode_selection_object", selection.selection_id),
                ("mode_profile_object", selection.mode_profile_id),
            ]
            + ([("mode_loadout_object", selection.loadout_id)] if selection.loadout_id else []),
            object_links=[
                (selection.selection_id, selection.mode_profile_id, "references_mode_profile")
            ]
            + (
                [(selection.selection_id, selection.loadout_id, "references_loadout")]
                if selection.loadout_id
                else []
            ),
            attrs={
                "selected_mode_type": selection.selected_mode_type,
                "selection_source": selection.selection_source or "",
                "private": selection.private,
            },
        )
        return selection

    def bind_runtime(
        self,
        *,
        selection: PersonalModeSelection,
        runtime_kind: str,
        runtime_path: str | None = None,
        context_ingress: str | None = None,
        capability_profile_ref: str | None = None,
        private: bool | None = None,
        binding_attrs: dict[str, Any] | None = None,
    ) -> PersonalRuntimeBinding:
        resolved_context_ingress = context_ingress or infer_context_ingress(runtime_kind)
        binding = PersonalRuntimeBinding(
            binding_id=new_personal_runtime_binding_id(),
            selection_id=selection.selection_id,
            core_profile_id=selection.core_profile_id,
            mode_profile_id=selection.mode_profile_id,
            loadout_id=selection.loadout_id,
            runtime_kind=runtime_kind,
            runtime_path=runtime_path,
            context_ingress=resolved_context_ingress,
            capability_profile_ref=capability_profile_ref,
            status="bound",
            private=selection.private if private is None else private,
            created_at=utc_now_iso(),
            binding_attrs={
                "runtime_executed": False,
                "runtime_mutated": False,
                "capability_grants_created": False,
                "active_tool_routing_enabled": False,
                **dict(binding_attrs or {}),
            },
        )
        self._record(
            "personal_runtime_binding_created",
            objects=[_object("personal_runtime_binding", binding.binding_id, binding.to_dict())],
            links=[
                ("runtime_binding_object", binding.binding_id),
                ("mode_selection_object", selection.selection_id),
            ],
            object_links=[(binding.binding_id, selection.selection_id, "belongs_to_selection")],
            attrs={
                "runtime_kind": binding.runtime_kind,
                "context_ingress": binding.context_ingress,
                "private": binding.private,
            },
        )
        return binding

    def register_runtime_capability_binding(
        self,
        *,
        runtime_binding_id: str,
        capability_name: str,
        capability_category: str,
        availability: str,
        can_execute_now: bool,
        requires_permission: bool = False,
        requires_review: bool = False,
        source_kind: str | None = None,
        source_ref: str | None = None,
        binding_attrs: dict[str, Any] | None = None,
    ) -> PersonalRuntimeCapabilityBinding:
        binding = PersonalRuntimeCapabilityBinding(
            runtime_capability_binding_id=new_personal_runtime_capability_binding_id(),
            runtime_binding_id=runtime_binding_id,
            capability_name=capability_name,
            capability_category=capability_category,
            availability=availability,
            can_execute_now=can_execute_now,
            requires_permission=requires_permission,
            requires_review=requires_review,
            source_kind=source_kind,
            source_ref=source_ref,
            created_at=utc_now_iso(),
            binding_attrs={
                "capability_grant_created": False,
                **dict(binding_attrs or {}),
            },
        )
        self._record(
            "personal_runtime_capability_binding_registered",
            objects=[
                _object(
                    "personal_runtime_capability_binding",
                    binding.runtime_capability_binding_id,
                    binding.to_dict(),
                )
            ],
            links=[
                ("runtime_capability_binding_object", binding.runtime_capability_binding_id),
                ("runtime_binding_object", binding.runtime_binding_id),
            ],
            object_links=[
                (
                    binding.runtime_capability_binding_id,
                    binding.runtime_binding_id,
                    "belongs_to_runtime_binding",
                )
            ],
            attrs={
                "availability": binding.availability,
                "can_execute_now": binding.can_execute_now,
                "requires_permission": binding.requires_permission,
            },
        )
        return binding

    def create_activation_request(
        self,
        *,
        mode_profile_id: str,
        runtime_kind: str,
        loadout_id: str | None = None,
        requested_by: str | None = None,
        session_id: str | None = None,
        turn_id: str | None = None,
        reason: str | None = None,
        request_attrs: dict[str, Any] | None = None,
    ) -> PersonalModeActivationRequest:
        request = PersonalModeActivationRequest(
            request_id=new_personal_mode_activation_request_id(),
            mode_profile_id=mode_profile_id,
            loadout_id=loadout_id,
            runtime_kind=runtime_kind,
            requested_by=requested_by,
            session_id=session_id,
            turn_id=turn_id,
            reason=reason,
            created_at=utc_now_iso(),
            request_attrs={
                "active_runtime_requested": False,
                **dict(request_attrs or {}),
            },
        )
        self._record(
            "personal_mode_activation_requested",
            objects=[
                _object(
                    "personal_mode_activation_request",
                    request.request_id,
                    request.to_dict(),
                )
            ],
            links=[
                ("activation_request_object", request.request_id),
                ("mode_profile_object", request.mode_profile_id),
            ]
            + ([("mode_loadout_object", request.loadout_id)] if request.loadout_id else []),
            object_links=[],
            attrs={"runtime_kind": request.runtime_kind, "requested_by": request.requested_by or ""},
        )
        return request

    def activate_mode_for_prompt_context(
        self,
        *,
        request: PersonalModeActivationRequest,
        mode_profile: PersonalModeProfile,
        loadout: PersonalModeLoadout | None = None,
        runtime_kind: str,
        capability_bindings: list[PersonalRuntimeCapabilityBinding] | None = None,
        result_attrs: dict[str, Any] | None = None,
    ) -> PersonalModeActivationResult:
        if request.mode_profile_id != mode_profile.mode_profile_id:
            raise PersonalModeBindingError("request does not match mode_profile")
        if loadout and request.loadout_id and loadout.loadout_id != request.loadout_id:
            raise PersonalModeBindingError("request does not match loadout")
        selection = self.select_mode(
            mode_profile=mode_profile,
            loadout=loadout,
            selection_source=request.requested_by or "manual",
            session_id=request.session_id,
            turn_id=request.turn_id,
        )
        runtime_binding = self.bind_runtime(
            selection=selection,
            runtime_kind=runtime_kind,
        )
        bindings = list(capability_bindings or [])
        denied_reason = None
        status = "activated"
        activated = True
        activation_scope = (
            "runtime_binding_only"
            if infer_context_ingress(runtime_kind) == "none"
            else "prompt_context_only"
        )
        if request.request_attrs.get("active_runtime_requested") is True:
            status = "denied"
            activated = False
            activation_scope = "none"
            denied_reason = "Active runtime mode switching is not implemented."
        summary = summarize_runtime_capability_boundaries(bindings)
        result = PersonalModeActivationResult(
            result_id=new_personal_mode_activation_result_id(),
            request_id=request.request_id,
            selection_id=selection.selection_id if activated else None,
            runtime_binding_id=runtime_binding.binding_id if activated else None,
            status=status,
            activated=activated,
            activation_scope=activation_scope,
            capability_boundary_summary=summary,
            denied_reason=denied_reason,
            finding_ids=[],
            created_at=utc_now_iso(),
            result_attrs={
                "runtime_executed": False,
                "runtime_mutated": False,
                "capability_grants_created": False,
                "active_tool_routing_enabled": False,
                **dict(result_attrs or {}),
            },
        )
        event_activity = (
            "personal_mode_activation_denied"
            if result.status == "denied"
            else "personal_mode_activation_recorded"
        )
        self._record(
            event_activity,
            objects=[
                _object("personal_mode_activation_request", request.request_id, request.to_dict()),
                _object("personal_mode_activation_result", result.result_id, result.to_dict()),
                _object("personal_mode_selection", selection.selection_id, selection.to_dict()),
                _object("personal_runtime_binding", runtime_binding.binding_id, runtime_binding.to_dict()),
            ],
            links=[
                ("activation_request_object", request.request_id),
                ("activation_result_object", result.result_id),
                ("mode_selection_object", selection.selection_id),
                ("runtime_binding_object", runtime_binding.binding_id),
            ],
            object_links=[
                (result.result_id, request.request_id, "belongs_to_activation_request"),
                (result.result_id, selection.selection_id, "references_selection"),
                (result.result_id, runtime_binding.binding_id, "references_runtime_binding"),
            ],
            attrs={
                "status": result.status,
                "activated": result.activated,
                "activation_scope": result.activation_scope,
            },
        )
        if result.activated:
            self._record(
                "personal_mode_binding_attached_to_prompt",
                objects=[_object("personal_mode_activation_result", result.result_id, result.to_dict())],
                links=[("activation_result_object", result.result_id)],
                object_links=[],
                attrs={"activation_scope": result.activation_scope},
            )
        return result

    def render_runtime_binding_block(
        self,
        *,
        selection: PersonalModeSelection,
        runtime_binding: PersonalRuntimeBinding,
        capability_bindings: list[PersonalRuntimeCapabilityBinding] | None = None,
    ) -> str:
        lines = [
            "Personal Mode Runtime Binding:",
            f"- selected_mode: {selection.selected_mode_name}",
            f"- selected_mode_type: {selection.selected_mode_type}",
            f"- runtime_kind: {runtime_binding.runtime_kind}",
            f"- context_ingress: {runtime_binding.context_ingress}",
            f"- binding_status: {runtime_binding.status}",
            f"- {RUNTIME_CAPABILITY_OVERRIDE_STATEMENT}",
            f"- {NO_CAPABILITY_GRANT_STATEMENT}",
            "- capability_boundaries:",
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
        return "\n".join(lines)

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
                "personal_mode_binding_framework": True,
                "runtime_execution_enabled": False,
                "capability_grants_created": False,
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


def infer_context_ingress(runtime_kind: str) -> str:
    return DEFAULT_CONTEXT_INGRESS_BY_RUNTIME_KIND.get(runtime_kind, "other")


def summarize_runtime_capability_boundaries(
    capability_bindings: list[PersonalRuntimeCapabilityBinding],
) -> str:
    if not capability_bindings:
        return (
            f"{RUNTIME_CAPABILITY_OVERRIDE_STATEMENT} "
            f"{NO_CAPABILITY_GRANT_STATEMENT}"
        )
    parts = [
        (
            f"{binding.capability_name}={binding.availability}"
            f"/execute={binding.can_execute_now}"
        )
        for binding in capability_bindings
    ]
    return (
        f"{RUNTIME_CAPABILITY_OVERRIDE_STATEMENT} "
        f"{NO_CAPABILITY_GRANT_STATEMENT} "
        + "; ".join(parts)
    )


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
