# ChantaCore v0.6.3 Restore Notes

Version name: ChantaCore v0.6.3 - PIGContext Feedback

## Scope

This version adds the PIGContext feedback pipeline:

OCELStore -> OCPXLoader / OCPXEngine -> PIGService -> PIGContext -> optional runtime context injection.

## Architecture

PIG remains the process intelligence layer. `PIGContext` lives in `src/chanta_core/pig/context.py`, and `PIGFeedbackService` lives in `src/chanta_core/pig/feedback.py`.

OCPX computes the lightweight process values used by PIGContext:

- activity sequence
- event activity counts
- object type counts
- relation coverage
- basic variant
- basic performance precursor fields

PIG contextualizes those values with guide, diagnostics, recommendations, and concise prompt-safe context text.

The forbidden process intelligence directories remain forbidden:

- `src/chanta_core/process_intelligence`
- `src/chanta_core/pi`
- `src/chanta_core/intelligence`

## Runtime Behavior

`ProcessContextAssembler` can accept an optional `pig_context`. When provided, it inserts `PIGContext.context_text` as a labeled system context block before the user request.

`ProcessRunPolicy.include_pig_context` defaults to `False`, so prompt inflation is avoided by default. When enabled, `ProcessRunLoop` builds PIGContext through `PIGFeedbackService` and passes it to skill execution context. Runtime PIGContext creation failures are non-fatal and skip injection.

## Future Work

Full OCPA algorithms are future work. Full OPeRA metrics are future work. This version does not implement process discovery, conformance checking, object-centric Petri nets, synchronization time, pooling time, lagging time, flow time, or full PIG recommendation learning.
