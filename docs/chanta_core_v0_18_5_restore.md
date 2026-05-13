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
