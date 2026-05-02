from __future__ import annotations

from typing import Any
from uuid import uuid4

from chanta_core.ocpx.engine import OCPXEngine
from chanta_core.ocpx.models import OCPXProcessView
from chanta_core.pig.models import PIGEdge, PIGGraph, PIGNode


class PIGBuilder:
    def __init__(self, engine: OCPXEngine | None = None) -> None:
        self.engine = engine or OCPXEngine()

    def build_from_ocpx_view(self, view: OCPXProcessView) -> PIGGraph:
        nodes_by_id: dict[str, PIGNode] = {}
        edges: list[PIGEdge] = []

        for event in view.events:
            event_node_id = f"event:{event.event_id}"
            nodes_by_id[event_node_id] = PIGNode(
                node_id=event_node_id,
                node_type="event",
                label=event.event_activity,
                attributes={
                    "event_id": event.event_id,
                    "event_activity": event.event_activity,
                    "event_timestamp": event.event_timestamp,
                },
            )

            for item in event.related_objects:
                object_node_id = f"object:{item['object_id']}"
                nodes_by_id[object_node_id] = PIGNode(
                    node_id=object_node_id,
                    node_type=item["object_type"],
                    label=(
                        item["object_attrs"].get("display_name")
                        or item["object_attrs"].get("object_key")
                        or item["object_id"]
                    ),
                    attributes=item,
                )
                qualifier = item.get("qualifier") or "related_object"
                edges.append(
                    PIGEdge(
                        edge_id=f"edge:{event.event_id}:{item['object_id']}:{qualifier}",
                        source_id=event_node_id,
                        target_id=object_node_id,
                        edge_type=qualifier,
                        attributes={"qualifier": qualifier},
                    )
                )

        return PIGGraph(
            graph_id=f"pig:{uuid4()}",
            nodes=list(nodes_by_id.values()),
            edges=edges,
            metadata={"source_view_id": view.view_id, "source": view.source},
        )

    def build_guide_from_view(self, view: OCPXProcessView) -> dict[str, Any]:
        object_type_counts = self.engine.count_objects_by_type(view)
        return {
            "event_count": len(view.events),
            "object_count": len(view.objects),
            "activity_sequence": self.engine.activity_sequence(view),
            "process_instance_count": object_type_counts.get("process_instance", 0),
            "skill_usage_count": object_type_counts.get("skill", 0),
            "top_event_activities": self.engine.count_events_by_activity(view),
            "top_event_types": self.engine.count_events_by_type(view),
            "top_object_types": object_type_counts,
            "note": (
                "This is foundational process intelligence, not full graph "
                "reasoning yet."
            ),
        }
