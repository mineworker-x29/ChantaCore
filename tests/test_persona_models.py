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
from chanta_core.utility.time import utc_now_iso


def test_persona_ids_use_expected_prefixes() -> None:
    assert new_soul_identity_id().startswith("soul_identity:")
    assert new_persona_profile_id().startswith("persona_profile:")
    assert new_persona_instruction_artifact_id().startswith("persona_instruction_artifact:")
    assert new_agent_role_binding_id().startswith("agent_role_binding:")
    assert new_persona_loadout_id().startswith("persona_loadout:")
    assert new_persona_projection_id().startswith("persona_projection:")


def test_persona_models_to_dict() -> None:
    now = utc_now_iso()
    soul = SoulIdentity("soul", "Default", "default_agent", "desc", "active", now, now, {})
    profile = PersonaProfile(
        "profile",
        "soul",
        "default",
        "identity",
        "role",
        ["tone"],
        ["behavior"],
        ["capability"],
        ["safety"],
        "active",
        now,
        now,
        {},
    )
    artifact = PersonaInstructionArtifact(
        "artifact",
        "soul",
        "profile",
        "capability_boundary",
        "Boundary",
        "body",
        "body",
        "hash",
        "runtime_default",
        None,
        "active",
        now,
        {},
    )
    binding = AgentRoleBinding("binding", "soul", "profile", "agent", "runtime", "active", now, {})
    loadout = PersonaLoadout("loadout", "soul", "profile", "binding", ["artifact"], "snapshot", now, {})
    projection = PersonaProjection("projection", "loadout", "soul", "profile", [{"content": "identity"}], 8, False, now, {})

    assert soul.to_dict()["soul_id"] == "soul"
    assert profile.to_dict()["capability_boundaries"] == ["capability"]
    assert artifact.to_dict()["artifact_type"] == "capability_boundary"
    assert binding.to_dict()["runtime_path"] == "runtime"
    assert loadout.to_dict()["artifact_ids"] == ["artifact"]
    assert projection.to_dict()["total_chars"] == 8
