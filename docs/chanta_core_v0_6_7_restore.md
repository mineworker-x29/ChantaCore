# ChantaCore v0.6.7 Restore Notes

ChantaCore v0.6.7 adds lightweight runtime self-conformance checking.

This is not formal process mining conformance checking. It does not implement
Petri net discovery, BPMN discovery, object-centric Petri net conformance, token
replay, alignment-based conformance, or fitness / precision / generalization
metrics.

The conformance implementation lives under PIG:

- `src/chanta_core/pig/conformance.py`
- `PIGConformanceIssue`
- `PIGConformanceReport`
- `PIGConformanceService`

The service reads `OCPXProcessView` and checks ChantaCore ProcessRunLoop runtime
trace contracts:

- expected activity fragments
- expected event-object relation coverage
- outcome object visibility on completed traces
- error object visibility on failed traces
- basic activity order sanity
- advisory decision-contract consistency when `decide_skill` exists

The result is diagnostic only. It does not mutate OCELStore, PIGGuidance,
DecisionService, SkillRegistry, ProcessRunPolicy, or runtime execution behavior.
It does not block process execution.

`PIGContext` may include a concise conformance summary through
`conformance_report`. `PIGFeedbackService` includes conformance by default for
PIGContext construction and can exclude it with `include_conformance=False`.

The built-in skill `skill:check_self_conformance` runs the same advisory check
without LLM or external tools.

Architecture guardrails remain unchanged:

- no `src/chanta_core/process_intelligence`
- no `src/chanta_core/pi`
- no `src/chanta_core/intelligence`
- PIG remains the process intelligence layer
- OCPX remains the lightweight computation/read model layer
- OCEL remains persistence and ingestion

Future work:

- no Petri net conformance yet
- no alignments yet
- no token replay yet
- no fitness / precision / generalization metrics yet
- no automatic policy enforcement
- no worker queue
- no tool dispatch
