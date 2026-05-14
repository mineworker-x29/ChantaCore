# ChantaCore v0.18.4 Restore Document

Version name: ChantaCore v0.18.4 - Workspace Read Summarization Pipeline

## Purpose

v0.18.4 adds deterministic Workspace Read Summarization for bounded, reviewable summaries of read-only workspace outputs.

The pipeline produces summary results and pending review summary candidates. It does not write memory, does not update persona, and does not update personal overlay.

## Scope

Implemented public concepts:

- Workspace Read Summary Policy
- Workspace Read Summary Request
- Workspace Read Summary Section
- Workspace Read Summary Result
- Workspace Read Summary Candidate
- Workspace Read Summary Finding
- Workspace Read Summarization Service
- Deterministic Summary Pipeline
- Reviewable Context Artifact
- CLI workspace-summary surface
- OCEL object/event/relation support
- ContextHistory adapter support
- PIG/OCPX lightweight report counts

## Deterministic Summaries

Supported input kinds:

- markdown heading and section outline
- plain text bounded preview
- JSON shallow key summary
- YAML shallow key summary with safe fallback
- TOML shallow key summary
- Python top-level import and symbol preview
- generic text preview

LLM summarization is disabled by default.

## Candidate Rules

Summary candidate creation:

- starts as `pending_review`;
- sets `canonical_promotion_enabled=false`;
- uses bounded summary preview and hash;
- does not create canonical memory, persona, overlay, or workspace records.

## CLI

```powershell
chanta-cli workspace-summary from-file --root <root> --path <relative_path>
chanta-cli workspace-summary from-envelope <envelope_id>
chanta-cli workspace-summary show <summary_result_id>
chanta-cli workspace-summary candidate <summary_result_id> --target workspace_summary_candidate
```

`from-file` uses the existing safe workspace read path handling. Traversal and outside-root reads are rejected by the workspace read layer.

## Future Work

- workbench;
- optional reviewed LLM summarization;
- controlled promotion if ever enabled.

## Restore-Grade Policy Addendum

### Implemented Files

Primary implementation:

- `src/chanta_core/workspace/summary.py`
- `src/chanta_core/workspace/summary_history_adapter.py`
- `src/chanta_core/workspace/__init__.py`
- `src/chanta_core/cli/main.py`
- `src/chanta_core/pig/reports.py`

Tests:

- `tests/test_workspace_read_summary_models.py`
- `tests/test_workspace_read_summary_service.py`
- `tests/test_workspace_read_summary_markdown.py`
- `tests/test_workspace_read_summary_structured.py`
- `tests/test_workspace_read_summary_python.py`
- `tests/test_workspace_read_summary_cli.py`
- `tests/test_workspace_read_summary_history_adapter.py`
- `tests/test_workspace_read_summary_ocel_shape.py`
- `tests/test_workspace_read_summary_boundaries.py`

### Public API / Model Surface

Models:

- `WorkspaceReadSummaryPolicy`
- `WorkspaceReadSummaryRequest`
- `WorkspaceReadSummarySection`
- `WorkspaceReadSummaryResult`
- `WorkspaceReadSummaryCandidate`
- `WorkspaceReadSummaryFinding`

Service:

- `WorkspaceReadSummarizationService`

Key service methods:

- `create_default_policy`
- `create_summary_request`
- `summarize_from_text`
- `summarize_from_execution_output`
- `summarize_from_envelope`
- `summarize_markdown`
- `summarize_plain_text`
- `summarize_json`
- `summarize_yaml`
- `summarize_toml`
- `summarize_python`
- `create_summary_candidate`
- `render_summary_cli`

### Persistence and Canonical State

Workspace read summaries are deterministic review artifacts. They are not
canonical memory, persona, overlay, or workspace source records.

Required default result attrs:

```text
uses_llm=False
memory_entries_written=False
persona_updated=False
overlay_updated=False
full_body_stored=False
```

Summary candidates start as `pending_review` and keep
`canonical_promotion_enabled=False`.

### OCEL Shape

Object types:

- `workspace_read_summary_policy`
- `workspace_read_summary_request`
- `workspace_read_summary_section`
- `workspace_read_summary_result`
- `workspace_read_summary_candidate`
- `workspace_read_summary_finding`

Events:

- `workspace_read_summary_policy_registered`
- `workspace_read_summary_requested`
- `workspace_read_summary_section_created`
- `workspace_read_summary_completed`
- `workspace_read_summary_skipped`
- `workspace_read_summary_failed`
- `workspace_read_summary_candidate_created`
- `workspace_read_summary_finding_recorded`

Expected relations:

- section belongs to request;
- result summarizes request;
- result includes sections;
- candidate derives from summary result;
- candidate may reference an execution result promotion candidate when supplied.

### CLI Surface

```powershell
chanta-cli workspace-summary from-file --root <root> --path <relative_path>
chanta-cli workspace-summary from-envelope <envelope_id>
chanta-cli workspace-summary show <summary_result_id>
chanta-cli workspace-summary candidate <summary_result_id> --target workspace_summary_candidate
```

`from-file` must preserve existing workspace read path boundaries. Traversal and
outside-root reads are denied by the workspace read layer.

### Restore Procedure

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m pytest tests\test_workspace_read_summary_models.py tests\test_workspace_read_summary_service.py tests\test_workspace_read_summary_markdown.py tests\test_workspace_read_summary_structured.py tests\test_workspace_read_summary_python.py tests\test_workspace_read_summary_cli.py tests\test_workspace_read_summary_history_adapter.py tests\test_workspace_read_summary_ocel_shape.py tests\test_workspace_read_summary_boundaries.py
.\.venv\Scripts\python.exe -m pytest
```

### Restore Checklist

- [ ] Markdown headings produce deterministic sections.
- [ ] JSON/YAML/TOML summaries stay shallow and bounded.
- [ ] Python summaries inspect top-level imports/symbols only.
- [ ] LLM summarization is disabled by default.
- [ ] Summary candidates are pending review and non-canonical.
- [ ] Traversal and outside-root reads are denied.
- [ ] OCEL summary objects/events/relations are recorded.
- [ ] ContextHistory adapter entries are generated.
- [ ] Boundary tests confirm no memory/persona/overlay/workspace mutation.
