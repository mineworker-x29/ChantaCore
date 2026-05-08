from chanta_core.session import SessionContextProjection, render_projection_to_prompt_result
from chanta_core.utility.time import utc_now_iso


def _projection() -> SessionContextProjection:
    return SessionContextProjection(
        projection_id="session_context_projection:test",
        session_id="session:test",
        policy_id="session_context_policy:test",
        source_turn_ids=["conversation_turn:test"],
        source_message_ids=["message:one", "message:two"],
        rendered_messages=[
            {
                "role": "user",
                "content": "previous question",
                "message_id": "message:one",
                "turn_id": "conversation_turn:test",
            },
            {
                "role": "assistant",
                "content": "previous answer",
                "message_id": "message:two",
                "turn_id": "conversation_turn:test",
                "reasoning_content": "hidden",
            },
        ],
        total_messages=2,
        total_chars=33,
        truncated=False,
        truncation_reason=None,
        created_at=utc_now_iso(),
        projection_attrs={"canonical": False},
    )


def test_prompt_renderer_includes_system_projection_and_current_user() -> None:
    result = render_projection_to_prompt_result(
        projection=_projection(),
        system_prompt="system prompt",
        capability_profile_block="capability block",
        current_user_message="current question",
    )

    assert result.system_prompt_included is True
    assert result.capability_profile_included is True
    assert [message["role"] for message in result.messages] == [
        "system",
        "system",
        "user",
        "assistant",
        "user",
    ]
    assert result.messages[-1]["content"] == "current question"
    assert all("reasoning_content" not in message for message in result.messages)


def test_prompt_renderer_avoids_duplicate_current_user_message() -> None:
    projection = _projection()
    duplicate_projection = SessionContextProjection(
        **{
            **projection.to_dict(),
            "rendered_messages": [
                *projection.rendered_messages,
                {"role": "user", "content": "current question"},
            ],
            "total_messages": 3,
        }
    )

    result = render_projection_to_prompt_result(
        projection=duplicate_projection,
        current_user_message="current question",
        avoid_duplicate_current_message=True,
    )

    assert [message["content"] for message in result.messages].count("current question") == 1
