# ChantaCore v0.17.4a Restore Notes

Patch: Read-only Gate Workspace Boundary Enforcement Fix
Applied on current package line: 0.17.5a1

## Scope

This patch fixes the read-only execution gate so workspace read paths are
validated before `ExplicitSkillInvocationService` is called.

The affected skills are:

- `skill:list_workspace_files`
- `skill:read_workspace_text_file`
- `skill:summarize_workspace_markdown`

## Root Cause

Before this patch, `WorkspaceReadService` rejected traversal and outside-root
paths independently, but `SkillExecutionGateService` did not pre-validate the
workspace read path before allowing invocation. As a result, the gate could
report `executed=true` even when the downstream workspace read was denied.

## Fix

`SkillExecutionGateService.evaluate_gate()` now validates workspace read inputs
before allowing execution:

- `root_path` is required.
- `relative_path` is required for file read and markdown summary.
- absolute `relative_path` values are denied.
- `..` traversal is denied.
- resolved targets outside `root_path` are denied.
- denied gate decisions do not call `ExplicitSkillInvocationService`.

The gate summary now includes:

- `gate_decision`
- `gate_decision_basis`
- `first_finding_type` when findings exist

If the gate allows execution but downstream invocation fails, the gate result no
longer reports a clean `executed` success.

## Workspace Read Service

`WorkspaceReadService` already enforced the root boundary through resolved paths.
This patch also improves violation classification so absolute target paths are
reported as `absolute_path_not_allowed`.

## Boundary Guarantees

- No shell execution was added.
- No network access was added.
- No write path was added.
- No permission grants are created.
- No natural-language routing was added.
- Workspace path checks use resolved path containment, not naive string prefix
  checks.

## Tests

Added or updated tests for:

- safe relative path allowed by gate;
- traversal denied by gate;
- absolute target denied by gate;
- list workspace traversal denied by gate;
- markdown summary traversal denied by gate;
- denied gate does not call explicit invocation;
- workspace path helpers reject traversal and absolute paths;
- explicit invocation cannot complete traversal reads successfully;
- CLI `gate-run` reports blocked traversal/absolute paths.

Targeted command:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_skill_execution_gate_workspace_read.py tests\test_workspace_read_path_helpers.py tests\test_explicit_skill_invocation_workspace_read.py tests\test_skill_execution_gate_cli.py
```

## Restore-Grade Policy Addendum

This patch note is part of the public restore record. It is a corrective patch
on the v0.17.4 read-only execution gate, not a new capability line.

### Implemented Files

Primary files affected:

- `src/chanta_core/skills/execution_gate.py`
- `src/chanta_core/workspace/read_service.py`
- `src/chanta_core/cli/main.py`
- `tests/test_skill_execution_gate_workspace_read.py`
- `tests/test_workspace_read_path_helpers.py`
- `tests/test_explicit_skill_invocation_workspace_read.py`
- `tests/test_skill_execution_gate_cli.py`
- `pyproject.toml`
- `src/chanta_core/__init__.py`

### Public API / Service Surface

No new public model family was introduced. The existing
`SkillExecutionGateService`, `ReadOnlyExecutionGatePolicy`,
`SkillExecutionGateRequest`, `SkillExecutionGateDecision`,
`SkillExecutionGateFinding`, and `SkillExecutionGateResult` surfaces were
hardened.

The restored behavior must preserve this invariant:

```text
denied gate decisions do not call ExplicitSkillInvocationService
```

For workspace reads, the gate must validate the structured payload before any
explicit invocation call is made.

### Persistence and Canonical State

No new persistence layer was introduced. The patch continues to use OCEL records
from the existing v0.17.4 execution gate and explicit invocation surfaces.
Markdown remains a human-readable restore note only.

### OCEL Expectations

No new object or event type is required beyond the v0.17.4 gate surface.
Rejected workspace payloads should still produce gate findings and denied gate
results rather than downstream invocation success records.

Expected finding categories include traversal, absolute path, outside-root, and
invalid workspace payload failures. The exact finding type may vary with the
workspace service classification, but the restored behavior must expose a
blocked result and a first finding.

### Runtime Integration

The patch does not attach a new runtime path. It only changes the safety
precondition before `SkillExecutionGateService.gate_explicit_invocation()`
delegates to explicit invocation. It must not mutate `ToolDispatcher`,
`SkillExecutor`, permissions, session permissions, or runtime capabilities.

### Verification Procedure

Run the targeted patch subset:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_skill_execution_gate_workspace_read.py tests\test_workspace_read_path_helpers.py tests\test_explicit_skill_invocation_workspace_read.py tests\test_skill_execution_gate_cli.py
```

Then run the broader explicit invocation and gate safety checks:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_skill_execution_gate_service.py tests\test_skill_execution_gate_boundaries.py tests\test_explicit_skill_invocation_workspace_read.py
```

Finally run the full suite when restoring the complete package line:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

### Restore Checklist

- [ ] Traversal input is denied before explicit invocation.
- [ ] Absolute `relative_path` input is denied before explicit invocation.
- [ ] Outside-root resolved targets are denied before explicit invocation.
- [ ] Denied gate summaries show `executed=false`.
- [ ] Denied gate summaries show `blocked=true`.
- [ ] Safe relative workspace reads still execute through the explicit read-only path.
- [ ] No shell, network, write, MCP, plugin, or natural-language execution path is added.
