# ChantaCore v0.18.5 Restore Notes

Version name: ChantaCore v0.18.5 - Personal Runtime Session Workbench / Operator UX

## Scope

Personal Runtime Workbench is a read-only operator UX. It aggregates runtime status, proposal and review state, execution activity, promotion candidates, workspace summary candidates, and health findings into redacted operator summaries.

## Guarantees

- Workbench does not execute skills.
- Workbench does not approve reviews.
- Workbench does not bridge proposals.
- Workbench does not promote outputs.
- Workbench does not create permission grants.
- Workbench does not mutate memory, persona, overlay, or source files.
- Workbench redacts private paths by default.
- Workbench records snapshot, panel, pending item, recent activity, finding, and result events as OCEL.

## CLI

The CLI group is:

- `chanta-cli workbench status`
- `chanta-cli workbench recent`
- `chanta-cli workbench pending`
- `chanta-cli workbench blockers`
- `chanta-cli workbench candidates`
- `chanta-cli workbench summaries`
- `chanta-cli workbench health`

Options include `--limit`, `--show-paths`, `--json`, and `--ocel-db`.

## Future Work

- Reviewed approval UI.
- Controlled promotion executor, if ever enabled.
- Richer dashboard/UI.

No private content is included in this public restore note.

## Restore-Grade Policy Addendum

### Implemented Files

Primary implementation:

- `src/chanta_core/runtime/workbench.py`
- `src/chanta_core/runtime/__init__.py`
- `src/chanta_core/cli/main.py`
- `src/chanta_core/pig/reports.py`

Tests:

- `tests/test_personal_runtime_workbench_models.py`
- `tests/test_personal_runtime_workbench_service.py`
- `tests/test_personal_runtime_workbench_cli.py`
- `tests/test_personal_runtime_workbench_history_adapter.py`
- `tests/test_personal_runtime_workbench_ocel_shape.py`
- `tests/test_personal_runtime_workbench_boundaries.py`

### Public API / Model Surface

Models:

- `PersonalRuntimeWorkbenchSnapshot`
- `PersonalRuntimeWorkbenchPanel`
- `PersonalRuntimeWorkbenchPendingItem`
- `PersonalRuntimeWorkbenchRecentActivity`
- `PersonalRuntimeWorkbenchFinding`
- `PersonalRuntimeWorkbenchResult`

Service:

- `PersonalRuntimeWorkbenchService`

Key service methods:

- `build_snapshot`
- `collect_runtime_status`
- `collect_pending_items`
- `collect_recent_activities`
- `collect_blockers`
- `collect_candidates`
- `collect_summary_candidates`
- `collect_health_findings`
- `record_result`
- `render_workbench_status`
- `render_workbench_recent`
- `render_workbench_pending`
- `render_workbench_blockers`
- `render_workbench_candidates`
- `render_workbench_summaries`
- `render_workbench_health`

### Persistence and Canonical State

The workbench is a read-only aggregate over existing runtime, proposal, review,
execution, promotion, and workspace summary records. It records workbench
snapshots and panels as OCEL diagnostic artifacts, but it does not mutate the
underlying records.

The workbench does not approve reviews, bridge proposals, execute skills,
promote candidates, create permission grants, or write memory/persona/overlay
state.

### OCEL Shape

Object types:

- `personal_runtime_workbench_snapshot`
- `personal_runtime_workbench_panel`
- `personal_runtime_workbench_pending_item`
- `personal_runtime_workbench_recent_activity`
- `personal_runtime_workbench_finding`
- `personal_runtime_workbench_result`

Events:

- `personal_runtime_workbench_snapshot_created`
- `personal_runtime_workbench_panel_recorded`
- `personal_runtime_workbench_pending_item_recorded`
- `personal_runtime_workbench_recent_activity_recorded`
- `personal_runtime_workbench_finding_recorded`
- `personal_runtime_workbench_result_recorded`

Expected relations:

- panels, pending items, recent activities, findings, and results belong to the
  snapshot;
- pending items and recent activities may reference source proposal, review,
  execution, promotion, or summary ids.

### CLI Surface

```powershell
chanta-cli workbench status
chanta-cli workbench recent
chanta-cli workbench pending
chanta-cli workbench blockers
chanta-cli workbench candidates
chanta-cli workbench summaries
chanta-cli workbench health
```

Options include `--limit`, `--show-paths`, `--json`, and `--ocel-db`.
Path-like fields are redacted by default.

### Restore Procedure

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m pytest tests\test_personal_runtime_workbench_models.py tests\test_personal_runtime_workbench_service.py tests\test_personal_runtime_workbench_cli.py tests\test_personal_runtime_workbench_history_adapter.py tests\test_personal_runtime_workbench_ocel_shape.py tests\test_personal_runtime_workbench_boundaries.py
.\.venv\Scripts\python.exe -m pytest
```

### Restore Checklist

- [ ] Workbench status renders redacted runtime state.
- [ ] Pending panels include pending proposals/reviews/candidates without approving them.
- [ ] Recent panels show blocked and failed executions without retrying them.
- [ ] Candidate panels do not promote candidates.
- [ ] `--show-paths` is required for path-like fields.
- [ ] OCEL workbench objects/events/relations are recorded.
- [ ] ContextHistory adapter entries are generated.
- [ ] Boundary tests confirm no execution, approval, bridge, promotion, or permission grant.
