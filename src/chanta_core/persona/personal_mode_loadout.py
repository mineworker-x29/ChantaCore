from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from chanta_core.ocel.models import OCELEvent, OCELObject, OCELRecord, OCELRelation
from chanta_core.ocel.store import OCELStore
from chanta_core.persona.errors import PersonalModeLoadoutError
from chanta_core.persona.ids import (
    new_personal_core_profile_id,
    new_personal_mode_boundary_id,
    new_personal_mode_capability_binding_id,
    new_personal_mode_loadout_draft_id,
    new_personal_mode_loadout_id,
    new_personal_mode_profile_id,
)
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso


RUNTIME_CAPABILITY_OVERRIDE_STATEMENT = (
    "Runtime capability profile overrides personal/persona claims."
)


@dataclass(frozen=True)
class PersonalCoreProfile:
    core_profile_id: str
    profile_name: str
    profile_type: str
    description: str | None
    identity_statement: str
    continuity_statement: str | None
    status: str
    private: bool
    created_at: str
    updated_at: str
    profile_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "core_profile_id": self.core_profile_id,
            "profile_name": self.profile_name,
            "profile_type": self.profile_type,
            "description": self.description,
            "identity_statement": self.identity_statement,
            "continuity_statement": self.continuity_statement,
            "status": self.status,
            "private": self.private,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "profile_attrs": dict(self.profile_attrs),
        }


@dataclass(frozen=True)
class PersonalModeProfile:
    mode_profile_id: str
    core_profile_id: str
    mode_name: str
    mode_type: str
    role_statement: str
    operating_context: str | None
    capability_summary: str | None
    limitation_summary: str | None
    status: str
    private: bool
    created_at: str
    updated_at: str
    mode_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "mode_profile_id": self.mode_profile_id,
            "core_profile_id": self.core_profile_id,
            "mode_name": self.mode_name,
            "mode_type": self.mode_type,
            "role_statement": self.role_statement,
            "operating_context": self.operating_context,
            "capability_summary": self.capability_summary,
            "limitation_summary": self.limitation_summary,
            "status": self.status,
            "private": self.private,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "mode_attrs": dict(self.mode_attrs),
        }


@dataclass(frozen=True)
class PersonalModeBoundary:
    boundary_id: str
    mode_profile_id: str
    boundary_type: str
    boundary_text: str
    severity: str | None
    required: bool
    status: str
    created_at: str
    boundary_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "boundary_id": self.boundary_id,
            "mode_profile_id": self.mode_profile_id,
            "boundary_type": self.boundary_type,
            "boundary_text": self.boundary_text,
            "severity": self.severity,
            "required": self.required,
            "status": self.status,
            "created_at": self.created_at,
            "boundary_attrs": dict(self.boundary_attrs),
        }


@dataclass(frozen=True)
class PersonalModeCapabilityBinding:
    binding_id: str
    mode_profile_id: str
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
            "binding_id": self.binding_id,
            "mode_profile_id": self.mode_profile_id,
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
class PersonalModeLoadout:
    loadout_id: str
    core_profile_id: str
    mode_profile_id: str
    loadout_name: str
    identity_block: str
    role_block: str
    capability_boundary_block: str
    safety_boundary_block: str
    privacy_boundary_block: str | None
    projection_ref_ids: list[str]
    source_candidate_ids: list[str]
    capability_binding_ids: list[str]
    total_chars: int
    truncated: bool
    private: bool
    created_at: str
    loadout_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "loadout_id": self.loadout_id,
            "core_profile_id": self.core_profile_id,
            "mode_profile_id": self.mode_profile_id,
            "loadout_name": self.loadout_name,
            "identity_block": self.identity_block,
            "role_block": self.role_block,
            "capability_boundary_block": self.capability_boundary_block,
            "safety_boundary_block": self.safety_boundary_block,
            "privacy_boundary_block": self.privacy_boundary_block,
            "projection_ref_ids": list(self.projection_ref_ids),
            "source_candidate_ids": list(self.source_candidate_ids),
            "capability_binding_ids": list(self.capability_binding_ids),
            "total_chars": self.total_chars,
            "truncated": self.truncated,
            "private": self.private,
            "created_at": self.created_at,
            "loadout_attrs": dict(self.loadout_attrs),
        }


