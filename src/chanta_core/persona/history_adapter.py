from __future__ import annotations

from chanta_core.context.history import ContextHistoryEntry, new_context_history_entry_id
from chanta_core.persona.models import (
    PersonaInstructionArtifact,
    PersonaProfile,
    PersonaProjection,
)
from chanta_core.persona.personal_overlay import (
    PersonalOverlayBoundaryFinding,
    PersonalOverlayLoadResult,
    PersonalDirectoryManifest,
    PersonalProjectionRef,
)
from chanta_core.persona.personal_mode_loadout import (
    PersonalCoreProfile,
    PersonalModeBoundary,
    PersonalModeLoadout,
    PersonalModeProfile,
)
from chanta_core.persona.source_import import (
    PersonaAssimilationDraft,
    PersonaProjectionCandidate,
    PersonaSource,
    PersonaSourceIngestionCandidate,
    PersonaSourceRiskNote,
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


def persona_sources_to_history_entries(
    sources: list[PersonaSource],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=source.content_preview,
            created_at=source.created_at,
            source="persona_source_import",
            priority=40,
            refs=[{"ref_type": "persona_source", "ref_id": source.source_id}],
            entry_attrs={
                "source_type": source.source_type,
                "content_hash": source.content_hash,
                "canonical_persona_source": False,
            },
        )
        for source in sources
    ]


def persona_ingestion_candidates_to_history_entries(
    candidates: list[PersonaSourceIngestionCandidate],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=(
                f"Persona source candidate {candidate.candidate_id}: "
                f"{candidate.review_status}; canonical_import_enabled="
                f"{candidate.canonical_import_enabled}"
            ),
            created_at=candidate.created_at,
            source="persona_source_import",
            priority=45,
            refs=[
                {
                    "ref_type": "persona_source_ingestion_candidate",
                    "ref_id": candidate.candidate_id,
                }
            ],
            entry_attrs={
                "review_status": candidate.review_status,
                "canonical_import_enabled": candidate.canonical_import_enabled,
            },
        )
        for candidate in candidates
    ]


def persona_assimilation_drafts_to_history_entries(
    drafts: list[PersonaAssimilationDraft],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content="\n".join(
                draft.identity_points
                + draft.role_points
                + draft.boundary_points
                + draft.safety_points
            ),
            created_at=draft.created_at,
            source="persona_source_import",
            priority=50,
            refs=[
                {"ref_type": "persona_assimilation_draft", "ref_id": draft.draft_id},
                {
                    "ref_type": "persona_source_ingestion_candidate",
                    "ref_id": draft.candidate_id,
                },
            ],
            entry_attrs={"draft_type": draft.draft_type},
        )
        for draft in drafts
    ]


def persona_projection_candidates_to_history_entries(
    projection_candidates: list[PersonaProjectionCandidate],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content="\n".join(
                "\n".join(str(item) for item in block.get("items", []))
                for block in projection.projected_blocks
            ),
            created_at=projection.created_at,
            source="persona_source_import",
            priority=50,
            refs=[
                {
                    "ref_type": "persona_projection_candidate",
                    "ref_id": projection.projection_candidate_id,
                },
                {"ref_type": "persona_assimilation_draft", "ref_id": projection.draft_id},
            ],
            entry_attrs={
                "projection_type": projection.projection_type,
                "truncated": projection.truncated,
                "canonical_import_enabled": projection.canonical_import_enabled,
            },
        )
        for projection in projection_candidates
    ]


def persona_source_risk_notes_to_history_entries(
    risk_notes: list[PersonaSourceRiskNote],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=note.message,
            created_at=note.created_at,
            source="persona_source_import",
            priority=70 if note.review_required else 40,
            refs=[
                {"ref_type": "persona_source_risk_note", "ref_id": note.risk_note_id},
                {"ref_type": "persona_source", "ref_id": note.source_id},
                {
                    "ref_type": "persona_source_ingestion_candidate",
                    "ref_id": note.candidate_id,
                },
            ],
            entry_attrs={
                "risk_level": note.risk_level,
                "risk_categories": list(note.risk_categories),
                "review_required": note.review_required,
            },
        )
        for note in risk_notes
    ]


def personal_directory_manifests_to_history_entries(
    manifests: list[PersonalDirectoryManifest],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=(
                "Personal Directory manifest "
                f"{manifest.manifest_id}: "
                f"{len(manifest.available_projection_refs)} projection refs, "
                f"{len(manifest.available_loadout_refs)} loadout refs."
            ),
            created_at=manifest.created_at,
            source="personal_overlay",
            priority=35,
            refs=[{"ref_type": "personal_directory_manifest", "ref_id": manifest.manifest_id}],
            entry_attrs={
                "directory_root_hash": manifest.manifest_attrs.get("root_hash"),
                "projection_ref_count": len(manifest.available_projection_refs),
                "loadout_ref_count": len(manifest.available_loadout_refs),
            },
        )
        for manifest in manifests
    ]


def personal_projection_refs_to_history_entries(
    refs: list[PersonalProjectionRef],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=(
                f"Personal Overlay projection ref {ref.projection_name}: "
                f"{ref.projection_kind}; safe_for_prompt={ref.safe_for_prompt}."
            ),
            created_at=ref.created_at,
            source="personal_overlay",
            priority=45 if ref.safe_for_prompt else 25,
            refs=[
                {
                    "ref_type": "personal_projection_ref",
                    "ref_id": ref.projection_ref_id,
                },
                {"ref_type": "personal_directory_manifest", "ref_id": ref.manifest_id},
            ],
            entry_attrs={
                "projection_kind": ref.projection_kind,
                "content_hash": ref.content_hash,
                "safe_for_prompt": ref.safe_for_prompt,
                "path_hash": ref.ref_attrs.get("path_hash"),
                "path_basename": ref.ref_attrs.get("path_basename"),
            },
        )
        for ref in refs
    ]


