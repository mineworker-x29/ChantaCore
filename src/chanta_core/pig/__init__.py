__all__ = [
    "HumanPIAssimilator",
    "PIArtifact",
    "PIArtifactStore",
    "PIEvidenceRef",
    "PIGDiagnostic",
    "PIGEdge",
    "PIGGraph",
    "PIGBuilder",
    "PIGConformanceIssue",
    "PIGConformanceReport",
    "PIGConformanceService",
    "PIGContext",
    "PIGNode",
    "PIGFeedbackService",
    "PIGGuidance",
    "PIGGuidanceService",
    "PIGReportService",
    "PIGRecommendation",
    "PIGService",
    "PISubstrateInspection",
    "PISubstrateInspector",
    "ProcessRunReport",
]


def __getattr__(name: str):
    if name == "HumanPIAssimilator":
        from chanta_core.pig.assimilation import HumanPIAssimilator

        return HumanPIAssimilator
    if name == "PIArtifact":
        from chanta_core.pig.artifacts import PIArtifact

        return PIArtifact
    if name == "PIArtifactStore":
        from chanta_core.pig.artifact_store import PIArtifactStore

        return PIArtifactStore
    if name == "PIEvidenceRef":
        from chanta_core.pig.evidence import PIEvidenceRef

        return PIEvidenceRef
    if name == "PIGBuilder":
        from chanta_core.pig.builder import PIGBuilder

        return PIGBuilder
    if name in {"PIGConformanceIssue", "PIGConformanceReport", "PIGConformanceService"}:
        from chanta_core.pig.conformance import (
            PIGConformanceIssue,
            PIGConformanceReport,
            PIGConformanceService,
        )

        return {
            "PIGConformanceIssue": PIGConformanceIssue,
            "PIGConformanceReport": PIGConformanceReport,
            "PIGConformanceService": PIGConformanceService,
        }[name]
    if name == "PIGContext":
        from chanta_core.pig.context import PIGContext

        return PIGContext
    if name == "PIGFeedbackService":
        from chanta_core.pig.feedback import PIGFeedbackService

        return PIGFeedbackService
    if name in {"PIGGuidance", "PIGGuidanceService"}:
        from chanta_core.pig.guidance import PIGGuidance, PIGGuidanceService

        return {"PIGGuidance": PIGGuidance, "PIGGuidanceService": PIGGuidanceService}[name]
    if name in {"PIGDiagnostic", "PIGEdge", "PIGGraph", "PIGNode", "PIGRecommendation"}:
        from chanta_core.pig.models import (
            PIGDiagnostic,
            PIGEdge,
            PIGGraph,
            PIGNode,
            PIGRecommendation,
        )

        return {
            "PIGDiagnostic": PIGDiagnostic,
            "PIGEdge": PIGEdge,
            "PIGGraph": PIGGraph,
            "PIGNode": PIGNode,
            "PIGRecommendation": PIGRecommendation,
        }[name]
    if name in {"PIGReportService", "ProcessRunReport"}:
        from chanta_core.pig.reports import PIGReportService, ProcessRunReport

        return {
            "PIGReportService": PIGReportService,
            "ProcessRunReport": ProcessRunReport,
        }[name]
    if name == "PIGService":
        from chanta_core.pig.service import PIGService

        return PIGService
    if name in {"PISubstrateInspection", "PISubstrateInspector"}:
        from chanta_core.pig.inspector import PISubstrateInspection, PISubstrateInspector

        return {
            "PISubstrateInspection": PISubstrateInspection,
            "PISubstrateInspector": PISubstrateInspector,
        }[name]
    raise AttributeError(name)
