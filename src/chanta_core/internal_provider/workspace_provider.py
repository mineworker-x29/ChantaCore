from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from fnmatch import fnmatch
from pathlib import Path
import time
from typing import Any

from chanta_core.internal_provider.contract import InternalProviderContract, InternalProviderContractReportService
from chanta_core.internal_provider.registry import (
    InternalProviderCapabilitySurface,
    InternalProviderRegistry,
    InternalProviderRegistrySkillService,
    InternalProviderRegistryReportService,
)

WORKSPACE_PROVIDER_VERSION = "v0.24.2"
WORKSPACE_PROVIDER_VERSION_NAME = "Read-only Workspace Provider"
WORKSPACE_PROVIDER_KOREAN_NAME = "읽기 전용 워크스페이스 Provider"
WORKSPACE_PROVIDER_ID = "workspace_read_provider"
WORKSPACE_PROVIDER_LAYER = "internal_provider"
WORKSPACE_PROVIDER_STATE = "workspace_tree_metadata_observed"
WORKSPACE_PROVIDER_NEXT_STEP = "v0.24.3 Repository Search / File Read Provider"

WORKSPACE_PROVIDER_OBJECT_TYPES = [
    "workspace_read_provider_policy",
    "workspace_root_descriptor",
    "workspace_ignore_pattern",
    "workspace_ignore_policy",
    "workspace_path_sanitization_policy",
    "workspace_tree_request",
    "workspace_directory_node",
    "workspace_file_metadata",
    "workspace_tree_snapshot",
    "workspace_metadata_summary",
    "workspace_read_finding",
    "workspace_read_report",
    "internal_provider_registry",
    "internal_provider_capability_surface",
    "execution_envelope",
    "pig_report",
    "ocpx_projection",
]

WORKSPACE_PROVIDER_EVENT_TYPES = [
    "workspace_read_requested",
    "workspace_provider_policy_created",
    "workspace_roots_discovered",
    "workspace_ignore_policy_created",
    "workspace_path_sanitization_policy_created",
    "workspace_tree_traversed",
    "workspace_file_metadata_observed",
    "workspace_tree_snapshot_created",
    "workspace_metadata_summary_created",
    "workspace_read_report_created",
    "workspace_read_warning_created",
    "workspace_read_blocked",
]

WORKSPACE_PROVIDER_RELATION_TYPES = [
    "uses_workspace_read_provider",
    "uses_internal_provider_registry",
    "applies_workspace_read_policy",
    "applies_workspace_ignore_policy",
    "applies_path_sanitization_policy",
    "observes_workspace_root",
    "observes_workspace_directory",
    "observes_file_metadata",
    "summarizes_workspace_metadata",
    "masks_secret_like_path",
    "sanitizes_private_path",
    "skips_ignored_path",
    "skips_hidden_path",
    "does_not_follow_symlink",
    "not_file_content_read",
    "not_file_excerpt_read",
    "not_repository_searched",
    "not_local_command_executed",
    "not_external_runtime_touched",
    "prevents_credential_exposure",
    "prepares_repository_search_provider",
    "defers_repository_search_execution_to_v0_24_3",
    "defers_file_read_execution_to_v0_24_3",
    "defers_local_runtime_execution_to_later_v0_24",
    "defers_general_agent_usability_to_v0_25",
    "visible_in_workbench_future",
    "recorded_in_envelope",
    "derived_from_internal_provider_registry",
]

WORKSPACE_PROVIDER_EFFECT_TYPES = [
    "read_only_observation",
    "workspace_tree_observed",
    "workspace_metadata_observed",
    "state_candidate_created",
]

WORKSPACE_PROVIDER_FORBIDDEN_EFFECT_TYPES = [
    "workspace_file_read_executed",
    "file_content_extracted",
    "file_excerpt_read",
    "repository_search_executed",
    "local_command_candidate_created",
    "local_command_executed",
    "bounded_local_command_executed",
    "unrestricted_shell_executed",
    "network_accessed",
    "package_installed",
    "destructive_command_executed",
    "external_runtime_touched",
    "external_control_dispatched",
    "credential_exposed",
    "raw_secret_output",
    "external_provider_called",
]


def _utc_now() -> str:
    return datetime.fromtimestamp(time.time(), timezone.utc).isoformat().replace("+00:00", "Z")


def _model_dict(value: Any) -> dict[str, Any]:
    return asdict(value)


