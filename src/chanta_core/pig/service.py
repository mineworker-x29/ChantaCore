from __future__ import annotations

from typing import Any

from chanta_core.ocpx.loader import OCPXLoader
from chanta_core.pig.builder import PIGBuilder
from chanta_core.pig.diagnostics import PIGDiagnosticService
from chanta_core.pig.recommendations import PIGRecommendationService


class PIGService:
    def __init__(self, loader: OCPXLoader | None = None) -> None:
        self.loader = loader or OCPXLoader()
        self.builder = PIGBuilder()
        self.diagnostic_service = PIGDiagnosticService()
        self.recommendation_service = PIGRecommendationService()

    def analyze_session(self, session_id: str) -> dict[str, Any]:
        view = self.loader.load_session_view(session_id)
        return self._analyze_view(view)

    def analyze_process_instance(self, process_instance_id: str) -> dict[str, Any]:
        view = self.loader.load_process_instance_view(process_instance_id)
        return self._analyze_view(view)

    def analyze_recent(self, limit: int = 20) -> dict[str, Any]:
        view = self.loader.load_recent_view(limit=limit)
        return self._analyze_view(view)

    def _analyze_view(self, view) -> dict[str, Any]:
        graph = self.builder.build_from_ocpx_view(view)
        guide = self.builder.build_guide_from_view(view)
        diagnostics = self.diagnostic_service.diagnose_view(view)
        recommendations = (
            self.recommendation_service.recommend_from_diagnostics(diagnostics)
        )
        return {
            "graph": graph.to_dict(),
            "guide": guide,
            "diagnostics": [item.to_dict() for item in diagnostics],
            "recommendations": [item.to_dict() for item in recommendations],
        }
