from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from uuid import uuid4

from chanta_core.external.errors import ExternalCapabilityRegistrySnapshotError
from chanta_core.external.ids import new_external_capability_registry_snapshot_id
from chanta_core.external.models import (
    ExternalAssimilationCandidate,
    ExternalCapabilityDescriptor,
    ExternalCapabilityNormalizationResult,
    ExternalCapabilityRiskNote,
    ExternalCapabilitySource,
)
from chanta_core.materialized_views.ids import new_materialized_view_id
from chanta_core.materialized_views.models import MaterializedView, MaterializedViewRenderResult, hash_content
from chanta_core.ocel.models import OCELEvent, OCELObject, OCELRecord, OCELRelation
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso


EXTERNAL_CAPABILITIES_VIEW_FILENAME = "EXTERNAL_CAPABILITIES.md"
EXTERNAL_REVIEW_VIEW_FILENAME = "EXTERNAL_REVIEW.md"
EXTERNAL_RISKS_VIEW_FILENAME = "EXTERNAL_RISKS.md"
_RISK_SEVERITY = {"critical": 5, "high": 4, "medium": 3, "low": 2, "unknown": 1}


@dataclass(frozen=True)
class ExternalCapabilityRegistrySnapshot:
    snapshot_id: str
    snapshot_name: str | None
    source_ids: list[str]
    descriptor_ids: list[str]
    normalization_ids: list[str]
    candidate_ids: list[str]
    risk_note_ids: list[str]
    disabled_candidate_count: int
    execution_enabled_candidate_count: int
    pending_review_count: int
    high_risk_count: int
    critical_risk_count: int
    created_at: str
    snapshot_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for field_name in [
            "disabled_candidate_count",
            "execution_enabled_candidate_count",
            "pending_review_count",
            "high_risk_count",
            "critical_risk_count",
        ]:
            if getattr(self, field_name) < 0:
                raise ExternalCapabilityRegistrySnapshotError(f"{field_name} must be non-negative")

    def to_dict(self) -> dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id,
            "snapshot_name": self.snapshot_name,
            "source_ids": self.source_ids,
            "descriptor_ids": self.descriptor_ids,
            "normalization_ids": self.normalization_ids,
            "candidate_ids": self.candidate_ids,
            "risk_note_ids": self.risk_note_ids,
            "disabled_candidate_count": self.disabled_candidate_count,
            "execution_enabled_candidate_count": self.execution_enabled_candidate_count,
            "pending_review_count": self.pending_review_count,
            "high_risk_count": self.high_risk_count,
            "critical_risk_count": self.critical_risk_count,
            "created_at": self.created_at,
            "snapshot_attrs": self.snapshot_attrs,
        }


def get_external_view_paths(root: Path | str) -> dict[str, Path]:
    chanta_dir = Path(root) / ".chanta"
    return {
        "external_capabilities": chanta_dir / EXTERNAL_CAPABILITIES_VIEW_FILENAME,
        "external_review": chanta_dir / EXTERNAL_REVIEW_VIEW_FILENAME,
        "external_risks": chanta_dir / EXTERNAL_RISKS_VIEW_FILENAME,
    }


