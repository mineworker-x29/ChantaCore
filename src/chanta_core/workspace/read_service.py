from __future__ import annotations

import fnmatch
import hashlib
from pathlib import Path
from typing import Any
from uuid import uuid4

from chanta_core.ocel.models import OCELEvent, OCELObject, OCELRecord, OCELRelation
from chanta_core.ocel.store import OCELStore
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso
from chanta_core.workspace.errors import (
    WorkspaceBinaryFileError,
    WorkspaceFileTooLargeError,
    WorkspacePathViolationError,
    WorkspaceReadRootError,
    WorkspaceTextReadError,
    WorkspaceUnsupportedFileError,
)
from chanta_core.workspace.ids import (
    new_workspace_file_list_request_id,
    new_workspace_file_list_result_id,
    new_workspace_markdown_summary_request_id,
    new_workspace_markdown_summary_result_id,
    new_workspace_read_boundary_id,
    new_workspace_read_root_id,
    new_workspace_read_violation_id,
    new_workspace_text_file_read_request_id,
    new_workspace_text_file_read_result_id,
)
from chanta_core.workspace.models import (
    WorkspaceFileListRequest,
    WorkspaceFileListResult,
    WorkspaceMarkdownSummaryRequest,
    WorkspaceMarkdownSummaryResult,
    WorkspaceReadBoundary,
    WorkspaceReadRoot,
    WorkspaceReadViolation,
    WorkspaceTextFileReadRequest,
    WorkspaceTextFileReadResult,
)


DEFAULT_TEXT_EXTENSIONS = {
    ".md",
    ".markdown",
    ".txt",
    ".py",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".ini",
    ".cfg",
    ".csv",
    ".log",
}


def normalize_workspace_root(root_path: str | Path) -> Path:
    root = Path(root_path).expanduser().resolve(strict=False)
    if not root.exists() or not root.is_dir():
        raise WorkspaceReadRootError(f"Workspace read root is not a directory: {root}")
    return root


def validate_relative_workspace_path(relative_path: str) -> None:
    if not relative_path:
        raise WorkspacePathViolationError("relative_path is required")
    path = Path(relative_path)
    if path.is_absolute():
        raise WorkspacePathViolationError("Absolute workspace target paths are rejected")
    if any(part == ".." for part in path.parts):
        raise WorkspacePathViolationError("Workspace path traversal is rejected")


def resolve_workspace_path(root_path: str | Path, relative_path: str) -> Path:
    root = normalize_workspace_root(root_path)
    validate_relative_workspace_path(relative_path)
    resolved = (root / relative_path).resolve(strict=False)
    if not is_path_inside_root(resolved, root):
        raise WorkspacePathViolationError("Resolved path is outside the workspace root")
    return resolved


def is_path_inside_root(path: Path, root: Path) -> bool:
    try:
        path.resolve(strict=False).relative_to(root.resolve(strict=False))
        return True
    except ValueError:
        return False


def is_binary_bytes(data: bytes) -> bool:
    return b"\x00" in data


