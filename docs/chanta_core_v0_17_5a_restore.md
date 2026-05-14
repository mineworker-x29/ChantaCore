# ChantaCore v0.17.5a Restore Notes

Version: 0.17.5a2
Name: CLI UX patch for explicit skill input payloads

## Scope

v0.17.5a is a small CLI compatibility patch on top of v0.17.5. It does not add
new execution capability. It improves how explicit skill invocation payloads are
provided from shells that make inline JSON quoting fragile.

## Implemented Files

- `src/chanta_core/cli/main.py`
- `tests/test_explicit_skill_invocation_cli.py`
- `tests/test_skill_execution_gate_cli.py`
- `pyproject.toml`
- `src/chanta_core/__init__.py`

## CLI Behavior

The existing `--input-json` option remains supported for:

- `chanta-cli skill run`
- `chanta-cli skill gate-run`

Both commands now also support:

- `--input-json-file`
- `--root`
- `--path`
- `--recursive`
- `--max-results`

The workspace read convenience flags are merged into the explicit input payload
after JSON parsing. They do not infer a skill from natural language and do not
grant capabilities.

Example:

```powershell
chanta-cli skill gate-run skill:read_workspace_text_file --root "<WORKSPACE_ROOT>" --path "docs/example.md"
```

## Error Diagnostics

Invalid JSON now returns a controlled CLI diagnostic with:

- the JSON error message;
- whether the source was `--input-json` or `--input-json-file`;
- a bounded received preview.

The preview is intended for shell quoting diagnosis. It is truncated and has
newlines escaped. It is still user-provided input, so callers should avoid
placing secrets in CLI payloads.

If both `--input-json` and `--input-json-file` are provided, the CLI rejects the
command with a controlled diagnostic.

## Boundaries

- No natural-language routing was added.
- No new skills were enabled.
- No shell, network, MCP, plugin, or write execution was added.
- No permission grants are created.
- The read-only execution gate remains the only gate-run enforcement path.
- Existing workspace read boundary checks remain delegated to the workspace read
  skill implementation.

## Tests

Added coverage for:

- `skill run` with `--input-json-file`;
- `skill gate-run` with `--input-json-file`;
- invalid inline JSON diagnostics with received preview;
- invalid JSON file diagnostics with received preview;
- rejecting simultaneous `--input-json` and `--input-json-file`.

## Restore Checklist

- Confirm `pyproject.toml` version is `0.17.5a0`.
- Confirm `src/chanta_core/__init__.py` reports `0.17.5a0`.
- Confirm `chanta-cli skill run` accepts both inline JSON and JSON files.
- Confirm `chanta-cli skill gate-run` accepts both inline JSON and JSON files.
- Confirm convenience flags can build workspace read payloads without inline JSON.
- Confirm invalid JSON does not produce a traceback.

## v0.17.5a2 Personal Modes Diagnostics Addendum

The v0.17.5a line also improves `chanta-cli personal modes` diagnostics.

`personal modes` now renders discovered mode loadout refs with safe metadata:

- inferred mode name;
- loadout file basename;
- projection kind;
- size character count;
- preview character count;
- `safe_for_prompt`.

The command still does not print private source bodies, private letter bodies, or
full private paths by default. `--show-paths` continues to follow the existing
Personal Runtime CLI path display behavior.

Prompt activation diagnostics were also added through
`PersonalPromptActivationService.render_activation_diagnostics()`. The
diagnostic output includes:

- selected mode;
- matched loadout ref;
- activation status and scope;
- attached/skipped/denied booleans;
- total activation chars;
- truncation status.

These diagnostics are descriptive only. They do not activate modes, grant
capabilities, execute tools, or read private source bodies.

## Restore-Grade Policy Addendum

This patch note is part of the public restore record. It is a CLI UX patch on
the v0.17.5 execution envelope line and does not change the execution model.

### Implemented Files

Primary files affected:

- `src/chanta_core/cli/main.py`
- `tests/test_explicit_skill_invocation_cli.py`
- `tests/test_skill_execution_gate_cli.py`
- `pyproject.toml`
- `src/chanta_core/__init__.py`

The later personal mode diagnostics addendum also exercises:

- `src/chanta_core/persona/personal_runtime_surface.py`
- `src/chanta_core/persona/personal_prompt_activation.py`
- `tests/test_personal_runtime_surface_cli.py`
- `tests/test_personal_prompt_activation_rendering.py`

### Public API / CLI Surface

No new model family was introduced. The public CLI surface was expanded for
already-explicit skill commands:

```powershell
chanta-cli skill run <skill_id> --input-json-file input.json
chanta-cli skill gate-run <skill_id> --input-json-file input.json
chanta-cli skill gate-run skill:read_workspace_text_file --root <WORKSPACE_ROOT> --path docs/example.md
```

The convenience flags are payload builders. They are not skill inference and do
not remove the requirement for an explicit `skill_id`.

`chanta-cli personal modes` remains diagnostic. It renders bounded loadout
metadata and prompt activation diagnostics without printing private source
bodies, private letter bodies, or full paths unless path display is explicitly
requested.

### Persistence and Canonical State

No new canonical state was introduced. JSON input files are caller-supplied CLI
payloads, not a ChantaCore store. Invalid JSON diagnostics are bounded
debugging output and must not be treated as persisted runtime state.

### OCEL Expectations

No new OCEL model family was added by this patch. The existing explicit skill
invocation, read-only gate, Personal Runtime CLI, and prompt activation
diagnostic records remain the relevant trace surfaces.

Expected trace behavior:

- `skill run` still records explicit invocation request/input/decision/result
  records through the existing invocation surface;
- `skill gate-run` still records gate request/decision/finding/result records
  through the existing gate surface;
- personal mode diagnostics remain descriptive and must not create activation
  grant records.

### Boundary Expectations

- Inline JSON and JSON file input are mutually exclusive.
- JSON files are read as UTF-8, including optional BOM.
- Invalid JSON returns a controlled diagnostic rather than a traceback.
- Payload previews are bounded and newline-escaped.
- Callers should not place secrets in CLI JSON payloads.
- No natural-language routing, permission grant, runtime mode activation, shell,
  network, write, MCP, or plugin capability is introduced.

### Verification Procedure

Run the CLI-focused subset:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_explicit_skill_invocation_cli.py tests\test_skill_execution_gate_cli.py
```

Run the personal diagnostics subset if restoring the v0.17.5a2 addendum:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_personal_runtime_surface_cli.py tests\test_personal_prompt_activation_rendering.py
```

Run the full suite for the package line:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

### Restore Checklist

- [ ] `skill run` accepts `--input-json-file`.
- [ ] `skill gate-run` accepts `--input-json-file`.
- [ ] `--root` and `--path` build a workspace read payload only with explicit `skill_id`.
- [ ] Simultaneous `--input-json` and `--input-json-file` is rejected.
- [ ] Invalid inline JSON returns a controlled diagnostic.
- [ ] Invalid JSON file input returns a controlled diagnostic.
- [ ] Personal mode diagnostics do not activate modes or grant capabilities.
- [ ] No private source bodies or private letter bodies are printed.
