# ChantaCore Legacy JSONL Boundary

ChantaCore v0.10.x to v0.11.x treats the PI substrate canonical source as OCEL
event/object/relation records.

Current legacy JSONL locations, including worker, scheduler, and editing stores,
are operational runtime stores, queue/debug stores, or compatibility stores.
They are not canonical persistence for the v0.10.x to v0.11.x PI substrate,
verification substrate, or process outcome evaluation substrate.

Markdown materialized views remain human-readable output only. Edits to Markdown
views do not update canonical OCEL state.

Future work should migrate or explicitly retire legacy JSONL operational stores
where the architecture requires full OCEL-native persistence.