def hash_content(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def preview_text(text: str, max_chars: int = 2000) -> str:
    return text[:max_chars]


def extract_markdown_headings(text: str, max_headings: int = 50) -> list[str]:
    headings: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("#"):
            continue
        marker = stripped.split(" ", 1)[0]
        if marker and set(marker) == {"#"} and 1 <= len(marker) <= 6:
            title = stripped[len(marker) :].strip()
            if title:
                headings.append(f"{marker} {title}")
        if len(headings) >= max_headings:
            break
    return headings


class WorkspaceReadService:
    def __init__(
        self,
        *,
        trace_service: TraceService | None = None,
        ocel_store: OCELStore | None = None,
    ) -> None:
        if trace_service is not None:
            self.trace_service = trace_service
        elif ocel_store is not None:
            self.trace_service = TraceService(ocel_store=ocel_store)
        else:
            self.trace_service = TraceService()

    def register_read_root(
        self,
        root_path: str | Path,
        *,
        root_name: str | None = None,
        status: str = "active",
        root_attrs: dict[str, Any] | None = None,
    ) -> WorkspaceReadRoot:
        root = normalize_workspace_root(root_path)
        now = utc_now_iso()
        item = WorkspaceReadRoot(
            root_id=new_workspace_read_root_id(),
            root_path=str(root),
            root_name=root_name or root.name,
            status=status,
            created_at=now,
            updated_at=now,
            root_attrs={
                "read_only": True,
                "ambient_access": False,
                **dict(root_attrs or {}),
            },
        )
        self._record(
            "workspace_read_root_registered",
            objects=[_object("workspace_read_root", item.root_id, item.to_dict())],
            links=[("root_object", item.root_id)],
            object_links=[],
            attrs={"root_id": item.root_id},
        )
        return item

    def register_read_boundary(
        self,
        *,
        root_id: str,
        boundary_type: str,
        path_ref: str,
        description: str | None = None,
        status: str = "active",
        priority: int | None = None,
        boundary_attrs: dict[str, Any] | None = None,
    ) -> WorkspaceReadBoundary:
        item = WorkspaceReadBoundary(
            boundary_id=new_workspace_read_boundary_id(),
            root_id=root_id,
            boundary_type=boundary_type,
            path_ref=path_ref,
            description=description,
            status=status,
            priority=priority,
            boundary_attrs=dict(boundary_attrs or {}),
        )
        self._record(
            "workspace_read_boundary_registered",
            objects=[_object("workspace_read_boundary", item.boundary_id, item.to_dict())],
            links=[("boundary_object", item.boundary_id), ("root_object", root_id)],
            object_links=[(item.boundary_id, root_id, "belongs_to_read_root")],
            attrs={"boundary_type": boundary_type},
        )
        return item

    def record_violation(
        self,
        *,
        request_kind: str,
        request_id: str,
        root_id: str,
        relative_path: str,
        violation_type: str,
        message: str,
        severity: str = "high",
        violation_attrs: dict[str, Any] | None = None,
    ) -> WorkspaceReadViolation:
        item = WorkspaceReadViolation(
            violation_id=new_workspace_read_violation_id(),
            request_kind=request_kind,
            request_id=request_id,
            root_id=root_id,
            relative_path=relative_path,
            violation_type=violation_type,
            severity=severity,
            message=message,
            created_at=utc_now_iso(),
            violation_attrs=dict(violation_attrs or {}),
        )
        self._record(
            "workspace_read_violation_recorded",
            objects=[_object("workspace_read_violation", item.violation_id, item.to_dict())],
            links=[
                ("violation_object", item.violation_id),
                ("request_object", request_id),
                ("root_object", root_id),
            ],
            object_links=[(item.violation_id, request_id, "belongs_to_request")],
            attrs={
                "violation_type": violation_type,
                "severity": severity,
            },
        )
        return item

    def list_workspace_files(
        self,
        *,
        root: WorkspaceReadRoot,
        relative_path: str = ".",
        pattern: str | None = None,
        recursive: bool = False,
        max_results: int = 200,
        session_id: str | None = None,
        turn_id: str | None = None,
        process_instance_id: str | None = None,
        permission_request_id: str | None = None,
        session_permission_resolution_id: str | None = None,
    ) -> WorkspaceFileListResult:
        request = WorkspaceFileListRequest(
            request_id=new_workspace_file_list_request_id(),
            root_id=root.root_id,
            relative_path=relative_path,
            pattern=pattern,
            recursive=recursive,
            max_results=max_results,
            session_id=session_id,
            turn_id=turn_id,
            process_instance_id=process_instance_id,
            permission_request_id=permission_request_id,
            session_permission_resolution_id=session_permission_resolution_id,
            created_at=utc_now_iso(),
            request_attrs={"read_only": True},
        )
        self._record_request("workspace_file_list_requested", request, "workspace_file_list_request")
        violation_ids: list[str] = []
        entries: list[dict[str, Any]] = []
        truncated = False
        denied = False
        try:
            root_path = normalize_workspace_root(root.root_path)
            target = resolve_workspace_path(root_path, relative_path)
            if not target.exists() or not target.is_dir():
                raise WorkspacePathViolationError("Workspace list target is not a directory")
            iterator = target.rglob("*") if recursive else target.iterdir()
            for child in sorted(iterator, key=lambda path: str(path.relative_to(target))):
                if not is_path_inside_root(child, root_path):
                    continue
                if pattern and not fnmatch.fnmatch(child.name, pattern):
                    continue
                entries.append(
                    {
                        "name": child.name,
                        "relative_path": str(child.relative_to(root_path)),
                        "is_dir": child.is_dir(),
                        "size_bytes": child.stat().st_size if child.is_file() else None,
                    }
                )
                if len(entries) >= max_results:
                    truncated = True
                    break
        except Exception as error:
            denied = True
            violation = self.record_violation(
                request_kind="file_list",
                request_id=request.request_id,
                root_id=root.root_id,
                relative_path=relative_path,
                violation_type=_violation_type(error),
                message=str(error),
                violation_attrs=_request_context_attrs(request),
            )
            violation_ids.append(violation.violation_id)
        result = WorkspaceFileListResult(
            result_id=new_workspace_file_list_result_id(),
            request_id=request.request_id,
            root_id=root.root_id,
            entries=entries,
            total_entries=len(entries),
            truncated=truncated,
            violation_ids=violation_ids,
            created_at=utc_now_iso(),
            result_attrs={
                "denied": denied,
                "read_only": True,
                "relative_path": relative_path,
                **_request_context_attrs(request),
            },
        )
        self._record_result(
            "workspace_file_list_denied" if denied else "workspace_file_list_completed",
            result,
            "workspace_file_list_result",
            request.request_id,
        )
        return result

    def read_workspace_text_file(
        self,
        *,
        root: WorkspaceReadRoot,
        relative_path: str,
        max_bytes: int = 262144,
        max_chars: int = 120000,
        encoding: str = "utf-8",
        allowed_extensions: set[str] | None = None,
        session_id: str | None = None,
        turn_id: str | None = None,
        process_instance_id: str | None = None,
        permission_request_id: str | None = None,
        session_permission_resolution_id: str | None = None,
    ) -> WorkspaceTextFileReadResult:
        request = WorkspaceTextFileReadRequest(
            request_id=new_workspace_text_file_read_request_id(),
            root_id=root.root_id,
            relative_path=relative_path,
            max_bytes=max_bytes,
            max_chars=max_chars,
            encoding=encoding,
            session_id=session_id,
            turn_id=turn_id,
            process_instance_id=process_instance_id,
            permission_request_id=permission_request_id,
            session_permission_resolution_id=session_permission_resolution_id,
            created_at=utc_now_iso(),
            request_attrs={"read_only": True},
        )
        self._record_request(
            "workspace_text_file_read_requested",
            request,
            "workspace_text_file_read_request",
        )
        content = ""
        size_bytes = 0
        truncated = False
        denied = False
        violation_ids: list[str] = []
        try:
            target = resolve_workspace_path(root.root_path, relative_path)
            if not target.exists() or not target.is_file():
                raise WorkspaceTextReadError("Workspace text read target is not a file")
            allowed = {item.casefold() for item in (allowed_extensions or DEFAULT_TEXT_EXTENSIONS)}
            if target.suffix.casefold() not in allowed:
                raise WorkspaceUnsupportedFileError("File extension is not in the read allowlist")
            size_bytes = target.stat().st_size
            if size_bytes > max_bytes:
                raise WorkspaceFileTooLargeError("File exceeds max_bytes")
            data = target.read_bytes()
            if is_binary_bytes(data):
                raise WorkspaceBinaryFileError("Binary file content is rejected")
            try:
                content = data.decode(encoding)
            except UnicodeDecodeError as error:
                raise WorkspaceBinaryFileError("File cannot be decoded as text") from error
            if len(content) > max_chars:
                content = content[:max_chars]
                truncated = True
        except Exception as error:
            denied = True
            content = ""
            violation = self.record_violation(
                request_kind="text_file_read",
                request_id=request.request_id,
                root_id=root.root_id,
                relative_path=relative_path,
                violation_type=_violation_type(error),
                message=str(error),
                violation_attrs=_request_context_attrs(request),
            )
            violation_ids.append(violation.violation_id)
        result = WorkspaceTextFileReadResult(
            result_id=new_workspace_text_file_read_result_id(),
            request_id=request.request_id,
            root_id=root.root_id,
            relative_path=relative_path,
            content=content,
            content_preview=preview_text(content),
            content_hash=hash_content(content) if content else "",
            size_bytes=size_bytes,
            truncated=truncated,
            denied=denied,
            violation_ids=violation_ids,
            created_at=utc_now_iso(),
            result_attrs={"read_only": True, **_request_context_attrs(request)},
        )
        self._record_result(
            "workspace_text_file_read_denied" if denied else "workspace_text_file_read_completed",
            result,
            "workspace_text_file_read_result",
            request.request_id,
        )
        return result

    def summarize_workspace_markdown(
        self,
        *,
        root: WorkspaceReadRoot,
        relative_path: str,
        max_bytes: int = 262144,
        max_chars: int = 120000,
        summary_style: str = "outline_preview",
        session_id: str | None = None,
        turn_id: str | None = None,
        process_instance_id: str | None = None,
    ) -> WorkspaceMarkdownSummaryResult:
        request = WorkspaceMarkdownSummaryRequest(
            request_id=new_workspace_markdown_summary_request_id(),
            root_id=root.root_id,
            relative_path=relative_path,
            max_bytes=max_bytes,
            max_chars=max_chars,
            summary_style=summary_style,
            session_id=session_id,
            turn_id=turn_id,
            process_instance_id=process_instance_id,
            created_at=utc_now_iso(),
            request_attrs={"read_only": True, "uses_llm": False},
        )
        self._record_request(
            "workspace_markdown_summary_requested",
            request,
            "workspace_markdown_summary_request",
        )
        violation_ids: list[str] = []
        denied = False
        title: str | None = None
        headings: list[str] = []
        preview = ""
        summary = ""
        content_hash = ""
        truncated = False
        try:
            if Path(relative_path).suffix.casefold() not in {".md", ".markdown"}:
                raise WorkspaceUnsupportedFileError("Markdown summary requires .md or .markdown")
            read_result = self.read_workspace_text_file(
                root=root,
                relative_path=relative_path,
                max_bytes=max_bytes,
                max_chars=max_chars,
                allowed_extensions={".md", ".markdown"},
                session_id=session_id,
                turn_id=turn_id,
                process_instance_id=process_instance_id,
            )
            if read_result.denied:
                raise WorkspaceTextReadError("Markdown source read was denied")
            headings = extract_markdown_headings(read_result.content)
            title = _title_from_markdown(relative_path, headings)
            preview = read_result.content_preview
            content_hash = read_result.content_hash
            truncated = read_result.truncated
            summary = _deterministic_markdown_summary(title, headings, preview)
        except Exception as error:
            denied = True
            violation = self.record_violation(
                request_kind="markdown_summary",
                request_id=request.request_id,
                root_id=root.root_id,
                relative_path=relative_path,
                violation_type=_violation_type(error),
                message=str(error),
                violation_attrs=_request_context_attrs(request),
            )
            violation_ids.append(violation.violation_id)
        result = WorkspaceMarkdownSummaryResult(
            result_id=new_workspace_markdown_summary_result_id(),
            request_id=request.request_id,
            root_id=root.root_id,
            relative_path=relative_path,
            title=title,
            heading_outline=headings,
            content_preview=preview,
            summary=summary,
            content_hash=content_hash,
            truncated=truncated,
            denied=denied,
            violation_ids=violation_ids,
            created_at=utc_now_iso(),
            result_attrs={
                "read_only": True,
                "uses_llm": False,
                **_request_context_attrs(request),
            },
        )
        self._record_result(
            "workspace_markdown_summary_denied"
            if denied
            else "workspace_markdown_summary_completed",
            result,
            "workspace_markdown_summary_result",
            request.request_id,
        )
        return result

    def _record_request(self, activity: str, request: Any, object_type: str) -> None:
        self._record(
            activity,
            objects=[_object(object_type, request.request_id, request.to_dict())],
            links=[
                ("request_object", request.request_id),
                ("root_object", request.root_id),
                *_context_links(request),
            ],
            object_links=[(request.request_id, request.root_id, "uses_workspace_read_root")],
            attrs={"request_id": request.request_id, "root_id": request.root_id},
        )

    def _record_result(
        self,
        activity: str,
        result: Any,
        object_type: str,
        request_id: str,
    ) -> None:
        self._record(
            activity,
            objects=[_object(object_type, result.result_id, result.to_dict())],
            links=[
                ("result_object", result.result_id),
                ("request_object", request_id),
                ("root_object", result.root_id),
            ],
            object_links=[(result.result_id, request_id, "belongs_to_request")],
            attrs={
                "result_id": result.result_id,
                "request_id": request_id,
                "violation_count": len(result.violation_ids),
            },
        )

    def _record(
        self,
        activity: str,
        *,
        objects: list[OCELObject],
        links: list[tuple[str, str]],
        object_links: list[tuple[str, str, str]],
        attrs: dict[str, Any],
    ) -> None:
        event = OCELEvent(
            event_id=f"evt:{uuid4()}",
            event_activity=activity,
            event_timestamp=utc_now_iso(),
            event_attrs={
                **attrs,
                "runtime_event_type": activity,
                "source_runtime": "chanta_core",
                "workspace_read_only": True,
            },
        )
        relations = [
            OCELRelation.event_object(event_id=event.event_id, object_id=object_id, qualifier=qualifier)
            for qualifier, object_id in links
            if object_id
        ]
        relations.extend(
            OCELRelation.object_object(source_object_id=source_id, target_object_id=target_id, qualifier=qualifier)
            for source_id, target_id, qualifier in object_links
            if source_id and target_id
        )
        self.trace_service.record_session_ocel_record(
            OCELRecord(event=event, objects=objects, relations=relations)
        )


def _title_from_markdown(relative_path: str, headings: list[str]) -> str:
    for heading in headings:
        if heading.startswith("# "):
            return heading[2:].strip()
    return Path(relative_path).stem


def _deterministic_markdown_summary(
    title: str | None,
    headings: list[str],
    preview: str,
) -> str:
    lines = [f"Title: {title or 'untitled'}"]
    lines.append(f"Heading count: {len(headings)}")
    if headings:
        lines.append("Top headings: " + "; ".join(headings[:5]))
    compact_preview = " ".join(preview.split())
    if compact_preview:
        lines.append("Preview: " + compact_preview[:500])
    return "\n".join(lines)


def _violation_type(error: Exception) -> str:
    if isinstance(error, WorkspacePathViolationError):
        message = str(error).casefold()
        if "absolute" in message:
            return "absolute_path_not_allowed"
        if "traversal" in message:
            return "path_traversal"
        return "outside_workspace"
    if isinstance(error, WorkspaceBinaryFileError):
        return "binary_rejected"
    if isinstance(error, WorkspaceFileTooLargeError):
        return "file_too_large"
    if isinstance(error, WorkspaceUnsupportedFileError):
        return "extension_not_allowed"
    return "read_denied"


def _context_links(request: Any) -> list[tuple[str, str]]:
    links: list[tuple[str, str]] = []
    if request.session_id:
        session_object_id = (
            request.session_id
            if str(request.session_id).startswith("session:")
            else f"session:{request.session_id}"
        )
        links.append(("session_context", session_object_id))
    if request.turn_id:
        links.append(("turn_context", request.turn_id))
    if request.process_instance_id:
        links.append(("process_context", request.process_instance_id))
    if getattr(request, "permission_request_id", None):
        links.append(("permission_request", request.permission_request_id))
    if getattr(request, "session_permission_resolution_id", None):
        links.append(("session_permission_resolution", request.session_permission_resolution_id))
    return links


def _request_context_attrs(request: Any) -> dict[str, Any]:
    return {
        "session_id": request.session_id,
        "turn_id": request.turn_id,
        "process_instance_id": request.process_instance_id,
        "permission_request_id": getattr(request, "permission_request_id", None),
        "session_permission_resolution_id": getattr(
            request, "session_permission_resolution_id", None
        ),
    }


def _object(object_type: str, object_id: str, attrs: dict[str, Any]) -> OCELObject:
    return OCELObject(
        object_id=object_id,
        object_type=object_type,
        object_attrs={
            "object_key": object_id,
            "display_name": object_id,
            **attrs,
        },
    )