def render_external_capabilities_view(
    *,
    snapshot: ExternalCapabilityRegistrySnapshot,
    sources: list[ExternalCapabilitySource],
    descriptors: list[ExternalCapabilityDescriptor],
    normalizations: list[ExternalCapabilityNormalizationResult],
    candidates: list[ExternalAssimilationCandidate],
    risk_notes: list[ExternalCapabilityRiskNote],
    target_path: str,
) -> MaterializedView:
    generated_at = snapshot.created_at
    lines = [
        "# External Capabilities",
        "",
        _capabilities_warning(),
        "",
        _metadata_lines(snapshot=snapshot, target_path=target_path, generated_at=generated_at),
        "",
        "## Summary",
        f"- Sources: {len(sources)}",
        f"- Descriptors: {len(descriptors)}",
        f"- Normalization results: {len(normalizations)}",
        f"- Candidates: {len(candidates)}",
        f"- Risk notes: {len(risk_notes)}",
        f"- Disabled candidates: {snapshot.disabled_candidate_count}",
        f"- Pending review candidates: {snapshot.pending_review_count}",
        f"- Execution-enabled candidates: {snapshot.execution_enabled_candidate_count}",
        f"- High risk notes: {snapshot.high_risk_count}",
        f"- Critical risk notes: {snapshot.critical_risk_count}",
        "",
        "## External Capability Sources",
        *_source_lines(sources),
        "",
        "## External Capability Descriptors",
        *_descriptor_lines(descriptors),
        "",
        "## Normalization Results",
        *_normalization_lines(normalizations),
        "",
        "## Assimilation Candidates",
        *_candidate_lines(candidates),
        "",
        "## Disabled Candidates",
        *_candidate_lines([item for item in _sort_candidates(candidates) if item.activation_status == "disabled"]),
    ]
    enabled = [item for item in _sort_candidates(candidates) if item.execution_enabled]
    if enabled:
        lines.extend(
            [
                "",
                "## Execution-Enabled Warning",
                "These candidates are reported only. This view does not disable or enable them.",
                *_candidate_lines(enabled),
            ]
        )
    return _materialized_view(
        view_type="external_capabilities",
        title="External Capabilities",
        target_path=target_path,
        content="\n".join(lines).rstrip() + "\n",
        generated_at=generated_at,
        snapshot=snapshot,
    )


def render_external_review_view(
    *,
    snapshot: ExternalCapabilityRegistrySnapshot,
    candidates: list[ExternalAssimilationCandidate],
    descriptors: list[ExternalCapabilityDescriptor],
    risk_notes: list[ExternalCapabilityRiskNote],
    target_path: str,
) -> MaterializedView:
    generated_at = snapshot.created_at
    pending = [item for item in _sort_candidates(candidates) if item.review_status == "pending_review"]
    more_info = [item for item in _sort_candidates(candidates) if item.review_status == "needs_more_info"]
    disabled = [item for item in _sort_candidates(candidates) if item.activation_status == "disabled"]
    inactive = [
        item
        for item in _sort_candidates(candidates)
        if item.review_status in {"rejected", "archived"} or item.activation_status == "rejected"
    ]
    enabled = [item for item in _sort_candidates(candidates) if item.execution_enabled]
    lines = [
        "# External Review",
        "",
        _review_warning(),
        "",
        _metadata_lines(snapshot=snapshot, target_path=target_path, generated_at=generated_at),
        "",
        "## Important Boundary",
        "- This file is not a review queue.",
        "- This file does not approve, reject, activate, or run external capabilities.",
        "- Formal review workflow belongs to a later version.",
        "",
        "## Pending Review Candidates",
        *_candidate_with_descriptor_lines(pending, descriptors, risk_notes),
        "",
        "## Needs More Information",
        *_candidate_with_descriptor_lines(more_info, descriptors, risk_notes),
        "",
        "## Disabled Candidates",
        *_candidate_with_descriptor_lines(disabled, descriptors, risk_notes),
    ]
    if inactive:
        lines.extend(["", "## Rejected / Archived Candidates", *_candidate_with_descriptor_lines(inactive, descriptors, risk_notes)])
    if enabled:
        lines.extend(
            [
                "",
                "## Execution-Enabled Warning",
                "These candidates are reported only. This view does not disable or enable them.",
                *_candidate_with_descriptor_lines(enabled, descriptors, risk_notes),
            ]
        )
    return _materialized_view(
        view_type="external_review",
        title="External Review",
        target_path=target_path,
        content="\n".join(lines).rstrip() + "\n",
        generated_at=generated_at,
        snapshot=snapshot,
    )


