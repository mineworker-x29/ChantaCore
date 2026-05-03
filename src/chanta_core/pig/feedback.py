from __future__ import annotations

from typing import Any

from chanta_core.ocpx.engine import OCPXEngine
from chanta_core.ocpx.loader import OCPXLoader
from chanta_core.ocpx.models import OCPXProcessView
from chanta_core.pig.artifact_store import PIArtifactStore
from chanta_core.pig.artifacts import PIArtifact
from chanta_core.pig.context import PIGContext
from chanta_core.pig.service import PIGService


class PIGFeedbackService:
    def __init__(
        self,
        *,
        ocpx_loader: OCPXLoader | None = None,
        ocpx_engine: OCPXEngine | None = None,
        pig_service: PIGService | None = None,
        artifact_store: PIArtifactStore | None = None,
    ) -> None:
        self.ocpx_loader = ocpx_loader or OCPXLoader()
        self.ocpx_engine = ocpx_engine or OCPXEngine()
        self.pig_service = pig_service or PIGService(loader=self.ocpx_loader)
        self.artifact_store = artifact_store or PIArtifactStore()

    def build_recent_context(
        self,
        limit: int = 20,
        *,
        include_pi_artifacts: bool = True,
        max_pi_artifacts: int = 5,
    ) -> PIGContext:
        view = self.ocpx_loader.load_recent_view(limit=limit)
        pig_result = self.pig_service.analyze_recent(limit=limit)
        pi_artifacts = (
            self.artifact_store.recent(limit=max_pi_artifacts)
            if include_pi_artifacts
            else []
        )
        return self._build_context(
            view=view,
            pig_result=pig_result,
            scope="recent",
            process_instance_id=None,
            session_id=None,
            pi_artifacts=pi_artifacts,
            context_attrs={"limit": limit},
        )

    def build_process_instance_context(
        self,
        process_instance_id: str,
        *,
        include_pi_artifacts: bool = True,
        max_pi_artifacts: int = 5,
    ) -> PIGContext:
        view = self.ocpx_loader.load_process_instance_view(process_instance_id)
        pig_result = self.pig_service.analyze_process_instance(process_instance_id)
        pi_artifacts = (
            self._limit_artifacts(
                self.artifact_store.find_by_scope(
                    "process_instance_id",
                    process_instance_id,
                ),
                max_pi_artifacts,
            )
            if include_pi_artifacts
            else []
        )
        return self._build_context(
            view=view,
            pig_result=pig_result,
            scope="process_instance",
            process_instance_id=process_instance_id,
            session_id=view.session_id,
            pi_artifacts=pi_artifacts,
            context_attrs={},
        )

    def build_session_context(
        self,
        session_id: str,
        *,
        include_pi_artifacts: bool = True,
        max_pi_artifacts: int = 5,
    ) -> PIGContext:
        view = self.ocpx_loader.load_session_view(session_id)
        pig_result = self.pig_service.analyze_session(session_id)
        pi_artifacts = (
            self._limit_artifacts(
                self.artifact_store.find_by_scope("session_id", session_id),
                max_pi_artifacts,
            )
            if include_pi_artifacts
            else []
        )
        return self._build_context(
            view=view,
            pig_result=pig_result,
            scope="session",
            process_instance_id=None,
            session_id=session_id,
            pi_artifacts=pi_artifacts,
            context_attrs={},
        )

    def render_context_text(
        self,
        *,
        scope: str,
        activity_sequence: list[str],
        object_type_counts: dict[str, int],
        relation_coverage: dict[str, Any],
        performance_summary: dict[str, Any],
        diagnostics: list[dict[str, Any]],
        recommendations: list[dict[str, Any]],
        pi_artifacts: list[dict[str, Any]] | None = None,
        max_chars: int = 1600,
    ) -> str:
        coverage_ratio = float(relation_coverage.get("coverage_ratio") or 0.0)
        event_count = int(performance_summary.get("event_count") or 0)
        object_count = sum(object_type_counts.values())
        failure_count = int(performance_summary.get("failure_count") or 0)
        diagnostics_text = (
            "none"
            if not diagnostics
            else ", ".join(
                self._compact_label(item.get("title") or item.get("diagnostic_id"))
                for item in diagnostics[:3]
            )
        )
        recommendations_text = (
            "continue current trace discipline"
            if not recommendations
            else ", ".join(
                self._recommendation_label(item) for item in recommendations[:3]
            )
        )
        sequence_text = self._sequence_text(activity_sequence)
        lines = [
            "Process Intelligence Context:",
            f"- Scope: {scope}",
            f"- Activity sequence: {sequence_text}",
            f"- Relation coverage: {coverage_ratio * 100:.1f}%",
            f"- Events: {event_count}",
            f"- Objects: {object_count}",
            f"- Failures: {failure_count}",
            f"- Diagnostics: {diagnostics_text}",
            f"- Recommendations: {recommendations_text}",
        ]
        if pi_artifacts:
            lines.append("Human / External PI:")
            for artifact in pi_artifacts[:5]:
                artifact_type = self._compact_label(artifact.get("artifact_type"))
                title = self._compact_label(artifact.get("title"))
                confidence = float(artifact.get("confidence") or 0.0)
                lines.append(f"- [{artifact_type}] {title} - confidence {confidence:.2f}")
        text = "\n".join(lines)
        if len(text) <= max_chars:
            return text
        return f"{text[: max_chars - 3].rstrip()}..."

    def _build_context(
        self,
        *,
        view: OCPXProcessView,
        pig_result: dict[str, Any],
        scope: str,
        process_instance_id: str | None,
        session_id: str | None,
        pi_artifacts: list[PIArtifact],
        context_attrs: dict[str, Any],
    ) -> PIGContext:
        summary = self.ocpx_engine.summarize_for_pig_context(view)
        guide = dict(pig_result.get("guide") or {})
        diagnostics = list(pig_result.get("diagnostics") or [])
        recommendations = list(pig_result.get("recommendations") or [])
        pi_artifact_dicts = [artifact.to_dict() for artifact in pi_artifacts]
        context_text = self.render_context_text(
            scope=scope,
            activity_sequence=summary["activity_sequence"],
            object_type_counts=summary["object_type_counts"],
            relation_coverage=summary["relation_coverage"],
            performance_summary=summary["performance_summary"],
            diagnostics=diagnostics,
            recommendations=recommendations,
            pi_artifacts=pi_artifact_dicts,
        )
        return PIGContext(
            source="pig",
            scope=scope,
            process_instance_id=process_instance_id,
            session_id=session_id,
            activity_sequence=summary["activity_sequence"],
            event_activity_counts=summary["event_activity_counts"],
            object_type_counts=summary["object_type_counts"],
            relation_coverage=summary["relation_coverage"],
            basic_variant=summary["basic_variant"],
            performance_summary=summary["performance_summary"],
            guide=guide,
            diagnostics=diagnostics,
            recommendations=recommendations,
            context_text=context_text,
            pi_artifacts=pi_artifact_dicts,
            context_attrs={
                **context_attrs,
                "view_id": view.view_id,
                "view_source": view.source,
                "pi_artifact_count": len(pi_artifact_dicts),
                "variant_summary": summary.get("variant_summary"),
            },
        )

    @staticmethod
    def _sequence_text(activity_sequence: list[str], max_items: int = 12) -> str:
        if not activity_sequence:
            return "none"
        visible = activity_sequence[:max_items]
        suffix = " -> ..." if len(activity_sequence) > max_items else ""
        return f"{' -> '.join(visible)}{suffix}"

    @staticmethod
    def _compact_label(value: Any) -> str:
        return str(value or "unknown").replace("\n", " ").strip()

    def _recommendation_label(self, item: dict[str, Any]) -> str:
        recommendation_type = self._compact_label(item.get("recommendation_type"))
        title = self._compact_label(item.get("title") or item.get("recommendation_id"))
        return f"{recommendation_type}: {title}"

    @staticmethod
    def _limit_artifacts(
        artifacts: list[PIArtifact],
        max_pi_artifacts: int,
    ) -> list[PIArtifact]:
        if max_pi_artifacts <= 0:
            return []
        return artifacts[-max_pi_artifacts:]
