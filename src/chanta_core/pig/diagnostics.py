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
        return diagnostics