def render_external_risks_view(
    *,
    snapshot: ExternalCapabilityRegistrySnapshot,
    risk_notes: list[ExternalCapabilityRiskNote],
    descriptors: list[ExternalCapabilityDescriptor],
    candidates: list[ExternalAssimilationCandidate],
    target_path: str,
) -> MaterializedView:
    generated_at = snapshot.created_at
    sorted_notes = _sort_risk_notes(risk_notes)
    critical = [item for item in sorted_notes if item.risk_level == "critical"]
    high = [item for item in sorted_notes if item.risk_level == "high"]
    other = [item for item in sorted_notes if item.risk_level not in {"critical", "high"}]
    review_required = [item for item in sorted_notes if item.review_required]
    lines = [
        "# External Risks",
        "",
        _risk_warning(),
        "",
        _metadata_lines(snapshot=snapshot, target_path=target_path, generated_at=generated_at),
        "",
        "## Risk Summary",
        f"- Risk notes: {len(risk_notes)}",
        f"- Critical risk notes: {snapshot.critical_risk_count}",
        f"- High risk notes: {snapshot.high_risk_count}",
        f"- Review required notes: {len(review_required)}",
        "",
        "## Critical Risk Notes",
        *_risk_note_lines(critical, descriptors, candidates),
        "",
        "## High Risk Notes",
        *_risk_note_lines(high, descriptors, candidates),
        "",
        "## Medium / Low / Unknown Risk Notes",
        *_risk_note_lines(other, descriptors, candidates),
        "",
        "## Review Required Notes",
        *_risk_note_lines(review_required, descriptors, candidates),
    ]
    return _materialized_view(
        view_type="external_risks",
        title="External Risks",
        target_path=target_path,
        content="\n".join(lines).rstrip() + "\n",
        generated_at=generated_at,
        snapshot=snapshot,
    )


