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
