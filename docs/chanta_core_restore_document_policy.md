# ChantaCore Restore Document Policy

This policy records the expected public restore-document standard for ChantaCore.

Restore documents are not short release notes. They are human-readable restore-grade records that should allow a future maintainer to reconstruct the expected source, runtime, trace, boundary, and test state of a version.

## Storage Layout

Version-specific documents are stored under `docs/versions/vMAJOR.MINOR/`.
For the current `v0.xx` release line, this means each minor release line gets
its own directory such as `v0.18`, `v0.19`, or `v0.20`. Patch-level restore
documents, version contracts, audits, and migration notes for that minor line
belong inside the matching directory.

Examples:

- `docs/versions/v0.19/chanta_core_v0_19_9_restore.md`
- `docs/versions/v0.20/v0.20.1_self_workspace_awareness.md`

Do not place new version-specific restore files directly under `docs/`.

This minor-version folder rule applies to restore documents, version contracts,
version audits, and migration notes tied to a release line. General docs that
are not version-specific remain under `docs/` or another topic-specific folder.

## Release-Line Orientation

Restore documents should explain version intent using the current release-line
orientation:

- `v0.10.x` through `v0.18.x`: Core / Process Intelligence. This range builds
  the organ of observation and the OCEL-native event/object/relation substrate.
- `v0.19.x`: Internal Observation + Digestion. This line observes and digests
  external trace, skill, and behavior into OCEL-observable state and candidates.
- `v0.20.x`: OCEL-native Self-Awareness. This line observes ChantaCore's own
  workspace, code, project surface, candidate, verification, and intention
  outputs as OCEL object-centric processes.
- `v0.21.x`: Deep Self-Introspection. This line is reserved for deeper
  OCEL-oriented inspection of runtime, capability, policy, context, and trace
  consistency.

Older future-track language that calls `v0.20.x` a write, shell, network, MCP,
plugin, or external harness safety track should be treated as superseded. In
current restore documents, those dangerous or mutating capabilities remain
explicitly excluded until a later release line defines and verifies a dedicated
safety layer.

## Required Sections

A restore document should include:

- version name and scope;
- restore goal;
- implemented file list;
- public model or API surface;
- service methods and expected behavior;
- persistence and canonical-state policy;
- runtime integration, if any;
- explicit non-goals and boundaries;
- OCEL object types;
- OCEL events;
- OCEL relation expectations;
- ContextHistory adapter notes, if any;
- PIG/OCPX report support, if any;
- test coverage;
- restore procedure;
- restore checklist;
- known limitations;
- future work.

## Boundary Expectations

Restore documents must distinguish:

- implemented behavior;
- intentionally absent behavior;
- future work;
- canonical state;
- human-readable documentation.

If a feature is only staged, draft, review-only, design-only, or optional, the document should say so directly.

If a feature must not grant capabilities, mutate runtime state, or activate external systems, the document should say so directly.

## Public Safety

Public restore documents must use generic product terminology. They must not contain user-specific private content, private local roots, private correspondence, or private assistant mappings.

Private/local overlays belong outside public restore docs unless described only as generic framework boundaries.

## Verification Standard

Every restore document should include targeted test commands and full-suite verification commands when applicable.

If a version has a known invariant, the document should state it in a searchable form. Examples:

- `canonical_import_enabled=False`
- `canonical_activation_enabled=False`
- runtime capability truth overrides personal/persona claims

## Length Guidance

Length is not the goal. Reconstructability is the goal.

A small patch may have a short restore document, but the document should still record the model, boundary, trace, test, and limitation information needed to restore the feature without relying on memory.