class ExternalCapabilityRegistryViewService:
    def __init__(
        self,
        *,
        trace_service: TraceService | None = None,
        root: Path | str | None = None,
    ) -> None:
        self.trace_service = trace_service
        self.root = Path(root) if root is not None else Path(".")
        self._last_snapshot: ExternalCapabilityRegistrySnapshot | None = None

    def build_registry_snapshot(
        self,
        *,
        sources: list[ExternalCapabilitySource] | None = None,
        descriptors: list[ExternalCapabilityDescriptor] | None = None,
        normalizations: list[ExternalCapabilityNormalizationResult] | None = None,
        candidates: list[ExternalAssimilationCandidate] | None = None,
        risk_notes: list[ExternalCapabilityRiskNote] | None = None,
        snapshot_name: str | None = None,
        snapshot_attrs: dict[str, Any] | None = None,
    ) -> ExternalCapabilityRegistrySnapshot:
        source_items = list(sources or [])
        descriptor_items = list(descriptors or [])
        normalization_items = list(normalizations or [])
        candidate_items = list(candidates or [])
        risk_note_items = list(risk_notes or [])
        snapshot = ExternalCapabilityRegistrySnapshot(
            snapshot_id=new_external_capability_registry_snapshot_id(),
            snapshot_name=snapshot_name,
            source_ids=[item.source_id for item in source_items],
            descriptor_ids=[item.descriptor_id for item in descriptor_items],
            normalization_ids=[item.normalization_id for item in normalization_items],
            candidate_ids=[item.candidate_id for item in candidate_items],
            risk_note_ids=[item.risk_note_id for item in risk_note_items],
            disabled_candidate_count=sum(1 for item in candidate_items if item.activation_status == "disabled"),
            execution_enabled_candidate_count=sum(1 for item in candidate_items if item.execution_enabled),
            pending_review_count=sum(1 for item in candidate_items if item.review_status == "pending_review"),
            high_risk_count=sum(1 for item in risk_note_items if item.risk_level == "high"),
            critical_risk_count=sum(1 for item in risk_note_items if item.risk_level == "critical"),
            created_at=utc_now_iso(),
            snapshot_attrs=dict(snapshot_attrs or {}),
        )
        self._last_snapshot = snapshot
        self._record_snapshot_event(
            "external_capability_registry_snapshot_created",
            snapshot=snapshot,
            sources=source_items,
            descriptors=descriptor_items,
            candidates=candidate_items,
            risk_notes=risk_note_items,
            event_attrs={},
        )
        if snapshot.execution_enabled_candidate_count > 0:
            self._record_snapshot_event(
                "external_capability_execution_enabled_candidate_detected",
                snapshot=snapshot,
                sources=[],
                descriptors=[],
                candidates=candidate_items,
                risk_notes=[],
                event_attrs={"execution_enabled_candidate_count": snapshot.execution_enabled_candidate_count},
            )
        return snapshot

    def render_registry_view(
        self,
        *,
        snapshot: ExternalCapabilityRegistrySnapshot,
        sources: list[ExternalCapabilitySource] | None = None,
        descriptors: list[ExternalCapabilityDescriptor] | None = None,
        normalizations: list[ExternalCapabilityNormalizationResult] | None = None,
        candidates: list[ExternalAssimilationCandidate] | None = None,
        risk_notes: list[ExternalCapabilityRiskNote] | None = None,
        target_path: Path | str | None = None,
    ) -> MaterializedView:
        path = str(target_path or get_external_view_paths(self.root)["external_capabilities"])
        view = render_external_capabilities_view(
            snapshot=snapshot,
            sources=list(sources or []),
            descriptors=list(descriptors or []),
            normalizations=list(normalizations or []),
            candidates=list(candidates or []),
            risk_notes=list(risk_notes or []),
            target_path=path,
        )
        self._record_view_event("external_capability_registry_view_rendered", view=view, snapshot=snapshot)
        return view

    def render_review_view(
        self,
        *,
        snapshot: ExternalCapabilityRegistrySnapshot,
        candidates: list[ExternalAssimilationCandidate] | None = None,
        descriptors: list[ExternalCapabilityDescriptor] | None = None,
        risk_notes: list[ExternalCapabilityRiskNote] | None = None,
        target_path: Path | str | None = None,
    ) -> MaterializedView:
        path = str(target_path or get_external_view_paths(self.root)["external_review"])
        view = render_external_review_view(
            snapshot=snapshot,
            candidates=list(candidates or []),
            descriptors=list(descriptors or []),
            risk_notes=list(risk_notes or []),
            target_path=path,
        )
        self._record_view_event("external_capability_review_view_rendered", view=view, snapshot=snapshot)
        return view

    def render_risk_view(
        self,
        *,
        snapshot: ExternalCapabilityRegistrySnapshot,
        risk_notes: list[ExternalCapabilityRiskNote] | None = None,
        descriptors: list[ExternalCapabilityDescriptor] | None = None,
        candidates: list[ExternalAssimilationCandidate] | None = None,
        target_path: Path | str | None = None,
    ) -> MaterializedView:
        path = str(target_path or get_external_view_paths(self.root)["external_risks"])
        view = render_external_risks_view(
            snapshot=snapshot,
            risk_notes=list(risk_notes or []),
            descriptors=list(descriptors or []),
            candidates=list(candidates or []),
            target_path=path,
        )
        self._record_view_event("external_capability_risk_view_rendered", view=view, snapshot=snapshot)
        return view

    def render_default_external_views(
        self,
        *,
        root: Path | str | None = None,
        sources: list[ExternalCapabilitySource] | None = None,
        descriptors: list[ExternalCapabilityDescriptor] | None = None,
        normalizations: list[ExternalCapabilityNormalizationResult] | None = None,
        candidates: list[ExternalAssimilationCandidate] | None = None,
        risk_notes: list[ExternalCapabilityRiskNote] | None = None,
    ) -> dict[str, MaterializedView]:
        paths = get_external_view_paths(root or self.root)
        snapshot = self.build_registry_snapshot(
            sources=sources,
            descriptors=descriptors,
            normalizations=normalizations,
            candidates=candidates,
            risk_notes=risk_notes,
        )
        return {
            "external_capabilities": self.render_registry_view(
                snapshot=snapshot,
                sources=sources,
                descriptors=descriptors,
                normalizations=normalizations,
                candidates=candidates,
                risk_notes=risk_notes,
                target_path=paths["external_capabilities"],
            ),
            "external_review": self.render_review_view(
                snapshot=snapshot,
                candidates=candidates,
                descriptors=descriptors,
                risk_notes=risk_notes,
                target_path=paths["external_review"],
            ),
            "external_risks": self.render_risk_view(
                snapshot=snapshot,
                risk_notes=risk_notes,
                descriptors=descriptors,
                candidates=candidates,
                target_path=paths["external_risks"],
            ),
        }

    def write_view(
        self,
        *,
        view: MaterializedView | str,
        target_path: Path | str,
        overwrite: bool = True,
    ) -> MaterializedViewRenderResult:
        materialized = view if isinstance(view, MaterializedView) else _string_view(view, target_path)
        target = Path(target_path)
        if target.exists() and not overwrite:
            return MaterializedViewRenderResult(
                view=materialized,
                written=False,
                target_path=str(target),
                skipped_reason="target exists and overwrite is False",
            )
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(materialized.content, encoding="utf-8")
        result = MaterializedViewRenderResult(
            view=materialized,
            written=True,
            target_path=str(target),
            skipped_reason=None,
        )
        activity = _written_activity_for_view(materialized.view_type)
        self._record_view_event(activity, view=materialized, snapshot=self._last_snapshot)
        return result

    def refresh_default_external_views(
        self,
        *,
        root: Path | str | None = None,
        sources: list[ExternalCapabilitySource] | None = None,
        descriptors: list[ExternalCapabilityDescriptor] | None = None,
        normalizations: list[ExternalCapabilityNormalizationResult] | None = None,
        candidates: list[ExternalAssimilationCandidate] | None = None,
        risk_notes: list[ExternalCapabilityRiskNote] | None = None,
        overwrite: bool = True,
    ) -> dict[str, MaterializedViewRenderResult]:
        self._record_refresh_event("external_capability_view_refresh_started", {"overwrite": overwrite})
        views = self.render_default_external_views(
            root=root,
            sources=sources,
            descriptors=descriptors,
            normalizations=normalizations,
            candidates=candidates,
            risk_notes=risk_notes,
        )
        results = {
            key: self.write_view(view=view, target_path=view.target_path, overwrite=overwrite)
            for key, view in views.items()
        }
        self._record_refresh_event(
            "external_capability_view_refresh_completed",
            {
                "view_count": len(results),
                "written_count": sum(1 for item in results.values() if item.written),
            },
        )
        return results

    def _record_snapshot_event(
        self,
        event_activity: str,
        *,
        snapshot: ExternalCapabilityRegistrySnapshot,
        sources: list[ExternalCapabilitySource],
        descriptors: list[ExternalCapabilityDescriptor],
        candidates: list[ExternalAssimilationCandidate],
        risk_notes: list[ExternalCapabilityRiskNote],
        event_attrs: dict[str, Any],
    ) -> None:
        if self.trace_service is None:
            return
        event = _event(event_activity, {**event_attrs, "snapshot_id": snapshot.snapshot_id})
        objects = [_snapshot_object(snapshot)]
        objects.extend(_source_object(item) for item in sources)
        objects.extend(_descriptor_object(item) for item in descriptors)
        objects.extend(_candidate_object(item) for item in candidates)
        objects.extend(_risk_note_object(item) for item in risk_notes)
        relations = [OCELRelation.event_object(event_id=event.event_id, object_id=snapshot.snapshot_id, qualifier="snapshot_object")]
        relations.extend(OCELRelation.event_object(event_id=event.event_id, object_id=item.source_id, qualifier="source_object") for item in sources)
        relations.extend(OCELRelation.event_object(event_id=event.event_id, object_id=item.descriptor_id, qualifier="descriptor_object") for item in descriptors)
        relations.extend(OCELRelation.event_object(event_id=event.event_id, object_id=item.candidate_id, qualifier="candidate_object") for item in candidates)
        relations.extend(OCELRelation.event_object(event_id=event.event_id, object_id=item.risk_note_id, qualifier="risk_note_object") for item in risk_notes)
        relations.extend(OCELRelation.object_object(source_object_id=snapshot.snapshot_id, target_object_id=item.source_id, qualifier="includes_source") for item in sources)
        relations.extend(OCELRelation.object_object(source_object_id=snapshot.snapshot_id, target_object_id=item.descriptor_id, qualifier="includes_descriptor") for item in descriptors)
        relations.extend(OCELRelation.object_object(source_object_id=snapshot.snapshot_id, target_object_id=item.candidate_id, qualifier="includes_candidate") for item in candidates)
        relations.extend(OCELRelation.object_object(source_object_id=snapshot.snapshot_id, target_object_id=item.risk_note_id, qualifier="includes_risk_note") for item in risk_notes)
        self.trace_service.record_session_ocel_record(OCELRecord(event=event, objects=objects, relations=relations))

    def _record_view_event(
        self,
        event_activity: str,
        *,
        view: MaterializedView,
        snapshot: ExternalCapabilityRegistrySnapshot | None,
    ) -> None:
        if self.trace_service is None:
            return
        event = _event(
            event_activity,
            {
                "view_type": view.view_type,
                "target_path": view.target_path,
                "content_hash": view.content_hash,
                "canonical": False,
                "snapshot_id": snapshot.snapshot_id if snapshot else None,
            },
        )
        objects = [_view_object(view)]
        relations = [
            OCELRelation.event_object(event_id=event.event_id, object_id=view.view_id, qualifier="view_object"),
        ]
        if snapshot is not None:
            objects.append(_snapshot_object(snapshot))
            relations.append(
                OCELRelation.event_object(
                    event_id=event.event_id,
                    object_id=snapshot.snapshot_id,
                    qualifier="snapshot_object",
                )
            )
            relations.append(
                OCELRelation.object_object(
                    source_object_id=view.view_id,
                    target_object_id=snapshot.snapshot_id,
                    qualifier="derived_from",
                )
            )
        self.trace_service.record_session_ocel_record(OCELRecord(event=event, objects=objects, relations=relations))

    def _record_refresh_event(self, event_activity: str, event_attrs: dict[str, Any]) -> None:
        if self.trace_service is None:
            return
        event = _event(event_activity, event_attrs)
        self.trace_service.record_session_ocel_record(OCELRecord(event=event, objects=[], relations=[]))


