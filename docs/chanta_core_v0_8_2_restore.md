# ChantaCore v0.8.2 — Repo Search / Symbol Scan

## Purpose

v0.8.2 adds read-only repository search and lightweight symbol scanning as part of the Internal Harness Layer.

Repository operations are exposed through:

```text
ToolDispatcher
-> tool:repo
-> OCEL tool lifecycle trace
-> OCPX/PIG visibility
```

## Implemented Scope

- `src/chanta_core/repo`
- `RepoScanner`
- `RepoSearchService`
- `RepoSymbolScanner`
- repo result models
- `tool:repo`

`tool:repo` is an `internal_readonly` tool gateway.

Supported operations:

- `find_files`
- `search_text`
- `scan_symbols`
- `find_definitions_light`
- `scan_tree`

## Read-Only Contract

All v0.8.2 repo operations are read-only. The implementation does not add:

- write/edit/patch functionality
- shell execution
- network/web fetch
- MCP/plugin system
- worker queue
- scheduler
- MissionLoop or GoalLoop
- async runtime

## Workspace Guard Reuse

Repo operations use `WorkspaceInspector`, `WorkspaceConfig`, and `WorkspacePathGuard`.

They do not bypass the workspace guard. Blocked files and directories, such as `.env`, `.venv`, `data`, `.git`, SQLite files, key files, and PEM files, are excluded or denied by the same v0.8.1 policy.

## Search and Symbol Strategy

Repository search uses Python standard library behavior only:

- `fnmatch` for file pattern matching
- substring text search for `search_text`
- `re` line heuristics for symbol candidates

No `rg`/ripgrep dependency is used.

No parser dependency is introduced:

- no tree-sitter
- no Jedi
- no LSP
- no semantic symbol graph

Symbol scanning is explicitly a lightweight candidate scan, not semantic parsing.

Recognized candidates include:

- Python `class`, `def`, and `async def`
- JavaScript/TypeScript `function`, `class`, `const`, and `let`
- Markdown headings as sections

## OCEL Trace

Repo operations use existing tool lifecycle events:

- `create_tool_request`
- `authorize_tool_request`
- `dispatch_tool`
- `execute_tool_operation`
- `complete_tool_operation` or `fail_tool_operation`
- `observe_tool_result`

Structured result details are returned in `ToolResult.output_attrs`.

## Limitations

- no semantic parser
- no LSP
- no deep symbol graph
- no edit proposal
- no patch application
- no shell
- no network
- no worker queue
