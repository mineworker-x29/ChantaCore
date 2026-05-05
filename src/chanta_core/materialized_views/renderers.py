from __future__ import annotations

from typing import Any

from chanta_core.instructions import InstructionArtifact, ProjectRule, UserPreference
from chanta_core.materialized_views.ids import new_materialized_view_id
from chanta_core.materialized_views.markdown import (
    markdown_bullet,
    markdown_heading,
    render_generated_warning,
    render_view_metadata_block,
)
from chanta_core.materialized_views.models import (
    MaterializedView,
    MaterializedViewInputSnapshot,
    hash_content,
)
from chanta_core.memory import MemoryEntry
from chanta_core.utility.time import utc_now_iso


def render_memory_view(
    snapshot: MaterializedViewInputSnapshot,
    *,
    target_path: str,
) -> MaterializedView:
    return _make_view(
        view_type="memory",
        title="ChantaCore Memory View",
        target_path=target_path,
        body_sections=[
            _memory_section("Active Memories", snapshot.memories, {"active"}),
            _memory_section("Draft Memories", snapshot.memories, {"draft"}),
            _memory_section(
                "Superseded / Archived / Withdrawn Memories",
                snapshot.memories,
                {"superseded", "archived", "withdrawn"},
            ),
            _revision_summary(snapshot.memories),
        ],
        view_attrs={"memory_count": len(snapshot.memories)},
    )


def render_project_view(
    snapshot: MaterializedViewInputSnapshot,
    *,
    target_path: str,
) -> MaterializedView:
    project_instructions = [
        item
        for item in snapshot.instructions
        if item.instruction_type == "project" or item.scope == "project"
    ]
    return _make_view(
        view_type="project",
        title="ChantaCore Project View",
        target_path=target_path,
        body_sections=[
            _instruction_section("Project Instructions", project_instructions),
            _rule_section("Project Rules", snapshot.project_rules, include_inactive=True),
        ],
        view_attrs={
            "instruction_count": len(project_instructions),
            "project_rule_count": len(snapshot.project_rules),
        },
    )


def render_user_view(
    snapshot: MaterializedViewInputSnapshot,
    *,
    target_path: str,
) -> MaterializedView:
    active = [item for item in snapshot.user_preferences if item.status == "active"]
    inactive = [item for item in snapshot.user_preferences if item.status != "active"]
    return _make_view(
        view_type="user",
        title="ChantaCore User Preference View",
        target_path=target_path,
        body_sections=[
            _preference_section("Active Preferences", active),
            _preference_section("Deprecated / Archived / Withdrawn Preferences", inactive),
        ],
        view_attrs={"user_preference_count": len(snapshot.user_preferences)},
    )


def render_pig_guidance_view(
    snapshot: MaterializedViewInputSnapshot,
    *,
    target_path: str,
) -> MaterializedView:
    report = snapshot.pig_report or {}
    body_sections = [
        _pig_summary_section(report),
        _pig_list_section("Guidance", report.get("guidance_summary")),
        _pig_list_section("Diagnostics", report.get("diagnostics")),
        _pig_list_section("Conformance Notes", report.get("conformance_report")),
    ]
    return _make_view(
        view_type="pig_guidance",
        title="ChantaCore PIG Guidance View",
        target_path=target_path,
        body_sections=body_sections,
        view_attrs={"has_pig_report": bool(snapshot.pig_report)},
    )


def render_context_rules_view(
    snapshot: MaterializedViewInputSnapshot,
    *,
    target_path: str,
) -> MaterializedView:
    active_rules = [item for item in snapshot.project_rules if item.status == "active"]
    active_preferences = [
        item for item in snapshot.user_preferences if item.status == "active"
    ]
    active_instructions = [
        item for item in snapshot.instructions if item.status == "active"
    ]
    excluded_count = (
        len(snapshot.project_rules)
        + len(snapshot.user_preferences)
        + len(snapshot.instructions)
        - len(active_rules)
        - len(active_preferences)
        - len(active_instructions)
    )
    return _make_view(
        view_type="context_rules",
        title="ChantaCore Context Rules View",
        target_path=target_path,
        body_sections=[
            "\n".join(
                [
                    markdown_heading("Context Assembly Notes", 2),
                    "- This file is a readable projection for future context assembly.",
                    "- It is not a prompt that must be injected wholesale.",
                    "- Use OCEL-native records as the canonical source.",
                ]
            ),
            _rule_section("Active Project Rules", active_rules, include_inactive=False),
            _preference_section("Active User Preferences", active_preferences),
            _instruction_section("Active Instruction Artifacts", active_instructions),
            "\n".join(
                [
                    markdown_heading("Excluded / Deprecated Items", 2),
                    markdown_bullet("excluded_count", excluded_count),
                ]
            ),
        ],
        view_attrs={
            "active_rule_count": len(active_rules),
            "active_preference_count": len(active_preferences),
            "active_instruction_count": len(active_instructions),
            "excluded_count": excluded_count,
        },
    )


def _make_view(
    *,
    view_type: str,
    title: str,
    target_path: str,
    body_sections: list[str],
    view_attrs: dict[str, Any],
) -> MaterializedView:
    generated_at = utc_now_iso()
    view_id = new_materialized_view_id()
    provisional = "\n\n".join(
        [
            markdown_heading(title, 1),
            render_generated_warning(view_type=view_type),
            *body_sections,
        ]
    ).rstrip() + "\n"
    content_hash = hash_content(provisional)
    content = "\n\n".join(
        [
            markdown_heading(title, 1),
            render_generated_warning(view_type=view_type),
            render_view_metadata_block(
                view_id=view_id,
                view_type=view_type,
                target_path=target_path,
                generated_at=generated_at,
                content_hash=content_hash,
                source_kind="ocel_materialized_projection",
                canonical=False,
            ),
            *body_sections,
        ]
    ).rstrip() + "\n"
    return MaterializedView(
        view_id=view_id,
        view_type=view_type,
        title=title,
        target_path=target_path,
        content=content,
        content_hash=hash_content(content),
        generated_at=generated_at,
        source_kind="ocel_materialized_projection",
        canonical=False,
        view_attrs=view_attrs,
    )