@dataclass
class WorkspaceReadProviderPolicy:
    policy_id: str = "workspace_read_provider_policy:v0.24.2"
    version: str = WORKSPACE_PROVIDER_VERSION
    provider_id: str = WORKSPACE_PROVIDER_ID
    read_only: bool = True
    file_content_read_enabled: bool = False
    file_excerpt_read_enabled: bool = False
    repository_search_enabled: bool = False
    local_command_execution_enabled: bool = False
    follow_symlinks: bool = False
    include_hidden_files_default: bool = False
    include_ignored_files_default: bool = False
    max_depth_default: int = 4
    max_entries_default: int = 2000
    max_file_size_metadata_only: int | None = None
    private_path_sanitization_required: bool = True
    credential_path_masking_required: bool = True
    raw_secret_output_forbidden: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class WorkspaceRootDescriptor:
    root_id: str
    root_name: str
    root_path_ref: dict[str, Any]
    sanitized_root_label: str
    root_kind: str
    exists_declared: bool | None
    resolved_without_following_symlink: bool
    allowed_for_workspace_observation: bool
    private_full_path_output: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class WorkspaceIgnorePattern:
    pattern_id: str
    pattern: str
    pattern_type: str
    reason: str
    source: str
    enabled: bool = True

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class WorkspaceIgnorePolicy:
    policy_id: str = "workspace_ignore_policy:v0.24.2"
    ignore_patterns: list[WorkspaceIgnorePattern] = field(default_factory=list)
    default_ignored_dirs: list[str] = field(
        default_factory=lambda: [
            ".git",
            ".venv",
            "venv",
            "node_modules",
            "__pycache__",
            ".pytest_cache",
            ".mypy_cache",
            ".ruff_cache",
            ".pytest-tmp",
            "dist",
            "build",
            "data",
            "letters",
            "references",
        ]
    )
    secret_like_patterns: list[str] = field(
        default_factory=lambda: [
            ".env",
            "*.pem",
            "*.key",
            "id_rsa",
            "secrets.*",
            "credentials.*",
            "token*",
        ]
    )
    apply_before_output: bool = True
    include_ignored_files: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            **_model_dict(self),
            "ignore_patterns": [item.to_dict() for item in self.ignore_patterns],
        }


@dataclass
class WorkspacePathSanitizationPolicy:
    policy_id: str = "workspace_path_sanitization_policy:v0.24.2"
    sanitize_private_full_paths: bool = True
    show_relative_paths_only: bool = True
    mask_home_directory: bool = True
    mask_user_name: bool = True
    mask_drive_root_if_needed: bool = True
    mask_secret_like_paths: bool = True
    max_path_display_chars: int = 240
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class WorkspaceTreeRequest:
    root_ids: list[str] = field(default_factory=list)
    max_depth: int | None = None
    max_entries: int | None = None
    include_hidden_files: bool = False
    include_ignored_files: bool = False
    include_file_metadata: bool = True
    include_directory_metadata: bool = True
    include_file_content: bool = False
    include_file_excerpt: bool = False
    follow_symlinks: bool = False
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    strictness: str = "standard"

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class WorkspaceDirectoryNode:
    node_id: str
    root_id: str
    relative_path: str
    sanitized_path: str
    depth: int
    child_directory_count: int
    child_file_count: int
    ignored: bool
    hidden: bool
    symlink: bool
    traversal_performed: bool
    file_content_read: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class WorkspaceFileMetadata:
    metadata_id: str
    root_id: str
    relative_path: str
    sanitized_path: str
    extension: str | None
    file_kind: str
    size_bytes: int | None
    modified_time_ref: str | None
    ignored: bool
    hidden: bool
    symlink: bool
    secret_like: bool
    binary_like: bool
    generated_like: bool
    file_content_read: bool = False
    file_excerpt_read: bool = False
    raw_secret_output: bool = False
    private_full_path_output: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class WorkspaceTreeSnapshot:
    snapshot_id: str
    created_at: str
    request: WorkspaceTreeRequest
    policy: WorkspaceReadProviderPolicy
    roots: list[WorkspaceRootDescriptor]
    directories: list[WorkspaceDirectoryNode]
    files: list[WorkspaceFileMetadata]
    ignored_count: int
    hidden_count: int
    secret_like_count: int
    binary_like_count: int
    generated_like_count: int
    total_directory_count: int
    total_file_count: int
    truncated: bool
    truncation_reason: str | None
    snapshot_status: str
    version: str = WORKSPACE_PROVIDER_VERSION
    provider_invocation_performed: bool = True
    file_content_read_performed: bool = False
    repository_search_performed: bool = False
    local_command_executed: bool = False
    external_runtime_touched: bool = False
    credential_exposed: bool = False
    raw_secret_output: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            **_model_dict(self),
            "request": self.request.to_dict(),
            "policy": self.policy.to_dict(),
            "roots": [item.to_dict() for item in self.roots],
            "directories": [item.to_dict() for item in self.directories],
            "files": [item.to_dict() for item in self.files],
        }


