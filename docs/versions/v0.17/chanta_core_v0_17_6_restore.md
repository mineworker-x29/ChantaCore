# ChantaCore v0.17.6 Restore Document

Version name: ChantaCore v0.17.6 - Read-only Execution Safety Hardening & CLI Input UX

## Purpose

v0.17.6 hardens the read-only execution gate for explicit workspace read skills and improves CLI input handling for shells where inline JSON quoting is fragile.

This release does not add new execution capabilities. It does not add write, shell, network, MCP, plugin, natural-language execution, permission grant creation, LLM classification, or a line-delimited execution store.

## Implemented Files

- `src/chanta_core/skills/execution_gate.py`
- `src/chanta_core/workspace/read_service.py`
- `src/chanta_core/cli/main.py`
- `tests/test_skill_execution_gate_workspace_read.py`
- `tests/test_workspace_read_path_helpers.py`
- `tests/test_explicit_skill_invocation_workspace_read.py`
- `tests/test_skill_execution_gate_cli.py`
- `tests/test_skill_execution_gate_boundaries.py`
- `tests/test_explicit_skill_invocation_cli.py`
- `pyproject.toml`
- `src/chanta_core/__init__.py`

## Root Cause

`WorkspaceReadService` already rejected traversal and outside-root reads, but the read-only gate did not pre-validate workspace read paths before invoking the explicit skill service. That allowed the gate summary to look like a clean execution path even when a downstream workspace read was denied.

PowerShell inline JSON passing also made direct `--input-json` usage fragile for paths containing backslashes and quotes.

## Public API / CLI Surface

Existing CLI options remain supported:

- `chanta-cli skill run <skill_id> --input-json <json>`
- `chanta-cli skill gate-run <skill_id> --input-json <json>`

New or hardened CLI input paths:

- `--input-json-file <path>`
- `--root <root_path>`
- `--path <relative_path>`
- `--recursive`
- `--max-results`

The workspace convenience flags build an explicit input payload only after a caller supplies an explicit `skill_id`.

JSON input files are read as UTF-8 with optional BOM support to accommodate common Windows PowerShell file output behavior.

## Gate Behavior

The gate now pre-validates workspace read paths for:

- `skill:list_workspace_files`
- `skill:read_workspace_text_file`
- `skill:summarize_workspace_markdown`

The gate denies:

- missing or invalid workspace read payloads;
- missing `root_path`;
- missing `relative_path` for file read and markdown summary;
- absolute `relative_path`;
- traversal through `..`;
- resolved targets outside the configured root.

If validation fails:

- `decision=deny`;
- `can_execute=False`;
- result status is `blocked`;
- `executed=false`;
- `blocked=true`;
- `ExplicitSkillInvocationService` is not called.

If the gate allows execution but downstream invocation denies or fails, the gate result no longer reports a clean executed success.

## Workspace Read Boundary

Workspace path checks use `pathlib.Path`, `resolve(strict=False)`, and resolved-path containment. They do not rely only on naive string prefix checks.

`WorkspaceReadService` independently rejects the same traversal and absolute-path cases. The gate is therefore an early enforcement layer, not a replacement for workspace service validation.

## Error Diagnostics

Invalid JSON now returns a controlled CLI diagnostic with:

- source kind: `input_json` or `input_json_file`;
- JSON parser message;
- bounded received preview with newlines escaped.

The diagnostic is intended to help debug shell quoting. Callers should not place secrets in CLI payloads.

## Boundary Guarantees

- No natural-language skill execution was added.
- No skill inference from arbitrary prompt was added.
- No write, shell, network, MCP, or plugin execution was added.
- No permission grants are created.
- No ToolDispatcher or SkillExecutor dynamic mutation was added.
- No LLM calls were added.
- No private source body printing was added.

## Restore Procedure

1. Install the package in editable mode:

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
```

2. Run targeted tests:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_skill_execution_gate_workspace_read.py tests\test_workspace_read_path_helpers.py tests\test_explicit_skill_invocation_workspace_read.py tests\test_skill_execution_gate_cli.py tests\test_skill_execution_gate_boundaries.py
```

3. Run the full suite:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

## Manual Verification

Safe read:

```powershell
chanta-cli skill gate-run skill:read_workspace_text_file --root "<WORKSPACE_ROOT>" --path "overlay\example.md"
```

Expected:

- `executed=true`
- `blocked=false`

Traversal attempt:

```powershell
chanta-cli skill gate-run skill:read_workspace_text_file --root "<WORKSPACE_ROOT>" --path "..\..\secret.md"
```

Expected:

- `executed=false`
- `blocked=true`
- finding type includes `path_traversal` or another workspace boundary violation.

Unsupported shell skill:

```powershell
chanta-cli skill gate-run skill:shell --input-json-file test_shell_input.json
```

Expected:

- `executed=false`
- `blocked=true`

## Test Coverage

Covered behavior:

- safe relative read is allowed and executed when the file exists;
- traversal read is denied at the gate;
- absolute `relative_path` is denied at the gate;
- list workspace traversal is denied;
- markdown summary traversal is denied;
- denied gates do not call explicit invocation;
- workspace path helpers reject absolute and traversal paths;
- explicit invocation cannot mark traversal reads as completed success;
- `--input-json-file` works for `skill run` and `skill gate-run`;
- UTF-8 JSON files with a BOM are accepted;
- `--root` / `--path` work for workspace read gate-run;
- invalid JSON diagnostics are controlled and traceback-free;
- unsupported write/shell/network/MCP/plugin skill IDs remain blocked.

## Known Limitations

- The gate remains scoped to explicit read-only workspace skills.
- No general tool gate is introduced.
- No write/shell/network execution gate is introduced.
- No natural-language automatic execution is introduced.
- This release hardens execution safety but does not replace future reviewed proposal-to-execution flow design.

## Checklist

- [x] Traversal paths are denied.
- [x] Absolute `relative_path` is denied.
- [x] Outside-root resolved targets are denied.
- [x] `list_workspace_files` traversal is denied.
- [x] `read_workspace_text_file` traversal is denied.
- [x] `summarize_workspace_markdown` traversal is denied.
- [x] Denied gate does not call explicit invocation.
- [x] Denied summary shows `executed=false`.
- [x] Denied summary shows `blocked=true`.
- [x] WorkspaceReadService independently rejects traversal.
- [x] `--input-json-file` works.
- [x] `--root` / `--path` work for workspace read.
- [x] Invalid JSON diagnostic improved.
- [x] Shell/network/write/MCP/plugin remain blocked.
- [x] No new capability added.
- [x] No permission auto-grant added.
- [x] No ToolDispatcher mutation added.
- [x] No SkillExecutor mutation added.
