# ChantaCore v0.8.4 — Edit Proposal, Not Direct Edit

## Purpose

v0.8.4 adds edit proposal generation only. It does not edit workspace files and does not apply patches.

This release is a prerequisite for v0.8.5 patch application with approval.

## Implemented Scope

- `src/chanta_core/editing`
- `EditProposal`
- `EditProposalStore`
- `EditProposalService`
- `create_unified_diff`
- `safe_preview`
- `tool:edit`
- `skill:propose_file_edit`

`tool:edit` is proposal-only. It has `safety_level="write"` because it belongs to the future edit path, but v0.8.4 proposal operations are classified as `internal_readonly`.

Supported operations:

- `propose_text_replacement`
- `propose_comment_only`
- `summarize_recent_proposals`

## No File Mutation

Workspace files are read through `WorkspaceInspector` and `WorkspacePathGuard`.

The implementation does not add:

- direct file write/edit
- patch application
- diff application
- rollback
- shell execution
- network/web fetch
- MCP/plugin system
- worker queue
- scheduler
- MissionLoop or GoalLoop
- async runtime

`EditProposalStore` writes append-only JSONL proposal records. It does not modify target workspace files.

## Proposal Contents

Edit proposals include:

- target path
- proposal type
- title
- rationale
- original text preview
- proposed text, if applicable
- unified diff, if applicable
- risk level
- status
- evidence refs

v0.8.4 only creates proposals with `status="proposed"`.

## Permission Behavior

Proposal-only edit operations are allowed by the permission skeleton because they do not mutate workspace files.

Future apply/write operations remain denied or approval-required. No approval token or interactive permission UI exists in v0.8.4.

## OCEL Trace

Edit proposal generation is traced through existing tool lifecycle events:

- `create_tool_request`
- `authorize_tool_request`
- `dispatch_tool`
- `execute_tool_operation`
- `complete_tool_operation`
- `observe_tool_result`

`ToolResult.output_attrs` includes proposal identifiers and proposal metadata for downstream reporting.

## Limitations

- no patch application
- no approval token
- no direct file edit
- no diff application
- no rollback
- no shell
- no worker queue
