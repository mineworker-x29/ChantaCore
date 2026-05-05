# ChantaCore v0.9.3 Restore Notes

ChantaCore v0.9.3 strengthens `ContextCollapseLayer` with deterministic reference projection.

Collapse is not semantic summarization. It does not call an LLM, does not create a learned summary, and does not delete or mutate OCEL, PIG, tool, report, worker, scheduler, edit, or patch stores. Collapse only changes the prompt-facing `ContextBlock` projection.

The release adds:

- `ContextReference`
- `ContextCollapsePolicy`
- `CollapsedContextManifest`
- `collapsed_context` prompt block rendering
- deterministic projection of collapsed/dropped blocks into compact references

When context pressure removes blocks from the prompt projection, the pipeline can preserve a compact manifest block that records type counts and source references. Raw content remains in source stores and is not injected into the prompt through the collapsed manifest.

`AutoCompactLayer` remains disabled by default. LLM-based semantic compaction is still not implemented.

Future work:

- semantic collapse
- auto-compact
- tokenizer-based budget
- learned reference ranking
- subagent context isolation
