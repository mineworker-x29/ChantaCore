# ChantaCore v0.15.2 Restore Notes

## Target

ChantaCore v0.15.2 adds explicit workspace read-only skills. Workspace read is now modeled as an explicit, root-constrained capability path, not as ambient filesystem access for the Default Agent.

## Canonical Boundary

Canonical persistence remains OCEL-based. Workspace read requests, results, violations, roots, and boundaries are recorded as OCEL objects/events. No canonical JSONL workspace read store is introduced.

The Default Agent must not claim arbitrary repository or filesystem access. Natural-language chat may describe that explicit read-only skills exist, but it must not imply that ambient chat can inspect files without an explicit skill path.

## Models

The workspace read package adds:

- `WorkspaceReadRoot`
- `WorkspaceReadBoundary`
- `WorkspaceFileListRequest`
- `WorkspaceFileListResult`
- `WorkspaceTextFileReadRequest`
- `WorkspaceTextFileReadResult`
- `WorkspaceMarkdownSummaryRequest`
- `WorkspaceMarkdownSummaryResult`
- `WorkspaceReadViolation`

These are read-side records for explicit operations under a configured workspace root.

## Service And Skills

`WorkspaceReadService` provides:

- read root registration
- read boundary registration
- bounded file listing
- bounded text file reading
- deterministic markdown summary generation
- violation recording

Built-in skills:

- `skill:list_workspace_files`
- `skill:read_workspace_text_file`
- `skill:summarize_workspace_markdown`

These skills require an explicit `root_path` and path input. They do not fall back to shell or network behavior.

## Safety Rules

Workspace read paths are constrained by:

- `pathlib.Path`
- `resolve(strict=False)`
- `relative_to` containment checks
- rejection of absolute target paths
- rejection of `..` traversal
- extension allowlist for text reads
- max byte and max character limits
- binary rejection

Markdown summaries are deterministic heading and preview summaries. They do not call an LLM.

## Explicit Non-goals

v0.15.2 does not add:

- ambient filesystem access
- arbitrary absolute path reads
- workspace writes
- delete, rename, chmod, mkdir, or rmdir behavior
- shell execution
- network calls
- MCP connections
- plugin loading
- permission auto-grants
- capability auto-routing from natural language to file read
- canonical JSONL workspace read persistence

## Capability Decision Surface

Workspace file read is no longer classified as simply impossible. It is classified as an explicit skill path. In the ambient chat path it remains non-executable until an explicit, root-constrained read-only skill invocation is used.

## PIG/OCPX Reporting

Lightweight reporting includes counts for workspace read roots, list/read/markdown requests and results, violations, denied reads, binary rejections, oversize rejections, outside-workspace violations, and traversal violations.

## Future Work

- capability-aware routing that can safely invoke explicit read skills
- reviewed workspace write skills after enforcement maturity
- richer deterministic and reviewed file summarization
- permission-aware workspace read policies
