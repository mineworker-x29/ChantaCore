from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import uuid4


READ_ONLY_OBSERVATION_EFFECT = "read_only_observation"
PRIMARY_WORKSPACE_ROOT_ID = "workspace_root:primary"
DEFAULT_EXCLUDED_NAMES = {
    ".git",
    ".venv",
    "__pycache__",
    "node_modules",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "dist",
    "build",
}
DEFAULT_PRIVATE_BOUNDARY_NAMES = frozenset({"private", ".private", "private_boundary", "letters", "Souls"})


@dataclass(frozen=True)
class WorkspaceRootRef:
    root_id: str
    display_name: str
    root_path: str
    canonical_path: str
    source: str
    is_primary: bool
    is_private_boundary: bool
    root_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "root_id": self.root_id,
            "display_name": self.display_name,
            "root_path": self.root_path,
            "canonical_path": self.canonical_path,
            "source": self.source,
            "is_primary": self.is_primary,
            "is_private_boundary": self.is_private_boundary,
            "root_attrs": dict(self.root_attrs),
        }


@dataclass(frozen=True)
class WorkspacePathResolution:
    input_path: str
    normalized_path: str
    canonical_path: str
    root_id: str | None
    within_workspace: bool
    blocked: bool
    finding_type: str
    reason: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "input_path": self.input_path,
            "normalized_path": self.normalized_path,
            "canonical_path": self.canonical_path,
            "root_id": self.root_id,
            "within_workspace": self.within_workspace,
            "blocked": self.blocked,
            "finding_type": self.finding_type,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class WorkspaceInventoryRequest:
    root_id: str | None = None
    relative_path: str = "."
    max_depth: int = 3
    max_entries: int = 500
    include_hidden: bool = False
    include_ignored: bool = False
    include_files: bool = True
    include_dirs: bool = True

    def normalized(self) -> "WorkspaceInventoryRequest":
        return WorkspaceInventoryRequest(
            root_id=self.root_id,
            relative_path=self.relative_path or ".",
            max_depth=max(0, int(self.max_depth)),
            max_entries=max(0, int(self.max_entries)),
            include_hidden=bool(self.include_hidden),
            include_ignored=bool(self.include_ignored),
            include_files=bool(self.include_files),
            include_dirs=bool(self.include_dirs),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "root_id": self.root_id,
            "relative_path": self.relative_path,
            "max_depth": self.max_depth,
            "max_entries": self.max_entries,
            "include_hidden": self.include_hidden,
            "include_ignored": self.include_ignored,
            "include_files": self.include_files,
            "include_dirs": self.include_dirs,
        }


@dataclass(frozen=True)
class WorkspaceInventoryEntry:
    entry_id: str
    root_id: str
    relative_path: str
    entry_type: str
    suffix: str
    size_bytes: int | None
    modified_at: str | None
    depth: int
    is_hidden: bool
    is_excluded: bool
    exclusion_reason: str | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "entry_id": self.entry_id,
            "root_id": self.root_id,
            "relative_path": self.relative_path,
            "entry_type": self.entry_type,
            "suffix": self.suffix,
            "size_bytes": self.size_bytes,
            "modified_at": self.modified_at,
            "depth": self.depth,
            "is_hidden": self.is_hidden,
            "is_excluded": self.is_excluded,
            "exclusion_reason": self.exclusion_reason,
        }


@dataclass(frozen=True)
class WorkspaceInventoryFinding:
    finding_id: str
    finding_type: str
    severity: str
    message: str
    subject_ref: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "finding_type": self.finding_type,
            "severity": self.severity,
            "message": self.message,
            "subject_ref": self.subject_ref,
        }


