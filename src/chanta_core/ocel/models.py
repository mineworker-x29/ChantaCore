from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

RelationKind = Literal["event_object", "object_object"]


@dataclass(frozen=True)
class OCELObject:
    object_id: str
    object_type: str
    object_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "object_id": self.object_id,
            "object_type": self.object_type,
            "object_attrs": self.object_attrs,
        }


@dataclass(frozen=True)
class OCELEvent:
    event_id: str
    event_activity: str
    event_timestamp: str
    event_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_activity": self.event_activity,
            "event_timestamp": self.event_timestamp,
            "event_attrs": self.event_attrs,
        }


@dataclass(frozen=True)
class OCELRelation:
    relation_kind: RelationKind
    source_id: str
    target_id: str
    qualifier: str
    relation_attrs: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def event_object(
        cls,
        *,
        event_id: str,
        object_id: str,
        qualifier: str,
        relation_attrs: dict[str, Any] | None = None,
    ) -> "OCELRelation":
        return cls(
            relation_kind="event_object",
            source_id=event_id,
            target_id=object_id,
            qualifier=qualifier,
            relation_attrs=relation_attrs or {},
        )

    @classmethod
    def object_object(
        cls,
        *,
        source_object_id: str,
        target_object_id: str,
        qualifier: str,
        relation_attrs: dict[str, Any] | None = None,
    ) -> "OCELRelation":
        return cls(
            relation_kind="object_object",
            source_id=source_object_id,
            target_id=target_object_id,
            qualifier=qualifier,
            relation_attrs=relation_attrs or {},
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "relation_kind": self.relation_kind,
            "source_id": self.source_id,
            "target_id": self.target_id,
            "qualifier": self.qualifier,
            "relation_attrs": self.relation_attrs,
        }


@dataclass(frozen=True)
class OCELRecord:
    event: OCELEvent
    objects: list[OCELObject]
    relations: list[OCELRelation]

    @property
    def event_object_relations(self) -> list[OCELRelation]:
        return [
            relation
            for relation in self.relations
            if relation.relation_kind == "event_object"
        ]

    @property
    def object_object_relations(self) -> list[OCELRelation]:
        return [
            relation
            for relation in self.relations
            if relation.relation_kind == "object_object"
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "event": self.event.to_dict(),
            "objects": [item.to_dict() for item in self.objects],
            "relations": [item.to_dict() for item in self.relations],
        }
