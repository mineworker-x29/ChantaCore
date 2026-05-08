from chanta_core.session import (
    ChatSessionContextPolicy,
    SessionContextProjection,
    SessionPromptRenderResult,
    new_session_context_policy_id,
    new_session_context_projection_id,
    new_session_prompt_render_id,
)
from chanta_core.utility.time import utc_now_iso


def test_session_context_policy_to_dict_and_id_prefix() -> None:
    policy = ChatSessionContextPolicy(
        policy_id=new_session_context_policy_id(),
        policy_name="recent",
        max_turns=8,
        max_messages=16,
        max_chars=12000,
        include_user_messages=True,
        include_assistant_messages=True,
        include_system_messages=False,
        include_tool_messages=False,
        strategy="recent_only",
        status="active",
        created_at=utc_now_iso(),
        policy_attrs={"canonical": False},
    )

    data = policy.to_dict()
    assert data["policy_id"].startswith("session_context_policy:")
    assert data["max_messages"] == 16
    assert data["include_tool_messages"] is False


def test_session_context_projection_to_dict_is_non_canonical() -> None:
    projection = SessionContextProjection(
        projection_id=new_session_context_projection_id(),
        session_id="session:one",
        policy_id="session_context_policy:one",
        source_turn_ids=["conversation_turn:one"],
        source_message_ids=["message:one"],
        rendered_messages=[
            {
                "role": "user",
                "content": "hello",
                "message_id": "message:one",
                "turn_id": "conversation_turn:one",
            }
        ],
        total_messages=1,
        total_chars=5,
        truncated=False,
        truncation_reason=None,
        created_at=utc_now_iso(),
        projection_attrs={},
    )

    data = projection.to_dict()
    assert data["projection_id"].startswith("session_context_projection:")
    assert data["projection_attrs"]["canonical"] is False
    assert data["rendered_messages"][0]["content"] == "hello"


def test_session_prompt_render_result_to_dict() -> None:
    result = SessionPromptRenderResult(
        render_id=new_session_prompt_render_id(),
        projection_id="session_context_projection:one",
        messages=[{"role": "user", "content": "hello"}],
        system_prompt_included=False,
        capability_profile_included=False,
        created_at=utc_now_iso(),
        render_attrs={"canonical": False},
    )

    data = result.to_dict()
    assert data["render_id"].startswith("session_prompt_render:")
    assert data["messages"] == [{"role": "user", "content": "hello"}]