@dataclass(frozen=True)
class WorkspaceInventoryReport:
    report_id: str
    root_id: str | None
    requested_path: str
    resolved_path: str
    entries: list[WorkspaceInventoryEntry]
    total_entries_seen: int
    total_entries_returned: int
    truncated: bool
    max_depth: int
    max_entries: int
    excluded_count: int
    blocked_count: int
    warnings: list[str]
    evidence_refs: list[str]
    findings: list[WorkspaceInventoryFinding] = field(default_factory=list)
    report_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "report_id": self.report_id,
            "root_id": self.root_id,
            "requested_path": self.requested_path,
            "resolved_path": self.resolved_path,
            "entries": [item.to_dict() for item in self.entries],
            "total_entries_seen": self.total_entries_seen,
            "total_entries_returned": self.total_entries_returned,
            "truncated": self.truncated,
            "max_depth": self.max_depth,
            "max_entries": self.max_entries,
            "excluded_count": self.excluded_count,
            "blocked_count": self.blocked_count,
            "warnings": list(self.warnings),
            "evidence_refs": list(self.evidence_refs),
            "findings": [item.to_dict() for item in self.findings],
            "report_attrs": dict(self.report_attrs),
        }


class SelfWorkspacePathPolicyService:
    def __init__(
        self,
        *,
        workspace_root: str | Path | None = None,
        private_boundary_names: set[str] | frozenset[str] | None = None,
    ) -> None:
        self.workspace_root = Path(workspace_root or Path.cwd()).resolve()
        self.private_boundary_names = frozenset(private_boundary_names or DEFAULT_PRIVATE_BOUNDARY_NAMES)

    def list_workspace_roots(self) -> list[WorkspaceRootRef]:
        return [
            WorkspaceRootRef(
                root_id=PRIMARY_WORKSPACE_ROOT_ID,
                display_name="primary_workspace",
                root_path=str(self.workspace_root),
                canonical_path=str(self.workspace_root),
                source="cwd",
                is_primary=True,
                is_private_boundary=False,
                root_attrs={
                    "full_path_redaction_required": True,
                    "metadata_only": True,
                    "effect_type": READ_ONLY_OBSERVATION_EFFECT,
                },
            )
        ]

    def resolve_path(self, input_path: str, root_id: str | None = None) -> WorkspacePathResolution:
        selected_root = self._select_root(root_id)
        raw_input = str(input_path or ".")
        input_candidate = Path(raw_input)
        normalized_path = _normalize_relative_display(raw_input)
        if input_candidate.is_absolute():
            canonical = input_candidate.resolve(strict=False)
            return self._blocked(
                input_path=raw_input,
                normalized_path=normalized_path,
                canonical_path=str(canonical),
                root_id=selected_root.root_id,
                finding_type="absolute_path_not_allowed",
                reason="Absolute paths are blocked for self-workspace awareness.",
                within_workspace=_is_relative_to(canonical, self.workspace_root),
            )
        if any(part == ".." for part in input_candidate.parts):
            return self._blocked(
                input_path=raw_input,
                normalized_path=normalized_path,
                canonical_path=str((self.workspace_root / input_candidate).resolve(strict=False)),
                root_id=selected_root.root_id,
                finding_type="path_traversal",
                reason="Path traversal is blocked.",
            )
        if self._contains_private_boundary_part(input_candidate):
            return self._blocked(
                input_path=raw_input,
                normalized_path=normalized_path,
                canonical_path=str((self.workspace_root / input_candidate).resolve(strict=False)),
                root_id=selected_root.root_id,
                finding_type="private_boundary",
                reason="The requested path crosses a configured private boundary.",
            )
        canonical = (self.workspace_root / input_candidate).resolve(strict=False)
        if not _is_relative_to(canonical, self.workspace_root):
            return self._blocked(
                input_path=raw_input,
                normalized_path=normalized_path,
                canonical_path=str(canonical),
                root_id=selected_root.root_id,
                finding_type="outside_workspace",
                reason="The resolved path is outside the workspace root.",
            )
        if self._contains_symlink(input_candidate):
            return self._blocked(
                input_path=raw_input,
                normalized_path=normalized_path,
                canonical_path=str(canonical),
                root_id=selected_root.root_id,
                finding_type="symlink_blocked",
                reason="Symlink traversal is blocked by default.",
            )
        return WorkspacePathResolution(
            input_path=raw_input,
            normalized_path=normalized_path,
            canonical_path=str(canonical),
            root_id=selected_root.root_id,
            within_workspace=True,
            blocked=False,
            finding_type="allowed",
            reason="Path is within workspace boundary.",
        )

    def assert_readonly_metadata_allowed(self, resolution: WorkspacePathResolution) -> WorkspacePathResolution:
        if resolution.blocked:
            raise PermissionError(resolution.reason)
        return resolution

    def _select_root(self, root_id: str | None) -> WorkspaceRootRef:
        root = self.list_workspace_roots()[0]
        if root_id and root_id != root.root_id:
            raise ValueError(f"Unknown workspace root id: {root_id}")
        return root

    def _blocked(
        self,
        *,
        input_path: str,
        normalized_path: str,
        canonical_path: str,
        root_id: str,
        finding_type: str,
        reason: str,
        within_workspace: bool = False,
    ) -> WorkspacePathResolution:
        return WorkspacePathResolution(
            input_path=input_path,
            normalized_path=normalized_path,
            canonical_path=canonical_path,
            root_id=root_id,
            within_workspace=within_workspace,
            blocked=True,
            finding_type=finding_type,
            reason=reason,
        )

    def _contains_private_boundary_part(self, path: Path) -> bool:
        return any(part in self.private_boundary_names for part in path.parts)

    def _contains_symlink(self, path: Path) -> bool:
        current = self.workspace_root
        for part in path.parts:
            current = current / part
            try:
                if current.is_symlink():
                    return True
            except OSError:
                return True
        return False


