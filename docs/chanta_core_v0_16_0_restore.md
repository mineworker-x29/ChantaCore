# ChantaCore v0.16.0 Restore Notes

Version name: ChantaCore v0.16.0 - Generic Persona Source Staged Import

This document is a restore-grade record of the v0.16.0 implementation. It is not canonical runtime state. ChantaCore canonical process and persona persistence remains OCEL-based.

## Restore Goal

v0.16.0 adds a generic staged import framework for readable persona source files. The framework lets ChantaCore register local `.md`, `.txt`, and `.html` content as reviewable ingestion candidates without treating those files as canonical persona state.

The important restoration point is the boundary:

- readable files are source candidates;
- candidate metadata can be traced and reviewed;
- deterministic drafts and projection candidates can be generated;
- `PersonaProfile` is not overwritten;
- `canonical_import_enabled` remains `False`.

## Implemented Files

Core implementation:

- `src/chanta_core/persona/source_import.py`
- `src/chanta_core/persona/ids.py`
- `src/chanta_core/persona/errors.py`
- `src/chanta_core/persona/history_adapter.py`
- `src/chanta_core/persona/__init__.py`
- `src/chanta_core/pig/reports.py`

Version marker:

- `pyproject.toml`
- `src/chanta_core/__init__.py`

Restore document:

- `docs/chanta_core_v0_16_0_restore.md`

Tests:

- `tests/test_persona_source_import_models.py`
- `tests/test_persona_source_import_service.py`
- `tests/test_persona_source_import_discovery.py`
- `tests/test_persona_source_import_validation.py`
- `tests/test_persona_source_import_history_adapter.py`
- `tests/test_persona_source_import_ocel_shape.py`
- `tests/test_persona_source_import_boundaries.py`
- `tests/test_imports.py`

## Public Models

`PersonaSource`

- Represents one readable local source or text registration.
- Stores metadata, hash, bounded preview, content length, trust level, privacy flag, and status.
- Does not store a canonical persona profile.

`PersonaSourceManifest`

- Records discovery context for a source root, include patterns, exclude patterns, and source ids.
- Makes discovery reproducible without promoting discovered files into canonical persona state.

`PersonaSourceIngestionCandidate`

- Groups source ids into a reviewable candidate.
- Uses `review_status="pending_review"` by default.
- Enforces `canonical_import_enabled=False`.

`PersonaSourceValidationResult`

- Records source-level or candidate-level validation.
- Captures missing fields, warnings, errors, and validation kind.

`PersonaAssimilationDraft`

- Deterministically extracts candidate-facing identity, role, boundary, style, safety, and unresolved-question points.
- It is a draft for human or later policy review, not a canonical import.

`PersonaProjectionCandidate`

- Builds bounded projected blocks from a draft.
- Enforces `canonical_import_enabled=False`.
- Tracks truncation and total character count.

`PersonaSourceRiskNote`

- Records review risk categories and review requirement metadata.

## Service Surface

`PersonaSourceStagedImportService` supports:

- `register_source_from_text`
- `register_source_from_file`
- `discover_sources`
- `create_manifest`
- `validate_source`
- `validate_candidate`
- `create_ingestion_candidate`
- `create_assimilation_draft`
- `create_projection_candidate`
- `record_risk_note`

Expected restoration behavior:

- text and local file registration generate hashes and bounded previews;
- `.html` content is converted to conservative text using local parsing only;
- include/exclude patterns are respected during discovery;
- validation can mark sources valid, invalid, or needing review;
- candidate creation never enables canonical import;
- projection candidates are bounded and can be truncated.

## Helper Functions

The public helper layer includes:

- `hash_text`
- `preview_text`
- `detect_source_type`
- `strip_html_to_text`
- `extract_persona_points`
- `validate_allowed_extension`
- `safe_read_text_file`

Restore-critical behavior:

- `safe_read_text_file` uses `pathlib`;
- root containment is checked when a source root is supplied;
- file reads are bounded by byte limit;
- binary-looking files are rejected;
- unsupported extensions are rejected;
- no network fetch is available.

## Default Source Policy

Allowed readable extensions:

- `.md`
- `.txt`
- `.html`

Default excluded areas include generic private or archival directories such as:

- `letters`
- `messages`
- `archive`

Default message-like note patterns are excluded generically. The public framework must not depend on a user-specific file name.

## Canonical Rule

Canonical persistence remains OCEL-based.

Readable Markdown, TXT, and HTML files are ingestion inputs only. They are not canonical persona state and they do not overwrite `PersonaProfile` records.

All ingestion candidates and projection candidates set:

```text
canonical_import_enabled=False
```

If a future version promotes any source-derived material into canonical persona state, that promotion must be explicit, reviewed, OCEL-traced, and covered by a separate conformance rule.

## Boundary Rules

v0.16.0 does not add:

- automatic persona overwrite;
- automatic runtime projection activation;
- canonical Markdown persona storage;
- JSONL persona store;
- LLM summarization;
- network fetch;
- shell execution;
- MCP connection;
- plugin loading;
- terminal scrollback import;
- self-modifying persona behavior;
- permission grant creation.