def _capabilities_warning() -> str:
    return "\n".join(
        [
            "> Generated materialized view.",
            "> Canonical source: OCEL.",
            "> This file is not the canonical external capability registry.",
            "> Edits to this file do not enable or disable capabilities.",
            "> No external capability is executable from this view.",
            "> Imported external capabilities are disabled candidates unless explicitly activated by a future reviewed workflow.",
        ]
    )


def _review_warning() -> str:
    return "\n".join(
        [
            "> Generated materialized view.",
            "> Canonical source: OCEL.",
            "> This file is not a review queue.",
            "> This file does not approve, reject, activate, or run external capabilities.",
            "> Formal review workflow belongs to a later version.",
        ]
    )


def _risk_warning() -> str:
    return "\n".join(
        [
            "> Generated materialized view.",
            "> Canonical source: OCEL.",
            "> This file is not an enforcement policy.",
            "> This file does not block or allow external capabilities.",
            "> Risk notes are advisory records only.",
        ]
    )


def _metadata_lines(*, snapshot: ExternalCapabilityRegistrySnapshot, target_path: str, generated_at: str) -> str:
    return "\n".join(
        [
            "## View Metadata",
            f"- Snapshot ID: {snapshot.snapshot_id}",
            f"- Snapshot name: {snapshot.snapshot_name or 'none'}",
            f"- Target path: {target_path}",
            f"- Generated at: {generated_at}",
            "- Canonical: False",
            "- Source kind: ocel_materialized_projection",
        ]
    )


