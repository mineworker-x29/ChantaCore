# ChantaCore v0.10.0 Restore Notes

ChantaCore v0.10.0 adds an OCEL-native session and message substrate.

## Scope

- `AgentSession`, `ConversationTurn`, and `SessionMessage` model the runtime conversation substrate.
- `SessionService` records session, turn, and message lifecycle facts as OCEL event/object/relation records.
- OCEL object types now actively include `session`, `conversation_turn`, and `message`.
- User and assistant messages are represented as message objects and lifecycle events:
  - `session_started`
  - `session_closed`
  - `conversation_turn_started`
  - `user_message_received`
  - `assistant_message_emitted`
  - `message_attached_to_turn`
  - `process_instance_attached_to_turn`
  - `conversation_turn_completed`
  - `conversation_turn_failed`
- `AgentRuntime` starts a session turn, records user and assistant messages, completes the turn, and attaches the process instance id when available.
- `session_messages_to_history_entries` adapts `SessionMessage` values into prompt-facing `ContextHistoryEntry` values.

## Persistence Rule

Session persistence is OCEL-based. JSONL transcript storage was not introduced as canonical persistence. Existing trace/raw mirrors remain debug/export conveniences, not the session/message source of truth.

## Future Work

- OCEL-native memory.
- Materialized Markdown views.
- Hook lifecycle.
- Session resume/fork.
- External artifact storage for full message content.
