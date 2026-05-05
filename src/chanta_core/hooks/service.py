from __future__ import annotations

from dataclasses import replace
from typing import Any
from uuid import uuid4

from chanta_core.hooks.errors import HookPolicyError
from chanta_core.hooks.ids import (
    new_hook_definition_id,
    new_hook_invocation_id,
    new_hook_policy_id,
    new_hook_result_id,
)
from chanta_core.hooks.lifecycle import normalize_lifecycle_stage
from chanta_core.hooks.models import (
    FORBIDDEN_HOOK_OUTCOMES,
    HookDefinition,
    HookInvocation,
    HookPolicy,
    HookResult,
    hash_payload,
    summarize_payload,
)
from chanta_core.hooks.registry import HookRegistry
from chanta_core.ocel.models import OCELObject, OCELRecord, OCELEvent, OCELRelation
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso


LIFECYCLE_SPECIFIC_EVENTS = {
    "pre_process_run": "pre_process_run_hook_invoked",
    "post_process_run": "post_process_run_hook_invoked",
    "pre_tool_dispatch": "pre_tool_dispatch_hook_invoked",
    "post_tool_dispatch": "post_tool_dispatch_hook_invoked",
    "pre_materialized_view_refresh": "pre_materialized_view_refresh_hook_invoked",
    "post_materialized_view_refresh": "post_materialized_view_refresh_hook_invoked",
    "on_error": "on_error_hook_invoked",
}