def _source_lines(sources: list[ExternalCapabilitySource]) -> list[str]:
    if not sources:
        return ["- none"]
    return [
        f"- `{item.source_id}` | {item.source_name} | type={item.source_type} | trust={item.trust_level} | status={item.status}"
        for item in sorted(sources, key=lambda item: (item.source_type, item.source_name, item.source_id))
    ]


def _descriptor_lines(descriptors: list[ExternalCapabilityDescriptor]) -> list[str]:
    if not descriptors:
        return ["- none"]
    return [
        f"- `{item.descriptor_id}` | {item.capability_name} | type={item.capability_type} | source={item.source_id or 'none'} | normalized={item.normalized} | entrypoint metadata={item.declared_entrypoint or 'none'}"
        for item in _sort_descriptors(descriptors)
    ]


def _normalization_lines(normalizations: list[ExternalCapabilityNormalizationResult]) -> list[str]:
    if not normalizations:
        return ["- none"]
    return [
        f"- `{item.normalization_id}` | descriptor={item.descriptor_id} | status={item.status} | type={item.normalized_capability_type or 'none'} | risks={', '.join(item.normalized_risk_categories) or 'none'}"
        for item in sorted(normalizations, key=lambda item: (item.status, item.normalized_name or "", item.normalization_id))
    ]


