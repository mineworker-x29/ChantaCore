# ChantaCore v0.10.2 Restore

## Version

ChantaCore v0.10.2 - Memory Materialized Views.

## Purpose

v0.10.2 adds deterministic Markdown materialized views generated from
OCEL-native memory, instruction, project rule, user preference, PIG, and context
rule objects.

Markdown is human-readable output only. The canonical source remains OCEL
event/object/relation records. Edits to generated Markdown files do not update
OCEL and must not be treated as canonical memory or project policy.

## Added Package

The release adds `src/chanta_core/materialized_views/`:

- `__init__.py`
- `ids.py`
- `errors.py`
- `models.py`
- `paths.py`
- `markdown.py`
- `renderers.py`
- `service.py`

## Models

`MaterializedView` records a generated view:

- `view_id`
- `view_type`
- `title`
- `target_path`
- `content`
- `content_hash`
- `generated_at`
- `source_kind`
- `canonical`
- `view_attrs`

`canonical` must be `False` for generated v0.10.2 views.

`MaterializedViewInputSnapshot` carries the in-memory input set:

- memories
- instruction artifacts
- project rules
- user preferences
- optional PIG report dict
- snapshot attrs

It does not load from OCEL automatically.

`MaterializedViewRenderResult` records whether a view was written or skipped.

The input snapshot is explicit on purpose. v0.10.2 does not define a canonical
OCEL query planner for "all relevant memory." Callers assemble the object set
they want rendered, then pass that snapshot to the renderer/service. This keeps
materialized views as deterministic projections rather than hidden retrieval
behavior.

## Default Paths

`paths.py` defines the default `.chanta` projection filenames:

- `memory` -> `.chanta/MEMORY.md`
- `project` -> `.chanta/PROJECT.md`
- `user` -> `.chanta/USER.md`
- `pig_guidance` -> `.chanta/PIG_GUIDANCE.md`
- `context_rules` -> `.chanta/CONTEXT_RULES.md`

`paths.py` does not write files.

Generated files may live at these paths, but the paths themselves do not make
the files canonical. A repository can delete and regenerate them from OCEL-native
objects without losing canonical memory, instruction, preference, session, or
process facts.

## Markdown Warning

Every generated view includes an explicit warning:

- Generated materialized view.
- Canonical source: OCEL.
- This file is not canonical memory.
- Do not treat edits to this file as canonical updates.

This warning is part of the boundary contract.

The warning is not decorative. It is the primary user-facing guardrail that
prevents `.chanta/*.md` from being mistaken for a direct memory editing surface.
Future staged assimilation may read edits, but it must be explicit and must
record new OCEL facts rather than overwrite canonical state silently.

## Renderers

`render_memory_view(...)` writes the logical content for `MEMORY.md`. It groups
memories into:

- active memories
- draft memories
- superseded / archived / withdrawn memories
- revision summary

Each memory includes identifiers, type, status, confidence, contradiction
status, scope, source kind, validity range, content hash, and content or
preview. It renders only provided `MemoryEntry` objects.

`render_project_view(...)` writes `PROJECT.md` from provided
`InstructionArtifact` and `ProjectRule` objects. It includes instruction IDs,
types, statuses, scopes, priorities, body hashes, source paths, rule IDs, rule
types, and source instruction IDs.

`render_user_view(...)` writes `USER.md` from provided `UserPreference`
objects. It groups active and inactive preferences and includes preference key,
value, status, confidence, and source kind.

`render_pig_guidance_view(...)` writes `PIG_GUIDANCE.md`. If no PIG report is
provided, it renders a stable empty state. If a report is provided, it renders
summary counts, guidance, diagnostics, and conformance notes.

`render_context_rules_view(...)` writes `CONTEXT_RULES.md` as a readable
projection for future context assembly. It explicitly states that the file is
not a prompt that must be injected wholesale. It includes active rules,
preferences, instructions, and excluded/deprecated counts.

Renderer determinism expectations:

- input ordering should be stable or explicitly sorted by renderer logic;
- the same input object set should produce the same sections and item ordering;
- `generated_at` is allowed to change between renders;
- content hashes must change only when rendered content changes;
- renderers must not infer new memories, preferences, project rules, or
  guidance facts.

## Service

`MaterializedViewService` provides:

- `render_default_views(snapshot, root=...)`
- `write_view(view, overwrite=True)`
- `refresh_default_views(snapshot, root=..., overwrite=True)`
- `record_view_rendered(view)`

`render_default_views` returns views without writing files. `write_view` writes
one view and respects `overwrite=False`. `refresh_default_views` renders and
writes all five default views.

