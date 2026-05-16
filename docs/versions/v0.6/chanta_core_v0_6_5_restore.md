# ChantaCore v0.6.5 Restore Notes

Version name: ChantaCore v0.6.5 - Trace-Informed Decision Guidance

## Scope

This version adds deterministic trace-informed decision guidance. It is not self-improvement.

ChantaCore does not modify source code, rewrite prompt templates, rewrite skill definitions, or promote human PI into hard policy in this version.

## Architecture

The guidance path is:

OCELStore -> OCPXEngine -> PIGContext / PIArtifact -> PIGGuidance -> DecisionService -> ProcessRunLoop -> SkillExecutor

PIG owns guidance generation. Runtime decision code lives under `src/chanta_core/runtime/decision` because it decides current runtime behavior.

## Guidance

`PIGGuidance` is advisory. It can suggest or bias a skill score, but it does not gate, deny, or force execution.

Initial guidance rules cover:

- recent failures -> inspect OCEL first
- low relation coverage -> inspect OCEL
- trace/process/history/variant context -> summarize process trace
- PIArtifact `suggested_skill_id` -> advisory skill bias

Human PI remains advisory and confidence-limited.

## DecisionService

`DecisionService` is deterministic and does not call an LLM. It selects skills by:

- explicit skill id first
- deterministic user input heuristics
- advisory PIGGuidance score bias
- fallback to `skill:llm_chat`

## Guardrails

No `process_intelligence`, `pi`, or `intelligence` package is introduced. No full OCPA/OPeRA algorithms, learned ranking model, bandit/RL, permission gate, tool dispatch, worker queue, or automatic policy promotion is implemented.