class SelfWorkspaceInventoryService:
    def __init__(self, *, path_policy_service: SelfWorkspacePathPolicyService | None = None) -> None:
        self.path_policy_service = path_policy_service or SelfWorkspacePathPolicyService()

    def build_inventory(self, request: WorkspaceInventoryRequest) -> WorkspaceInventoryReport:
        normalized_request = request.normalized()
        resolution = self.path_policy_service.resolve_path(
            normalized_request.relative_path,
            root_id=normalized_request.root_id,
        )
        if resolution.blocked:
            finding = WorkspaceInventoryFinding(
                finding_id=f"workspace_inventory_finding:{uuid4()}",
                finding_type=resolution.finding_type,
                severity="high",
                message=resolution.reason,
                subject_ref=resolution.normalized_path,
            )
            return WorkspaceInventoryReport(
                report_id=f"workspace_inventory_report:{uuid4()}",
                root_id=resolution.root_id,
                requested_path=normalized_request.relative_path,
                resolved_path=resolution.normalized_path,
                entries=[],
                total_entries_seen=0,
                total_entries_returned=0,
                truncated=False,
                max_depth=normalized_request.max_depth,
                max_entries=normalized_request.max_entries,
                excluded_count=0,
                blocked_count=1,
                warnings=[resolution.reason],
                evidence_refs=[resolution.finding_type],
                findings=[finding],
                report_attrs={
                    "effect_type": READ_ONLY_OBSERVATION_EFFECT,
                    "metadata_only": True,
                    "file_content_read": False,
                    "content_hash_calculated": False,
                },
            )
        root = self.path_policy_service.workspace_root
        start = Path(resolution.canonical_path)
        entries: list[WorkspaceInventoryEntry] = []
        stats = {"seen": 0, "excluded": 0, "truncated": False}
        self._walk(start, root, normalized_request, 0, entries, stats)
        return WorkspaceInventoryReport(
            report_id=f"workspace_inventory_report:{uuid4()}",
            root_id=resolution.root_id,
            requested_path=normalized_request.relative_path,
            resolved_path=resolution.normalized_path,
            entries=entries,
            total_entries_seen=stats["seen"],
            total_entries_returned=len(entries),
            truncated=bool(stats["truncated"]),
            max_depth=normalized_request.max_depth,
            max_entries=normalized_request.max_entries,
            excluded_count=stats["excluded"],
            blocked_count=0,
            warnings=[],
            evidence_refs=[resolution.root_id or PRIMARY_WORKSPACE_ROOT_ID, "metadata_only_inventory"],
            report_attrs={
                "effect_type": READ_ONLY_OBSERVATION_EFFECT,
                "metadata_only": True,
                "file_content_read": False,
                "content_hash_calculated": False,
                "ast_parsed": False,
                "content_search_used": False,
            },
        )

    def _walk(
        self,
        path: Path,
        root: Path,
        request: WorkspaceInventoryRequest,
        depth: int,
        entries: list[WorkspaceInventoryEntry],
        stats: dict[str, int | bool],
    ) -> None:
        if bool(stats["truncated"]) or depth >= request.max_depth:
            return
        try:
            children = sorted(path.iterdir(), key=lambda item: item.name.casefold())
        except OSError:
            stats["excluded"] = int(stats["excluded"]) + 1
            return
        for child in children:
            if bool(stats["truncated"]):
                return
            stats["seen"] = int(stats["seen"]) + 1
            is_hidden = child.name.startswith(".")
            exclusion_reason = _exclusion_reason(
                child,
                is_hidden,
                request,
                self.path_policy_service.private_boundary_names,
            )
            if exclusion_reason:
                stats["excluded"] = int(stats["excluded"]) + 1
                continue
            entry_type = _entry_type(child)
            child_depth = depth + 1
            should_include = (
                (entry_type == "directory" and request.include_dirs)
                or (entry_type in {"file", "symlink", "other"} and request.include_files)
            )
            if should_include:
                if len(entries) >= request.max_entries:
                    stats["truncated"] = True
                    return
                entries.append(_entry_for(child, root, entry_type, child_depth, is_hidden))
            if entry_type == "directory" and child_depth < request.max_depth:
                self._walk(child, root, request, child_depth, entries, stats)


