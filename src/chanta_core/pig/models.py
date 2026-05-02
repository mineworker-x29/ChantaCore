from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class PIGNode:
    node_id: str
    node_type: str
    label: str
    attributes: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "node_id": self.node_id,
            "node_type": self.node_type,
            "label": self.label,
            "attributes": self.attributes,
        }


@dataclass(frozen=True)
class PIGEdge:
    edge_id: str
    source_id: str
    target_id: str
    edge_type: str
    attributes: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "edge_id": self.edge_id,
            "source_id": self.source_id,
            "target_id": self.target_id,
            "edge_type": self.edge_type,
            "attributes": self.attributes,
        }


@dataclass(frozen=True)
class PIGGraph:
    graph_id: str
    nodes: list[PIGNode]
    edges: list[PIGEdge]
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "graph_id": self.graph_id,
            "nodes": [node.to_dict() for node in self.nodes],
            "edges": [edge.to_dict() for edge in self.edges],
            "metadata": self.metadata,
        }


@dataclass(frozen=True)
class PIGDiagnostic:
    diagnostic_id: str
    severity: str
    title: str
    description: str
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "diagnostic_id": self.diagnostic_id,
            "severity": self.severity,
            "title": self.title,
            "description": self.description,
            "evidence_refs": self.evidence_refs,
            "metadata": self.metadata,
        }


@dataclass(frozen=True)
class PIGRecommendation:
    recommendation_id: str
    recommendation_type: str
    title: str
    payload: dict[str, Any]
    rationale_refs: list[str]
    confidence: float
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "recommendation_id": self.recommendation_id,
            "recommendation_type": self.recommendation_type,
            "title": self.title,
            "payload": self.payload,
            "rationale_refs": self.rationale_refs,
            "confidence": self.confidence,
            "metadata": self.metadata,
        }