@dataclass(frozen=True)
class PersonalModeLoadoutDraft:
    draft_id: str
    core_profile_id: str
    mode_profile_id: str
    draft_name: str
    projected_blocks: list[dict[str, Any]]
    source_refs: list[dict[str, Any]]
    unresolved_questions: list[str]
    review_status: str
    private: bool
    canonical_activation_enabled: bool
    created_at: str
    draft_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "draft_id": self.draft_id,
            "core_profile_id": self.core_profile_id,
            "mode_profile_id": self.mode_profile_id,
            "draft_name": self.draft_name,
            "projected_blocks": [dict(item) for item in self.projected_blocks],
            "source_refs": [dict(item) for item in self.source_refs],
            "unresolved_questions": list(self.unresolved_questions),
            "review_status": self.review_status,
            "private": self.private,
            "canonical_activation_enabled": self.canonical_activation_enabled,
            "created_at": self.created_at,
            "draft_attrs": dict(self.draft_attrs),
        }


class PersonalModeLoadoutService:
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

    def register_core_profile(
        self,
        *,
        profile_name: str,
        profile_type: str,
        identity_statement: str,
        continuity_statement: str | None = None,
        description: str | None = None,
        private: bool = False,
        status: str = "active",
        profile_attrs: dict[str, Any] | None = None,
    ) -> PersonalCoreProfile:
        if not identity_statement.strip():
            raise PersonalModeLoadoutError("identity_statement is required")
        now = utc_now_iso()
        profile = PersonalCoreProfile(
            core_profile_id=new_personal_core_profile_id(),
            profile_name=profile_name,
            profile_type=profile_type,
            description=description,
            identity_statement=identity_statement,
            continuity_statement=continuity_statement,
            status=status,
            private=private,
            created_at=now,
            updated_at=now,
            profile_attrs=dict(profile_attrs or {}),
        )
        self._record(
            "personal_core_profile_registered",
            objects=[_object("personal_core_profile", profile.core_profile_id, profile.to_dict())],
            links=[("core_profile_object", profile.core_profile_id)],
            object_links=[],
            attrs={"profile_type": profile.profile_type, "private": profile.private},
        )
        return profile

    def register_mode_profile(
        self,
        *,
        core_profile_id: str,
        mode_name: str,
        mode_type: str,
        role_statement: str,
        operating_context: str | None = None,
        capability_summary: str | None = None,
        limitation_summary: str | None = None,
        private: bool = False,
        status: str = "active",
        mode_attrs: dict[str, Any] | None = None,
    ) -> PersonalModeProfile:
        if not role_statement.strip():
            raise PersonalModeLoadoutError("role_statement is required")
        now = utc_now_iso()
        mode = PersonalModeProfile(
            mode_profile_id=new_personal_mode_profile_id(),
            core_profile_id=core_profile_id,
            mode_name=mode_name,
            mode_type=mode_type,
            role_statement=role_statement,
            operating_context=operating_context,
            capability_summary=capability_summary,
            limitation_summary=limitation_summary,
            status=status,
            private=private,
            created_at=now,
            updated_at=now,
            mode_attrs=dict(mode_attrs or {}),
        )
        self._record(
            "personal_mode_profile_registered",
            objects=[_object("personal_mode_profile", mode.mode_profile_id, mode.to_dict())],
            links=[
                ("mode_profile_object", mode.mode_profile_id),
                ("core_profile_object", core_profile_id),
            ],
            object_links=[(mode.mode_profile_id, core_profile_id, "belongs_to_core_profile")],
            attrs={"mode_type": mode.mode_type, "private": mode.private},
        )
        return mode

    def register_mode_boundary(
        self,
        *,
        mode_profile_id: str,
        boundary_type: str,
        boundary_text: str,
        severity: str | None = None,
        required: bool = True,
        status: str = "active",
        boundary_attrs: dict[str, Any] | None = None,
    ) -> PersonalModeBoundary:
        if not boundary_text.strip():
            raise PersonalModeLoadoutError("boundary_text is required")
        boundary = PersonalModeBoundary(
            boundary_id=new_personal_mode_boundary_id(),
            mode_profile_id=mode_profile_id,
            boundary_type=boundary_type,
            boundary_text=boundary_text,
            severity=severity,
            required=required,
            status=status,
            created_at=utc_now_iso(),
            boundary_attrs=dict(boundary_attrs or {}),
        )
        self._record(
            "personal_mode_boundary_registered",
            objects=[_object("personal_mode_boundary", boundary.boundary_id, boundary.to_dict())],
            links=[
                ("boundary_object", boundary.boundary_id),
                ("mode_profile_object", mode_profile_id),
            ],
            object_links=[(boundary.boundary_id, mode_profile_id, "belongs_to_mode_profile")],
            attrs={"boundary_type": boundary.boundary_type, "required": boundary.required},
        )
        if boundary.boundary_type in {"capability_boundary", "runtime_boundary"}:
            self._record(
                "personal_mode_capability_boundary_attached",
                objects=[_object("personal_mode_boundary", boundary.boundary_id, boundary.to_dict())],
                links=[("boundary_object", boundary.boundary_id), ("mode_profile_object", mode_profile_id)],
                object_links=[(boundary.boundary_id, mode_profile_id, "attached_to_mode_profile")],
                attrs={"boundary_type": boundary.boundary_type},
            )
        else:
            self._record(
                "personal_mode_boundary_attached",
                objects=[_object("personal_mode_boundary", boundary.boundary_id, boundary.to_dict())],
                links=[("boundary_object", boundary.boundary_id), ("mode_profile_object", mode_profile_id)],
                object_links=[(boundary.boundary_id, mode_profile_id, "attached_to_mode_profile")],
                attrs={"boundary_type": boundary.boundary_type},
            )
        return boundary

    def register_capability_binding(
        self,
        *,
        mode_profile_id: str,
        capability_name: str,
        capability_category: str,
        availability: str,
        can_execute_now: bool,
        requires_permission: bool = False,
        requires_review: bool = False,
        source_kind: str | None = None,
        source_ref: str | None = None,
        binding_attrs: dict[str, Any] | None = None,
    ) -> PersonalModeCapabilityBinding:
        binding = PersonalModeCapabilityBinding(
            binding_id=new_personal_mode_capability_binding_id(),
            mode_profile_id=mode_profile_id,
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
            "personal_mode_capability_binding_registered",
            objects=[
                _object(
                    "personal_mode_capability_binding",
                    binding.binding_id,
                    binding.to_dict(),
                )
            ],
            links=[
                ("capability_binding_object", binding.binding_id),
                ("mode_profile_object", mode_profile_id),
            ],
            object_links=[(binding.binding_id, mode_profile_id, "belongs_to_mode_profile")],
            attrs={
                "availability": binding.availability,
                "can_execute_now": binding.can_execute_now,
                "requires_permission": binding.requires_permission,
            },
        )
        return binding

    def create_mode_loadout(
        self,
        *,
        core_profile: PersonalCoreProfile,
        mode_profile: PersonalModeProfile,
        boundaries: list[PersonalModeBoundary] | None = None,
        capability_bindings: list[PersonalModeCapabilityBinding] | None = None,
        projection_ref_ids: list[str] | None = None,
        source_candidate_ids: list[str] | None = None,
        loadout_name: str | None = None,
        max_chars: int = 6000,
        private: bool | None = None,
        loadout_attrs: dict[str, Any] | None = None,
    ) -> PersonalModeLoadout:
        if mode_profile.core_profile_id != core_profile.core_profile_id:
            raise PersonalModeLoadoutError("mode_profile does not belong to core_profile")
        boundaries = list(boundaries or [])
        capability_bindings = list(capability_bindings or [])
        identity_block = _render_identity_block(core_profile)
        role_block = _render_role_block(mode_profile)
        capability_boundary_block = _render_capability_boundary_block(boundaries, capability_bindings)
        safety_boundary_block = _render_boundary_block(boundaries, "safety_boundary")
        privacy_boundary_block = _render_boundary_block(boundaries, "privacy_boundary")
        bounded_blocks, total_chars, truncated = _bound_blocks(
            [
                identity_block,
                role_block,
                capability_boundary_block,
                safety_boundary_block,
                privacy_boundary_block or "",
            ],
            max_chars=max_chars,
        )
        loadout = PersonalModeLoadout(
            loadout_id=new_personal_mode_loadout_id(),
            core_profile_id=core_profile.core_profile_id,
            mode_profile_id=mode_profile.mode_profile_id,
            loadout_name=loadout_name or f"{core_profile.profile_name}:{mode_profile.mode_name}",
            identity_block=bounded_blocks[0],
            role_block=bounded_blocks[1],
            capability_boundary_block=bounded_blocks[2],
            safety_boundary_block=bounded_blocks[3],
            privacy_boundary_block=bounded_blocks[4] or None,
            projection_ref_ids=list(projection_ref_ids or []),
            source_candidate_ids=list(source_candidate_ids or []),
            capability_binding_ids=[binding.binding_id for binding in capability_bindings],
            total_chars=total_chars,
            truncated=truncated,
            private=core_profile.private if private is None else private,
            created_at=utc_now_iso(),
            loadout_attrs={
                "runtime_mode_selection_enabled": False,
                "capability_grants_created": False,
                **dict(loadout_attrs or {}),
            },
        )
        self._record(
            "personal_mode_loadout_created",
            objects=[_object("personal_mode_loadout", loadout.loadout_id, loadout.to_dict())],
            links=[
                ("mode_loadout_object", loadout.loadout_id),
                ("core_profile_object", core_profile.core_profile_id),
                ("mode_profile_object", mode_profile.mode_profile_id),
            ]
            + [("capability_binding_object", binding_id) for binding_id in loadout.capability_binding_ids],
            object_links=[
                (loadout.loadout_id, core_profile.core_profile_id, "uses_core_profile"),
                (loadout.loadout_id, mode_profile.mode_profile_id, "uses_mode_profile"),
            ]
            + [
                (loadout.loadout_id, binding_id, "includes_capability_binding")
                for binding_id in loadout.capability_binding_ids
            ],
            attrs={
                "mode_type": mode_profile.mode_type,
                "truncated": loadout.truncated,
                "private": loadout.private,
            },
        )
        return loadout

    def create_mode_loadout_draft(
        self,
        *,
        core_profile: PersonalCoreProfile,
        mode_profile: PersonalModeProfile,
        projected_blocks: list[dict[str, Any]],
        source_refs: list[dict[str, Any]] | None = None,
        unresolved_questions: list[str] | None = None,
        draft_name: str | None = None,
        private: bool | None = None,
        draft_attrs: dict[str, Any] | None = None,
    ) -> PersonalModeLoadoutDraft:
        draft = PersonalModeLoadoutDraft(
            draft_id=new_personal_mode_loadout_draft_id(),
            core_profile_id=core_profile.core_profile_id,
            mode_profile_id=mode_profile.mode_profile_id,
            draft_name=draft_name or f"{mode_profile.mode_name}_draft",
            projected_blocks=[dict(block) for block in projected_blocks],
            source_refs=[dict(ref) for ref in (source_refs or [])],
            unresolved_questions=list(unresolved_questions or []),
            review_status="pending_review",
            private=core_profile.private if private is None else private,
            canonical_activation_enabled=False,
            created_at=utc_now_iso(),
            draft_attrs={
                "runtime_activation_enabled": False,
                **dict(draft_attrs or {}),
            },
        )
        self._record(
            "personal_mode_loadout_draft_created",
            objects=[_object("personal_mode_loadout_draft", draft.draft_id, draft.to_dict())],
            links=[
                ("mode_loadout_draft_object", draft.draft_id),
                ("core_profile_object", core_profile.core_profile_id),
                ("mode_profile_object", mode_profile.mode_profile_id),
            ],
            object_links=[
                (draft.draft_id, core_profile.core_profile_id, "belongs_to_core_profile"),
                (draft.draft_id, mode_profile.mode_profile_id, "belongs_to_mode_profile"),
            ],
            attrs={
                "review_status": draft.review_status,
                "canonical_activation_enabled": draft.canonical_activation_enabled,
            },
        )
        return draft

    def create_multi_mode_loadout_set(
        self,
        *,
        core_profile: PersonalCoreProfile,
        mode_specs: list[dict[str, Any]],
        private: bool = False,
    ) -> list[PersonalModeLoadout]:
        loadouts: list[PersonalModeLoadout] = []
        for spec in mode_specs:
            mode_profile = self.register_mode_profile(
                core_profile_id=core_profile.core_profile_id,
                mode_name=str(spec["mode_name"]),
                mode_type=str(spec.get("mode_type") or "manual"),
                role_statement=str(spec["role_statement"]),
                operating_context=spec.get("operating_context"),
                capability_summary=spec.get("capability_summary"),
                limitation_summary=spec.get("limitation_summary"),
                private=private,
                mode_attrs=dict(spec.get("mode_attrs") or {}),
            )
            boundaries = [
                self.register_mode_boundary(
                    mode_profile_id=mode_profile.mode_profile_id,
                    boundary_type=str(item.get("boundary_type") or "manual"),
                    boundary_text=str(item["boundary_text"]),
                    severity=item.get("severity"),
                    required=bool(item.get("required", True)),
                    status=str(item.get("status") or "active"),
                    boundary_attrs=dict(item.get("boundary_attrs") or {}),
                )
                for item in spec.get("boundaries", [])
            ]
            capability_bindings = [
                self.register_capability_binding(
                    mode_profile_id=mode_profile.mode_profile_id,
                    capability_name=str(item["capability_name"]),
                    capability_category=str(item.get("capability_category") or "general"),
                    availability=str(item.get("availability") or "unknown"),
                    can_execute_now=bool(item.get("can_execute_now", False)),
                    requires_permission=bool(item.get("requires_permission", False)),
                    requires_review=bool(item.get("requires_review", False)),
                    source_kind=item.get("source_kind"),
                    source_ref=item.get("source_ref"),
                    binding_attrs=dict(item.get("binding_attrs") or {}),
                )
                for item in spec.get("capability_bindings", [])
            ]
            loadouts.append(
                self.create_mode_loadout(
                    core_profile=core_profile,
                    mode_profile=mode_profile,
                    boundaries=boundaries,
                    capability_bindings=capability_bindings,
                    projection_ref_ids=list(spec.get("projection_ref_ids") or []),
                    source_candidate_ids=list(spec.get("source_candidate_ids") or []),
                    loadout_name=spec.get("loadout_name"),
                    max_chars=int(spec.get("max_chars") or 6000),
                    private=private,
                    loadout_attrs=dict(spec.get("loadout_attrs") or {}),
                )
            )
        return loadouts

    def render_mode_loadout_block(self, *, loadout: PersonalModeLoadout) -> str:
        blocks = [
            "Personal Mode Loadout:",
            loadout.identity_block,
            loadout.role_block,
            loadout.capability_boundary_block,
            loadout.safety_boundary_block,
        ]
        if loadout.privacy_boundary_block:
            blocks.append(loadout.privacy_boundary_block)
        blocks.append(RUNTIME_CAPABILITY_OVERRIDE_STATEMENT)
        return "\n\n".join(block for block in blocks if block)

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
                "personal_mode_loadout_framework": True,
                "runtime_mode_selection_enabled": False,
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