class HookLifecycleService:
    def __init__(
        self,
        *,
        trace_service: TraceService | None = None,
        registry: HookRegistry | None = None,
    ) -> None:
        self.trace_service = trace_service or TraceService()
        self.registry = registry or HookRegistry()

    def register_hook_definition(
        self,
        *,
        hook_name: str,
        hook_type: str,
        lifecycle_stage: str,
        description: str | None = None,
        status: str = "active",
        priority: int | None = None,
        scope: str | None = None,
        source_kind: str | None = None,
        handler_ref: str | None = None,
        hook_attrs: dict[str, Any] | None = None,
    ) -> HookDefinition:
        now = utc_now_iso()
        hook = HookDefinition(
            hook_id=new_hook_definition_id(),
            hook_name=hook_name,
            hook_type=hook_type,
            lifecycle_stage=normalize_lifecycle_stage(lifecycle_stage),
            description=description,
            status=status,
            priority=priority,
            scope=scope,
            source_kind=source_kind,
            handler_ref=handler_ref,
            created_at=now,
            updated_at=now,
            hook_attrs=dict(hook_attrs or {}),
        )
        self.registry.register(hook)
        self._record_hook_event(
            "hook_definition_registered",
            hook=hook,
            event_attrs={},
            event_relations=[("hook_definition_object", hook.hook_id)],
            object_relations=[],
        )
        return hook

    def update_hook_definition(
        self,
        *,
        definition: HookDefinition,
        description: str | None = None,
        status: str | None = None,
        priority: int | None = None,
        scope: str | None = None,
        hook_attrs: dict[str, Any] | None = None,
    ) -> HookDefinition:
        updated = replace(
            definition,
            description=definition.description if description is None else description,
            status=definition.status if status is None else status,
            priority=definition.priority if priority is None else priority,
            scope=definition.scope if scope is None else scope,
            updated_at=utc_now_iso(),
            hook_attrs={**definition.hook_attrs, **dict(hook_attrs or {})},
        )
        self.registry.register(updated)
        self._record_hook_event(
            "hook_definition_updated",
            hook=updated,
            event_attrs={"updated_fields": sorted(dict(hook_attrs or {}).keys())},
            event_relations=[("hook_definition_object", updated.hook_id)],
            object_relations=[],
        )
        return updated

    def deprecate_hook_definition(
        self,
        *,
        definition: HookDefinition,
        reason: str | None = None,
    ) -> HookDefinition:
        deprecated = replace(definition, status="deprecated", updated_at=utc_now_iso())
        self.registry.register(deprecated)
        self._record_hook_event(
            "hook_definition_deprecated",
            hook=deprecated,
            event_attrs={"reason": reason},
            event_relations=[("hook_definition_object", deprecated.hook_id)],
            object_relations=[],
        )
        return deprecated

    def register_hook_policy(
        self,
        *,
        hook_id: str,
        policy_kind: str = "observe_only",
        status: str = "active",
        scope: str | None = None,
        policy_attrs: dict[str, Any] | None = None,
    ) -> HookPolicy:
        if policy_kind in FORBIDDEN_HOOK_OUTCOMES:
            raise HookPolicyError(f"Forbidden hook policy kind: {policy_kind}")
        now = utc_now_iso()
        policy = HookPolicy(
            policy_id=new_hook_policy_id(),
            hook_id=hook_id,
            policy_kind=policy_kind,
            status=status,
            scope=scope,
            created_at=now,
            updated_at=now,
            policy_attrs=dict(policy_attrs or {}),
        )
        hook = self.registry.get_hook(hook_id)
        self._record_hook_event(
            "hook_policy_registered",
            hook=hook,
            policy=policy,
            event_attrs={"hook_id": hook_id, "policy_kind": policy_kind},
            event_relations=[
                ("hook_policy_object", policy.policy_id),
                ("hook_definition_object", hook_id),
            ],
            object_relations=[(policy.policy_id, hook_id, "applies_to_hook")],
        )
        return policy

    def match_hooks(
        self,
        *,
        lifecycle_stage: str,
        session_id: str | None = None,
        turn_id: str | None = None,
        process_instance_id: str | None = None,
        triggering_event_id: str | None = None,
        match_attrs: dict[str, Any] | None = None,
    ) -> list[HookDefinition]:
        stage = normalize_lifecycle_stage(lifecycle_stage)
        hooks = [hook for hook in self.registry.find_by_stage(stage) if hook.status == "active"]
        for hook in hooks:
            self._record_hook_event(
                "hook_matched",
                hook=hook,
                event_attrs={
                    "lifecycle_stage": stage,
                    "triggering_event_id": triggering_event_id,
                    **dict(match_attrs or {}),
                },
                event_relations=self._context_event_relations(
                    hook=hook,
                    invocation=None,
                    result=None,
                    session_id=session_id,
                    turn_id=turn_id,
                    process_instance_id=process_instance_id,
                ),
                object_relations=self._context_object_relations(
                    invocation_id=None,
                    hook_id=hook.hook_id,
                    session_id=session_id,
                    turn_id=turn_id,
                    process_instance_id=process_instance_id,
                ),
            )
        return hooks

    def record_hook_invocation(
        self,
        *,
        hook: HookDefinition,
        lifecycle_stage: str | None = None,
        status: str = "invoked",
        session_id: str | None = None,
        turn_id: str | None = None,
        process_instance_id: str | None = None,
        triggering_event_id: str | None = None,
        input_payload: dict[str, Any] | None = None,
        invocation_attrs: dict[str, Any] | None = None,
    ) -> HookInvocation:
        stage = normalize_lifecycle_stage(lifecycle_stage or hook.lifecycle_stage)
        payload = input_payload or {}
        invocation = HookInvocation(
            invocation_id=new_hook_invocation_id(),
            hook_id=hook.hook_id,
            lifecycle_stage=stage,
            status=status,
            started_at=utc_now_iso(),
            completed_at=None,
            session_id=session_id,
            turn_id=turn_id,
            process_instance_id=process_instance_id,
            triggering_event_id=triggering_event_id,
            input_summary=summarize_payload(payload) if payload else None,
            input_hash=hash_payload(payload) if payload else None,
            invocation_attrs=dict(invocation_attrs or {}),
        )
        self._record_invocation_event("hook_invoked", hook, invocation)
        specific_event = LIFECYCLE_SPECIFIC_EVENTS.get(stage)
        if specific_event:
            self._record_invocation_event(specific_event, hook, invocation)
        return invocation

    def complete_hook_invocation(
        self,
        *,
        invocation: HookInvocation,
        output_payload: dict[str, Any] | None = None,
        result_attrs: dict[str, Any] | None = None,
    ) -> HookResult:
        payload = output_payload or {"observed": True}
        result = HookResult(
            result_id=new_hook_result_id(),
            invocation_id=invocation.invocation_id,
            hook_id=invocation.hook_id,
            status="completed",
            result_kind="observed",
            output_summary=summarize_payload(payload),
            output_hash=hash_payload(payload),
            error_message=None,
            created_at=utc_now_iso(),
            result_attrs=dict(result_attrs or {}),
        )
        self._record_result_event("hook_result_recorded", invocation, result)
        self._record_result_event("hook_completed", invocation, result)
        return result

    def fail_hook_invocation(
        self,
        *,
        invocation: HookInvocation,
        error_message: str,
        result_attrs: dict[str, Any] | None = None,
    ) -> HookResult:
        result = HookResult(
            result_id=new_hook_result_id(),
            invocation_id=invocation.invocation_id,
            hook_id=invocation.hook_id,
            status="failed",
            result_kind="failed",
            output_summary=None,
            output_hash=None,
            error_message=error_message,
            created_at=utc_now_iso(),
            result_attrs=dict(result_attrs or {}),
        )
        self._record_result_event("hook_result_recorded", invocation, result)
        self._record_result_event("hook_failed", invocation, result)
        return result

    def skip_hook_invocation(
        self,
        *,
        hook: HookDefinition,
        lifecycle_stage: str | None = None,
        reason: str | None = None,
        session_id: str | None = None,
        turn_id: str | None = None,
        process_instance_id: str | None = None,
    ) -> HookResult:
        invocation = self.record_hook_invocation(
            hook=hook,
            lifecycle_stage=lifecycle_stage,
            status="skipped",
            session_id=session_id,
            turn_id=turn_id,
            process_instance_id=process_instance_id,
            input_payload={"reason": reason},
        )
        result = HookResult(
            result_id=new_hook_result_id(),
            invocation_id=invocation.invocation_id,
            hook_id=hook.hook_id,
            status="skipped",
            result_kind="skipped",
            output_summary=summarize_payload({"reason": reason}),
            output_hash=hash_payload({"reason": reason}),
            error_message=None,
            created_at=utc_now_iso(),
            result_attrs={"reason": reason},
        )
        self._record_result_event("hook_result_recorded", invocation, result)
        self._record_result_event("hook_skipped", invocation, result)
        return result

    def observe_lifecycle_point(
        self,
        *,
        lifecycle_stage: str,
        session_id: str | None = None,
        turn_id: str | None = None,
        process_instance_id: str | None = None,
        triggering_event_id: str | None = None,
        input_payload: dict[str, Any] | None = None,
        observation_attrs: dict[str, Any] | None = None,
    ) -> list[HookInvocation]:
        hooks = self.match_hooks(
            lifecycle_stage=lifecycle_stage,
            session_id=session_id,
            turn_id=turn_id,
            process_instance_id=process_instance_id,
            triggering_event_id=triggering_event_id,
            match_attrs=observation_attrs,
        )
        invocations: list[HookInvocation] = []
        for hook in hooks:
            invocation = self.record_hook_invocation(
                hook=hook,
                lifecycle_stage=lifecycle_stage,
                session_id=session_id,
                turn_id=turn_id,
                process_instance_id=process_instance_id,
                triggering_event_id=triggering_event_id,
                input_payload=input_payload,
                invocation_attrs=observation_attrs,
            )
            self.complete_hook_invocation(
                invocation=invocation,
                output_payload={"result_kind": "noop", "observed": True},
                result_attrs={"noop": True},
            )
            invocations.append(invocation)
        return invocations

    def _record_invocation_event(
        self,
        event_activity: str,
        hook: HookDefinition,
        invocation: HookInvocation,
    ) -> None:
        self._record_hook_event(
            event_activity,
            hook=hook,
            invocation=invocation,
            event_attrs={"lifecycle_stage": invocation.lifecycle_stage, "status": invocation.status},
            event_relations=self._context_event_relations(
                hook=hook,
                invocation=invocation,
                result=None,
                session_id=invocation.session_id,
                turn_id=invocation.turn_id,
                process_instance_id=invocation.process_instance_id,
            ),
            object_relations=self._context_object_relations(
                invocation_id=invocation.invocation_id,
                hook_id=hook.hook_id,
                session_id=invocation.session_id,
                turn_id=invocation.turn_id,
                process_instance_id=invocation.process_instance_id,
            ),
        )

    def _record_result_event(
        self,
        event_activity: str,
        invocation: HookInvocation,
        result: HookResult,
    ) -> None:
        hook = self.registry.get_hook(invocation.hook_id)
        self._record_hook_event(
            event_activity,
            hook=hook,
            invocation=invocation,
            result=result,
            event_attrs={
                "status": result.status,
                "result_kind": result.result_kind,
                "lifecycle_stage": invocation.lifecycle_stage,
            },
            event_relations=self._context_event_relations(
                hook=hook,
                invocation=invocation,
                result=result,
                session_id=invocation.session_id,
                turn_id=invocation.turn_id,
                process_instance_id=invocation.process_instance_id,
            ),
            object_relations=[
                (result.result_id, invocation.invocation_id, "result_of"),
                *self._context_object_relations(
                    invocation_id=invocation.invocation_id,
                    hook_id=invocation.hook_id,
                    session_id=invocation.session_id,
                    turn_id=invocation.turn_id,
                    process_instance_id=invocation.process_instance_id,
                ),
            ],
        )

    def _record_hook_event(
        self,
        event_activity: str,
        *,
        hook: HookDefinition | None = None,
        invocation: HookInvocation | None = None,
        result: HookResult | None = None,
        policy: HookPolicy | None = None,
        event_attrs: dict[str, Any],
        event_relations: list[tuple[str, str]],
        object_relations: list[tuple[str, str, str]],
    ) -> None:
        event = OCELEvent(
            event_id=f"evt:{uuid4()}",
            event_activity=event_activity,
            event_timestamp=utc_now_iso(),
            event_attrs={
                **event_attrs,
                "runtime_event_type": event_activity,
                "source_runtime": "chanta_core",
                "observability_only": True,
                "enforcement_enabled": False,
            },
        )
        objects: list[OCELObject] = []
        if hook is not None:
            objects.append(self._hook_object(hook))
        elif any(qualifier == "hook_definition_object" for qualifier, _ in event_relations):
            hook_id = next(object_id for qualifier, object_id in event_relations if qualifier == "hook_definition_object")
            objects.append(self._hook_placeholder(hook_id))
        if invocation is not None:
            objects.append(self._invocation_object(invocation))
        if result is not None:
            objects.append(self._result_object(result))
        if policy is not None:
            objects.append(self._policy_object(policy))
        objects.extend(self._context_objects(event_relations))
        relations = [
            OCELRelation.event_object(
                event_id=event.event_id,
                object_id=object_id,
                qualifier=qualifier,
            )
            for qualifier, object_id in event_relations
            if object_id
        ]
        relations.extend(
            OCELRelation.object_object(
                source_object_id=source,
                target_object_id=target,
                qualifier=qualifier,
            )
            for source, target, qualifier in object_relations
            if source and target
        )
        self.trace_service.record_session_ocel_record(
            OCELRecord(event=event, objects=objects, relations=relations)
        )

    @staticmethod
    def _context_event_relations(
        *,
        hook: HookDefinition | None,
        invocation: HookInvocation | None,
        result: HookResult | None,
        session_id: str | None,
        turn_id: str | None,
        process_instance_id: str | None,
    ) -> list[tuple[str, str]]:
        relations: list[tuple[str, str]] = []
        hook_id = hook.hook_id if hook is not None else invocation.hook_id if invocation is not None else None
        if hook_id:
            relations.append(("hook_definition_object", hook_id))
        if invocation is not None:
            relations.append(("hook_invocation_object", invocation.invocation_id))
        if result is not None:
            relations.append(("hook_result_object", result.result_id))
        if session_id:
            relations.append(("session_context", HookLifecycleService._session_object_id(session_id)))
        if turn_id:
            relations.append(("turn_context", turn_id))
        if process_instance_id:
            relations.append(("process_context", process_instance_id))
        return relations

    @staticmethod
    def _context_object_relations(
        *,
        invocation_id: str | None,
        hook_id: str,
        session_id: str | None,
        turn_id: str | None,
        process_instance_id: str | None,
    ) -> list[tuple[str, str, str]]:
        relations: list[tuple[str, str, str]] = []
        if invocation_id:
            relations.append((invocation_id, hook_id, "invokes"))
            if session_id:
                relations.append((invocation_id, HookLifecycleService._session_object_id(session_id), "belongs_to_session"))
            if turn_id:
                relations.append((invocation_id, turn_id, "belongs_to_turn"))
            if process_instance_id:
                relations.append((invocation_id, process_instance_id, "observes_process_instance"))
        return relations

    @staticmethod
    def _context_objects(event_relations: list[tuple[str, str]]) -> list[OCELObject]:
        objects: list[OCELObject] = []
        for qualifier, object_id in event_relations:
            if qualifier == "session_context":
                objects.append(
                    OCELObject(
                        object_id=object_id,
                        object_type="session",
                        object_attrs={"object_key": object_id, "display_name": object_id},
                    )
                )
            if qualifier == "turn_context":
                objects.append(
                    OCELObject(
                        object_id=object_id,
                        object_type="conversation_turn",
                        object_attrs={"object_key": object_id, "display_name": object_id},
                    )
                )
            if qualifier == "process_context":
                objects.append(
                    OCELObject(
                        object_id=object_id,
                        object_type="process_instance",
                        object_attrs={"object_key": object_id, "display_name": object_id},
                    )
                )
        return objects

    @staticmethod
    def _hook_object(hook: HookDefinition) -> OCELObject:
        return OCELObject(
            object_id=hook.hook_id,
            object_type="hook_definition",
            object_attrs={**hook.to_dict(), "object_key": hook.hook_id, "display_name": hook.hook_name},
        )

    @staticmethod
    def _hook_placeholder(hook_id: str) -> OCELObject:
        return OCELObject(
            object_id=hook_id,
            object_type="hook_definition",
            object_attrs={"object_key": hook_id, "display_name": hook_id},
        )

    @staticmethod
    def _invocation_object(invocation: HookInvocation) -> OCELObject:
        return OCELObject(
            object_id=invocation.invocation_id,
            object_type="hook_invocation",
            object_attrs={**invocation.to_dict(), "object_key": invocation.invocation_id, "display_name": invocation.lifecycle_stage},
        )

    @staticmethod
    def _result_object(result: HookResult) -> OCELObject:
        return OCELObject(
            object_id=result.result_id,
            object_type="hook_result",
            object_attrs={**result.to_dict(), "object_key": result.result_id, "display_name": result.result_kind},
        )

    @staticmethod
    def _policy_object(policy: HookPolicy) -> OCELObject:
        return OCELObject(
            object_id=policy.policy_id,
            object_type="hook_policy",
            object_attrs={**policy.to_dict(), "object_key": policy.policy_id, "display_name": policy.policy_kind},
        )

    @staticmethod
    def _session_object_id(session_id: str) -> str:
        return session_id if session_id.startswith("session:") else f"session:{session_id}"
