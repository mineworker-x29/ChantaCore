from chanta_core.instructions import (
    InstructionArtifact,
    ProjectRule,
    UserPreference,
    hash_body,
    instruction_artifacts_to_history_entries,
    project_rules_to_history_entries,
    user_preferences_to_history_entries,
)


def test_instruction_history_adapters_convert_active_objects() -> None:
    instruction = InstructionArtifact(
        instruction_id="instruction:test",
        instruction_type="project",
        title="Project",
        body="Follow project rules.",
        body_preview="Follow project rules.",
        body_hash=hash_body("Follow project rules."),
        status="active",
        scope="project",
        priority=90,
        created_at="2026-05-05T00:00:00Z",
        updated_at="2026-05-05T00:00:00Z",
        source_path=None,
    )
    rule = ProjectRule(
        rule_id="project_rule:test",
        rule_type="constraint",
        text="Use OCEL.",
        status="active",
        priority=85,
        created_at="2026-05-05T00:00:00Z",
        updated_at="2026-05-05T00:00:00Z",
        source_instruction_id=instruction.instruction_id,
    )
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

    instruction_entries = instruction_artifacts_to_history_entries([instruction])
    rule_entries = project_rules_to_history_entries([rule])
    preference_entries = user_preferences_to_history_entries([preference])

    assert instruction_entries[0].source == "instruction"
    assert rule_entries[0].source == "project_rule"
    assert preference_entries[0].source == "user_preference"
    assert instruction_entries[0].refs[0]["ref_id"] == "instruction:test"
    assert rule_entries[0].refs[0]["source_instruction_id"] == "instruction:test"
    assert preference_entries[0].refs[0]["preference_key"] == "tone"


def test_instruction_history_adapters_skip_deprecated_objects() -> None:
    instruction = InstructionArtifact(
        instruction_id="instruction:old",
        instruction_type="project",
        title="Old",
        body="old",
        body_preview="old",
        body_hash=hash_body("old"),
        status="deprecated",
        scope=None,
        priority=10,
        created_at="2026-05-05T00:00:00Z",
        updated_at="2026-05-05T00:00:00Z",
        source_path=None,
    )

    assert instruction_artifacts_to_history_entries([instruction]) == []