def _candidate_lines(candidates: list[ExternalAssimilationCandidate]) -> list[str]:
    if not candidates:
        return ["- none"]
    return [
        f"- `{item.candidate_id}` | {item.candidate_name} | type={item.candidate_type} | review={item.review_status} | activation={item.activation_status} | execution_enabled={item.execution_enabled}"
        for item in _sort_candidates(candidates)
    ]


def _candidate_with_descriptor_lines(
    candidates: list[ExternalAssimilationCandidate],
    descriptors: list[ExternalCapabilityDescriptor],
    risk_notes: list[ExternalCapabilityRiskNote],
) -> list[str]:
    if not candidates:
        return ["- none"]
    descriptor_by_id = {item.descriptor_id: item for item in descriptors}
    note_count_by_candidate: dict[str, int] = {}
    for note in risk_notes:
        if note.candidate_id:
            note_count_by_candidate[note.candidate_id] = note_count_by_candidate.get(note.candidate_id, 0) + 1
    lines = []
    for item in _sort_candidates(candidates):
        descriptor = descriptor_by_id.get(item.descriptor_id)
        descriptor_name = descriptor.capability_name if descriptor else item.descriptor_id
        lines.append(
            f"- `{item.candidate_id}` | {item.candidate_name} | descriptor={descriptor_name} | review={item.review_status} | activation={item.activation_status} | execution_enabled={item.execution_enabled} | risk_notes={note_count_by_candidate.get(item.candidate_id, 0)}"
        )
    return lines


def _risk_note_lines(
    risk_notes: list[ExternalCapabilityRiskNote],
    descriptors: list[ExternalCapabilityDescriptor],
    candidates: list[ExternalAssimilationCandidate],
) -> list[str]:
    if not risk_notes:
        return ["- none"]
    descriptor_by_id = {item.descriptor_id: item for item in descriptors}
    candidate_by_id = {item.candidate_id: item for item in candidates}
    lines = []
    for item in _sort_risk_notes(risk_notes):
        descriptor = descriptor_by_id.get(item.descriptor_id or "")
        candidate = candidate_by_id.get(item.candidate_id or "")
        lines.append(
            f"- `{item.risk_note_id}` | level={item.risk_level} | categories={', '.join(item.risk_categories) or 'none'} | descriptor={(descriptor.capability_name if descriptor else item.descriptor_id) or 'none'} | candidate={(candidate.candidate_name if candidate else item.candidate_id) or 'none'} | review_required={item.review_required} | {item.message}"
        )
    return lines


def _sort_descriptors(descriptors: list[ExternalCapabilityDescriptor]) -> list[ExternalCapabilityDescriptor]:
    return sorted(descriptors, key=lambda item: (item.capability_type, item.capability_name, item.descriptor_id))


def _sort_candidates(candidates: list[ExternalAssimilationCandidate]) -> list[ExternalAssimilationCandidate]:
    return sorted(candidates, key=lambda item: (item.review_status, item.activation_status, item.candidate_name, item.candidate_id))


