from __future__ import annotations

from chanta_core.materialized_views.ids import new_materialized_view_id
from chanta_core.materialized_views.markdown import (
    markdown_bullet,
    markdown_heading,
    render_view_metadata_block,
)
from chanta_core.materialized_views.models import MaterializedView, hash_content
from chanta_core.tool_registry.models import (
    ToolDescriptor,
    ToolPolicyNote,
    ToolRegistrySnapshot,
    ToolRiskAnnotation,
)
from chanta_core.utility.time import utc_now_iso


def render_tools_view(
    *,
    tools: list[ToolDescriptor],
    snapshot: ToolRegistrySnapshot | None,
    target_path: str,
) -> MaterializedView:
    generated_at = utc_now_iso()
    view_id = new_materialized_view_id()
    body_without_metadata = "\n\n".join(
        [
            markdown_heading("Tool Registry View", 1),
            _tools_generated_warning(),
            _tool_summary(tools),
            _tool_section("Active Tools", [tool for tool in _sort_tools(tools) if tool.status == "active"]),
            _tool_section(
                "Disabled / Deprecated Tools",
                [tool for tool in _sort_tools(tools) if tool.status != "active"],
            ),
        ]
    )
    content_hash = hash_content(body_without_metadata)
    metadata = render_view_metadata_block(
        view_id=view_id,
        view_type="tool_registry",
        target_path=target_path,
        generated_at=generated_at,
        content_hash=content_hash,
        source_kind="ocel_tool_registry_projection",
        canonical=False,
    )
    snapshot_block = _snapshot_block(snapshot)
    content = "\n\n".join(
        [
            markdown_heading("Tool Registry View", 1),
            _tools_generated_warning(),
            metadata,
            snapshot_block,
            _tool_summary(tools),
            _tool_section("Active Tools", [tool for tool in _sort_tools(tools) if tool.status == "active"]),
            _tool_section(
                "Disabled / Deprecated Tools",
                [tool for tool in _sort_tools(tools) if tool.status != "active"],
            ),
        ]
    )
    return MaterializedView(
        view_id=view_id,
        view_type="tool_registry",
        title="Tool Registry View",
        target_path=target_path,
        content=content,
        content_hash=hash_content(content),
        generated_at=generated_at,
        source_kind="ocel_tool_registry_projection",
        canonical=False,
        view_attrs={"snapshot_id": snapshot.snapshot_id if snapshot else None},
    )


def render_tool_policy_view(
    *,
    tools: list[ToolDescriptor],
    policy_notes: list[ToolPolicyNote],
    risk_annotations: list[ToolRiskAnnotation],
    target_path: str,
) -> MaterializedView:
    generated_at = utc_now_iso()
    view_id = new_materialized_view_id()
    body_without_metadata = "\n\n".join(
        [
            markdown_heading("Tool Policy View", 1),
            _policy_generated_warning(),
            _important_boundary(),
            _risk_annotation_section(risk_annotations),
            _policy_note_section(policy_notes),
            _future_permission_boundary(),
        ]
    )
    content_hash = hash_content(body_without_metadata)
    metadata = render_view_metadata_block(
        view_id=view_id,
        view_type="tool_policy",
        target_path=target_path,
        generated_at=generated_at,
        content_hash=content_hash,
        source_kind="ocel_tool_policy_projection",
        canonical=False,
    )
    content = "\n\n".join(
        [
            markdown_heading("Tool Policy View", 1),
            _policy_generated_warning(),
            metadata,
            _important_boundary(),
            _tool_reference_section(tools),
            _risk_annotation_section(risk_annotations),
            _policy_note_section(policy_notes),
            _future_permission_boundary(),
        ]
    )
    return MaterializedView(
        view_id=view_id,
        view_type="tool_policy",
        title="Tool Policy View",
        target_path=target_path,
        content=content,
        content_hash=hash_content(content),
        generated_at=generated_at,
        source_kind="ocel_tool_policy_projection",
        canonical=False,
        view_attrs={"policy_note_count": len(policy_notes), "risk_annotation_count": len(risk_annotations)},
    )


def _tools_generated_warning() -> str:
    return "\n".join(
        [
            "> Generated materialized view.",
            "> Canonical source: OCEL.",
            "> This file is not the canonical tool registry.",
            "> Edits to this file do not change runtime tool availability.",
        ]
    )


def _policy_generated_warning() -> str:
    return "\n".join(
        [
            "> Generated materialized view.",
            "> Canonical source: OCEL.",
            "> This file is not PermissionPolicy.",
            "> It does not grant, deny, allow, ask, block, or sandbox tool usage.",
            "> Actual permission scope/grant enforcement belongs to v0.12.x.",
        ]
    )


def _important_boundary() -> str:
    return "\n".join(
        [
            markdown_heading("Important Boundary", 2),
            "- Informational view only.",
            "- Not a runtime registry.",
            "- Not a permission policy.",
            "- Markdown edits do not change runtime tool availability.",
        ]
    )


