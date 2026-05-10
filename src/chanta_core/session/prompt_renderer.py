from __future__ import annotations

from typing import Any

from chanta_core.session.context_projection import (
    SessionContextProjection,
    SessionPromptRenderResult,
)
from chanta_core.session.ids import new_session_prompt_render_id
from chanta_core.utility.time import utc_now_iso


def render_projection_to_llm_messages(
    *,
    projection: SessionContextProjection,
    system_prompt: str | None = None,
    persona_projection_block: str | None = None,
    personal_prompt_activation_block: str | None = None,
    capability_profile_block: str | None = None,
    current_user_message: str | None = None,
    avoid_duplicate_current_message: bool = True,
) -> list[dict[str, str]]:
    result = render_projection_to_prompt_result(
        projection=projection,
        system_prompt=system_prompt,
        persona_projection_block=persona_projection_block,
        personal_prompt_activation_block=personal_prompt_activation_block,
        capability_profile_block=capability_profile_block,
        current_user_message=current_user_message,
        avoid_duplicate_current_message=avoid_duplicate_current_message,
    )
    return [{"role": item["role"], "content": item["content"]} for item in result.messages]


def render_projection_to_prompt_result(
    *,
    projection: SessionContextProjection,
    system_prompt: str | None = None,
    persona_projection_block: str | None = None,
    personal_prompt_activation_block: str | None = None,
    capability_profile_block: str | None = None,
    current_user_message: str | None = None,
    avoid_duplicate_current_message: bool = True,
) -> SessionPromptRenderResult:
    messages: list[dict[str, Any]] = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    if persona_projection_block:
        messages.append({"role": "system", "content": persona_projection_block})
    if personal_prompt_activation_block:
        messages.append({"role": "system", "content": personal_prompt_activation_block})
    if capability_profile_block:
        messages.append({"role": "system", "content": capability_profile_block})
    for message in projection.rendered_messages:
        role = str(message.get("role") or "")
        content = str(message.get("content") or "")
        if role in {"user", "assistant", "system", "tool"} and content:
            messages.append({"role": role, "content": content})
    if current_user_message:
        duplicate = bool(
            avoid_duplicate_current_message
            and messages
            and messages[-1].get("role") == "user"
            and messages[-1].get("content") == current_user_message
        )
        if not duplicate:
            messages.append({"role": "user", "content": current_user_message})
    return SessionPromptRenderResult(
        render_id=new_session_prompt_render_id(),
        projection_id=projection.projection_id,
        messages=messages,
        system_prompt_included=bool(system_prompt),
        capability_profile_included=bool(capability_profile_block),
        created_at=utc_now_iso(),
        render_attrs={
            "hidden_reasoning_excluded": True,
            "scrollback_source": False,
            "personal_prompt_activation_included": bool(personal_prompt_activation_block),
        },
    )
