from __future__ import annotations

from chanta_core.ocpx.models import OCPXProcessView
from chanta_core.pig.models import PIGDiagnostic


class PIGDiagnosticService:
    def diagnose_view(self, view: OCPXProcessView) -> list[PIGDiagnostic]:
        diagnostics: list[PIGDiagnostic] = []
        if not view.events:
            diagnostics.append(
                PIGDiagnostic(
                    diagnostic_id="no_events",
                    severity="warning",
                    title="No events found",
                    description="The process view contains no events.",
                    evidence_refs=[view.view_id],
                )
            )
        if not view.objects:
            diagnostics.append(
                PIGDiagnostic(
                    diagnostic_id="no_objects",
                    severity="warning",
                    title="No objects found",
                    description="The process view contains no related objects.",
                    evidence_refs=[view.view_id],
                )
            )

        events_without_objects = [
            event.event_id for event in view.events if not event.related_objects
        ]
        if events_without_objects:
            diagnostics.append(
                PIGDiagnostic(
                    diagnostic_id="events_without_related_objects",
                    severity="warning",
                    title="Events without related objects",
                    description=(
                        "Some events do not have event-object relations in the "
                        "loaded view."
                    ),
                    evidence_refs=events_without_objects,
                    metadata={"count": len(events_without_objects)},
                )
            )
        activity_sequence = [event.event_activity for event in view.events]
        failed_process_objects = [
            item.object_id
            for item in view.objects
            if item.object_type == "process_instance"
            and item.object_attrs.get("status") == "failed"
        ]
        if "fail_process_instance" in activity_sequence or failed_process_objects:
            evidence_refs = [
                event.event_id
                for event in view.events
                if event.event_activity == "fail_process_instance"
            ] or failed_process_objects
            diagnostics.append(
                PIGDiagnostic(
                    diagnostic_id="failed_process_instance",
                    severity="error",
                    title="Failed process instance",
                    description=(
                        "The process view contains a failed process instance "
                        "or a fail_process_instance event."
                    ),
                    evidence_refs=evidence_refs,
                    metadata={"failed_process_objects": failed_process_objects},
                )
            )
        if "fail_skill_execution" in activity_sequence:
            diagnostics.append(
                PIGDiagnostic(
                    diagnostic_id="failed_skill_execution",
                    severity="error",
                    title="Failed skill execution",
                    description="The process view contains a failed skill execution event.",
                    evidence_refs=[
                        event.event_id
                        for event in view.events
                        if event.event_activity == "fail_skill_execution"
                    ],
                )
            )
        return diagnostics
