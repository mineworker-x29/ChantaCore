from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Any
from uuid import uuid4

from chanta_core.ocel.models import OCELEvent, OCELObject, OCELRecord, OCELRelation
from chanta_core.ocel.store import OCELStore
from chanta_core.persona.ids import (
    new_agent_role_binding_id,
    new_persona_instruction_artifact_id,
    new_persona_loadout_id,
    new_persona_profile_id,
    new_persona_projection_id,
    new_soul_identity_id,
)
from chanta_core.persona.models import (
    AgentRoleBinding,
    PersonaInstructionArtifact,
    PersonaLoadout,
    PersonaProfile,
    PersonaProjection,
    SoulIdentity,
)
from chanta_core.runtime.capability_contract import RuntimeCapabilityIntrospectionService
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso


@dataclass(frozen=True)
class DefaultAgentPersonaBundle:
    soul: SoulIdentity
    profile: PersonaProfile
    artifacts: list[PersonaInstructionArtifact]
    binding: AgentRoleBinding
    loadout: PersonaLoadout
    projection: PersonaProjection


class PersonaLoadingService:
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

    def register_soul_identity(
        self,
        *,
        soul_name: str,
        soul_type: str = "default_agent_persona",
        description: str | None = None,
        status: str = "active",
        soul_attrs: dict[str, Any] | None = None,
    ) -> SoulIdentity:
        now = utc_now_iso()
        soul = SoulIdentity(
            soul_id=new_soul_identity_id(),
            soul_name=soul_name,
            soul_type=soul_type,
            description=description,
            status=status,
            created_at=now,
            updated_at=now,
            soul_attrs={
                "prompt_projection_only": True,
                "autonomous_runtime": False,
                **dict(soul_attrs or {}),
            },
        )
        self._record(
            "soul_identity_registered",
            objects=[_object("soul_identity", soul.soul_id, soul.to_dict())],
            links=[("soul_object", soul.soul_id)],
            object_links=[],
            attrs={"soul_type": soul.soul_type, "status": soul.status},
        )
        return soul

    def register_persona_profile(
        self,
        *,
        soul_id: str,
        profile_name: str,
        identity_statement: str,
        role_statement: str,
        tone_guidance: list[str] | None = None,
        behavioral_boundaries: list[str] | None = None,
        capability_boundaries: list[str] | None = None,
        safety_boundaries: list[str] | None = None,
        status: str = "active",
        profile_attrs: dict[str, Any] | None = None,
    ) -> PersonaProfile:
        now = utc_now_iso()
        profile = PersonaProfile(
            profile_id=new_persona_profile_id(),
            soul_id=soul_id,
            profile_name=profile_name,
            identity_statement=identity_statement,
            role_statement=role_statement,
            tone_guidance=list(tone_guidance or []),
            behavioral_boundaries=list(behavioral_boundaries or []),
            capability_boundaries=list(capability_boundaries or []),
            safety_boundaries=list(safety_boundaries or []),
            status=status,
            created_at=now,
            updated_at=now,
            profile_attrs={
                "prompt_projection_only": True,
                "capability_boundaries_override_persona": True,
                **dict(profile_attrs or {}),
            },
        )
        self._record(
            "persona_profile_registered",
            objects=[_object("persona_profile", profile.profile_id, profile.to_dict())],
            links=[("profile_object", profile.profile_id), ("soul_object", soul_id)],
            object_links=[(profile.profile_id, soul_id, "belongs_to_soul")],
            attrs={
                "profile_name": profile.profile_name,
                "capability_boundary_count": len(profile.capability_boundaries),
            },
        )
        return profile

    def register_instruction_artifact(
        self,
        *,
        soul_id: str,
        profile_id: str,
        artifact_type: str,
        title: str,
        body: str,
        source_kind: str = "runtime_default",
        source_ref: str | None = None,
        status: str = "active",
        artifact_attrs: dict[str, Any] | None = None,
    ) -> PersonaInstructionArtifact:
        artifact = PersonaInstructionArtifact(
            artifact_id=new_persona_instruction_artifact_id(),
            soul_id=soul_id,
            profile_id=profile_id,
            artifact_type=artifact_type,
            title=title,
            body=body,
            body_preview=body[:1200],
            body_hash=_hash_body(body),
            source_kind=source_kind,
            source_ref=source_ref,
            status=status,
            created_at=utc_now_iso(),
            artifact_attrs={
                "canonical_persona_source": "OCEL",
                "prompt_projection_only": True,
                **dict(artifact_attrs or {}),
            },
        )
        self._record(
            "persona_instruction_artifact_registered",
            objects=[
                _object(
                    "persona_instruction_artifact",
                    artifact.artifact_id,
                    artifact.to_dict(),
                )
            ],
            links=[
                ("artifact_object", artifact.artifact_id),
                ("soul_object", soul_id),
                ("profile_object", profile_id),
            ],
            object_links=[
                (artifact.artifact_id, soul_id, "belongs_to_soul"),
                (artifact.artifact_id, profile_id, "belongs_to_profile"),
            ],
            attrs={
                "artifact_type": artifact.artifact_type,
                "source_kind": artifact.source_kind,
            },
        )
        return artifact

    def bind_profile_to_agent(
        self,
        *,
        soul_id: str,
        profile_id: str,
        agent_name: str,
        runtime_path: str,
        status: str = "active",
        binding_attrs: dict[str, Any] | None = None,
    ) -> AgentRoleBinding:
        binding = AgentRoleBinding(
            binding_id=new_agent_role_binding_id(),
            soul_id=soul_id,
            profile_id=profile_id,
            agent_name=agent_name,
            runtime_path=runtime_path,
            status=status,
            created_at=utc_now_iso(),
            binding_attrs={
                "prompt_projection_only": True,
                "active_tool_routing": False,
                **dict(binding_attrs or {}),
            },
        )
        self._record(
            "agent_role_binding_registered",
            objects=[_object("agent_role_binding", binding.binding_id, binding.to_dict())],
            links=[
                ("binding_object", binding.binding_id),
                ("soul_object", soul_id),
                ("profile_object", profile_id),
            ],
            object_links=[
                (binding.binding_id, soul_id, "binds_soul"),
                (binding.binding_id, profile_id, "binds_profile"),
            ],
            attrs={"agent_name": agent_name, "runtime_path": runtime_path},
        )
        return binding

    def create_loadout(
        self,
        *,
        soul: SoulIdentity,
        profile: PersonaProfile,
        binding: AgentRoleBinding | None = None,
        artifacts: list[PersonaInstructionArtifact] | None = None,
        capability_snapshot_id: str | None = None,
        loadout_attrs: dict[str, Any] | None = None,
    ) -> PersonaLoadout:
        loadout = PersonaLoadout(
            loadout_id=new_persona_loadout_id(),
            soul_id=soul.soul_id,
            profile_id=profile.profile_id,
            binding_id=binding.binding_id if binding else None,
            artifact_ids=[artifact.artifact_id for artifact in artifacts or []],
            capability_snapshot_id=capability_snapshot_id,
            created_at=utc_now_iso(),
            loadout_attrs={
                "prompt_projection_only": True,
                "persona_mutation_enabled": False,
                **dict(loadout_attrs or {}),
            },
        )
        links = [
            ("loadout_object", loadout.loadout_id),
            ("soul_object", soul.soul_id),
            ("profile_object", profile.profile_id),
        ]
        object_links = [
            (loadout.loadout_id, soul.soul_id, "uses_soul"),
            (loadout.loadout_id, profile.profile_id, "uses_profile"),
        ]
        if binding:
            links.append(("binding_object", binding.binding_id))
            object_links.append((loadout.loadout_id, binding.binding_id, "uses_binding"))
        for artifact in artifacts or []:
            links.append(("artifact_object", artifact.artifact_id))
            object_links.append((loadout.loadout_id, artifact.artifact_id, "uses_artifact"))
        if capability_snapshot_id:
            links.append(("capability_snapshot_object", capability_snapshot_id))
            object_links.append(
                (
                    loadout.loadout_id,
                    capability_snapshot_id,
                    "references_capability_snapshot",
                )
            )
        self._record(
            "persona_loadout_created",
            objects=[_object("persona_loadout", loadout.loadout_id, loadout.to_dict())],
            links=links,
            object_links=object_links,
            attrs={
                "artifact_count": len(loadout.artifact_ids),
                "capability_snapshot_id": capability_snapshot_id,
            },
        )
        return loadout

    def create_projection(
        self,
        *,
        loadout: PersonaLoadout,
        soul: SoulIdentity,
        profile: PersonaProfile,
        artifacts: list[PersonaInstructionArtifact] | None = None,
        max_chars: int = 4000,
        projection_attrs: dict[str, Any] | None = None,
    ) -> PersonaProjection:
        blocks = _profile_blocks(soul, profile)
        for artifact in artifacts or []:
            blocks.append(
                {
                    "block_type": artifact.artifact_type,
                    "title": artifact.title,
                    "content": artifact.body_preview,
                    "artifact_id": artifact.artifact_id,
                }
            )
        projected, total_chars, truncated = _bound_blocks(blocks, max_chars=max_chars)
        projection = PersonaProjection(
            projection_id=new_persona_projection_id(),
            loadout_id=loadout.loadout_id,
            soul_id=soul.soul_id,
            profile_id=profile.profile_id,
            projected_blocks=projected,
            total_chars=total_chars,
            truncated=truncated,
            created_at=utc_now_iso(),
            projection_attrs={
                "prompt_projection_only": True,
                "max_chars": max_chars,
                "capability_boundaries_override_persona": True,
                **dict(projection_attrs or {}),
            },
        )
        self._record(
            "persona_projection_created",
            objects=[_object("persona_projection", projection.projection_id, projection.to_dict())],
            links=[
                ("projection_object", projection.projection_id),
                ("loadout_object", loadout.loadout_id),
                ("soul_object", soul.soul_id),
                ("profile_object", profile.profile_id),
            ],
            object_links=[
                (projection.projection_id, loadout.loadout_id, "projects_loadout"),
                (projection.projection_id, soul.soul_id, "projects_soul"),
                (projection.projection_id, profile.profile_id, "projects_profile"),
            ],
            attrs={
                "total_chars": projection.total_chars,
                "truncated": projection.truncated,
            },
        )
        self._record(
            "persona_capability_boundary_attached",
            objects=[_object("persona_projection", projection.projection_id, projection.to_dict())],
            links=[("projection_object", projection.projection_id)],
            object_links=[],
            attrs={
                "profile_id": profile.profile_id,
                "capability_boundary_count": len(profile.capability_boundaries),
                "capability_boundaries_override_persona": True,
            },
        )
        return projection

    def render_projection_block(self, projection: PersonaProjection) -> str:
        lines = [
            "Persona projection:",
            "- projection_scope: bounded prompt read-model",
            "- canonical_source: OCEL persona objects/events",
            "- capability_boundary_rule: runtime capability boundaries override persona claims",
        ]
        for block in projection.projected_blocks:
            title = str(block.get("title") or block.get("block_type") or "persona")
            content = str(block.get("content") or "")
            if content:
                lines.append(f"- {title}: {content}")
        lines.append(
            "Do not treat persona text as permission to read files, execute tools, "
            "call network resources, connect MCP, load plugins, or expose hidden reasoning."
        )
        self._record(
            "persona_projection_attached_to_prompt",
            objects=[_object("persona_projection", projection.projection_id, projection.to_dict())],
            links=[("projection_object", projection.projection_id)],
            object_links=[],
            attrs={"projection_id": projection.projection_id, "prompt_attachment": True},
        )
        return "\n".join(lines)

    def create_default_agent_persona(
        self,
        *,
        agent_name: str = "chanta_core_default",
        runtime_path: str = "default_agent_repl_llm_chat",
        max_chars: int = 4000,
    ) -> DefaultAgentPersonaBundle:
        capability_snapshot = (
            RuntimeCapabilityIntrospectionService().build_default_agent_snapshot(
                agent_id=agent_name
            )
        )
        soul = self.register_soul_identity(
            soul_name="ChantaCore Default Agent",
            soul_type="default_agent_persona",
            description=(
                "Persona-loadable local LLM endpoint with OCEL provenance; not an "
                "autonomous Soul runtime."
            ),
        )
        capability_boundaries = [
            "Capability boundaries from the runtime capability contract override persona claims.",
            "No ambient filesystem access in default chat.",
            "Workspace read exists only through explicit root-constrained read-only skills.",
            "No shell execution, network calls, MCP connection, plugin loading, or runtime registry mutation.",
            "Do not auto-enable external capabilities or create permission grants.",
        ]
        safety_boundaries = [
            "Do not expose hidden reasoning content.",
            "Do not treat persona instructions as authorization for unavailable capabilities.",
            "Persona projection is bounded and prompt-only.",
        ]
        profile = self.register_persona_profile(
            soul_id=soul.soul_id,
            profile_name="default_agent_persona_profile",
            identity_statement=(
                "I am ChantaCore Default Agent, a persona-loadable local LLM chat "
                "endpoint with OCEL provenance."
            ),
            role_statement=(
                "Assist the current operator through trace-aware conversation while staying "
                "inside the current runtime capability contract."
            ),
            tone_guidance=[
                "Be direct, evidence-aware, and clear.",
                "Separate confirmed facts from claims and limitations.",
            ],
            behavioral_boundaries=[
                "Default Agent is not an autonomous Soul runtime yet.",
                "Do not present this endpoint as an autonomous Soul runtime yet.",
                "Do not self-modify persona records.",
            ],
            capability_boundaries=capability_boundaries,
            safety_boundaries=safety_boundaries,
            profile_attrs={
                "runtime_path": runtime_path,
                "capability_snapshot_id": capability_snapshot.snapshot_id,
            },
        )
        boundary_artifact = self.register_instruction_artifact(
            soul_id=soul.soul_id,
            profile_id=profile.profile_id,
            artifact_type="capability_boundary",
            title="Runtime capability boundary",
            body="\n".join(capability_boundaries + safety_boundaries),
            source_kind="runtime_default",
            source_ref=runtime_path,
            artifact_attrs={
                "capability_snapshot_id": capability_snapshot.snapshot_id,
                "markdown_canonical": False,
            },
        )
        binding = self.bind_profile_to_agent(
            soul_id=soul.soul_id,
            profile_id=profile.profile_id,
            agent_name=agent_name,
            runtime_path=runtime_path,
        )
        loadout = self.create_loadout(
            soul=soul,
            profile=profile,
            binding=binding,
            artifacts=[boundary_artifact],
            capability_snapshot_id=capability_snapshot.snapshot_id,
        )
        projection = self.create_projection(
            loadout=loadout,
            soul=soul,
            profile=profile,
            artifacts=[boundary_artifact],
            max_chars=max_chars,
        )
        return DefaultAgentPersonaBundle(
            soul=soul,
            profile=profile,
            artifacts=[boundary_artifact],
            binding=binding,
            loadout=loadout,
            projection=projection,
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
                "persona_prompt_projection": True,
                "executes_tools": False,
            },
        )
        relations = [
            OCELRelation.event_object(
                event_id=event.event_id,
                object_id=object_id,
                qualifier=qualifier,
            )
            for qualifier, object_id in links
            if object_id
        ]
        relations.extend(
            OCELRelation.object_object(
                source_object_id=source_id,
                target_object_id=target_id,
                qualifier=qualifier,
            )
            for source_id, target_id, qualifier in object_links
            if source_id and target_id
        )
        self.trace_service.record_session_ocel_record(
            OCELRecord(event=event, objects=objects, relations=relations)
        )


