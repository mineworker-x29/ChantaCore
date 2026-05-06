# ChantaCore v0.11.2 Restore Notes

ChantaCore v0.11.2 adds OCEL-native process outcome evaluation.

The outcome substrate introduces `ProcessOutcomeContract`, `ProcessOutcomeCriterion`,
`ProcessOutcomeTarget`, `ProcessOutcomeSignal`, and `ProcessOutcomeEvaluation`.
Each is persisted as an OCEL object, with lifecycle events for contract,
criterion, target, signal, and evaluation records.

Outcome evaluation consumes existing `VerificationResult` records and the evidence
references carried by those results. The evaluation policy is deterministic:
it counts passed, failed, inconclusive, skipped, and error verification results;
calculates pass rate, evidence coverage, score, and confidence; and then assigns
an outcome status from those values and the configured thresholds.

Default strict thresholds are:

- `min_required_pass_rate = 1.0`
- `min_evidence_coverage = 1.0`

No verification result list produces `inconclusive`. All skipped results produce
`skipped`. Error-only results produce `error`. Failed verification results produce
`failed`. Passed results that do not meet strict thresholds produce
`partial_success`.

This version does not enforce permissions. It does not block tools, mutate tool
inputs or outputs, mutate runtime behavior, auto-correct process execution, call
an LLM judge, execute shell commands, call network services, promote memory, or
update policy. It does not introduce a canonical JSONL outcome store. Markdown
remains a human-readable materialized view only.

Future work:

- v0.12.x permission scope, grant, and sandbox layers
- later recommendation and policy feedback loops
- deeper PIG/OCPX outcome analysis
