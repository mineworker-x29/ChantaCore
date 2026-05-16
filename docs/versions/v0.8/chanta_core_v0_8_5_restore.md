# ChantaCore v0.8.5 — Patch Application with Approval

## Purpose

v0.8.5 adds approved patch application to the Internal Harness Layer. It builds on v0.8.4 edit proposals and introduces the first controlled workspace mutation path.

This is not silent editing automation. A patch can be applied only from an existing `EditProposal`, only with a valid `PatchApproval`, and only when `ToolPolicy(allow_approved_writes=True)` is explicitly configured.

## Scope

Implemented in this phase:

| Area | Status |
| --- | --- |
| `PatchApproval` | Explicit approval object with required phrase |
| `PatchApplication` | Records application attempt/result |
| `PatchApplicationStore` | Append-only JSONL application log |
| `PatchBackupService` | Writes backups under `data/editing/backups` |
| `PatchApplicationService` | Validates, backs up, and applies approved replace-file proposals |
| `tool:edit` | Adds dry-run, apply-approved, and summary operations |

The required approval phrase is:

```text
I APPROVE PATCH APPLICATION
```

## Safety Rules

- No proposal means no patch.
- No valid approval means no patch.
- Approval for a different proposal is rejected.
- Blocked paths still go through `WorkspacePathGuard`.
- `.env`, `.venv`, `data`, sqlite/db/key/pem paths remain blocked.
- Backups are created before target file mutation.
- Default `ToolPolicy` does not execute writes.
- Actual tool-based application requires `allow_approved_writes=True`.

## Tool Behavior

`tool:edit` supports:

- `propose_text_replacement`
- `propose_comment_only`
- `summarize_recent_proposals`
- `dry_run_approved_proposal`
- `apply_approved_proposal`
- `summarize_recent_patch_applications`

Proposal and dry-run operations do not mutate workspace files. `apply_approved_proposal` may mutate exactly the proposal target path only after approval validation and explicit policy allowance.

## OCEL Trace

Patch application runs through the existing tool gateway lifecycle:

- `create_tool_request`
- `authorize_tool_request`
- `dispatch_tool`
- `execute_tool_operation`
- `complete_tool_operation` or `fail_tool_operation`
- `observe_tool_result`

Authorization decisions include permission state, approval requirements, risk level, and policy mode.

## Guardrails

v0.8.5 does not add:

- shell execution
- subprocess patch commands
- network/web fetch
- MCP/plugin system
- worker queue
- scheduler
- MissionLoop or GoalLoop
- interactive permission UI
- automatic policy promotion

Patch application uses Python file I/O only after explicit approval checks. It is still limited to single-file `replace_file` proposals.

## Remaining Limitations

- no interactive approval UI
- no approval token exchange
- no rollback execution command yet
- no patch conflict handling
- no multi-file patch application
- no shell/network tools
- no worker queue