def _render_identity_block(profile: PersonalCoreProfile) -> str:
    lines = [
        "Identity:",
        profile.identity_statement,
    ]
    if profile.continuity_statement:
        lines.append(profile.continuity_statement)
    return "\n".join(lines)


def _render_role_block(mode_profile: PersonalModeProfile) -> str:
    lines = [
        f"Mode: {mode_profile.mode_name}",
        f"Role: {mode_profile.role_statement}",
    ]
    if mode_profile.operating_context:
        lines.append(f"Operating context: {mode_profile.operating_context}")
    if mode_profile.capability_summary:
        lines.append(f"Capability summary: {mode_profile.capability_summary}")
    if mode_profile.limitation_summary:
        lines.append(f"Limitation summary: {mode_profile.limitation_summary}")
    return "\n".join(lines)


def _render_capability_boundary_block(
    boundaries: list[PersonalModeBoundary],
    capability_bindings: list[PersonalModeCapabilityBinding],
) -> str:
    lines = ["Capability boundary:", RUNTIME_CAPABILITY_OVERRIDE_STATEMENT]
    for boundary in boundaries:
        if boundary.boundary_type in {"capability_boundary", "runtime_boundary", "tool_boundary"}:
            lines.append(f"- {boundary.boundary_text}")
    for binding in capability_bindings:
        lines.append(
            "- "
            f"{binding.capability_name}: {binding.availability}; "
            f"can_execute_now={binding.can_execute_now}; "
            f"requires_permission={binding.requires_permission}; "
            f"requires_review={binding.requires_review}"
        )
    return "\n".join(lines)


def _render_boundary_block(boundaries: list[PersonalModeBoundary], boundary_type: str) -> str:
    matching = [boundary.boundary_text for boundary in boundaries if boundary.boundary_type == boundary_type]
    if not matching:
        label = boundary_type.replace("_", " ").title()
        return f"{label}: no explicit entries; defer to runtime policy."
    return "\n".join([f"{boundary_type.replace('_', ' ').title()}:"] + [f"- {item}" for item in matching])


def _bound_blocks(blocks: list[str], *, max_chars: int) -> tuple[list[str], int, bool]:
    bounded: list[str] = []
    total = 0
    truncated = False
    for block in blocks:
        remaining = max_chars - total
        if remaining <= 0:
            bounded.append("")
            truncated = True
            continue
        kept = block if len(block) <= remaining else block[:remaining]
        if len(kept) < len(block):
            truncated = True
        bounded.append(kept)
        total += len(kept)
    return bounded, total, truncated


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
