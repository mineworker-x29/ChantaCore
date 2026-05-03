# ChantaCore v0.8.1 — Workspace/File Read-Only Inspection

## Purpose

v0.8.1 is the first concrete Internal Harness Layer implementation. It adds read-only workspace and file inspection while preserving the ChantaCore process-intelligence spine.

Workspace operations are internal harness capabilities, not external plugins. They should be invoked through:

```text
ToolDispatcher
-> tool:workspace
-> OCEL tool lifecycle trace
-> OCPX/PIG visibility
```

## Implemented Scope

- `src/chanta_core/workspace`
- `WorkspaceConfig`
- `WorkspacePathGuard`
- `WorkspaceInspector`
- workspace errors
- `tool:workspace`

`tool:workspace` is an `internal_readonly` tool gateway.

Supported operations:

- `get_workspace_root`
- `path_exists`
- `list_files`
- `read_text_file`
- `summarize_tree`

## Read-Only Contract

All v0.8.1 workspace operations are read-only.

This version does not add:

- write/edit/patch functionality
- shell execution
- network/web fetch
- MCP/plugin system
- worker queue
- scheduler
- MissionLoop or GoalLoop
- external connector layer
- async runtime

## Path Guard

`WorkspacePathGuard` prevents:

- path traversal outside `workspace_root`
- absolute paths outside `workspace_root`
- symlink escapes outside `workspace_root`
- blocked names such as `.env`, `.venv`, `data`, `.git`, `node_modules`, and cache directories
- blocked suffixes such as `.sqlite`, `.sqlite3`, `.db`, `.pem`, `.key`, `.p12`, and `.pfx`

`WorkspaceInspector.read_text_file` also checks:

- maximum file size
- binary files using a null-byte heuristic
- optional extension allowlists if configured

## OCEL Trace

Workspace operations use the existing tool lifecycle events:

- `create_tool_request`
- `authorize_tool_request`
- `dispatch_tool`
- `execute_tool_operation`
- `complete_tool_operation` or `fail_tool_operation`
- `observe_tool_result`

When available, workspace and file context is represented as OCEL objects:

- `workspace`
- `file`

Relations include:

- `tool_request --targets_file--> file`
- `file --belongs_to_workspace--> workspace`

The implementation avoids exposing raw absolute paths in normal tool outputs. Relative paths are preferred.

## Limitations

- no repo search/symbol scan yet
- no edit proposal
- no patch application
- no shell
- no network
- no worker queue
- no scheduler
- no full sandbox or interactive permission UI
