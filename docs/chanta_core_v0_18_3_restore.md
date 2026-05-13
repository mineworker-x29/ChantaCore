# ChantaCore v0.18.3 Restore Document

Version name: ChantaCore v0.18.3 - Controlled Result Promotion Candidate

## Purpose

v0.18.3 adds a review-only workflow for turning execution envelope results into promotion candidates.

Promotion candidates are not canonical memory, persona, overlay, context, or workspace summary records. They are pending review records that preserve preview, hash, and reference information from execution outputs.

## Scope

Implemented public concepts:

- Execution Result Promotion Policy
- Execution Result Promotion Candidate
- Execution Result Promotion Review Request
- Execution Result Promotion Decision
- Execution Result Promotion Finding
- Execution Result Promotion Result
- Controlled Promotion Workflow
- CLI promotion surface
- OCEL object/event/relation support
- ContextHistory adapter support
- PIG/OCPX lightweight report counts

## Candidate Rules

Candidate creation:

- is review-only;
- does not write memory;
- does not update persona;
- does not update personal overlay;
- uses preview, hash, and reference fields;
- does not copy full raw output bodies;
- starts as `pending_review`;
- sets `canonical_promotion_enabled=false`;
- sets `promoted=false`.

The default policy allows review candidates for context history, memory, personal overlay, persona source, workspace summary, manual note, process pattern, and other generic target kinds.

Denied target kinds include canonical memory, canonical persona, direct overlay write, and direct file write.

## Review

Supported review decisions:

- `approved_for_later_promotion`
- `rejected`
- `no_action`
- `needs_more_info`
- `archive`
- `error`

`approved_for_later_promotion` is not immediate promotion. It records only that a later controlled workflow may consider the candidate.

`no_action` is valid and records that no promotion action should be taken.

## CLI

```powershell
chanta-cli promotion candidate-from-envelope <envelope_id> --target memory_candidate
chanta-cli promotion candidate-from-envelope --envelope-json-file envelope.json --target memory_candidate
chanta-cli promotion list
chanta-cli promotion show <candidate_id>
chanta-cli promotion review <candidate_id> --decision no_action
```

The CLI emits summaries only. It does not perform canonical promotion.

## Future Work

- workspace read summarization pipeline;
- workbench pending review UI;
- actual controlled promotion in a later version, if ever enabled.
