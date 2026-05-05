from chanta_core.instructions import (
    InstructionArtifact,
    ProjectRule,
    UserPreference,
    hash_body,
    new_instruction_artifact_id,
    new_project_rule_id,
    new_user_preference_id,
    preview_body,
)


def test_instruction_ids_use_expected_prefixes() -> None:
    assert new_instruction_artifact_id().startswith("instruction:")
    assert new_project_rule_id().startswith("project_rule:")
    assert new_user_preference_id().startswith("user_preference:")


def test_instruction_hash_and_preview_helpers() -> None:
    assert hash_body("body") == hash_body("body")
    assert preview_body("short") == "short"


def test_instruction_artifact_to_dict() -> None:
    artifact = InstructionArtifact(
        instruction_id="instruction:test",
        instruction_type="project",
        title="Project",
        body="body",
        body_preview="body",
        body_hash=hash_body("body"),
        status="active",
        scope="project",
        priority=90,
        created_at="2026-05-05T00:00:00Z",
        updated_at="2026-05-05T00:00:00Z",
        source_path=None,
    )

    assert artifact.to_dict()["instruction_type"] == "project"


def test_project_rule_to_dict() -> None:
    rule = ProjectRule(
        rule_id="project_rule:test",
        rule_type="do_not",
        text="Do not add markdown memory.",
        status="active",
        priority=100,
        created_at="2026-05-05T00:00:00Z",
        updated_at="2026-05-05T00:00:00Z",
        source_instruction_id="instruction:test",
    )

    assert rule.to_dict()["rule_type"] == "do_not"


def test_user_preference_to_dict() -> None:
    preference = UserPreference(
        preference_id="user_preference:test",
        preference_key="tone",
        preference_value="direct",
        status="active",
        confidence=1.0,
        source_kind="explicit_user_statement",
        created_at="2026-05-05T00:00:00Z",
        updated_at="2026-05-05T00:00:00Z",
    )

    assert preference.to_dict()["preference_key"] == "tone"
