from __future__ import annotations

from dataclasses import replace
from typing import Any
from uuid import uuid4

from chanta_core.instructions.ids import (
    new_instruction_artifact_id,
    new_project_rule_id,
    new_user_preference_id,
)
from chanta_core.instructions.models import (
    InstructionArtifact,
    ProjectRule,
    UserPreference,
    hash_body,
    preview_body,
)
from chanta_core.ocel.models import OCELObject, OCELRecord, OCELEvent, OCELRelation
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso


class InstructionService:
    def __init__(self, *, trace_service: TraceService | None = None) -> None:
        self.trace_service = trace_service or TraceService()

    def register_instruction_artifact(
        self,
        *,
        instruction_type: str,
        title: str,
        body: str,
        status: str = "active",
        scope: str | None = None,
        priority: int | None = None,
        source_path: str | None = None,
        session_id: str | None = None,
        message_id: str | None = None,
        instruction_attrs: dict[str, Any] | None = None,
    ) -> InstructionArtifact:
        now = utc_now_iso()
        instruction = InstructionArtifact(
            instruction_id=new_instruction_artifact_id(),
            instruction_type=instruction_type,
            title=title,
            body=body,
            body_preview=preview_body(body),
            body_hash=hash_body(body),
            status=status,
            scope=scope,
            priority=priority,
            created_at=now,
            updated_at=now,
            source_path=source_path,
            instruction_attrs=dict(instruction_attrs or {}),
        )
        self._record_instruction_event(
            "instruction_artifact_registered",
            objects=[self._instruction_object(instruction)],
            event_relations=[
                ("instruction_object", instruction.instruction_id),
                *self._source_event_relations(session_id, message_id),
            ],
            object_relations=self._source_object_relations(
                instruction.instruction_id,
                session_id,
                message_id,
            ),
            event_attrs={"session_id": session_id, "message_id": message_id},
        )
        return instruction

    def revise_instruction_artifact(
        self,
        *,
        instruction: InstructionArtifact,
        new_body: str,
        reason: str | None = None,
        instruction_attrs: dict[str, Any] | None = None,
    ) -> InstructionArtifact:
        updated = replace(
            instruction,
            body=new_body,
            body_preview=preview_body(new_body),
            body_hash=hash_body(new_body),
            updated_at=utc_now_iso(),
            instruction_attrs={
                **instruction.instruction_attrs,
                **dict(instruction_attrs or {}),
            },
        )
        self._record_instruction_event(
            "instruction_artifact_revised",
            objects=[self._instruction_object(updated)],
            event_relations=[("instruction_object", updated.instruction_id)],
            object_relations=[],
            event_attrs={"reason": reason},
        )
        return updated

    def deprecate_instruction_artifact(
        self,
        *,
        instruction: InstructionArtifact,
        reason: str | None = None,
    ) -> InstructionArtifact:
        deprecated = replace(instruction, status="deprecated", updated_at=utc_now_iso())
        self._record_instruction_event(
            "instruction_artifact_deprecated",
            objects=[self._instruction_object(deprecated)],
            event_relations=[("instruction_object", deprecated.instruction_id)],
            object_relations=[],
            event_attrs={"reason": reason},
        )
        return deprecated

    def register_project_rule(
        self,
        *,
        rule_type: str,
        text: str,
        status: str = "active",
        priority: int | None = None,
        source_instruction_id: str | None = None,
        rule_attrs: dict[str, Any] | None = None,
    ) -> ProjectRule:
        now = utc_now_iso()
        rule = ProjectRule(
            rule_id=new_project_rule_id(),
            rule_type=rule_type,
            text=text,
            status=status,
            priority=priority,
            created_at=now,
            updated_at=now,
            source_instruction_id=source_instruction_id,
            rule_attrs=dict(rule_attrs or {}),
        )
        objects = [self._rule_object(rule)]
        event_relations = [("rule_object", rule.rule_id)]
        object_relations: list[tuple[str, str, str]] = []
        if source_instruction_id:
            objects.append(self._instruction_placeholder(source_instruction_id))
            event_relations.append(("instruction_object", source_instruction_id))
            object_relations.extend(
                [
                    (rule.rule_id, source_instruction_id, "derived_from_instruction"),
                    (source_instruction_id, rule.rule_id, "defines_rule"),
                ]
            )
        self._record_instruction_event(
            "project_rule_registered",
            objects=objects,
            event_relations=event_relations,
            object_relations=object_relations,
            event_attrs={"source_instruction_id": source_instruction_id},
        )
        return rule

    def revise_project_rule(
        self,
        *,
        rule: ProjectRule,
        new_text: str,
        reason: str | None = None,
        rule_attrs: dict[str, Any] | None = None,
    ) -> ProjectRule:
        updated = replace(
            rule,
            text=new_text,
            updated_at=utc_now_iso(),
            rule_attrs={**rule.rule_attrs, **dict(rule_attrs or {})},
        )
        self._record_instruction_event(
            "project_rule_revised",
            objects=[self._rule_object(updated)],
            event_relations=[("rule_object", updated.rule_id)],
            object_relations=[],
            event_attrs={"reason": reason},
        )
        return updated

    def register_user_preference(
        self,
        *,
        preference_key: str,
        preference_value: str,
        status: str = "active",
        confidence: float | None = None,
        source_kind: str | None = None,
        session_id: str | None = None,
        message_id: str | None = None,
        preference_attrs: dict[str, Any] | None = None,
    ) -> UserPreference:
        now = utc_now_iso()
        preference = UserPreference(
            preference_id=new_user_preference_id(),
            preference_key=preference_key,
            preference_value=preference_value,
            status=status,
            confidence=confidence,
            source_kind=source_kind,
            created_at=now,
            updated_at=now,
            preference_attrs=dict(preference_attrs or {}),
        )
        self._record_instruction_event(
            "user_preference_registered",
            objects=[self._preference_object(preference)],
            event_relations=[
                ("preference_object", preference.preference_id),
                *self._source_event_relations(session_id, message_id),
            ],
            object_relations=self._source_object_relations(
                preference.preference_id,
                session_id,
                message_id,
            ),
            event_attrs={"session_id": session_id, "message_id": message_id},
        )
        return preference

    def revise_user_preference(
        self,
        *,
        preference: UserPreference,
        new_value: str,
        reason: str | None = None,
        preference_attrs: dict[str, Any] | None = None,
    ) -> UserPreference:
        updated = replace(
            preference,
            preference_value=new_value,
            updated_at=utc_now_iso(),
            preference_attrs={
                **preference.preference_attrs,
                **dict(preference_attrs or {}),
            },
        )
        self._record_instruction_event(
            "user_preference_revised",
            objects=[self._preference_object(updated)],
            event_relations=[("preference_object", updated.preference_id)],
            object_relations=[],
            event_attrs={"reason": reason},
        )
        return updated

    def _record_instruction_event(
        self,
        event_activity: str,
        *,
        objects: list[OCELObject],
        event_relations: list[tuple[str, str]],
        object_relations: list[tuple[str, str, str]],
        event_attrs: dict[str, Any],
    ) -> None:
        timestamp = utc_now_iso()
        event = OCELEvent(
            event_id=f"evt:{uuid4()}",
            event_activity=event_activity,
            event_timestamp=timestamp,
            event_attrs={
                **event_attrs,
                "runtime_event_type": event_activity,
                "lifecycle": event_activity,
                "source_runtime": "chanta_core",
            },
        )
        extra_objects = self._objects_for_source_relations(event_relations)
        relations = [
            OCELRelation.event_object(
                event_id=event.event_id,
                object_id=object_id,
                qualifier=qualifier,
            )
            for qualifier, object_id in event_relations
        ]
        relations.extend(
            OCELRelation.object_object(
                source_object_id=source,
                target_object_id=target,
                qualifier=qualifier,
            )
            for source, target, qualifier in object_relations
        )
        self.trace_service.record_session_ocel_record(
            OCELRecord(event=event, objects=[*objects, *extra_objects], relations=relations)
        )

    def _source_event_relations(
        self,
        session_id: str | None,
        message_id: str | None,
    ) -> list[tuple[str, str]]:
        relations: list[tuple[str, str]] = []
        if session_id:
            relations.append(("source_session", self._session_object_id(session_id)))
        if message_id:
            relations.append(("source_message", message_id))
        return relations

    def _source_object_relations(
        self,
        source_id: str,
        session_id: str | None,
        message_id: str | None,
    ) -> list[tuple[str, str, str]]:
        relations: list[tuple[str, str, str]] = []
        if session_id:
            relations.append((source_id, self._session_object_id(session_id), "belongs_to_session"))
        if message_id:
            relations.append((source_id, message_id, "derived_from_message"))
        return relations

    def _objects_for_source_relations(
        self,
        event_relations: list[tuple[str, str]],
    ) -> list[OCELObject]:
        objects: list[OCELObject] = []
        for qualifier, object_id in event_relations:
            if qualifier == "source_session":
                objects.append(
                    OCELObject(
                        object_id=object_id,
                        object_type="session",
                        object_attrs={"object_key": object_id, "display_name": object_id},
                    )
                )
            if qualifier == "source_message":
                objects.append(
                    OCELObject(
                        object_id=object_id,
                        object_type="message",
                        object_attrs={"object_key": object_id, "display_name": object_id},
                    )
                )
        return objects

    @staticmethod
    def _instruction_object(instruction: InstructionArtifact) -> OCELObject:
        return OCELObject(
            object_id=instruction.instruction_id,
            object_type="instruction_artifact",
            object_attrs={**instruction.to_dict(), "object_key": instruction.instruction_id, "display_name": instruction.title},
        )

    @staticmethod
    def _instruction_placeholder(instruction_id: str) -> OCELObject:
        return OCELObject(
            object_id=instruction_id,
            object_type="instruction_artifact",
            object_attrs={"object_key": instruction_id, "display_name": instruction_id},
        )

    @staticmethod
    def _rule_object(rule: ProjectRule) -> OCELObject:
        return OCELObject(
            object_id=rule.rule_id,
            object_type="project_rule",
            object_attrs={**rule.to_dict(), "object_key": rule.rule_id, "display_name": rule.text[:80]},
        )

    @staticmethod
    def _preference_object(preference: UserPreference) -> OCELObject:
        return OCELObject(
            object_id=preference.preference_id,
            object_type="user_preference",
            object_attrs={**preference.to_dict(), "object_key": preference.preference_id, "display_name": preference.preference_key},
        )

    @staticmethod
    def _session_object_id(session_id: str) -> str:
        return session_id if session_id.startswith("session:") else f"session:{session_id}"
