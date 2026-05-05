from __future__ import annotations

from pathlib import Path
from typing import Any
from uuid import uuid4

from chanta_core.materialized_views.models import (
    MaterializedView,
    MaterializedViewInputSnapshot,
    MaterializedViewRenderResult,
)
from chanta_core.materialized_views.paths import get_default_view_paths
from chanta_core.materialized_views.renderers import (
    render_context_rules_view,
    render_memory_view,
    render_pig_guidance_view,
    render_project_view,
    render_user_view,
)
from chanta_core.ocel.models import OCELObject, OCELRecord, OCELEvent, OCELRelation
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso


class MaterializedViewService:
    def __init__(
        self,
        *,
        trace_service: TraceService | None = None,
        root: Path | str | None = None,
    ) -> None:
        self.trace_service = trace_service
        self.root = Path(root) if root is not None else Path(".")

    def render_default_views(
        self,
        snapshot: MaterializedViewInputSnapshot,
        *,
        root: Path | str | None = None,
    ) -> dict[str, MaterializedView]:
        paths = get_default_view_paths(root or self.root)
        return {
            "memory": render_memory_view(snapshot, target_path=str(paths["memory"])),
            "project": render_project_view(snapshot, target_path=str(paths["project"])),
            "user": render_user_view(snapshot, target_path=str(paths["user"])),
            "pig_guidance": render_pig_guidance_view(
                snapshot,
                target_path=str(paths["pig_guidance"]),
            ),
            "context_rules": render_context_rules_view(
                snapshot,
                target_path=str(paths["context_rules"]),
            ),
        }

    def write_view(
        self,
        view: MaterializedView,
        *,
        overwrite: bool = True,
    ) -> MaterializedViewRenderResult:
        target = Path(view.target_path)
        if target.exists() and not overwrite:
            result = MaterializedViewRenderResult(
                view=view,
                written=False,
                target_path=str(target),
                skipped_reason="target exists and overwrite is False",
            )
            self._record_view_event("materialized_view_skipped", view, {"reason": result.skipped_reason})
            return result
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(view.content, encoding="utf-8")
        result = MaterializedViewRenderResult(
            view=view,
            written=True,
            target_path=str(target),
            skipped_reason=None,
        )
        self._record_view_event("materialized_view_written", view, {"target_path": str(target)})
        return result

    def refresh_default_views(
        self,
        snapshot: MaterializedViewInputSnapshot,
        *,
        root: Path | str | None = None,
        overwrite: bool = True,
    ) -> dict[str, MaterializedViewRenderResult]:
        self._record_refresh_event(
            "materialized_view_refresh_started",
            {"overwrite": overwrite},
        )
        views = self.render_default_views(snapshot, root=root)
        results: dict[str, MaterializedViewRenderResult] = {}
        for key in sorted(views):
            view = views[key]
            self.record_view_rendered(view)
            results[key] = self.write_view(view, overwrite=overwrite)
        self._record_refresh_event(
            "materialized_view_refresh_completed",
            {
                "view_count": len(results),
                "written_count": sum(1 for item in results.values() if item.written),
            },
        )
        return results

    def record_view_rendered(self, view: MaterializedView) -> None:
        self._record_view_event("materialized_view_rendered", view, {})

    def _record_view_event(
        self,
        event_activity: str,
        view: MaterializedView,
        event_attrs: dict[str, Any],
    ) -> None:
        if self.trace_service is None:
            return
        event = OCELEvent(
            event_id=f"evt:{uuid4()}",
            event_activity=event_activity,
            event_timestamp=utc_now_iso(),
            event_attrs={
                **event_attrs,
                "runtime_event_type": event_activity,
                "source_runtime": "chanta_core",
                "view_type": view.view_type,
                "target_path": view.target_path,
                "content_hash": view.content_hash,
                "canonical": False,
            },
        )
        view_object = self._view_object(view)
        self.trace_service.record_session_ocel_record(
            OCELRecord(
                event=event,
                objects=[view_object],
                relations=[
                    OCELRelation.event_object(
                        event_id=event.event_id,
                        object_id=view_object.object_id,
                        qualifier="view_object",
                    )
                ],
            )
        )

    def _record_refresh_event(
        self,
        event_activity: str,
        event_attrs: dict[str, Any],
    ) -> None:
        if self.trace_service is None:
            return
        event = OCELEvent(
            event_id=f"evt:{uuid4()}",
            event_activity=event_activity,
            event_timestamp=utc_now_iso(),
            event_attrs={
                **event_attrs,
                "runtime_event_type": event_activity,
                "source_runtime": "chanta_core",
            },
        )
        refresh_object = OCELObject(
            object_id=f"materialized_view:refresh:{event.event_id}",
            object_type="materialized_view",
            object_attrs={
                "object_key": f"materialized_view:refresh:{event.event_id}",
                "display_name": event_activity,
                "view_type": "refresh",
                "title": event_activity,
                "target_path": None,
                "content_hash": None,
                "generated_at": event.event_timestamp,
                "source_kind": "ocel_materialized_projection",
                "canonical": False,
            },
        )
        self.trace_service.record_session_ocel_record(
            OCELRecord(
                event=event,
                objects=[refresh_object],
                relations=[
                    OCELRelation.event_object(
                        event_id=event.event_id,
                        object_id=refresh_object.object_id,
                        qualifier="view_object",
                    )
                ],
            )
        )

    @staticmethod
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
