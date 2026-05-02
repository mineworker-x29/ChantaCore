from __future__ import annotations

from chanta_core.pig.models import PIGDiagnostic, PIGRecommendation


class PIGRecommendationService:
    def recommend_from_diagnostics(
        self,
        diagnostics: list[PIGDiagnostic],
    ) -> list[PIGRecommendation]:
        recommendations: list[PIGRecommendation] = []
        diagnostic_ids = {item.diagnostic_id for item in diagnostics}

        if "no_events" in diagnostic_ids:
            recommendations.append(
                PIGRecommendation(
                    recommendation_id="check_trace_emission",
                    recommendation_type="trace_configuration",
                    title="Check trace emission",
                    payload={"action": "verify_agent_runtime_trace_sequence"},
                    rationale_refs=["no_events"],
                    confidence=0.8,
                )
            )
        if "no_objects" in diagnostic_ids:
            recommendations.append(
                PIGRecommendation(
                    recommendation_id="check_object_mapping",
                    recommendation_type="object_mapping",
                    title="Check object mapping",
                    payload={"action": "verify_ocel_factory_objects"},
                    rationale_refs=["no_objects"],
                    confidence=0.8,
                )
            )
        if "events_without_related_objects" in diagnostic_ids:
            recommendations.append(
                PIGRecommendation(
                    recommendation_id="improve_event_object_relations",
                    recommendation_type="relation_mapping",
                    title="Improve event-object relation mapping",
                    payload={"action": "add_event_object_relations"},
                    rationale_refs=["events_without_related_objects"],
                    confidence=0.7,
                )
            )
        if "failed_process_instance" in diagnostic_ids:
            recommendations.append(
                PIGRecommendation(
                    recommendation_id="inspect_error_object",
                    recommendation_type="failure_analysis",
                    title="Inspect error object and failure stage",
                    payload={"action": "review_failure_stage"},
                    rationale_refs=["failed_process_instance"],
                    confidence=0.8,
                )
            )
        return recommendations