def _future_permission_boundary() -> str:
    return "\n".join(
        [
            markdown_heading("Future Permission Boundary", 2),
            "- Permission scope/grant/enforcement is future v0.12.x work.",
            "- This view can inform future review, but it does not enforce decisions.",
        ]
    )


def _snapshot_block(snapshot: ToolRegistrySnapshot | None) -> str:
    if snapshot is None:
        return "\n".join([markdown_heading("Snapshot", 2), "- none"])
    return "\n".join(
        [
            markdown_heading("Snapshot", 2),
            markdown_bullet("snapshot_id", snapshot.snapshot_id),
            markdown_bullet("snapshot_name", snapshot.snapshot_name),
            markdown_bullet("created_at", snapshot.created_at),
            markdown_bullet("source_kind", snapshot.source_kind),
            markdown_bullet("snapshot_hash", snapshot.snapshot_hash),
            markdown_bullet("tool_count", len(snapshot.tool_ids)),
        ]
    )


def _tool_summary(tools: list[ToolDescriptor]) -> str:
    by_type: dict[str, int] = {}
    by_risk: dict[str, int] = {}
    for tool in tools:
        by_type[tool.tool_type] = by_type.get(tool.tool_type, 0) + 1
        risk = tool.risk_level or "unknown"
        by_risk[risk] = by_risk.get(risk, 0) + 1
    return "\n".join(
        [
            markdown_heading("Tool Summary", 2),
            markdown_bullet("tool_count", len(tools)),
            markdown_bullet("tool_type_distribution", _inline_counts(by_type)),
            markdown_bullet("risk_level_distribution", _inline_counts(by_risk)),
        ]
    )


def _tool_section(title: str, tools: list[ToolDescriptor]) -> str:
    if not tools:
        return "\n".join([markdown_heading(title, 2), "- none"])
    lines = [markdown_heading(title, 2)]
    for tool in tools:
        lines.extend(
            [
                markdown_heading(f"{tool.tool_name} ({tool.tool_id})", 3),
                markdown_bullet("tool_type", tool.tool_type),
                markdown_bullet("status", tool.status),
                markdown_bullet("risk_level", tool.risk_level),
                markdown_bullet("source_kind", tool.source_kind),
                markdown_bullet("capability_tags", ", ".join(tool.capability_tags) or "none"),
                markdown_bullet("execution_owner", tool.execution_owner),
                markdown_bullet("input_schema_ref", tool.input_schema_ref),
                markdown_bullet("output_schema_ref", tool.output_schema_ref),
                markdown_bullet("description", tool.description),
            ]
        )
    return "\n".join(lines)


def _tool_reference_section(tools: list[ToolDescriptor]) -> str:
    if not tools:
        return "\n".join([markdown_heading("Tool References", 2), "- none"])
    lines = [markdown_heading("Tool References", 2)]
    for tool in _sort_tools(tools):
        lines.append(f"- `{tool.tool_name}` / `{tool.tool_id}` / risk `{tool.risk_level or 'unknown'}`")
    return "\n".join(lines)


def _risk_annotation_section(annotations: list[ToolRiskAnnotation]) -> str:
    if not annotations:
        return "\n".join([markdown_heading("Risk Annotations", 2), "- none"])
    lines = [markdown_heading("Risk Annotations", 2)]
    for annotation in sorted(annotations, key=lambda item: (item.tool_id, item.risk_category, item.risk_annotation_id)):
        lines.extend(
            [
                markdown_heading(annotation.risk_annotation_id, 3),
                markdown_bullet("tool_id", annotation.tool_id),
                markdown_bullet("risk_level", annotation.risk_level),
                markdown_bullet("risk_category", annotation.risk_category),
                markdown_bullet("status", annotation.status),
                markdown_bullet("rationale", annotation.rationale),
            ]
        )
    return "\n".join(lines)


def _policy_note_section(notes: list[ToolPolicyNote]) -> str:
    if not notes:
        return "\n".join([markdown_heading("Policy Notes", 2), "- none"])
    lines = [markdown_heading("Policy Notes", 2)]
    for note in sorted(notes, key=lambda item: (1 if item.priority is None else 0, -(item.priority or 0), item.tool_name or "", item.policy_note_id)):
        lines.extend(
            [
                markdown_heading(note.policy_note_id, 3),
                markdown_bullet("tool_id", note.tool_id),
                markdown_bullet("tool_name", note.tool_name),
                markdown_bullet("note_type", note.note_type),
                markdown_bullet("status", note.status),
                markdown_bullet("priority", note.priority),
                markdown_bullet("source_kind", note.source_kind),
                markdown_bullet("text", note.text),
            ]
        )
    return "\n".join(lines)


def _sort_tools(tools: list[ToolDescriptor]) -> list[ToolDescriptor]:
    return sorted(tools, key=lambda tool: (tool.tool_name, tool.tool_id))


def _inline_counts(counts: dict[str, int]) -> str:
    if not counts:
        return "none"
    return ", ".join(f"{key}={counts[key]}" for key in sorted(counts))
