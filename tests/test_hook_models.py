import pytest

from chanta_core.hooks import (
    HookDefinition,
    HookPolicy,
    HookResult,
    hash_payload,
    new_hook_definition_id,
    new_hook_invocation_id,
    new_hook_policy_id,
    new_hook_result_id,
)
from chanta_core.hooks.errors import HookPolicyError, HookResultError
from chanta_core.hooks.models import HookInvocation


def test_hook_models_to_dict_and_hashes() -> None:
    definition = HookDefinition(
        hook_id=new_hook_definition_id(),
        hook_name="Observe process",
        hook_type="observer",
        lifecycle_stage="pre_process_run",
        description="Records lifecycle only",
        status="active",
        priority=10,
        scope="test",
        source_kind="test",
        handler_ref="metadata.only",
        created_at="2026-01-01T00:00:00Z",
        updated_at="2026-01-01T00:00:00Z",
        hook_attrs={"k": "v"},
    )
    invocation = HookInvocation(
        invocation_id=new_hook_invocation_id(),
        hook_id=definition.hook_id,
        lifecycle_stage="pre_process_run",
        status="invoked",
        started_at="2026-01-01T00:00:01Z",
        completed_at=None,
        session_id="session:test",
        turn_id="conversation_turn:test",
        process_instance_id="process_instance:test",
        triggering_event_id=None,
        input_summary="{}",
        input_hash=hash_payload({}),
        invocation_attrs={},
    )
    result = HookResult(
        result_id=new_hook_result_id(),
        invocation_id=invocation.invocation_id,
        hook_id=definition.hook_id,
        status="completed",
        result_kind="observed",
        output_summary="{}",
        output_hash=hash_payload({}),
        error_message=None,
        created_at="2026-01-01T00:00:02Z",
        result_attrs={},
    )
    policy = HookPolicy(
        policy_id=new_hook_policy_id(),
        hook_id=definition.hook_id,
        policy_kind="observe_only",
        status="active",
        scope=None,
        created_at="2026-01-01T00:00:03Z",
        updated_at="2026-01-01T00:00:03Z",
        policy_attrs={},
    )

    assert definition.to_dict()["handler_ref"] == "metadata.only"
    assert invocation.to_dict()["input_hash"] == hash_payload({})
    assert result.to_dict()["result_kind"] == "observed"
    assert policy.to_dict()["policy_kind"] == "observe_only"
    assert hash_payload({"b": 2, "a": 1}) == hash_payload({"a": 1, "b": 2})
    assert definition.hook_id.startswith("hook_definition:")
    assert invocation.invocation_id.startswith("hook_invocation:")
    assert result.result_id.startswith("hook_result:")
    assert policy.policy_id.startswith("hook_policy:")


def test_forbidden_hook_result_and_policy_kinds_rejected() -> None:
    with pytest.raises(HookResultError):
        HookResult(
            result_id="hook_result:test",
            invocation_id="hook_invocation:test",
            hook_id="hook_definition:test",
            status="completed",
            result_kind="block",
            output_summary=None,
            output_hash=None,
            error_message=None,
            created_at="2026-01-01T00:00:00Z",
        )
    with pytest.raises(HookPolicyError):
        HookPolicy(
            policy_id="hook_policy:test",
            hook_id="hook_definition:test",
            policy_kind="deny",
            status="active",
            scope=None,
            created_at="2026-01-01T00:00:00Z",
            updated_at="2026-01-01T00:00:00Z",
        )
