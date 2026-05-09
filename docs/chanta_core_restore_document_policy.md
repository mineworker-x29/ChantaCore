# ChantaCore Restore Document Policy

This policy records the expected public restore-document standard for ChantaCore.

Restore documents are not short release notes. They are human-readable restore-grade records that should allow a future maintainer to reconstruct the expected source, runtime, trace, boundary, and test state of a version.

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