@dataclass
class WorkspaceMetadataSummary:
    summary_id: str
    snapshot_id: str
    root_count: int
    directory_count: int
    file_count: int
    extension_counts: dict[str, int]
    file_kind_counts: dict[str, int]
    largest_files: list[dict[str, Any]]
    secret_like_files_masked_count: int
    ignored_count: int
    hidden_count: int
    truncated: bool
    summary_status: str
    raw_file_content_included: bool = False
    private_full_paths_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class WorkspaceReadFinding:
    finding_id: str
    severity: str
    finding_type: str
    message: str
    path_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class WorkspaceReadReport:
    report_id: str
    created_at: str
    request: WorkspaceTreeRequest
    snapshot: WorkspaceTreeSnapshot
    summary: WorkspaceMetadataSummary
    findings: list[WorkspaceReadFinding]
    report_status: str
    ready_for_v0_24_3: bool
    provider_invocation_performed: bool
    workspace_tree_observed: bool
    workspace_metadata_observed: bool
    version: str = WORKSPACE_PROVIDER_VERSION
    ready_for_v0_25: bool = False
    file_content_read_performed: bool = False
    file_excerpt_read_performed: bool = False
    repository_search_performed: bool = False
    local_command_executed: bool = False
    external_provider_adapter_implemented: bool = False
    schumpeter_split_introduced: bool = False
    credential_exposed: bool = False
    raw_secret_output: bool = False
    llm_judge_used: bool = False
    next_required_step: str = WORKSPACE_PROVIDER_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = (
        "Valid until workspace layout, ignore policy, sanitization policy, or provider policy changes."
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            **_model_dict(self),
            "request": self.request.to_dict(),
            "snapshot": self.snapshot.to_dict(),
            "summary": self.summary.to_dict(),
            "findings": [item.to_dict() for item in self.findings],
        }


class WorkspaceProviderContractSourceService:
    def load_internal_provider_contract(self) -> InternalProviderContract:
        return InternalProviderContractReportService().build_report().contract

    def load_provider_registry(self) -> InternalProviderRegistry:
        return InternalProviderRegistryReportService().build_report().registry

    def load_workspace_provider_surface(self) -> InternalProviderCapabilitySurface | None:
        registry = self.load_provider_registry()
        for surface in registry.capability_surfaces:
            if surface.provider_type == WORKSPACE_PROVIDER_ID:
                return surface
        return None


class WorkspaceReadProviderSkillService:
    def list_skill_contracts(self) -> list[dict[str, Any]]:
        registry_skills = {
            item["skill_id"]: dict(item)
            for item in InternalProviderRegistrySkillService().list_skill_contracts()
        }
        workspace_skill = registry_skills.get("skill:workspace_read_provider_view")
        if workspace_skill:
            workspace_skill.update(
                {
                    "status": "implemented",
                    "implemented": True,
                    "stub": False,
                    "contract_only": False,
                    "workspace_tree_metadata_only": True,
                    "file_content_read_enabled": False,
                    "repository_search_enabled": False,
                    "local_command_execution_enabled": False,
                }
            )
        return list(registry_skills.values())


class WorkspaceReadPolicyService:
    def build_policy(self) -> WorkspaceReadProviderPolicy:
        return WorkspaceReadProviderPolicy(
            evidence_refs=[{"type": "provider_registry", "id": "internal_provider_registry:v0.24.1"}]
        )


class WorkspaceIgnorePolicyService:
    def build_ignore_policy(self) -> WorkspaceIgnorePolicy:
        policy = WorkspaceIgnorePolicy(
            evidence_refs=[{"type": "default_policy", "id": "workspace_ignore_defaults:v0.24.2"}]
        )
        patterns: list[WorkspaceIgnorePattern] = []
        for name in policy.default_ignored_dirs:
            patterns.append(
                WorkspaceIgnorePattern(
                    pattern_id=f"workspace_ignore_pattern:{name}",
                    pattern=name,
                    pattern_type="directory",
                    reason="Default noisy or private workspace directory.",
                    source="default_policy",
                )
            )
        for pattern in policy.secret_like_patterns:
            patterns.append(
                WorkspaceIgnorePattern(
                    pattern_id=f"workspace_ignore_pattern:secret:{pattern}",
                    pattern=pattern,
                    pattern_type="glob",
                    reason="Secret-looking path must be masked or excluded.",
                    source="default_policy",
                )
            )
        policy.ignore_patterns = patterns
        return policy

    def should_ignore_path(self, path: Path, policy: WorkspaceIgnorePolicy | None = None) -> bool:
        policy = policy or self.build_ignore_policy()
        if path.name.lower() in {name.lower() for name in policy.default_ignored_dirs}:
            return True
        return self.detect_secret_like_path(path, policy)

    def detect_secret_like_path(self, path: Path, policy: WorkspaceIgnorePolicy | None = None) -> bool:
        policy = policy or self.build_ignore_policy()
        name = path.name.lower()
        return any(fnmatch(name, pattern.lower()) for pattern in policy.secret_like_patterns)


class WorkspacePathSanitizationService:
    def __init__(self, policy: WorkspacePathSanitizationPolicy | None = None) -> None:
        self.policy = policy or WorkspacePathSanitizationPolicy()

    def build_policy(self) -> WorkspacePathSanitizationPolicy:
        return self.policy

    def sanitize_root(self, path: Path) -> str:
        return "workspace_root"

    def sanitize_path(self, path: Path | str) -> str:
        text = str(path).replace("\\", "/")
        if text in {"", "."}:
            sanitized = "."
        else:
            sanitized = text
        parts = []
        for part in sanitized.split("/"):
            if self.detect_secret_like_path(part):
                parts.append("[secret-like]")
            elif part:
                parts.append(part)
        sanitized = "/".join(parts) or "."
        if len(sanitized) > self.policy.max_path_display_chars:
            sanitized = "..." + sanitized[-(self.policy.max_path_display_chars - 3) :]
        return sanitized

    def detect_secret_like_path(self, path: Path | str) -> bool:
        name = Path(str(path)).name.lower()
        patterns = WorkspaceIgnorePolicy().secret_like_patterns
        return any(fnmatch(name, pattern.lower()) for pattern in patterns)