def _sort_risk_notes(risk_notes: list[ExternalCapabilityRiskNote]) -> list[ExternalCapabilityRiskNote]:
    return sorted(risk_notes, key=lambda item: (-_RISK_SEVERITY.get(item.risk_level, 0), item.risk_note_id))


def _materialized_view(
    *,
    view_type: str,
    title: str,
    target_path: str,
    content: str,
    generated_at: str,
    snapshot: ExternalCapabilityRegistrySnapshot,
) -> MaterializedView:
    return MaterializedView(
        view_id=new_materialized_view_id(),
        view_type=view_type,
        title=title,
        target_path=target_path,
        content=content,
        content_hash=hash_content(content),
        generated_at=generated_at,
        source_kind="ocel_materialized_projection",
        canonical=False,
        view_attrs={"snapshot_id": snapshot.snapshot_id, "external_capability_view": True},
    )


def _string_view(content: str, target_path: Path | str) -> MaterializedView:
    generated_at = utc_now_iso()
    return MaterializedView(
        view_id=new_materialized_view_id(),
        view_type="external_custom",
        title="External Custom",
        target_path=str(target_path),
        content=content,
        content_hash=hash_content(content),
        generated_at=generated_at,
        source_kind="ocel_materialized_projection",
        canonical=False,
        view_attrs={"external_capability_view": True},
    )


def _written_activity_for_view(view_type: str) -> str:
    return {
        "external_capabilities": "external_capability_registry_view_written",
        "external_review": "external_capability_review_view_written",
        "external_risks": "external_capability_risk_view_written",
    }.get(view_type, "external_capability_registry_view_written")


def _event(event_activity: str, event_attrs: dict[str, Any]) -> OCELEvent:
    return OCELEvent(
        event_id=f"evt:{uuid4()}",
        event_activity=event_activity,
        event_timestamp=utc_now_iso(),
        event_attrs={
            **event_attrs,
            "runtime_event_type": event_activity,
            "source_runtime": "chanta_core",
            "observability_only": True,
            "external_capability_view_only": True,
            "runtime_effect": False,
            "canonical": False,
        },
    )


def _snapshot_object(snapshot: ExternalCapabilityRegistrySnapshot) -> OCELObject:
    return OCELObject(
        object_id=snapshot.snapshot_id,
        object_type="external_capability_registry_snapshot",
        object_attrs={
            **snapshot.to_dict(),
            "object_key": snapshot.snapshot_id,
            "display_name": snapshot.snapshot_name or "external capability registry snapshot",
        },
    )


def _view_object(view: MaterializedView) -> OCELObject:
    return OCELObject(
        object_id=view.view_id,
        object_type="materialized_view",
        object_attrs={
            "object_key": view.view_id,
            "display_name": view.title,
            "view_type": view.view_type,
            "title": view.title,
            "target_path": view.target_path,
            "content_hash": view.content_hash,
            "generated_at": view.generated_at,
            "source_kind": view.source_kind,
            "canonical": False,
        },
    )


def _source_object(source: ExternalCapabilitySource) -> OCELObject:
    return OCELObject(source.source_id, "external_capability_source", {**source.to_dict(), "object_key": source.source_id})


def _descriptor_object(descriptor: ExternalCapabilityDescriptor) -> OCELObject:
    return OCELObject(
        descriptor.descriptor_id,
        "external_capability_descriptor",
        {**descriptor.to_dict(), "object_key": descriptor.descriptor_id, "execution_enabled": False},
    )


def _candidate_object(candidate: ExternalAssimilationCandidate) -> OCELObject:
    return OCELObject(
        candidate.candidate_id,
        "external_assimilation_candidate",
        {**candidate.to_dict(), "object_key": candidate.candidate_id},
    )


def _risk_note_object(note: ExternalCapabilityRiskNote) -> OCELObject:
    return OCELObject(note.risk_note_id, "external_capability_risk_note", {**note.to_dict(), "object_key": note.risk_note_id})
