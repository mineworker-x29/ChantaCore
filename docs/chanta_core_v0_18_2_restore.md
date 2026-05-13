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