`render_default_views(...)` is safe for dry runs because it has no filesystem
side effects. `write_view(...)` is the point where files are created. When
`overwrite=False`, existing files are left untouched and the result reports a
skip reason. `refresh_default_views(...)` combines render and write for all five
default views.

## Optional OCEL Events

When a `TraceService` is supplied, the service records best-effort OCEL events:

- `materialized_view_rendered`
- `materialized_view_written`
- `materialized_view_skipped`
- `materialized_view_refresh_started`
- `materialized_view_refresh_completed`

It uses OCEL object type:

- `materialized_view`

Object attrs include view type, title, target path, content hash, generated
timestamp, source kind, and `canonical=False`.

OCEL materialized view events are audit events for view generation/writing. They
do not make Markdown canonical, and they do not change memory or instruction
objects. If TraceService is unavailable, rendering and writing still work without
OCEL event recording.

## Boundary Rules

v0.10.2 does not implement:

- Markdown-to-OCEL overwrite
- direct Markdown import into canonical memory
- staged assimilation
- automatic OCEL retrieval
- semantic retrieval
- embeddings or vector DB
- memory consolidation
- hooks, permission grants, resume/fork, MCP, plugins, or UI
- canonical JSONL memory/instruction stores

Forbidden reverse functions are intentionally absent:

- `import_memory_from_markdown`
- `load_memory_from_markdown_as_canonical`
- `sync_markdown_to_memory`
- `overwrite_ocel_from_markdown`

Absence of these functions is part of the release contract. If future code adds
Markdown ingestion, it must be named and documented as staged assimilation and
must produce new OCEL events rather than treating Markdown as source of truth.

## Restore Checklist

Use this checklist when rebuilding or auditing the release:

- `src/chanta_core/materialized_views/` contains IDs, errors, models, paths,
  Markdown helpers, renderers, and service.
- `MaterializedView.canonical` is always `False` for generated views.
- `hash_content(...)` is deterministic.
- Default paths map exactly to `.chanta/MEMORY.md`, `.chanta/PROJECT.md`,
  `.chanta/USER.md`, `.chanta/PIG_GUIDANCE.md`, and
  `.chanta/CONTEXT_RULES.md`.
- `paths.py` computes paths only and does not write files.
- All five renderers include the generated/non-canonical warning.
- `MEMORY.md` renders only provided `MemoryEntry` objects.
- `PROJECT.md` renders only provided `InstructionArtifact` and `ProjectRule`
  objects.
- `USER.md` renders only provided `UserPreference` objects.
- `PIG_GUIDANCE.md` has a stable empty state when no PIG report is supplied.
- `CONTEXT_RULES.md` states that it is not a wholesale prompt injection file.
- `MaterializedViewService.render_default_views(...)` does not write files.
- `write_view(...)` creates parent directories and respects `overwrite=False`.
- `refresh_default_views(...)` writes all five default views.
- Optional OCEL events use `materialized_view` object attrs with
  `canonical=False`.
- Markdown-to-OCEL overwrite/import functions are absent.
- No canonical JSONL memory or instruction store is introduced.

## Restore / Verification Commands

Representative tests:

```powershell
.\.venv\Scripts\python.exe -m pytest `
  tests\test_materialized_view_models.py `
  tests\test_materialized_view_renderers.py `
  tests\test_materialized_view_service.py `
  tests\test_materialized_view_ocel_shape.py `
  tests\test_materialized_view_boundaries.py
```

Full related regression set:

```powershell
.\.venv\Scripts\python.exe -m pytest `
  tests\test_imports.py `
  tests\test_materialized_view_models.py `
  tests\test_materialized_view_renderers.py `
  tests\test_materialized_view_service.py `
  tests\test_materialized_view_ocel_shape.py `
  tests\test_materialized_view_boundaries.py `
  tests\test_memory_models.py `
  tests\test_instruction_models.py `
  tests\test_memory_service.py `
  tests\test_instruction_service.py `
  tests\test_session_models.py `
  tests\test_session_service.py `
  tests\test_process_run_loop.py `
  tests\test_ocel_store.py `
  tests\test_pig_reports.py
```

Smoke script:

```powershell
.\.venv\Scripts\python.exe scripts\test_materialized_views.py
```

The script writes generated views into a temporary directory, not the repository
root.

## Operational Notes

Use materialized views for human inspection only. To change canonical memory or
instructions, use OCEL-native services such as `MemoryService` and
`InstructionService`. A future staged Markdown assimilation workflow may parse
Markdown edits, but it must be explicit and must not overwrite OCEL directly.

## Remaining Limitations

- No automatic OCEL retrieval into snapshots.
- No staged Markdown assimilation yet.
- No semantic retrieval.
- No embeddings or vector DB.
- No hook lifecycle.
- No permission/grant model.
- No session resume/fork.
