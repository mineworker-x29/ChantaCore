# ChantaCore v0.10.5 Restore

## Version

ChantaCore v0.10.5 - File-based Tool Registry & Policy View.

## Purpose

v0.10.5 adds OCEL-native tool registry view objects and generated Markdown
views for human inspection:

- `.chanta/TOOLS.md`
- `.chanta/TOOL_POLICY.md`

These files are materialized views only. They are not the runtime tool registry,
not `PermissionPolicy`, and not canonical persistence. Markdown edits do not
change runtime tool availability.

## Added Package

The release adds `src/chanta_core/tool_registry/`:

- `__init__.py`
- `ids.py`
- `errors.py`
- `models.py`
- `paths.py`
- `renderers.py`
- `service.py`

## Models

`ToolDescriptor` records informational tool metadata:

- tool ID/name/type
- description
- status
- capability tags
- schema refs
- execution owner
- source kind
- risk level
- timestamps
- attrs

`ToolRegistrySnapshot` records a deterministic snapshot of tool descriptor IDs
and snapshot hash.

`ToolPolicyNote` records informational notes. It rejects enforcement-like note
types:

- `allow`
- `deny`
- `ask`
- `grant`
- `revoke`
- `block`
- `sandbox`

`ToolRiskAnnotation` records risk level/category/rationale metadata for a tool.

## Paths

`paths.py` computes default view paths only:

- `tools` -> `.chanta/TOOLS.md`
- `tool_policy` -> `.chanta/TOOL_POLICY.md`

It does not write files.

## Markdown Views

`render_tools_view(...)` returns a non-canonical `MaterializedView` for
`.chanta/TOOLS.md`.

The generated warning states:

- Generated materialized view.
- Canonical source: OCEL.
- This file is not the canonical tool registry.
- Edits to this file do not change runtime tool availability.

The view includes tool summary, active tools, disabled/deprecated tools, IDs,
names, types, statuses, risk levels, capability tags, schema refs, owners, and
descriptions.

`render_tool_policy_view(...)` returns a non-canonical `MaterializedView` for
`.chanta/TOOL_POLICY.md`.

The generated warning states:

- This file is not PermissionPolicy.
- It does not grant, deny, allow, ask, block, or sandbox tool usage.
- Actual permission scope/grant enforcement belongs to v0.12.x.

The policy view includes risk annotations, policy notes, and a future permission
boundary section.

## ToolRegistryViewService

`ToolRegistryViewService` provides:

- `register_tool_descriptor(...)`
- `update_tool_descriptor(...)`
- `deprecate_tool_descriptor(...)`
- `create_registry_snapshot(...)`
- `register_tool_policy_note(...)`
- `update_tool_policy_note(...)`
- `register_tool_risk_annotation(...)`
- `update_tool_risk_annotation(...)`
- `render_tools_view(...)`
- `render_tool_policy_view(...)`
- `write_tool_views(...)`

The service records OCEL facts through `TraceService`. It does not mutate
runtime `ToolDispatcher`, does not register runtime tools, does not create
permission grants, does not enforce policy, and does not execute tools.

## OCEL Object Types

The release actively uses:

- `tool_descriptor`
- `tool_registry_snapshot`
- `tool_policy_note`
- `tool_risk_annotation`

Generated Markdown views reuse the existing `materialized_view` object type with
`canonical=False`.

## OCEL Event Activities

Tool registry/policy events:

- `tool_descriptor_registered`
- `tool_descriptor_updated`
- `tool_descriptor_deprecated`
- `tool_registry_snapshot_created`
- `tool_policy_note_registered`
- `tool_policy_note_updated`
- `tool_risk_annotation_registered`
- `tool_risk_annotation_updated`
- `tool_registry_view_rendered`
- `tool_registry_view_written`
- `tool_policy_view_rendered`
- `tool_policy_view_written`

Events include `informational_only=True`, `enforcement_enabled=False`, and
`runtime_registry_mutated=False`.

## Relation Intent

Object-object relation qualifiers:

- `includes_tool`
- `describes_tool`
- `annotates_tool`

Event-object relation qualifiers:

- `tool_object`
- `snapshot_object`
- `policy_note_object`
- `risk_annotation_object`
- `view_object`

If relation helper APIs change, the restoration standard is that tool snapshot,
note, annotation, and view lineage remain reconstructible from OCEL records.

## PIG/OCPX Support

`PIGReportService` includes `tool_registry_summary`:

- tool descriptor count
- registry snapshot count
- policy note count
- risk annotation count
- tool type distribution
- risk level distribution
- view written counts

This is reporting only. It is not conformance failure or permission
enforcement.

## Boundaries

v0.10.5 does not:

- implement permission enforcement;
- implement allow/deny/ask;
- create permission grants;
- implement sandbox;
- block tool calls;
- mutate tool inputs or outputs;
- mutate runtime `ToolDispatcher`;
- dynamically load external plugins;
- load MCP tools;
- execute tools from the registry view;
- use Markdown as runtime registry;
- create canonical JSONL tool registry persistence;
- add async or UI.

## Restore Checklist

- `src/chanta_core/tool_registry/` exists with models, paths, renderers, and
  service.
- `ToolDescriptor`, `ToolRegistrySnapshot`, `ToolPolicyNote`, and
  `ToolRiskAnnotation` expose `to_dict()`.
- Forbidden `ToolPolicyNote.note_type` values are rejected.
- `.chanta/TOOLS.md` and `.chanta/TOOL_POLICY.md` views are supported.
- Markdown warnings explicitly state non-canonical status.
- `TOOL_POLICY.md` states it is not `PermissionPolicy`.
- OCEL objects/events are emitted for descriptors, snapshots, notes,
  annotations, and view writes.
- Runtime `ToolDispatcher` is not mutated.
- PIG report exposes tool registry/policy counts.
- No Markdown-to-runtime registry import exists.

## Restore / Verification Commands

Representative tests:

```powershell
.\.venv\Scripts\python.exe -m pytest `
  tests\test_tool_registry_models.py `
  tests\test_tool_registry_service.py `
  tests\test_tool_registry_renderers.py `
  tests\test_tool_registry_view_files.py `
  tests\test_tool_registry_ocel_shape.py `
  tests\test_tool_registry_boundaries.py `
  tests\test_pig_reports.py
```

Smoke script:

```powershell
.\.venv\Scripts\python.exe scripts\test_tool_registry_views.py
```

The smoke script writes views into a temporary directory, not the repository
root.

## Remaining Limitations

- No permission/grant model yet.
- No runtime enforcement.
- No sandbox.
- No MCP/plugin tools.
- No Markdown-to-runtime registry import.
- No UI.
