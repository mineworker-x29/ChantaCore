# ChantaCore v0.6.6 Restore Notes

Version name: ChantaCore v0.6.6 - Variant-Aware Decision Tightening

## Scope

This version hardens deterministic trace-informed decision guidance. It is not self-improvement.

ChantaCore still does not modify source code, rewrite prompts, rewrite skill definitions, promote policies automatically, use learned ranking, use RL/bandits, or call an LLM for routing.

## OCPX Variants

OCPX now computes lightweight `OCPXVariantSummary` objects. These summaries use activity sequence based variant keys and aggregate trace count, success count, failure count, skill ids, and example process instance ids.

This is not full process mining variant discovery and does not add OCPA/pm4py dependencies.

## Variant-Aware PIG Guidance

PIG can create advisory `PIGGuidance` from variant summaries:

- failure-prone variants bias toward `skill:inspect_ocel_recent`
- trace-oriented variants bias toward `skill:summarize_process_trace`
- clean successful variants do not receive strong guidance
- human PI with variant evidence remains advisory and confidence-capped

Guidance remains suggest/bias only. It is not a gate, deny rule, or hard policy.

## Decision Tightening

`DecisionPolicy` controls deterministic routing behavior:

- minimum guidance confidence
- maximum guidance boost per skill
- fallback skill
- deterministic tie-break order

`DecisionScorer` now reports applied guidance, ignored guidance, capped skills, boost by skill, tie-break diagnostics, and fallback diagnostics.

Explicit skill ids still override guidance.

## Guardrails

No `process_intelligence`, `pi`, or `intelligence` package is introduced. No learned ranking model, bandit/RL, automatic policy promotion, tool dispatch, permission gate, or worker queue is implemented.
