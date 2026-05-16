# ChantaCore v0.17.2 Restore Document

Version name: ChantaCore v0.17.2 - Capability-aware Explicit Skill Invocation Surface

## Purpose

v0.17.2 adds a generic Explicit Skill Invocation surface. Callers must provide an explicit `skill_id` and explicit structured input. The surface is not natural-language routing and does not infer a skill from arbitrary user text.

The initial supported skill family is read-only workspace read skills:

- `skill:list_workspace_files`
- `skill:read_workspace_text_file`
- `skill:summarize_workspace_markdown`

Unsupported skill identifiers return controlled violations. The surface does not grant capabilities, create permission grants, write files, execute shell/network operations, connect MCP, load plugins, or call an LLM.

## Implemented Files

- `src/chanta_core/skills/invocation.py`
- `src/chanta_core/skills/ids.py`
- `src/chanta_core/skills/errors.py`
- `src/chanta_core/skills/history_adapter.py`
- `src/chanta_core/skills/__init__.py`
- `src/chanta_core/cli/main.py`
- `src/chanta_core/pig/reports.py`
- `tests/test_explicit_skill_invocation_models.py`
- `tests/test_explicit_skill_invocation_service.py`
- `tests/test_explicit_skill_invocation_workspace_read.py`
- `tests/test_explicit_skill_invocation_cli.py`
- `tests/test_explicit_skill_invocation_history_adapter.py`
- `tests/test_explicit_skill_invocation_ocel_shape.py`
- `tests/test_explicit_skill_invocation_boundaries.py`
- `tests/test_imports.py`
- `pyproject.toml`
- `src/chanta_core/__init__.py`

## Public API / Model Surface

New models:

- `ExplicitSkillInvocationRequest`
- `ExplicitSkillInvocationInput`
- `ExplicitSkillInvocationDecision`
- `ExplicitSkillInvocationResult`
- `ExplicitSkillInvocationViolation`

New service:

- `ExplicitSkillInvocationService`

New ID helpers:

- `new_explicit_skill_invocation_request_id`
- `new_explicit_skill_invocation_input_id`
- `new_explicit_skill_invocation_decision_id`
- `new_explicit_skill_invocation_result_id`
- `new_explicit_skill_invocation_violation_id`

## Service Behavior

`ExplicitSkillInvocationService.invoke_explicit_skill` follows a narrow explicit flow:

1. Create an invocation request.
2. Record structured input with preview and hash.
3. Validate that `skill_id` was provided by the caller.
4. Validate that the skill is supported.
5. Validate required input fields.
6. Decide whether invocation is allowed, unsupported, denied, or needs review.
7. Invoke only supported read-only workspace skills.
8. Return a structured result envelope.

The service accepts capability, permission, sandbox, and risk references as metadata. It does not create grants, does not bypass workspace root containment, and does not dynamically mutate any tool or skill dispatcher.

## CLI Surface

The CLI includes an explicit skill command:

```powershell
chanta-cli skill run <skill_id> --input-json '{"root_path":"<WORKSPACE_ROOT>","relative_path":"docs/example.md"}'
```

Convenience flags can also provide workspace read inputs:

```powershell
chanta-cli skill run skill:read_workspace_text_file --root <WORKSPACE_ROOT> --path docs/example.md
```

The CLI requires an explicit skill identifier. Unsupported or invalid requests return controlled diagnostics instead of tracebacks.

## OCEL Shape

Object types:

- `explicit_skill_invocation_request`
- `explicit_skill_invocation_input`
- `explicit_skill_invocation_decision`
- `explicit_skill_invocation_result`
- `explicit_skill_invocation_violation`

Events:

- `explicit_skill_invocation_requested`
- `explicit_skill_invocation_input_recorded`
- `explicit_skill_invocation_input_validated`
- `explicit_skill_invocation_decided`
- `explicit_skill_invocation_started`
- `explicit_skill_invocation_completed`
- `explicit_skill_invocation_denied`
- `explicit_skill_invocation_failed`
- `explicit_skill_invocation_violation_recorded`

Relations:

- input belongs to request
- decision belongs to request
- result belongs to request
- violation belongs to request
- request may reference capability, permission, session permission, sandbox, and risk decision identifiers
- result may reference workspace read result identifiers when produced

## Context History

New adapters use `source="explicit_skill_invocation"`:

- `explicit_skill_invocation_requests_to_history_entries`
- `explicit_skill_invocation_results_to_history_entries`
- `explicit_skill_invocation_violations_to_history_entries`

Violations, denied results, and failed results receive high priority. Completed results are medium priority. Requests are low to medium priority.

## PIG / OCPX Report Support

The PIG skill usage summary includes:

- `explicit_skill_invocation_request_count`
- `explicit_skill_invocation_input_count`
- `explicit_skill_invocation_decision_count`
- `explicit_skill_invocation_result_count`
- `explicit_skill_invocation_violation_count`
- `explicit_skill_invocation_completed_count`
- `explicit_skill_invocation_denied_count`
- `explicit_skill_invocation_unsupported_count`
- `explicit_skill_invocation_failed_count`
- `explicit_skill_invocation_by_skill_id`
- `explicit_skill_invocation_violation_by_type`

## Restore Procedure

1. Install the package in editable mode:

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
```

2. Run targeted tests:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_explicit_skill_invocation_models.py tests\test_explicit_skill_invocation_service.py tests\test_explicit_skill_invocation_workspace_read.py tests\test_explicit_skill_invocation_cli.py tests\test_explicit_skill_invocation_history_adapter.py tests\test_explicit_skill_invocation_ocel_shape.py tests\test_explicit_skill_invocation_boundaries.py
```

3. Run the full suite:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

4. Check public hygiene with generic private-boundary tokens only:

```powershell
rg -n "private_persona_name|private_user_name|<LOCAL_PRIVATE_ROOT>" src tests docs README.md pyproject.toml
```

Expected result: no public private-content matches.

## Test Coverage

Covered behavior:

- request/input/decision/result/violation model serialization
- unsupported skill returns controlled unsupported/denied result
- missing input returns controlled `invalid_input` violation
- explicit workspace file listing works with a temporary root
- explicit workspace text read works with a safe relative path
- outside-root read is rejected by workspace read boundaries
- write/shell/network/MCP/plugin skill identifiers are unsupported
- CLI requires explicit skill identifier
- CLI invalid and unsupported cases avoid tracebacks
- no natural-language skill inference
- no LLM/shell/network/MCP/plugin/write execution
- OCEL objects/events/relations
- ContextHistory adapters
- PIG/OCPX lightweight counts

## Known Limitations

- No natural-language skill proposal router yet.
- No permission-aware execution gate yet.
- No general tool orchestration yet.
- Supported execution is intentionally limited to read-only workspace skills.

## Future Work

- v0.17.3: skill proposal router.
- v0.17.4: read-only execution gate.
- v0.17.5: execution provenance envelope.

## Checklist

- [x] Public terminology uses generic Explicit Skill Invocation concepts.
- [x] Explicit skill identifier is required.
- [x] Natural-language automatic routing is not implemented.
- [x] Read-only workspace skills are supported.
- [x] Unsupported skills return controlled violations.
- [x] Invalid input returns controlled violations.
- [x] Workspace root boundaries are preserved by the workspace read service.
- [x] CLI explicit skill command is present.
- [x] OCEL shape added.
- [x] ContextHistory adapter added.
- [x] PIG/OCPX lightweight report support added.
- [x] No private names/content are included.
- [x] No hardcoded private root is included.
- [x] No permission auto-grant is included.
- [x] No LLM/shell/network/MCP/plugin/write execution is added.
