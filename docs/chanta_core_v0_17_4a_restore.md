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
