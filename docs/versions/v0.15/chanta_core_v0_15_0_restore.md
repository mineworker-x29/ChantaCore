# ChantaCore v0.15.0 Restore Notes

Version name: ChantaCore v0.15.0 - OCEL-native Chat Context Projection

## Scope

v0.15.0 adds bounded same-session chat context projection for the Default Agent chat path.

The canonical records remain the OCEL session, conversation turn, and message objects/events. A `SessionContextProjection` is a non-canonical prompt read-model generated from those records so the REPL can include recent prior user/assistant turns in the next LLM call.

## Added Runtime Pieces

- `SessionContextPolicy`
- `SessionContextProjection`
- `SessionPromptRenderResult`
- `SessionContextAssembler`
- prompt rendering from projection to OpenAI-compatible message lists
- `skill:llm_chat` support for either prompt-only or pre-rendered message-list input
- ChatService / AgentRuntime integration for bounded recent same-session context

Default policy:

- `max_turns=8`
- `max_messages=16`
- `max_chars=12000`
- include user and assistant messages
- exclude system and tool messages by default
- strategy: `recent_only`

## OCEL Shape

The patch records lightweight OCEL objects/events for observability:

- `session_context_policy`
- `session_context_projection`
- `session_prompt_render`
- `session_context_policy_registered`
- `session_context_projection_created`
- `session_context_projection_truncated`
- `session_prompt_rendered`

These projection records are read-model observability artifacts. They are not canonical conversation storage.

## Boundaries

v0.15.0 does not introduce a canonical JSONL transcript.

It does not use terminal scrollback as source of truth.

It does not add:

- workspace file read
- shell execution
- network calls
- MCP connection
- plugin loading
- ToolDispatcher mutation
- permission enforcement
- external capability activation
- unbounded full session history injection

Hidden model reasoning content is not emitted as assistant output.

## REPL Behavior

The REPL should now feel like a bounded same-session conversation instead of isolated single-turn calls. Previous user/assistant messages from the same OCEL session can be projected into the next prompt, subject to policy limits.

Different sessions are not projected into the current session prompt.

The current user message is excluded from the projection and appended once during prompt rendering to avoid duplicate prompt entries.

## Future Work

- summarized long-context compaction
- explicit workspace read skills
- SessionContextPolicy configuration surface
- Soul identity/persona loading
- reviewed tool and workspace capability activation through explicit gates