def _memory_section(
    title: str,
    memories: list[MemoryEntry],
    statuses: set[str],
) -> str:
    selected = [item for item in memories if item.status in statuses]
    lines = [markdown_heading(title, 2)]
    if not selected:
        lines.append("- none")
        return "\n".join(lines)
    for memory in sorted(selected, key=lambda item: item.memory_id):
        lines.extend(
            [
                markdown_heading(memory.title, 3),
                markdown_bullet("memory_id", memory.memory_id),
                markdown_bullet("memory_type", memory.memory_type),
                markdown_bullet("status", memory.status),
                markdown_bullet("confidence", memory.confidence),
                markdown_bullet("contradiction_status", memory.contradiction_status),
                markdown_bullet("scope", memory.scope),
                markdown_bullet("source_kind", memory.source_kind),
                markdown_bullet("valid_from", memory.valid_from),
                markdown_bullet("valid_until", memory.valid_until),
                markdown_bullet("content_hash", memory.content_hash),
                "",
                memory.content or memory.content_preview,
            ]
        )
    return "\n".join(lines).rstrip()


def _revision_summary(memories: list[MemoryEntry]) -> str:
    revision_count = sum(
        int(item.memory_attrs.get("revision_count") or 0) for item in memories
    )
    return "\n".join(
        [
            markdown_heading("Revision Summary", 2),
            markdown_bullet("known_revision_count", revision_count),
            "- Detailed revisions remain canonical OCEL records.",
        ]
    )


def _instruction_section(
    title: str,
    instructions: list[InstructionArtifact],
) -> str:
    lines = [markdown_heading(title, 2)]
    if not instructions:
        lines.append("- none")
        return "\n".join(lines)
    for instruction in sorted(instructions, key=lambda item: item.instruction_id):
        lines.extend(
            [
                markdown_heading(instruction.title, 3),
                markdown_bullet("instruction_id", instruction.instruction_id),
                markdown_bullet("instruction_type", instruction.instruction_type),
                markdown_bullet("status", instruction.status),
                markdown_bullet("scope", instruction.scope),
                markdown_bullet("priority", instruction.priority),
                markdown_bullet("body_hash", instruction.body_hash),
                markdown_bullet("source_path", instruction.source_path),
                "",
                instruction.body or instruction.body_preview,
            ]
        )
    return "\n".join(lines).rstrip()


def _rule_section(
    title: str,
    rules: list[ProjectRule],
    *,
    include_inactive: bool,
) -> str:
    selected = rules if include_inactive else [item for item in rules if item.status == "active"]
    lines = [markdown_heading(title, 2)]
    if not selected:
        lines.append("- none")
        return "\n".join(lines)
    for rule in sorted(selected, key=lambda item: item.rule_id):
        lines.extend(
            [
                markdown_heading(rule.rule_id, 3),
                markdown_bullet("rule_id", rule.rule_id),
                markdown_bullet("rule_type", rule.rule_type),
                markdown_bullet("status", rule.status),
                markdown_bullet("priority", rule.priority),
                markdown_bullet("source_instruction_id", rule.source_instruction_id),
                "",
                rule.text,
            ]
        )
    return "\n".join(lines).rstrip()


def _preference_section(
    title: str,
    preferences: list[UserPreference],
) -> str:
    lines = [markdown_heading(title, 2)]
    if not preferences:
        lines.append("- none")
        return "\n".join(lines)
    for preference in sorted(preferences, key=lambda item: item.preference_id):
        lines.extend(
            [
                markdown_heading(preference.preference_key, 3),
                markdown_bullet("preference_id", preference.preference_id),
                markdown_bullet("preference_key", preference.preference_key),
                markdown_bullet("preference_value", preference.preference_value),
                markdown_bullet("status", preference.status),
                markdown_bullet("confidence", preference.confidence),
                markdown_bullet("source_kind", preference.source_kind),
            ]
        )
    return "\n".join(lines).rstrip()


def _pig_summary_section(report: dict[str, Any]) -> str:
    if not report:
        return "\n".join(
            [
                markdown_heading("Summary Counts", 2),
                "- No PIG report snapshot was provided.",
            ]
        )
    attrs = report.get("report_attrs") or {}
    return "\n".join(
        [
            markdown_heading("Summary Counts", 2),
            markdown_bullet("report_id", report.get("report_id")),
            markdown_bullet("scope", report.get("scope")),
            markdown_bullet("event_count", len(report.get("activity_sequence") or [])),
            markdown_bullet("memory_instruction_summary", attrs.get("memory_instruction_summary")),
        ]
    )


def _pig_list_section(title: str, value: Any) -> str:
    lines = [markdown_heading(title, 2)]
    if not value:
        lines.append("- none")
    elif isinstance(value, dict):
        for key in sorted(value):
            lines.append(markdown_bullet(str(key), value[key]))
    elif isinstance(value, list):
        for item in value:
            lines.append(f"- {item}")
    else:
        lines.append(str(value))
    return "\n".join(lines)
