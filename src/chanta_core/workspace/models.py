from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class WorkspaceReadRoot:
    root_id: str
    root_path: str
    root_name: str | None
    status: str
    created_at: str
    updated_at: str
    root_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "root_id": self.root_id,
            "root_path": self.root_path,
            "root_name": self.root_name,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "root_attrs": dict(self.root_attrs),
        }


@dataclass(frozen=True)
class WorkspaceReadBoundary:
    boundary_id: str
    root_id: str
    boundary_type: str
    path_ref: str
    description: str | None
    status: str
    priority: int | None
    boundary_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "boundary_id": self.boundary_id,
            "root_id": self.root_id,
            "boundary_type": self.boundary_type,
            "path_ref": self.path_ref,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "boundary_attrs": dict(self.boundary_attrs),
        }


@dataclass(frozen=True)
class WorkspaceFileListRequest:
    request_id: str
    root_id: str
    relative_path: str
    pattern: str | None
    recursive: bool
    max_results: int
    session_id: str | None
    turn_id: str | None
    process_instance_id: str | None
    permission_request_id: str | None
    session_permission_resolution_id: str | None
    created_at: str
    request_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {**self.__dict__, "request_attrs": dict(self.request_attrs)}


@dataclass(frozen=True)
class WorkspaceFileListResult:
    result_id: str
    request_id: str
    root_id: str
    entries: list[dict[str, Any]]
    total_entries: int
    truncated: bool
    violation_ids: list[str]
    created_at: str
    result_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "result_id": self.result_id,
            "request_id": self.request_id,
            "root_id": self.root_id,
            "entries": [dict(item) for item in self.entries],
            "total_entries": self.total_entries,
            "truncated": self.truncated,
            "violation_ids": list(self.violation_ids),
            "created_at": self.created_at,
            "result_attrs": dict(self.result_attrs),
        }


@dataclass(frozen=True)
class WorkspaceTextFileReadRequest:
    request_id: str
    root_id: str
    relative_path: str
    max_bytes: int
    max_chars: int
    encoding: str
    session_id: str | None
    turn_id: str | None
    process_instance_id: str | None
    permission_request_id: str | None
    session_permission_resolution_id: str | None
    created_at: str
    request_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {**self.__dict__, "request_attrs": dict(self.request_attrs)}


@dataclass(frozen=True)
class WorkspaceTextFileReadResult:
    result_id: str
    request_id: str
    root_id: str
    relative_path: str
    content: str
    content_preview: str
    content_hash: str
    size_bytes: int
    truncated: bool
    denied: bool
    violation_ids: list[str]
    created_at: str
    result_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "result_id": self.result_id,
            "request_id": self.request_id,
            "root_id": self.root_id,
            "relative_path": self.relative_path,
            "content": self.content,
            "content_preview": self.content_preview,
            "content_hash": self.content_hash,
            "size_bytes": self.size_bytes,
            "truncated": self.truncated,
            "denied": self.denied,
            "violation_ids": list(self.violation_ids),
            "created_at": self.created_at,
            "result_attrs": dict(self.result_attrs),
        }


@dataclass(frozen=True)
class WorkspaceMarkdownSummaryRequest:
    request_id: str
    root_id: str
    relative_path: str
    max_bytes: int
    max_chars: int
    summary_style: str
    session_id: str | None
    turn_id: str | None
    process_instance_id: str | None
    created_at: str
    request_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {**self.__dict__, "request_attrs": dict(self.request_attrs)}


@dataclass(frozen=True)
class WorkspaceMarkdownSummaryResult:
    result_id: str
    request_id: str
    root_id: str
    relative_path: str
    title: str | None
    heading_outline: list[str]
    content_preview: str
    summary: str
    content_hash: str
    truncated: bool
    denied: bool
    violation_ids: list[str]
    created_at: str
    result_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "result_id": self.result_id,
            "request_id": self.request_id,
            "root_id": self.root_id,
            "relative_path": self.relative_path,
            "title": self.title,
            "heading_outline": list(self.heading_outline),
            "content_preview": self.content_preview,
            "summary": self.summary,
            "content_hash": self.content_hash,
            "truncated": self.truncated,
            "denied": self.denied,
            "violation_ids": list(self.violation_ids),
            "created_at": self.created_at,
            "result_attrs": dict(self.result_attrs),
        }


@dataclass(frozen=True)
class WorkspaceReadViolation:
    violation_id: str
    request_kind: str
    request_id: str
    root_id: str
    relative_path: str
    violation_type: str
    severity: str
    message: str
    created_at: str
    violation_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "violation_id": self.violation_id,
            "request_kind": self.request_kind,
            "request_id": self.request_id,
            "root_id": self.root_id,
            "relative_path": self.relative_path,
            "violation_type": self.violation_type,
            "severity": self.severity,
            "message": self.message,
            "created_at": self.created_at,
            "violation_attrs": dict(self.violation_attrs),
        }