Capability truth remains outside the source import layer. Source text may claim a capability, but this framework does not grant or activate that capability.

## OCEL Object Types

The staged import service records:

- `persona_source`
- `persona_source_manifest`
- `persona_source_ingestion_candidate`
- `persona_source_validation_result`
- `persona_assimilation_draft`
- `persona_projection_candidate`
- `persona_source_risk_note`

## OCEL Events

The staged import service records:

- `persona_source_registered`
- `persona_source_manifest_created`
- `persona_source_ingestion_candidate_created`
- `persona_source_validation_recorded`
- `persona_assimilation_draft_created`
- `persona_projection_candidate_created`
- `persona_source_risk_note_recorded`
- `persona_source_review_required`
- `persona_source_rejected`
- `persona_source_archived`

`persona_source_archived` is part of the intended public event vocabulary. If not emitted by a specific workflow, it remains reserved for future archival behavior.

## OCEL Relations

Best-effort relations link:

- manifest includes source;
- candidate uses source;
- candidate uses manifest;
- validation validates source or candidate;
- draft derives from candidate and source;
- projection candidate projects draft;
- risk note describes source or candidate.

These relations are used for process inspection and report counts, not for canonical persona activation.

## Context History Adapter

The history adapter exports generic entries for:

- persona sources;
- ingestion candidates;
- assimilation drafts;
- projection candidates;
- risk notes.

The adapter source is:

```text
persona_source_import
```

History entries use bounded previews and metadata. They must not introduce a complete source body as a canonical persona memory.

## PIG/OCPX Reporting

`PIGReportService` includes lightweight counts for:

- `persona_source_count`
- `persona_source_manifest_count`
- `persona_source_ingestion_candidate_count`
- `persona_source_validation_result_count`
- `persona_assimilation_draft_count`
- `persona_projection_candidate_count`
- `persona_source_risk_note_count`
- `persona_source_valid_count`
- `persona_source_invalid_count`
- `persona_source_needs_review_count`
- `persona_candidate_pending_review_count`
- `persona_candidate_canonical_import_enabled_count`
- `persona_source_by_type`
- `persona_source_by_risk_level`
- `persona_private_source_count`

Expected invariant:

```text
persona_candidate_canonical_import_enabled_count == 0
```

## Test Coverage

The v0.16.0 tests cover:

- model `to_dict` shape;
- `.md` source registration;
- `.txt` source registration;
- `.html` source registration and text extraction;
- source hash generation;
- bounded preview generation;
- include/exclude discovery;
- generic letters/messages/archive exclusion;
- validation results;
- candidate creation with `canonical_import_enabled=False`;
- deterministic draft extraction;
- bounded/truncated projection candidate behavior;
- OCEL object/event shape;
- history adapter entries;
- public boundary checks against JSONL stores, LLM calls, network calls, shell calls, MCP/plugin loading, and persona overwrite.

All test content is dummy public-safe content.

## Restore Procedure

1. Confirm public version markers:

```powershell
.\.venv\Scripts\python.exe -c "import chanta_core; print(chanta_core.__version__)"
```

Expected:

```text
0.16.0
```

2. Run the v0.16.0 targeted test set:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_persona_source_import_models.py tests\test_persona_source_import_service.py tests\test_persona_source_import_discovery.py tests\test_persona_source_import_validation.py tests\test_persona_source_import_history_adapter.py tests\test_persona_source_import_ocel_shape.py tests\test_persona_source_import_boundaries.py
```

3. Run the full suite:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

4. Confirm no public source has enabled canonical source import:

```powershell
rg -n "canonical_import_enabled=True|overwrite_persona|markdown_as_persona_source" src tests docs
```

Expected:

```text
no matches
```

## Restore Checklist

- [ ] `source_import.py` exists.
- [ ] All seven public source import models exist.
- [ ] `PersonaSourceStagedImportService` exists.
- [ ] `.md`, `.txt`, and `.html` registration work.
- [ ] Discovery include/exclude policy is generic.
- [ ] Letters/messages/archive are excluded by default.
- [ ] Hash and preview generation work.
- [ ] Candidate creation sets `canonical_import_enabled=False`.
- [ ] Projection candidates are bounded.
- [ ] OCEL objects/events are recorded.
- [ ] ContextHistory adapter entries exist.
- [ ] PIG/OCPX report counts exist.
- [ ] No JSONL persona store is introduced.
- [ ] No LLM/network/shell/MCP/plugin execution is introduced.
- [ ] No runtime persona overwrite is introduced.

## Known Limitations

- No reviewed promotion from source candidate to canonical persona profile.
- No UI for staged import review.
- No source import conformance report beyond the lightweight tests and PIG counts.
- No runtime activation of projection candidates.

## Future Work

- Personal Directory loader boundary.
- Personal mode loadout binding.
- Staged import review UI.
- Conformance checks for persona import policies.
- Reviewed promotion from staged candidate to explicit persona profile update.
