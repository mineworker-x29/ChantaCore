from chanta_core.instructions import (
    InstructionArtifact,
    ProjectRule,
    UserPreference,
    hash_body,
)
from chanta_core.materialized_views import (
    MaterializedViewInputSnapshot,
    render_context_rules_view,
    render_memory_view,
    render_pig_guidance_view,
    render_project_view,
    render_user_view,
)
from chanta_core.memory import MemoryEntry, hash_content


def make_snapshot() -> MaterializedViewInputSnapshot:
    return MaterializedViewInputSnapshot(
        memories=[
            MemoryEntry(
                memory_id="memory:active",
                memory_type="semantic",
                title="Active Memory",
                content="Active content",
                content_preview="Active content",
                content_hash=hash_content("Active content"),
                status="active",
                confidence=0.9,
                created_at="2026-05-05T00:00:00Z",
                updated_at="2026-05-05T00:00:00Z",
                valid_from=None,
                valid_until=None,
                contradiction_status="none",
                source_kind="manual_entry",
                scope="project",
            ),
            MemoryEntry(
                memory_id="memory:archived",
                memory_type="semantic",
                title="Archived Memory",
                content="Archived content",
                content_preview="Archived content",
                content_hash=hash_content("Archived content"),
                status="archived",
                confidence=None,
                created_at="2026-05-05T00:00:00Z",
                updated_at="2026-05-05T00:00:00Z",
                valid_from=None,
                valid_until=None,
                contradiction_status="unknown",
                source_kind=None,
                scope=None,
            ),
        ],
        instructions=[
            InstructionArtifact(
                instruction_id="instruction:project",
                instruction_type="project",
                title="Project Instruction",
                body="Project body",
                body_preview="Project body",
                body_hash=hash_body("Project body"),
                status="active",
                scope="project",
                priority=90,
                created_at="2026-05-05T00:00:00Z",
                updated_at="2026-05-05T00:00:00Z",
                source_path=None,
            )
        ],
        project_rules=[
            ProjectRule(
                rule_id="project_rule:constraint",
                rule_type="constraint",
                text="Use OCEL.",
                status="active",
                priority=100,
                created_at="2026-05-05T00:00:00Z",
                updated_at="2026-05-05T00:00:00Z",
                source_instruction_id="instruction:project",
            )
        ],
        user_preferences=[
            UserPreference(
                preference_id="user_preference:tone",
                preference_key="tone",
                preference_value="direct",
                status="active",
                confidence=1.0,
                source_kind="explicit_user_statement",
                created_at="2026-05-05T00:00:00Z",
                updated_at="2026-05-05T00:00:00Z",
            )
        ],
        pig_report=None,
    )


def test_render_memory_view_contains_warning_ids_and_hash() -> None:
    view = render_memory_view(make_snapshot(), target_path=".chanta/MEMORY.md")

    assert "Canonical source: OCEL" in view.content
    assert "This file is not canonical memory" in view.content
    assert "memory:active" in view.content
    assert "memory:archived" in view.content
    assert hash_content("Active content") in view.content
    assert view.canonical is False


def test_project_user_and_context_views_include_expected_objects() -> None:
    snapshot = make_snapshot()

    project = render_project_view(snapshot, target_path=".chanta/PROJECT.md")
    user = render_user_view(snapshot, target_path=".chanta/USER.md")
    context = render_context_rules_view(snapshot, target_path=".chanta/CONTEXT_RULES.md")

    assert "instruction:project" in project.content
    assert "project_rule:constraint" in project.content
    assert "user_preference:tone" in user.content
    assert "not a prompt that must be injected wholesale" in context.content
    assert "Use OCEL." in context.content


def test_pig_guidance_view_handles_empty_state() -> None:
    view = render_pig_guidance_view(make_snapshot(), target_path=".chanta/PIG_GUIDANCE.md")

    assert "No PIG report snapshot was provided." in view.content
    assert "Guidance" in view.content
    assert "Diagnostics" in view.content
    assert "Conformance Notes" in view.content


def test_render_output_is_deterministic_except_generated_metadata() -> None:
    first = render_memory_view(make_snapshot(), target_path=".chanta/MEMORY.md")
    second = render_memory_view(make_snapshot(), target_path=".chanta/MEMORY.md")

    def normalize(content: str) -> str:
        lines = []
        for line in content.splitlines():
            if any(key in line for key in ["view_id", "generated_at", "content_hash"]):
                continue
            lines.append(line)
        return "\n".join(lines)

    assert normalize(first.content) == normalize(second.content)
