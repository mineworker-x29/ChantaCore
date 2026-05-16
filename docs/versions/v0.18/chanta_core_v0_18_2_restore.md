# ChantaCore v0.18.2 Restore Document

Version name: ChantaCore v0.18.2 - Execution Envelope Query / Audit CLI

## Purpose

v0.18.2 adds a generic read-only Execution Audit surface for existing ExecutionEnvelope records.

Execution Audit queries envelope, provenance, input snapshot, and output snapshot records that already exist in OCEL. It does not execute skills, does not grant permissions, and does not promote outputs into memory or persona state.

## Scope

Implemented public concepts:

- Execution Audit Query
- Execution Audit Filter
- Execution Audit Record View
- Execution Audit Result
- Execution Audit Finding
- Execution Audit Service
- Execution Query CLI
- Read-only Audit Surface
- OCEL object/event/relation support
- ContextHistory adapter support
- PIG/OCPX lightweight report counts

## CLI

The execution command group is read-only:

```powershell
chanta-cli execution list
chanta-cli execution recent
chanta-cli execution show <envelope_id>
chanta-cli execution audit
```

Supported filters:

- `--skill-id`
- `--status`
- `--session-id`
- `--blocked`
- `--failed`
- `--limit`
- `--show-paths`
- `--json`

By default, path-like fields are redacted and full input/output payload bodies are not printed. JSON output uses the same redacted record views.

## Redaction

Execution Audit shows previews by default. Sensitive fields remain redacted, including password, token, secret, API key, private key, and credential fields.

Path-like fields are hidden by default. Use `--show-paths` only when local path visibility is explicitly needed.

## Boundary

Execution Audit:

- is read-only;
- queries existing ExecutionEnvelope records;
- does not execute skills;
- does not call explicit invocation, gate, or reviewed bridge services;
- does not create permission grants;
- does not create promotion candidates;
- does not mutate memory or persona state;
- does not support write, shell, network, MCP, or plugin execution.

## Future Work

- controlled result promotion candidate;
- workspace read summarization pipeline;
- personal runtime workbench.

## Restore-Grade Policy Addendum

### Implemented Files

Primary implementation:

- `src/chanta_core/execution/audit.py`
- `src/chanta_core/execution/history_adapter.py`
- `src/chanta_core/execution/__init__.py`
- `src/chanta_core/cli/main.py`
- `src/chanta_core/pig/reports.py`

Tests:

- `tests/test_execution_audit_models.py`
- `tests/test_execution_audit_service.py`
- `tests/test_execution_audit_cli.py`
- `tests/test_execution_audit_history_adapter.py`
- `tests/test_execution_audit_ocel_shape.py`
- `tests/test_execution_audit_boundaries.py`

### Public API / Model Surface

Models:

- `ExecutionAuditQuery`
- `ExecutionAuditFilter`
- `ExecutionAuditRecordView`
- `ExecutionAuditResult`
- `ExecutionAuditFinding`

Service:

- `ExecutionAuditService`

Key service methods:

- `create_query`
- `create_filter`
- `query_envelopes`
- `recent_envelopes`
- `show_envelope`
- `audit_envelopes`
- `create_record_view`
- `record_finding`
- `record_result`
- `render_audit_table`
- `render_audit_detail`

### Persistence and Canonical State

Execution Audit is a read-only projection over existing OCEL execution envelope
records. It does not create execution envelopes, promote outputs, write memory,
write persona state, or modify workspace files.

Full input and output bodies remain outside the audit surface. Audit record
views expose bounded previews and references. Path-like fields are redacted by
default.

### OCEL Shape

Object types:

- `execution_audit_query`
- `execution_audit_filter`
- `execution_audit_record_view`
- `execution_audit_result`
- `execution_audit_finding`

Events:

- `execution_audit_query_created`
- `execution_audit_filter_created`
- `execution_audit_record_view_created`
- `execution_audit_result_recorded`
- `execution_audit_finding_recorded`

Expected relations:

- filter belongs to query;
- record view belongs to query;
- result belongs to query;
- finding belongs to query;
- record views reference existing execution envelope ids when available.

### Context History and PIG/OCPX

ContextHistory adapters project audit queries, record views, results, and
findings as `source="execution_audit"` entries. Failed, not-found, and warning
findings should receive higher priority than normal list results.

The PIG/OCPX execution summary should include lightweight audit counts for
queries, filters, record views, findings, results, blocked/failed filters, and
not-found results when the corresponding OCEL records exist.

### Restore Procedure

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m pytest tests\test_execution_audit_models.py tests\test_execution_audit_service.py tests\test_execution_audit_cli.py tests\test_execution_audit_history_adapter.py tests\test_execution_audit_ocel_shape.py tests\test_execution_audit_boundaries.py
.\.venv\Scripts\python.exe -m pytest
```

Manual CLI checks:

```powershell
chanta-cli execution list
chanta-cli execution recent --limit 5
chanta-cli execution audit --blocked
chanta-cli execution show <execution_envelope_id>
```

### Restore Checklist

- [ ] Audit list/recent/show/audit commands are read-only.
- [ ] `show` returns a controlled not-found result for missing envelope ids.
- [ ] `--show-paths` is required to reveal path-like fields.
- [ ] Sensitive keys remain redacted in previews.
- [ ] Audit does not call explicit invocation, gate, bridge, or promotion services.
- [ ] OCEL audit objects/events/relations are recorded.
- [ ] ContextHistory adapter entries are generated.
- [ ] Boundary tests confirm no execution or permission grants.