class SelfWorkspaceAwarenessSkillService:
    def __init__(self, *, path_policy_service: SelfWorkspacePathPolicyService | None = None) -> None:
        self.path_policy_service = path_policy_service or SelfWorkspacePathPolicyService()
        self.inventory_service = SelfWorkspaceInventoryService(path_policy_service=self.path_policy_service)

    def verify_path(self, input_path: str, root_id: str | None = None) -> WorkspacePathResolution:
        return self.path_policy_service.resolve_path(input_path, root_id=root_id)

    def inventory_workspace(self, request: WorkspaceInventoryRequest) -> WorkspaceInventoryReport:
        return self.inventory_service.build_inventory(request)


def _entry_for(path: Path, root: Path, entry_type: str, depth: int, is_hidden: bool) -> WorkspaceInventoryEntry:
    try:
        stat = path.lstat()
        size_bytes = stat.st_size if entry_type == "file" else None
        modified_at = datetime.fromtimestamp(stat.st_mtime, tz=UTC).isoformat().replace("+00:00", "Z")
    except OSError:
        size_bytes = None
        modified_at = None
    return WorkspaceInventoryEntry(
        entry_id=f"workspace_inventory_entry:{uuid4()}",
        root_id=PRIMARY_WORKSPACE_ROOT_ID,
        relative_path=path.relative_to(root).as_posix(),
        entry_type=entry_type,
        suffix=path.suffix,
        size_bytes=size_bytes,
        modified_at=modified_at,
        depth=depth,
        is_hidden=is_hidden,
        is_excluded=False,
        exclusion_reason=None,
    )


def _entry_type(path: Path) -> str:
    if path.is_symlink():
        return "symlink"
    if path.is_dir():
        return "directory"
    if path.is_file():
        return "file"
    return "other"


def _exclusion_reason(
    path: Path,
    is_hidden: bool,
    request: WorkspaceInventoryRequest,
    private_boundary_names: frozenset[str],
) -> str | None:
    if path.name in private_boundary_names:
        return "private_boundary_excluded"
    if is_hidden and not request.include_hidden:
        return "hidden_excluded"
    if path.name in DEFAULT_EXCLUDED_NAMES and not request.include_ignored:
        return "noisy_directory_excluded" if path.is_dir() else "ignored_path_excluded"
    return None


def _normalize_relative_display(path: str) -> str:
    raw = str(Path(path or "."))
    return "." if raw == "" else raw.replace("\\", "/")


def _is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True
