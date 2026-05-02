from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class OCPXEventView:
    event_id: str
    event_activity: str
    event_timestamp: str
    related_objects: list[dict[str, Any]]
    event_attrs: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_activity": self.event_activity,
            "event_timestamp": self.event_timestamp,
            "related_objects": self.related_objects,
            "event_attrs": self.event_attrs,
        }


@dataclass(frozen=True)
class OCPXObjectView:
    object_id: str
    object_type: str
    object_attrs: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "object_id": self.object_id,
            "object_type": self.object_type,
            "object_attrs": self.object_attrs,
        }


@dataclass(frozen=True)
class OCPXProcessView:
    view_id: str
    source: str
    session_id: str | None
    events: list[OCPXEventView]
    objects: list[OCPXObjectView]
    view_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "view_id": self.view_id,
            "source": self.source,
            "session_id": self.session_id,
            "events": [event.to_dict() for event in self.events],
            "objects": [item.to_dict() for item in self.objects],
            "view_attrs": self.view_attrs,
        }