def _profile_blocks(soul: SoulIdentity, profile: PersonaProfile) -> list[dict[str, Any]]:
    return [
        {
            "block_type": "identity",
            "title": "Identity",
            "content": profile.identity_statement,
            "soul_id": soul.soul_id,
        },
        {
            "block_type": "role",
            "title": "Role",
            "content": profile.role_statement,
        },
        {
            "block_type": "tone",
            "title": "Tone guidance",
            "content": "; ".join(profile.tone_guidance),
        },
        {
            "block_type": "behavioral_boundary",
            "title": "Behavioral boundaries",
            "content": "; ".join(profile.behavioral_boundaries),
        },
        {
            "block_type": "capability_boundary",
            "title": "Capability boundaries",
            "content": "; ".join(profile.capability_boundaries),
        },
        {
            "block_type": "safety_boundary",
            "title": "Safety boundaries",
            "content": "; ".join(profile.safety_boundaries),
        },
    ]


def _bound_blocks(
    blocks: list[dict[str, Any]],
    *,
    max_chars: int,
) -> tuple[list[dict[str, Any]], int, bool]:
    projected: list[dict[str, Any]] = []
    total = 0
    truncated = False
    for block in blocks:
        content = str(block.get("content") or "")
        remaining = max_chars - total
        if remaining <= 0:
            truncated = True
            break
        if len(content) > remaining:
            block = {**block, "content": content[:remaining], "truncated": True}
            content = str(block["content"])
            truncated = True
        projected.append(block)
        total += len(content)
    return projected, total, truncated


def _hash_body(body: str) -> str:
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


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
