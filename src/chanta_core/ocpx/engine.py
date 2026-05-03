from __future__ import annotations

from datetime import datetime
from typing import Any

from chanta_core.ocpx.models import OCPXEventView, OCPXProcessView
from chanta_core.ocpx.variant import OCPXVariantSummary


class OCPXEngine:
    def summarize_view(self, view: OCPXProcessView) -> dict[str, Any]:
        return {
            "view_id": view.view_id,
            "source": view.source,
            "session_id": view.session_id,
            "event_count": len(view.events),
            "object_count": len(view.objects),
            "activity_sequence": self.activity_sequence(view),
            "activity_counts": self.count_events_by_activity(view),
            "event_types": self.count_events_by_type(view),
            "object_types": self.count_objects_by_type(view),
        }

    def summarize_process_instance_view(self, view: OCPXProcessView) -> dict[str, Any]:
        process_instances = [
            item.object_id
            for item in view.objects
            if item.object_type == "process_instance"
        ]
        return {
            **self.summarize_view(view),
            "process_instance_ids": process_instances,
            "process_instance_count": len(process_instances),
        }

    def activity_sequence(self, view: OCPXProcessView) -> list[str]:
        return [event.event_activity for event in self._events_in_timestamp_order(view)]

    def count_events_by_type(self, view: OCPXProcessView) -> dict[str, int]:
        return self.count_events_by_activity(view)

    def count_events_by_activity(self, view: OCPXProcessView) -> dict[str, int]:
        counts: dict[str, int] = {}
        for event in view.events:
            counts[event.event_activity] = counts.get(event.event_activity, 0) + 1
        return counts

    def count_objects_by_type(self, view: OCPXProcessView) -> dict[str, int]:
        counts: dict[str, int] = {}
        for item in view.objects:
            counts[item.object_type] = counts.get(item.object_type, 0) + 1
        return counts

    def compute_relation_coverage(self, view: OCPXProcessView) -> dict[str, Any]:
        events_total = len(view.events)
        events_with_related_objects = sum(
            1 for event in view.events if event.related_objects
        )
        events_without_related_objects = events_total - events_with_related_objects
        coverage_ratio = (
            events_with_related_objects / events_total if events_total else 0.0
        )
        return {
            "events_total": events_total,
            "events_with_related_objects": events_with_related_objects,
            "events_without_related_objects": events_without_related_objects,
            "coverage_ratio": coverage_ratio,
        }

    def compute_basic_variant(self, view: OCPXProcessView) -> dict[str, Any]:
        activity_sequence = self.activity_sequence(view)
        return {
            "variant_key": ">".join(activity_sequence),
            "activity_sequence": activity_sequence,
            "event_count": len(activity_sequence),
        }

    def compute_variant_summary(self, view: OCPXProcessView) -> OCPXVariantSummary:
        activity_sequence = self.activity_sequence(view)
        activity_set = set(activity_sequence)
        failure_count = (
            1
            if "fail_process_instance" in activity_set
            or "fail_skill_execution" in activity_set
            else 0
        )
        success_count = (
            1
            if "complete_process_instance" in activity_set
            and "fail_process_instance" not in activity_set
            else 0
        )
        return OCPXVariantSummary(
            variant_key=">".join(activity_sequence),
            activity_sequence=activity_sequence,
            trace_count=1,
            success_count=success_count,
            failure_count=failure_count,
            skill_ids=self._extract_skill_ids(view),
            example_process_instance_ids=self._extract_process_instance_ids(view)[:5],
            variant_attrs={"source_view_id": view.view_id, "source": view.source},
        )

    def compute_variant_summaries(
        self,
        views: list[OCPXProcessView],
    ) -> list[OCPXVariantSummary]:
        grouped: dict[str, dict[str, Any]] = {}
        for view in views:
            summary = self.compute_variant_summary(view)
            item = grouped.setdefault(
                summary.variant_key,
                {
                    "activity_sequence": summary.activity_sequence,
                    "trace_count": 0,
                    "success_count": 0,
                    "failure_count": 0,
                    "skill_ids": set(),
                    "example_process_instance_ids": [],
                },
            )
            item["trace_count"] += summary.trace_count
            item["success_count"] += summary.success_count
            item["failure_count"] += summary.failure_count
            item["skill_ids"].update(summary.skill_ids)
            for process_instance_id in summary.example_process_instance_ids:
                if process_instance_id not in item["example_process_instance_ids"]:
                    item["example_process_instance_ids"].append(process_instance_id)

        summaries = [
            OCPXVariantSummary(
                variant_key=variant_key,
                activity_sequence=list(item["activity_sequence"]),
                trace_count=int(item["trace_count"]),
                success_count=int(item["success_count"]),
                failure_count=int(item["failure_count"]),
                skill_ids=sorted(item["skill_ids"]),
                example_process_instance_ids=item["example_process_instance_ids"][:5],
                variant_attrs={"grouped": True},
            )
            for variant_key, item in grouped.items()
        ]
        return sorted(summaries, key=lambda item: item.variant_key)

    def compute_basic_performance(self, view: OCPXProcessView) -> dict[str, Any]:
        ordered_events = self._events_in_timestamp_order(view)
        start_timestamp = ordered_events[0].event_timestamp if ordered_events else None
        end_timestamp = ordered_events[-1].event_timestamp if ordered_events else None
        duration_seconds: float | None = None
        parse_warnings: list[str] = []

        if start_timestamp and end_timestamp:
            start = self._parse_timestamp(start_timestamp)
            end = self._parse_timestamp(end_timestamp)
            if start is not None and end is not None:
                duration_seconds = (end - start).total_seconds()
            else:
                parse_warnings.append("duration_seconds unavailable: timestamp parse failed")

        activity_counts = self.count_events_by_activity(view)
        failure_count = sum(
            count
            for activity, count in activity_counts.items()
            if activity in {"fail_process_instance", "fail_skill_execution"}
            or activity.startswith("fail_")
        )
        result: dict[str, Any] = {
            "start_timestamp": start_timestamp,
            "end_timestamp": end_timestamp,
            "duration_seconds": duration_seconds,
            "event_count": len(view.events),
            "llm_call_count": activity_counts.get("call_llm", 0),
            "skill_execution_count": activity_counts.get("execute_skill", 0),
            "failure_count": failure_count,
        }
        if parse_warnings:
            result["parse_warnings"] = parse_warnings
        return result

    def summarize_for_pig_context(self, view: OCPXProcessView) -> dict[str, Any]:
        return {
            "activity_sequence": self.activity_sequence(view),
            "event_activity_counts": self.count_events_by_activity(view),
            "object_type_counts": self.count_objects_by_type(view),
            "relation_coverage": self.compute_relation_coverage(view),
            "basic_variant": self.compute_basic_variant(view),
            "variant_summary": self.compute_variant_summary(view).to_dict(),
            "performance_summary": self.compute_basic_performance(view),
        }

    def _events_in_timestamp_order(
        self,
        view: OCPXProcessView,
    ) -> list[OCPXEventView]:
        indexed_events = list(enumerate(view.events))
        parsed = [
            (index, event, self._parse_timestamp(event.event_timestamp))
            for index, event in indexed_events
        ]
        if all(timestamp is not None for _, _, timestamp in parsed):
            return [
                event
                for _, event, _ in sorted(
                    parsed,
                    key=lambda item: (item[2], item[0]),
                )
            ]
        return [
            event
            for _, event in sorted(
                indexed_events,
                key=lambda item: (item[1].event_timestamp, item[0]),
            )
        ]

    @staticmethod
    def _parse_timestamp(value: str | None) -> datetime | None:
        if not value:
            return None
        normalized = value.strip()
        if normalized.endswith("Z"):
            normalized = f"{normalized[:-1]}+00:00"
        try:
            return datetime.fromisoformat(normalized)
        except ValueError:
            return None

    @staticmethod
    def _extract_skill_ids(view: OCPXProcessView) -> list[str]:
        skill_ids = {
            item.object_id
            for item in view.objects
            if item.object_type == "skill"
        }
        skill_ids.update(
            str(event.event_attrs["skill_id"])
            for event in view.events
            if event.event_attrs.get("skill_id")
        )
        return sorted(skill_ids)

    @staticmethod
    def _extract_process_instance_ids(view: OCPXProcessView) -> list[str]:
        process_instance_ids = [
            item.object_id
            for item in view.objects
            if item.object_type == "process_instance"
        ]
        if not process_instance_ids:
            process_instance_ids = [
                str(event.event_attrs["process_instance_id"])
                for event in view.events
                if event.event_attrs.get("process_instance_id")
            ]
        return sorted(dict.fromkeys(process_instance_ids))