def personal_overlay_load_results_to_history_entries(
    results: list[PersonalOverlayLoadResult],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=(
                f"Personal Overlay load result {result.result_id}: "
                f"denied={result.denied}; loaded_refs={len(result.loaded_projection_ref_ids)}."
            ),
            created_at=result.created_at,
            source="personal_overlay",
            priority=65 if result.denied else 50,
            refs=[
                {"ref_type": "personal_overlay_load_result", "ref_id": result.result_id},
                {
                    "ref_type": "personal_overlay_load_request",
                    "ref_id": result.request_id,
                },
                {"ref_type": "personal_directory_manifest", "ref_id": result.manifest_id},
            ],
            entry_attrs={
                "denied": result.denied,
                "truncated": result.truncated,
                "loaded_projection_ref_count": len(result.loaded_projection_ref_ids),
                "total_chars": result.total_chars,
            },
        )
        for result in results
    ]


def personal_overlay_boundary_findings_to_history_entries(
    findings: list[PersonalOverlayBoundaryFinding],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=(
                f"Personal Overlay boundary finding {finding.finding_type}: "
                f"{finding.status}/{finding.severity}."
            ),
            created_at=finding.created_at,
            source="personal_overlay",
            priority=80 if finding.status == "failed" else 40,
            refs=[
                {
                    "ref_type": "personal_overlay_boundary_finding",
                    "ref_id": finding.finding_id,
                },
                {"ref_type": "personal_directory_manifest", "ref_id": finding.manifest_id},
            ],
            entry_attrs={
                "finding_type": finding.finding_type,
                "status": finding.status,
                "severity": finding.severity,
                "subject_ref": finding.subject_ref,
            },
        )
        for finding in findings
    ]


def personal_core_profiles_to_history_entries(
    profiles: list[PersonalCoreProfile],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=profile.identity_statement,
            created_at=profile.created_at,
            source="personal_mode_loadout",
            priority=55,
            refs=[
                {
                    "ref_type": "personal_core_profile",
                    "ref_id": profile.core_profile_id,
                }
            ],
            entry_attrs={
                "profile_name": profile.profile_name,
                "profile_type": profile.profile_type,
                "private": profile.private,
            },
        )
        for profile in profiles
    ]


def personal_mode_profiles_to_history_entries(
    profiles: list[PersonalModeProfile],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=profile.role_statement,
            created_at=profile.created_at,
            source="personal_mode_loadout",
            priority=55,
            refs=[
                {"ref_type": "personal_mode_profile", "ref_id": profile.mode_profile_id},
                {"ref_type": "personal_core_profile", "ref_id": profile.core_profile_id},
            ],
            entry_attrs={
                "mode_name": profile.mode_name,
                "mode_type": profile.mode_type,
                "private": profile.private,
            },
        )
        for profile in profiles
    ]


def personal_mode_loadouts_to_history_entries(
    loadouts: list[PersonalModeLoadout],
) -> list[ContextHistoryEntry]:
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content="\n".join(
                [
                    loadout.identity_block,
                    loadout.role_block,
                    loadout.capability_boundary_block,
                    loadout.safety_boundary_block,
                    loadout.privacy_boundary_block or "",
                ]
            ),
            created_at=loadout.created_at,
            source="personal_mode_loadout",
            priority=70,
            refs=[
                {"ref_type": "personal_mode_loadout", "ref_id": loadout.loadout_id},
                {"ref_type": "personal_core_profile", "ref_id": loadout.core_profile_id},
                {"ref_type": "personal_mode_profile", "ref_id": loadout.mode_profile_id},
            ],
            entry_attrs={
                "loadout_name": loadout.loadout_name,
                "truncated": loadout.truncated,
                "private": loadout.private,
                "capability_binding_count": len(loadout.capability_binding_ids),
            },
        )
        for loadout in loadouts
    ]


def personal_mode_boundaries_to_history_entries(
    boundaries: list[PersonalModeBoundary],
) -> list[ContextHistoryEntry]:
    priority_by_type = {
        "capability_boundary": 80,
        "privacy_boundary": 80,
        "mode_separation": 80,
        "runtime_boundary": 75,
        "safety_boundary": 75,
        "source_boundary": 65,
        "tool_boundary": 65,
        "memory_boundary": 65,
    }
    return [
        ContextHistoryEntry(
            entry_id=new_context_history_entry_id(),
            session_id=None,
            process_instance_id=None,
            role="context",
            content=boundary.boundary_text,
            created_at=boundary.created_at,
            source="personal_mode_loadout",
            priority=priority_by_type.get(boundary.boundary_type, 50),
            refs=[
                {"ref_type": "personal_mode_boundary", "ref_id": boundary.boundary_id},
                {"ref_type": "personal_mode_profile", "ref_id": boundary.mode_profile_id},
            ],
            entry_attrs={
                "boundary_type": boundary.boundary_type,
                "severity": boundary.severity,
                "required": boundary.required,
            },
        )
        for boundary in boundaries
    ]