class WorkspaceRootDiscoveryService:
    def __init__(
        self,
        workspace_root: Path | None = None,
        sanitizer: WorkspacePathSanitizationService | None = None,
    ) -> None:
        self.workspace_root = (workspace_root or Path.cwd()).resolve()
        self.sanitizer = sanitizer or WorkspacePathSanitizationService()

    def discover_declared_roots(self) -> list[WorkspaceRootDescriptor]:
        root = self.workspace_root
        exists = root.exists() and root.is_dir()
        return [
            WorkspaceRootDescriptor(
                root_id="workspace_root",
                root_name="workspace",
                root_path_ref={"type": "workspace_root", "label": self.sanitizer.sanitize_root(root)},
                sanitized_root_label=self.sanitizer.sanitize_root(root),
                root_kind="workspace",
                exists_declared=exists,
                resolved_without_following_symlink=not root.is_symlink(),
                allowed_for_workspace_observation=exists and not root.is_symlink(),
                evidence_refs=[{"type": "workspace_root", "label": self.sanitizer.sanitize_root(root)}],
            )
        ]

    def validate_roots_without_content_read(self, roots: list[WorkspaceRootDescriptor]) -> list[WorkspaceRootDescriptor]:
        return roots


class WorkspaceFileMetadataService:
    _SOURCE_EXTENSIONS = {".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".c", ".cpp", ".h", ".rs", ".go"}
    _DOC_EXTENSIONS = {".md", ".rst", ".txt", ".adoc"}
    _CONFIG_EXTENSIONS = {".toml", ".yaml", ".yml", ".json", ".ini", ".cfg"}
    _BINARY_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf", ".zip", ".sqlite", ".db"}

    def __init__(self, sanitizer: WorkspacePathSanitizationService | None = None) -> None:
        self.sanitizer = sanitizer or WorkspacePathSanitizationService()

    def build_metadata(self, path: Path, root_path: Path, root_id: str, ignored: bool, hidden: bool) -> WorkspaceFileMetadata:
        relative = self._relative(path, root_path)
        symlink = path.is_symlink()
        size_bytes: int | None = None
        modified_time_ref: str | None = None
        try:
            stat_result = path.lstat()
            size_bytes = stat_result.st_size
            modified_time_ref = datetime.fromtimestamp(stat_result.st_mtime, timezone.utc).isoformat().replace("+00:00", "Z")
        except OSError:
            pass
        secret_like = self.sanitizer.detect_secret_like_path(path)
        binary_like = path.suffix.lower() in self._BINARY_EXTENSIONS
        generated_like = any(part in {"dist", "build", "__pycache__"} for part in path.parts)
        return WorkspaceFileMetadata(
            metadata_id=f"workspace_file_metadata:{root_id}:{self.sanitizer.sanitize_path(relative)}",
            root_id=root_id,
            relative_path=relative,
            sanitized_path=self.sanitizer.sanitize_path(relative),
            extension=path.suffix.lower() or None,
            file_kind=self.classify_file_kind(path, secret_like, binary_like, generated_like),
            size_bytes=size_bytes,
            modified_time_ref=modified_time_ref,
            ignored=ignored,
            hidden=hidden,
            symlink=symlink,
            secret_like=secret_like,
            binary_like=binary_like,
            generated_like=generated_like,
            evidence_refs=[{"type": "filesystem_metadata", "path": self.sanitizer.sanitize_path(relative)}],
        )

    def classify_file_kind(self, path: Path, secret_like: bool, binary_like: bool, generated_like: bool) -> str:
        name = path.name.lower()
        suffix = path.suffix.lower()
        if secret_like:
            return "secret_like"
        if generated_like:
            return "generated"
        if binary_like:
            return "binary"
        if name.startswith("test_") or "_test" in name or "/tests/" in str(path).replace("\\", "/"):
            return "test"
        if suffix in self._CONFIG_EXTENSIONS or name in {"dockerfile", "makefile"}:
            return "config"
        if suffix in self._DOC_EXTENSIONS:
            return "docs"
        if suffix in self._SOURCE_EXTENSIONS:
            return "source"
        return "unknown"

    def _relative(self, path: Path, root_path: Path) -> str:
        try:
            return path.relative_to(root_path).as_posix()
        except ValueError:
            return path.name


class WorkspaceTreeTraversalService:
    def __init__(
        self,
        metadata_service: WorkspaceFileMetadataService | None = None,
        workspace_root: Path | None = None,
    ) -> None:
        self.metadata_service = metadata_service or WorkspaceFileMetadataService()
        self.workspace_root = (workspace_root or Path.cwd()).resolve()
        self._ignored_count = 0
        self._hidden_count = 0
        self._secret_like_count = 0

    def build_tree_snapshot(
        self,
        request: WorkspaceTreeRequest,
        roots: list[WorkspaceRootDescriptor],
        policy: WorkspaceReadProviderPolicy,
        ignore_policy: WorkspaceIgnorePolicy,
        sanitizer: WorkspacePathSanitizationService,
    ) -> WorkspaceTreeSnapshot:
        max_depth = request.max_depth if request.max_depth is not None else policy.max_depth_default
        max_entries = request.max_entries if request.max_entries is not None else policy.max_entries_default
        directories: list[WorkspaceDirectoryNode] = []
        files: list[WorkspaceFileMetadata] = []
        truncated = False
        truncation_reason: str | None = None
        self._ignored_count = 0
        self._hidden_count = 0
        self._secret_like_count = 0

        root_path = self.workspace_root
        selected_roots = [root for root in roots if not request.root_ids or root.root_id in request.root_ids]
        for root in selected_roots:
            if not root.allowed_for_workspace_observation:
                continue
            if len(directories) + len(files) >= max_entries:
                truncated = True
                truncation_reason = "max_entries_exceeded"
                break
            truncated, truncation_reason = self._visit_directory(
                root_path,
                root_path,
                root.root_id,
                0,
                max_depth,
                max_entries,
                request,
                ignore_policy,
                sanitizer,
                directories,
                files,
            )
            if truncated:
                break

        binary_like_count = sum(1 for item in files if item.binary_like)
        generated_like_count = sum(1 for item in files if item.generated_like)
        status = "warning" if truncated or any(not root.allowed_for_workspace_observation for root in selected_roots) else "observed"
        if request.include_file_content or request.include_file_excerpt:
            status = "blocked"
        return WorkspaceTreeSnapshot(
            snapshot_id="workspace_tree_snapshot:v0.24.2",
            created_at=_utc_now(),
            request=request,
            policy=policy,
            roots=selected_roots,
            directories=directories,
            files=files,
            ignored_count=self._ignored_count,
            hidden_count=self._hidden_count,
            secret_like_count=self._secret_like_count,
            binary_like_count=binary_like_count,
            generated_like_count=generated_like_count,
            total_directory_count=len(directories),
            total_file_count=len(files),
            truncated=truncated,
            truncation_reason=truncation_reason,
            snapshot_status=status,
            evidence_refs=[{"type": "provider_registry", "id": "internal_provider_registry:v0.24.1"}],
        )

    def _visit_directory(
        self,
        current: Path,
        root_path: Path,
        root_id: str,
        depth: int,
        max_depth: int,
        max_entries: int,
        request: WorkspaceTreeRequest,
        ignore_policy: WorkspaceIgnorePolicy,
        sanitizer: WorkspacePathSanitizationService,
        directories: list[WorkspaceDirectoryNode],
        files: list[WorkspaceFileMetadata],
    ) -> tuple[bool, str | None]:
        if depth > max_depth:
            return True, "max_depth_exceeded"
        if len(directories) + len(files) >= max_entries:
            return True, "max_entries_exceeded"
        relative = "." if current == root_path else current.relative_to(root_path).as_posix()
        try:
            children = sorted(current.iterdir(), key=lambda item: item.name.lower())
        except OSError:
            children = []
        visible_children = [child for child in children if self._is_visible(child, request, ignore_policy)]
        child_dirs = [child for child in visible_children if child.is_dir() and not child.is_symlink()]
        child_files = [child for child in visible_children if child.is_file() or child.is_symlink()]
        directories.append(
            WorkspaceDirectoryNode(
                node_id=f"workspace_directory_node:{root_id}:{sanitizer.sanitize_path(relative)}",
                root_id=root_id,
                relative_path=relative,
                sanitized_path=sanitizer.sanitize_path(relative),
                depth=depth,
                child_directory_count=len(child_dirs),
                child_file_count=len(child_files),
                ignored=False,
                hidden=current.name.startswith(".") and current != root_path,
                symlink=current.is_symlink(),
                traversal_performed=not current.is_symlink(),
                evidence_refs=[{"type": "filesystem_metadata", "path": sanitizer.sanitize_path(relative)}],
            )
        )
        if depth == max_depth:
            return bool(child_dirs), "max_depth_exceeded" if child_dirs else None
        for child in visible_children:
            if len(directories) + len(files) >= max_entries:
                return True, "max_entries_exceeded"
            if child.is_symlink() and not request.follow_symlinks:
                if child.is_file():
                    files.append(self.metadata_service.build_metadata(child, root_path, root_id, False, child.name.startswith(".")))
                continue
            if child.is_dir():
                truncated, reason = self._visit_directory(
                    child,
                    root_path,
                    root_id,
                    depth + 1,
                    max_depth,
                    max_entries,
                    request,
                    ignore_policy,
                    sanitizer,
                    directories,
                    files,
                )
                if truncated:
                    return truncated, reason
            elif request.include_file_metadata:
                files.append(self.metadata_service.build_metadata(child, root_path, root_id, False, child.name.startswith(".")))
        return False, None

    def _is_visible(self, path: Path, request: WorkspaceTreeRequest, ignore_policy: WorkspaceIgnorePolicy) -> bool:
        hidden = path.name.startswith(".")
        ignored = WorkspaceIgnorePolicyService().should_ignore_path(path, ignore_policy)
        secret_like = WorkspaceIgnorePolicyService().detect_secret_like_path(path, ignore_policy)
        if hidden and not request.include_hidden_files:
            self._hidden_count += 1
            return False
        if secret_like:
            self._secret_like_count += 1
        if ignored and not request.include_ignored_files:
            self._ignored_count += 1
            return False
        return True


class WorkspaceMetadataSummaryService:
    def build_summary(self, snapshot: WorkspaceTreeSnapshot) -> WorkspaceMetadataSummary:
        extension_counts: dict[str, int] = {}
        file_kind_counts: dict[str, int] = {}
        for item in snapshot.files:
            extension = item.extension or "[none]"
            extension_counts[extension] = extension_counts.get(extension, 0) + 1
            file_kind_counts[item.file_kind] = file_kind_counts.get(item.file_kind, 0) + 1
        largest = sorted(
            [
                {
                    "path": item.sanitized_path,
                    "size_bytes": item.size_bytes,
                    "file_kind": item.file_kind,
                }
                for item in snapshot.files
                if item.size_bytes is not None
            ],
            key=lambda item: int(item["size_bytes"] or 0),
            reverse=True,
        )[:10]
        return WorkspaceMetadataSummary(
            summary_id="workspace_metadata_summary:v0.24.2",
            snapshot_id=snapshot.snapshot_id,
            root_count=len(snapshot.roots),
            directory_count=snapshot.total_directory_count,
            file_count=snapshot.total_file_count,
            extension_counts=extension_counts,
            file_kind_counts=file_kind_counts,
            largest_files=largest,
            secret_like_files_masked_count=snapshot.secret_like_count,
            ignored_count=snapshot.ignored_count,
            hidden_count=snapshot.hidden_count,
            truncated=snapshot.truncated,
            summary_status="warning" if snapshot.truncated else "ready",
            evidence_refs=[{"type": "workspace_tree_snapshot", "id": snapshot.snapshot_id}],
        )


class WorkspaceReadFindingService:
    _MARKERS: dict[str, tuple[str, str]] = {
        "file_content_read_attempted": ("critical", "file_content_read_attempted"),
        "file_excerpt_read_attempted": ("critical", "file_excerpt_read_attempted"),
        "repository_search_attempted": ("critical", "repository_search_attempted"),
        "local_command_execution_attempted": ("critical", "local_command_execution_attempted"),
        "provider_api_call_performed": ("critical", "provider_api_call_performed"),
        "external_runtime_touched": ("critical", "external_runtime_touched"),
        "credential_exposure": ("critical", "credential_exposure_detected"),
        "raw_secret_output": ("critical", "raw_secret_output_detected"),
        "vendor_hardcoding": ("critical", "vendor_hardcoding_detected"),
        "growthkernel_dependency": ("critical", "growthkernel_dependency_detected"),
        "schumpeter_split": ("critical", "schumpeter_split_detected"),
        "general_agent_usability": ("error", "general_agent_usability_premature"),
        "llm_judge": ("critical", "llm_judge_detected"),
    }

    def build_findings(
        self,
        snapshot: WorkspaceTreeSnapshot,
        summary: WorkspaceMetadataSummary,
        policy: WorkspaceReadProviderPolicy,
        markers: list[str] | None = None,
    ) -> list[WorkspaceReadFinding]:
        findings: list[WorkspaceReadFinding] = []

        def finding(severity: str, finding_type: str, message: str, path: str | None = None) -> WorkspaceReadFinding:
            return WorkspaceReadFinding(
                finding_id=f"workspace_read_finding:{finding_type}:{len(findings) + 1}",
                severity=severity,
                finding_type=finding_type,
                message=message,
                path_ref={"path": path} if path else None,
                evidence_refs=[{"type": "workspace_tree_snapshot", "id": snapshot.snapshot_id}],
                withdrawal_condition="Withdraw when the finding condition no longer applies.",
            )

        if not snapshot.roots:
            findings.append(finding("error", "missing_workspace_root", "No workspace root descriptor is available."))
        for root in snapshot.roots:
            if root.exists_declared is False:
                findings.append(finding("warning", "root_missing_or_unresolved", "Workspace root is missing or unresolved."))
            if not root.allowed_for_workspace_observation:
                findings.append(finding("error", "root_not_allowed", "Workspace root is not allowed for observation."))
        if snapshot.truncated:
            finding_type = "max_entries_exceeded" if snapshot.truncation_reason == "max_entries_exceeded" else "max_depth_exceeded"
            findings.append(finding("warning", finding_type, f"Workspace traversal truncated: {snapshot.truncation_reason}."))
            findings.append(finding("warning", "traversal_truncated", "Workspace traversal was truncated by policy limits."))
        if snapshot.ignored_count:
            findings.append(finding("info", "ignored_path_skipped", "Ignored paths were skipped before output."))
        if snapshot.hidden_count:
            findings.append(finding("info", "hidden_path_skipped", "Hidden paths were skipped before output."))
        if any(item.symlink for item in snapshot.directories + snapshot.files):
            findings.append(finding("info", "symlink_not_followed", "Symlinks were not followed by default."))
        if snapshot.secret_like_count:
            findings.append(finding("warning", "secret_like_path_masked", "Secret-like paths were masked or excluded."))
        if policy.private_path_sanitization_required:
            findings.append(finding("info", "private_path_sanitized", "Private full paths are not emitted."))
        if snapshot.request.include_file_content:
            findings.append(finding("critical", "file_content_read_attempted", "File content read was requested and blocked."))
        if snapshot.request.include_file_excerpt:
            findings.append(finding("critical", "file_excerpt_read_attempted", "File excerpt read was requested and blocked."))
        for marker in markers or []:
            severity, finding_type = self._MARKERS.get(marker, ("warning", marker))
            findings.append(finding(severity, finding_type, f"Marker detected: {marker}."))
        if not findings:
            findings.append(finding("info", "ok", "Workspace tree and metadata observed under read-only policy."))
        return findings


def _status_from_findings(findings: list[WorkspaceReadFinding]) -> str:
    if any(item.severity == "critical" for item in findings):
        return "blocked"
    if any(item.severity == "error" for item in findings):
        return "failed"
    if any(item.severity == "warning" for item in findings):
        return "warning"
    return "passed"


class WorkspaceReadReportService:
    def __init__(
        self,
        source_service: WorkspaceProviderContractSourceService | None = None,
        policy_service: WorkspaceReadPolicyService | None = None,
        root_service: WorkspaceRootDiscoveryService | None = None,
        ignore_service: WorkspaceIgnorePolicyService | None = None,
        sanitizer: WorkspacePathSanitizationService | None = None,
        traversal_service: WorkspaceTreeTraversalService | None = None,
        summary_service: WorkspaceMetadataSummaryService | None = None,
        finding_service: WorkspaceReadFindingService | None = None,
    ) -> None:
        self.source_service = source_service or WorkspaceProviderContractSourceService()
        self.policy_service = policy_service or WorkspaceReadPolicyService()
        self.sanitizer = sanitizer or WorkspacePathSanitizationService()
        self.root_service = root_service or WorkspaceRootDiscoveryService(sanitizer=self.sanitizer)
        self.ignore_service = ignore_service or WorkspaceIgnorePolicyService()
        traversal_root = self.root_service.workspace_root if hasattr(self.root_service, "workspace_root") else Path.cwd()
        self.traversal_service = traversal_service or WorkspaceTreeTraversalService(
            metadata_service=WorkspaceFileMetadataService(self.sanitizer),
            workspace_root=traversal_root,
        )
        self.summary_service = summary_service or WorkspaceMetadataSummaryService()
        self.finding_service = finding_service or WorkspaceReadFindingService()

    def build_report(self, request: WorkspaceTreeRequest | None = None, markers: list[str] | None = None) -> WorkspaceReadReport:
        request = request or WorkspaceTreeRequest()
        policy = self.policy_service.build_policy()
        ignore_policy = self.ignore_service.build_ignore_policy()
        roots = self.root_service.validate_roots_without_content_read(self.root_service.discover_declared_roots())
        surface = self.source_service.load_workspace_provider_surface()
        snapshot = self.traversal_service.build_tree_snapshot(request, roots, policy, ignore_policy, self.sanitizer)
        summary = self.summary_service.build_summary(snapshot)
        findings = self.finding_service.build_findings(snapshot, summary, policy, markers=markers)
        if surface is None:
            findings.append(
                WorkspaceReadFinding(
                    finding_id="workspace_read_finding:workspace_provider_not_declared",
                    severity="error",
                    finding_type="missing_workspace_root",
                    message="Workspace provider surface is not declared in the internal provider registry.",
                    path_ref=None,
                    evidence_refs=[],
                    withdrawal_condition="Withdraw when workspace_read_provider is declared in v0.24.1 registry.",
                )
            )
        status = _status_from_findings(findings)
        usable_root = any(root.allowed_for_workspace_observation for root in roots)
        if request.strictness == "strict" and not usable_root and status == "warning":
            status = "failed"
        return WorkspaceReadReport(
            report_id="workspace_read_report:v0.24.2",
            created_at=_utc_now(),
            request=request,
            snapshot=snapshot,
            summary=summary,
            findings=findings,
            report_status=status,
            ready_for_v0_24_3=status in {"passed", "warning"} and usable_root,
            provider_invocation_performed=snapshot.provider_invocation_performed,
            workspace_tree_observed=bool(snapshot.directories),
            workspace_metadata_observed=bool(snapshot.files) or request.include_file_metadata,
            limitations=[
                "v0.24.2 observes workspace roots, directory structure, and file metadata only.",
                "File content, file excerpts, repository search, and local command execution remain disabled.",
                "Paths are reported as relative or sanitized labels; private full paths are not emitted.",
            ],
            withdrawal_conditions=[
                "Withdraw if file content or excerpts are read by the workspace provider.",
                "Withdraw if repository search or local command execution is added in v0.24.2.",
                "Withdraw if private full paths, credentials, raw secrets, vendor runtime logic, or Schumpeter split logic are emitted.",
            ],
        )

    def build_pig_report(self, report: WorkspaceReadReport | None = None) -> dict[str, Any]:
        report = report or self.build_report()
        return {
            "version": WORKSPACE_PROVIDER_VERSION,
            "layer": WORKSPACE_PROVIDER_LAYER,
            "subject": "read_only_workspace_provider",
            "principles": [
                "workspace provider is read-only",
                "workspace tree observation is not file content reading",
                "file metadata is not file content",
                "ignore policy must be applied before output",
                "private paths must be sanitized",
                "secret-like paths must be masked or excluded",
            ],
            "safety_boundary": {
                "workspace_tree_observed": report.workspace_tree_observed,
                "workspace_metadata_observed": report.workspace_metadata_observed,
                "file_content_read_performed": False,
                "file_excerpt_read_performed": False,
                "repository_search_performed": False,
                "local_command_executed": False,
                "external_runtime_touched": False,
                "provider_api_call_performed": False,
                "credential_exposed": False,
                "raw_secret_output": False,
                "private_full_paths_included": False,
                "external_provider_adapter_implemented": False,
                "schumpeter_split_introduced": False,
                "llm_judge_enabled": False,
            },
            "next_step": WORKSPACE_PROVIDER_NEXT_STEP,
            "roadmap": {
                "v0.24": "Internal Provider / Local Runtime Provider",
                "v0.25": "General Agent Usability & Tool Routing",
                "v0.26": "Workspace Agent Workbench",
                "v0.27": "Memory Candidate & Continuity",
                "v0.28": "Public Alpha / Schumpeter Split Preparation",
                "v0.29+": "External Skill / External Provider Adapters",
            },
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": WORKSPACE_PROVIDER_STATE,
            "version": WORKSPACE_PROVIDER_VERSION,
            "source_read_models": [
                "InternalProviderRegistryState",
                "InternalProviderCapabilitySurfaceState",
                "InternalProviderPermissionPolicyState",
                "InternalProviderInvocationBoundaryState",
            ],
            "target_read_models": [
                "WorkspaceReadProviderState",
                "WorkspaceTreeState",
                "WorkspaceMetadataState",
                "WorkspacePathSanitizationState",
                "V024ReadinessState",
            ],
            "effect_types": list(WORKSPACE_PROVIDER_EFFECT_TYPES),
        }

    def render_report_cli(self, report: WorkspaceReadReport, section: str = "report") -> str:
        common = [
            f"version={report.version}",
            f"provider={WORKSPACE_PROVIDER_ID}",
            "read_only=true",
            f"report_status={report.report_status}",
            f"root_count={report.summary.root_count}",
            f"directory_count={report.summary.directory_count}",
            f"file_count={report.summary.file_count}",
            f"truncated={report.summary.truncated}",
            f"file_content_read_performed={report.file_content_read_performed}",
            f"file_excerpt_read_performed={report.file_excerpt_read_performed}",
            f"repository_search_performed={report.repository_search_performed}",
            f"local_command_executed={report.local_command_executed}",
            f"external_runtime_touched={report.snapshot.external_runtime_touched}",
            f"credential_exposed={report.credential_exposed}",
            f"raw_secret_output={report.raw_secret_output}",
            f"private_full_paths_included={report.summary.private_full_paths_included}",
            f"ready_for_v0_24_3={report.ready_for_v0_24_3}",
            f"ready_for_v0_25={report.ready_for_v0_25}",
            f"next_required_step={report.next_required_step}",
        ]
        if section == "roots":
            roots = ",".join(root.sanitized_root_label for root in report.snapshot.roots)
            return "\n".join(["Read-only Workspace Provider Roots", f"roots={roots}"] + common)
        if section == "tree":
            directories = ",".join(item.sanitized_path for item in report.snapshot.directories[:50])
            return "\n".join(["Read-only Workspace Provider Tree", f"directories={directories}"] + common)
        if section == "metadata":
            files = ",".join(item.sanitized_path for item in report.snapshot.files[:50])
            return "\n".join(["Read-only Workspace Provider Metadata", f"files={files}"] + common)
        if section == "summary":
            return "\n".join(
                [
                    "Read-only Workspace Provider Summary",
                    f"extension_counts={report.summary.extension_counts}",
                    f"file_kind_counts={report.summary.file_kind_counts}",
                ]
                + common
            )
        if section == "findings":
            findings = ",".join(item.finding_type for item in report.findings)
            return "\n".join(["Read-only Workspace Provider Findings", f"findings={findings}"] + common)
        return "\n".join(["Read-only Workspace Provider Report"] + common)


class ReadOnlyWorkspaceProviderService:
    def __init__(self, report_service: WorkspaceReadReportService | None = None) -> None:
        self.report_service = report_service or WorkspaceReadReportService()

    def observe_workspace(self, request: WorkspaceTreeRequest | None = None) -> WorkspaceReadReport:
        return self.report_service.build_report(request)
