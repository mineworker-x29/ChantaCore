from __future__ import annotations

from chanta_core.context.history import ContextHistoryEntry, new_context_history_entry_id
from chanta_core.persona.models import (
    PersonaInstructionArtifact,
    PersonaProfile,
    PersonaProjection,
)


def persona_profiles_to_history_entries(
    profiles: list[PersonaProfile],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=profile.identity_statement,
            created_at=profile.created_at,
            source="persona",
            priority=70 if profile.capability_boundaries or profile.safety_boundaries else 55,
            refs=[
                {"ref_type": "persona_profile", "ref_id": profile.profile_id},
                {"ref_type": "soul_identity", "ref_id": profile.soul_id},
            ],
            entry_attrs={
                "profile_name": profile.profile_name,
                "capability_boundaries": list(profile.capability_boundaries),
            },
        )
        for profile in profiles
    ]


def persona_projections_to_history_entries(
    projections: list[PersonaProjection],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content="\n".join(str(block.get("content") or "") for block in projection.projected_blocks),
            created_at=projection.created_at,
            source="persona",
            priority=75,
            refs=[
                {"ref_type": "persona_projection", "ref_id": projection.projection_id},
                {"ref_type": "persona_loadout", "ref_id": projection.loadout_id},
                {"ref_type": "soul_identity", "ref_id": projection.soul_id},
                {"ref_type": "persona_profile", "ref_id": projection.profile_id},
            ],
            entry_attrs={
                "total_chars": projection.total_chars,
                "truncated": projection.truncated,
            },
        )
        for projection in projections
    ]


def persona_instruction_artifacts_to_history_entries(
    artifacts: list[PersonaInstructionArtifact],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=artifact.body_preview,
            created_at=artifact.created_at,
            source="persona",
            priority=75 if artifact.artifact_type in {"capability_boundary", "safety_boundary"} else 45,
            refs=[
                {"ref_type": "persona_instruction_artifact", "ref_id": artifact.artifact_id},
                {"ref_type": "soul_identity", "ref_id": artifact.soul_id},
                {"ref_type": "persona_profile", "ref_id": artifact.profile_id},
            ],
            entry_attrs={
                "artifact_type": artifact.artifact_type,
                "title": artifact.title,
                "body_hash": artifact.body_hash,
                "source_kind": artifact.source_kind,
            },
        )
        for artifact in artifacts
    ]
