from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from fnmatch import fnmatch
from pathlib import Path
import re
import time
from typing import Any

from chanta_core.internal_provider.registry import (
    InternalProviderRegistryReportService,
)
from chanta_core.internal_provider.workspace_provider import (
    WorkspaceIgnorePolicy,
    WorkspaceIgnorePolicyService,
    WorkspacePathSanitizationService,
    WorkspaceRootDiscoveryService,
    WorkspaceReadReportService,
    WorkspaceTreeRequest,
)


REPOSITORY_FILE_PROVIDER_VERSION = "v0.24.3"
REPOSITORY_FILE_PROVIDER_VERSION_NAME = "Repository Search / File Read Provider"
REPOSITORY_FILE_PROVIDER_KOREAN_NAME = "저장소 검색·파일 읽기 Provider"
REPOSITORY_FILE_PROVIDER_LAYER = "internal_provider"
REPOSITORY_SEARCH_PROVIDER_ID = "repository_search_provider"
FILE_READ_PROVIDER_ID = "file_read_provider"
REPOSITORY_FILE_PROVIDER_NEXT_STEP = "v0.24.4 OCEL / PIG / OCPX Inspection Provider"
REPOSITORY_FILE_PROVIDER_STATE = "repository_search_file_read_enabled"

REPOSITORY_FILE_PROVIDER_OBJECT_TYPES = [
    "repository_provider_policy",
    "repository_search_scope",
    "repository_search_request",
    "repository_search_query",
    "repository_search_match",
    "repository_search_result",
    "repository_search_report",
    "file_read_policy",
    "file_read_request",
    "file_read_window",
    "file_read_excerpt",
    "file_read_sanitization_report",
    "file_read_report",
    "repository_file_provider_finding",
    "repository_file_provider_report",
    "internal_provider_registry",
    "internal_provider_capability_surface",
    "workspace_tree_snapshot",
    "execution_envelope",
    "pig_report",
    "ocpx_projection",
]

REPOSITORY_FILE_PROVIDER_EVENT_TYPES = [
    "repository_search_requested",
    "repository_search_scope_created",
    "repository_search_query_created",
    "repository_file_name_search_performed",
    "repository_text_search_performed",
    "repository_symbol_search_performed",
    "repository_search_result_created",
    "repository_search_report_created",
    "file_read_requested",
    "file_read_window_created",
    "file_excerpt_read",
    "bounded_file_read",
    "file_read_sanitization_performed",
    "file_read_report_created",
    "repository_file_provider_report_created",
    "repository_file_provider_warning_created",
    "repository_file_provider_blocked",
]

REPOSITORY_FILE_PROVIDER_RELATION_TYPES = [
    "uses_repository_search_provider",
    "uses_file_read_provider",
    "uses_workspace_tree_snapshot",
    "applies_repository_provider_policy",
    "applies_file_read_policy",
    "applies_workspace_ignore_policy",
    "applies_path_sanitization_policy",
    "searches_file_name",
    "searches_text",
    "searches_symbol_like_pattern",
    "observes_repository_match",
    "reads_bounded_file_excerpt",
    "sanitizes_file_excerpt",
    "redacts_secret_like_content",
    "blocks_binary_raw_output",
    "skips_ignored_file",
    "skips_hidden_file",
    "does_not_follow_symlink",
    "not_unrestricted_file_read",
    "not_full_repository_dump",
    "not_file_written",
    "not_file_edited",
    "not_file_deleted",
    "not_local_command_executed",
    "not_external_runtime_touched",
    "prevents_credential_exposure",
    "prepares_process_state_inspection_provider",
    "defers_process_state_inspection_execution_to_v0_24_4",
    "defers_local_runtime_execution_to_later_v0_24",
    "defers_general_agent_usability_to_v0_25",
    "visible_in_workbench_future",
    "recorded_in_envelope",
    "derived_from_internal_provider_registry",
    "derived_from_workspace_tree_snapshot",
]

REPOSITORY_FILE_PROVIDER_EFFECT_TYPES = [
    "read_only_observation",
    "repository_search_performed",
    "file_excerpt_read",
    "bounded_file_read",
    "repository_match_observed",
    "state_candidate_created",
]

REPOSITORY_FILE_PROVIDER_FORBIDDEN_EFFECT_TYPES = [
    "unrestricted_file_read",
    "full_repository_dump",
    "raw_binary_output",
    "raw_secret_output",
    "file_written",
    "file_edited",
    "file_deleted",
    "repository_mutated",
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
    "external_provider_called",
]


def _utc_now() -> str:
    return datetime.fromtimestamp(time.time(), timezone.utc).isoformat().replace("+00:00", "Z")


def _model_dict(value: Any) -> dict[str, Any]:
    return asdict(value)


def _safe_id(text: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9_.:-]+", "_", text.strip())
    return normalized[:120] or "empty"


@dataclass
class RepositoryProviderPolicy:
    policy_id: str = "repository_provider_policy:v0.24.3"
    version: str = REPOSITORY_FILE_PROVIDER_VERSION
    provider_id: str = REPOSITORY_SEARCH_PROVIDER_ID
    read_only: bool = True
    file_name_search_enabled: bool = True
    text_search_enabled: bool = True
    symbol_search_enabled: bool = True
    full_repository_dump_enabled: bool = False
    unrestricted_file_read_enabled: bool = False
    file_write_enabled: bool = False
    file_edit_enabled: bool = False
    file_delete_enabled: bool = False
    local_command_execution_enabled: bool = False
    follow_symlinks: bool = False
    include_hidden_files_default: bool = False
    include_ignored_files_default: bool = False
    max_files_scanned_default: int = 5000
    max_matches_default: int = 200
    max_match_context_lines_default: int = 3
    max_output_chars_default: int = 20000
    binary_file_scan_enabled: bool = False
    secret_redaction_required: bool = True
    private_path_sanitization_required: bool = True
    raw_secret_output_forbidden: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class RepositorySearchScope:
    scope_id: str
    root_ids: list[str]
    include_globs: list[str]
    exclude_globs: list[str]
    allowed_extensions: list[str]
    denied_extensions: list[str]
    include_hidden_files: bool = False
    include_ignored_files: bool = False
    follow_symlinks: bool = False
    max_files_scanned: int = 5000
    max_matches: int = 200
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class RepositorySearchRequest:
    query_text: str
    search_mode: str = "mixed"
    scope: RepositorySearchScope | None = None
    max_matches: int | None = None
    max_context_lines: int | None = None
    include_file_metadata: bool = True
    include_match_context: bool = True
    include_raw_file_content: bool = False
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    strictness: str = "standard"

    def to_dict(self) -> dict[str, Any]:
        return {
            **_model_dict(self),
            "scope": self.scope.to_dict() if self.scope else None,
        }


@dataclass
class RepositorySearchQuery:
    query_id: str
    raw_query_text: str
    normalized_query_text: str
    search_mode: str
    case_sensitive: bool = False
    regex_enabled: bool = False
    literal_search: bool = True
    tokenized_terms: list[str] = field(default_factory=list)
    query_status: str = "ready"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class RepositorySearchMatch:
    match_id: str
    root_id: str
    relative_path: str
    sanitized_path: str
    extension: str | None
    file_kind: str
    match_type: str
    line_number: int | None
    column_number: int | None
    score: float | None
    context_before: list[str]
    matched_line: str | None
    context_after: list[str]
    content_redacted: bool
    secret_like_match: bool
    binary_like_file: bool
    ignored: bool
    hidden: bool
    private_full_path_output: bool = False
    raw_secret_output: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class RepositorySearchResult:
    result_id: str
    query: RepositorySearchQuery
    matches: list[RepositorySearchMatch]
    scanned_file_count: int
    skipped_file_count: int
    ignored_file_count: int
    binary_skipped_count: int
    secret_like_match_count: int
    redacted_match_count: int
    truncated: bool
    truncation_reason: str | None
    repository_search_performed: bool = True
    file_content_scanned_for_search: bool = False
    raw_file_content_output: bool = False
    private_full_paths_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            **_model_dict(self),
            "query": self.query.to_dict(),
            "matches": [item.to_dict() for item in self.matches],
        }


@dataclass
class RepositorySearchReport:
    report_id: str
    version: str
    created_at: str
    request: RepositorySearchRequest
    result: RepositorySearchResult
    findings: list["RepositoryFileProviderFinding"]
    report_status: str
    ready_for_file_read: bool
    ready_for_v0_24_4: bool
    ready_for_v0_25: bool = False
    repository_search_performed: bool = True
    unrestricted_file_read_performed: bool = False
    full_repository_dump_performed: bool = False
    local_command_executed: bool = False
    external_provider_adapter_implemented: bool = False
    credential_exposed: bool = False
    raw_secret_output: bool = False
    private_full_paths_included: bool = False
    llm_judge_used: bool = False
    next_required_step: str = REPOSITORY_FILE_PROVIDER_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = (
        "Valid until repository layout, ignore policy, search policy, or provider policy changes."
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            **_model_dict(self),
            "request": self.request.to_dict(),
            "result": self.result.to_dict(),
            "findings": [item.to_dict() for item in self.findings],
        }


@dataclass
class FileReadPolicy:
    policy_id: str = "file_read_policy:v0.24.3"
    version: str = REPOSITORY_FILE_PROVIDER_VERSION
    provider_id: str = FILE_READ_PROVIDER_ID
    read_only: bool = True
    bounded_file_read_enabled: bool = True
    file_excerpt_read_enabled: bool = True
    unrestricted_file_read_enabled: bool = False
    full_file_dump_enabled: bool = False
    binary_raw_output_enabled: bool = False
    secret_redaction_required: bool = True
    private_path_sanitization_required: bool = True
    max_bytes_per_read_default: int = 20000
    max_lines_per_read_default: int = 400
    max_file_size_readable_default: int = 1000000
    allowed_text_extensions: list[str] = field(
        default_factory=lambda: [
            ".py",
            ".md",
            ".txt",
            ".toml",
            ".json",
            ".yaml",
            ".yml",
            ".ini",
            ".cfg",
            ".rst",
            ".js",
            ".ts",
            ".tsx",
            ".jsx",
            ".css",
            ".html",
        ]
    )
    denied_extensions: list[str] = field(
        default_factory=lambda: [
            ".png",
            ".jpg",
            ".jpeg",
            ".gif",
            ".webp",
            ".ico",
            ".pdf",
            ".zip",
            ".sqlite",
            ".db",
            ".pyc",
        ]
    )
    file_write_enabled: bool = False
    file_edit_enabled: bool = False
    file_delete_enabled: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class FileReadRequest:
    relative_path: str
    read_mode: str = "excerpt"
    root_id: str | None = None
    start_line: int | None = None
    end_line: int | None = None
    byte_offset: int | None = None
    max_bytes: int | None = None
    max_lines: int | None = None
    include_line_numbers: bool = True
    include_raw_content: bool = False
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    strictness: str = "standard"

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class FileReadWindow:
    window_id: str
    start_line: int | None
    end_line: int | None
    byte_offset: int | None
    max_bytes: int
    max_lines: int
    bounded: bool = True
    window_status: str = "ready"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class FileReadExcerpt:
    excerpt_id: str
    root_id: str | None
    relative_path: str
    sanitized_path: str
    read_mode: str
    line_start: int | None
    line_end: int | None
    content_lines: list[str]
    content_truncated: bool
    redacted: bool
    redaction_count: int
    secret_like_content_detected: bool
    binary_like_file: bool
    file_size_bytes: int | None
    private_full_path_output: bool = False
    raw_secret_output: bool = False
    unrestricted_read: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class FileReadSanitizationReport:
    report_id: str
    file_ref: dict[str, Any]
    secret_like_content_detected: bool
    redaction_applied: bool
    redaction_count: int
    private_path_sanitized: bool
    binary_output_blocked: bool
    raw_secret_output_blocked: bool
    sanitized_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class FileReadReport:
    report_id: str
    version: str
    created_at: str
    request: FileReadRequest
    policy: FileReadPolicy
    read_window: FileReadWindow
    excerpt: FileReadExcerpt | None
    sanitization_report: FileReadSanitizationReport | None
    findings: list["RepositoryFileProviderFinding"]
    report_status: str
    bounded_file_read_performed: bool
    file_excerpt_read_performed: bool
    unrestricted_file_read_performed: bool = False
    full_file_dump_performed: bool = False
    binary_raw_output_performed: bool = False
    file_write_performed: bool = False
    file_edit_performed: bool = False
    file_delete_performed: bool = False
    local_command_executed: bool = False
    credential_exposed: bool = False
    raw_secret_output: bool = False
    private_full_paths_included: bool = False
    llm_judge_used: bool = False
    next_required_step: str = REPOSITORY_FILE_PROVIDER_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            **_model_dict(self),
            "request": self.request.to_dict(),
            "policy": self.policy.to_dict(),
            "read_window": self.read_window.to_dict(),
            "excerpt": self.excerpt.to_dict() if self.excerpt else None,
            "sanitization_report": self.sanitization_report.to_dict() if self.sanitization_report else None,
            "findings": [item.to_dict() for item in self.findings],
        }


@dataclass
class RepositoryFileProviderFinding:
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
class RepositoryFileProviderReport:
    report_id: str
    version: str
    created_at: str
    search_reports: list[RepositorySearchReport]
    file_read_reports: list[FileReadReport]
    findings: list[RepositoryFileProviderFinding]
    report_status: str
    ready_for_v0_24_4: bool
    ready_for_v0_25: bool
    repository_search_performed: bool
    bounded_file_read_performed: bool
    file_excerpt_read_performed: bool
    unrestricted_file_read_performed: bool = False
    full_repository_dump_performed: bool = False
    file_write_performed: bool = False
    file_edit_performed: bool = False
    file_delete_performed: bool = False
    local_command_executed: bool = False
    external_provider_adapter_implemented: bool = False
    credential_exposed: bool = False
    raw_secret_output: bool = False
    private_full_paths_included: bool = False
    llm_judge_used: bool = False
    next_required_step: str = REPOSITORY_FILE_PROVIDER_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            **_model_dict(self),
            "search_reports": [item.to_dict() for item in self.search_reports],
            "file_read_reports": [item.to_dict() for item in self.file_read_reports],
            "findings": [item.to_dict() for item in self.findings],
        }


class RepositoryFileProviderContractSourceService:
    def __init__(self, workspace_root: Path | None = None) -> None:
        self.workspace_root = (workspace_root or Path.cwd()).resolve()

    def load_internal_provider_contract(self) -> dict[str, Any]:
        return {"version": "v0.24.0", "provider_contract_available": True}

    def load_provider_registry(self) -> Any:
        return InternalProviderRegistryReportService().build_report().registry

    def load_repository_provider_surface(self) -> Any | None:
        registry = self.load_provider_registry()
        return next(
            (
                item for item in registry.capability_surfaces
                if item.provider_id.endswith(REPOSITORY_SEARCH_PROVIDER_ID) or item.provider_type == REPOSITORY_SEARCH_PROVIDER_ID
            ),
            None,
        )

    def load_file_read_provider_surface(self) -> Any | None:
        registry = self.load_provider_registry()
        return next(
            (
                item for item in registry.capability_surfaces
                if item.provider_id.endswith(FILE_READ_PROVIDER_ID) or item.provider_type == FILE_READ_PROVIDER_ID
            ),
            None,
        )

    def load_workspace_snapshot_if_available(self) -> Any | None:
        return WorkspaceReadReportService(
            root_service=WorkspaceRootDiscoveryService(workspace_root=self.workspace_root),
        ).build_report(WorkspaceTreeRequest(max_depth=4, max_entries=2000)).snapshot


class RepositoryFileProviderSkillService:
    def list_skill_contracts(self) -> list[dict[str, Any]]:
        from chanta_core.internal_provider.workspace_provider import WorkspaceReadProviderSkillService

        skills = {item["skill_id"]: dict(item) for item in WorkspaceReadProviderSkillService().list_skill_contracts()}
        for skill_id, purpose in {
            "skill:repository_search_provider_view": "implemented/read-only/bounded-search-only",
            "skill:file_read_provider_view": "implemented/read-only/bounded-read-only",
        }.items():
            if skill_id in skills:
                skills[skill_id]["status"] = "implemented"
                skills[skill_id]["scope"] = purpose
                skills[skill_id]["read_only"] = True
                skills[skill_id]["provider_invocation_enabled"] = True
                skills[skill_id]["external_provider_invocation_enabled"] = False
                skills[skill_id]["local_command_execution_enabled"] = False
        return list(skills.values())


class RepositoryProviderPolicyService:
    def build_search_policy(self) -> RepositoryProviderPolicy:
        return RepositoryProviderPolicy(evidence_refs=[{"type": "policy", "id": "repository_provider_policy:v0.24.3"}])


class RepositorySearchScopeService:
    _DEFAULT_DENIED_EXTENSIONS = [".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf", ".zip", ".sqlite", ".db", ".pyc"]

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.workspace_root = (workspace_root or Path.cwd()).resolve()

    def build_scope(
        self,
        request: RepositorySearchRequest,
        workspace_snapshot: Any | None,
        policy: RepositoryProviderPolicy,
    ) -> RepositorySearchScope:
        scope = request.scope
        if scope is not None:
            return scope
        root_id = "workspace_root"
        if workspace_snapshot and getattr(workspace_snapshot, "roots", None):
            root_id = workspace_snapshot.roots[0].root_id
        return RepositorySearchScope(
            scope_id="repository_search_scope:v0.24.3:default",
            root_ids=[root_id],
            include_globs=["*", "**/*"],
            exclude_globs=[],
            allowed_extensions=[],
            denied_extensions=list(self._DEFAULT_DENIED_EXTENSIONS),
            include_hidden_files=policy.include_hidden_files_default,
            include_ignored_files=policy.include_ignored_files_default,
            follow_symlinks=policy.follow_symlinks,
            max_files_scanned=policy.max_files_scanned_default,
            max_matches=request.max_matches or policy.max_matches_default,
            evidence_refs=[{"type": "workspace_root", "label": "workspace_root"}],
        )

    def validate_scope(self, scope: RepositorySearchScope) -> list[RepositoryFileProviderFinding]:
        findings: list[RepositoryFileProviderFinding] = []
        if scope.follow_symlinks:
            findings.append(_finding("error", "symlink_not_followed", "Repository search scope cannot follow symlinks.", None))
        if scope.max_files_scanned <= 0 or scope.max_matches <= 0:
            findings.append(_finding("error", "max_files_scanned_exceeded", "Repository search scope limits must be positive.", None))
        return findings


class RepositorySearchQueryService:
    def build_query(self, request: RepositorySearchRequest) -> RepositorySearchQuery:
        normalized = " ".join(request.query_text.strip().split())
        status = "ready" if normalized else ("blocked" if request.strictness == "strict" else "warning")
        return RepositorySearchQuery(
            query_id=f"repository_search_query:{_safe_id(normalized or 'empty')}",
            raw_query_text=request.query_text,
            normalized_query_text=normalized,
            search_mode=request.search_mode,
            tokenized_terms=[item for item in re.split(r"\s+", normalized) if item],
            query_status=status,
            evidence_refs=[{"type": "request", "id": "repository_search_request:v0.24.3"}],
        )


class FileReadSanitizationService:
    _SECRET_PATTERNS = [
        re.compile(r"(?i)([a-z0-9_.-]*(password|passwd|secret|token|api[_-]?key|credential)[a-z0-9_.-]*)(\s*[:=]\s*)([^\s,'\"]+)"),
        re.compile(r"(?i)(bearer\s+)[a-z0-9._~+/=-]{12,}"),
        re.compile(r"(?i)(sk-|ghp_|xox[baprs]-)[a-z0-9_-]{8,}"),
    ]

    def __init__(self, sanitizer: WorkspacePathSanitizationService | None = None) -> None:
        self.sanitizer = sanitizer or WorkspacePathSanitizationService()

    def detect_secret_like_content(self, text: str) -> bool:
        return any(pattern.search(text) for pattern in self._SECRET_PATTERNS)

    def redact_secret_like_content(self, text: str) -> tuple[str, int]:
        redaction_count = 0
        redacted = text
        for pattern in self._SECRET_PATTERNS:
            def replace(match: re.Match[str]) -> str:
                if len(match.groups()) >= 4:
                    return f"{match.group(1)}{match.group(3)}[REDACTED]"
                return f"{match.group(1)}[REDACTED]"

            redacted, count = pattern.subn(replace, redacted)
            redaction_count += count
        return redacted, redaction_count

    def sanitize_path(self, path: Path | str) -> str:
        return self.sanitizer.sanitize_path(path)

    def block_binary_output(self, path: Path, metadata: dict[str, Any] | None = None) -> bool:
        suffix = path.suffix.lower()
        denied = set(FileReadPolicy().denied_extensions)
        if suffix in denied:
            return True
        try:
            with path.open("rb") as handle:
                sample = handle.read(512)
        except OSError:
            return False
        return b"\x00" in sample


class RepositorySearchService:
    def __init__(
        self,
        workspace_root: Path | None = None,
        ignore_service: WorkspaceIgnorePolicyService | None = None,
        sanitizer: FileReadSanitizationService | None = None,
    ) -> None:
        self.workspace_root = (workspace_root or Path.cwd()).resolve()
        self.ignore_service = ignore_service or WorkspaceIgnorePolicyService()
        self.sanitizer = sanitizer or FileReadSanitizationService()
        self.ignore_policy = self.ignore_service.build_ignore_policy()

    def search_file_names(
        self,
        query: RepositorySearchQuery,
        scope: RepositorySearchScope,
        policy: RepositoryProviderPolicy,
    ) -> tuple[list[RepositorySearchMatch], dict[str, int | bool | str | None]]:
        return self._search(query, scope, policy, {"file_name"})

    def search_text(
        self,
        query: RepositorySearchQuery,
        scope: RepositorySearchScope,
        policy: RepositoryProviderPolicy,
    ) -> tuple[list[RepositorySearchMatch], dict[str, int | bool | str | None]]:
        return self._search(query, scope, policy, {"text"})

    def search_symbols(
        self,
        query: RepositorySearchQuery,
        scope: RepositorySearchScope,
        policy: RepositoryProviderPolicy,
    ) -> tuple[list[RepositorySearchMatch], dict[str, int | bool | str | None]]:
        return self._search(query, scope, policy, {"symbol"})

    def search_mixed(
        self,
        query: RepositorySearchQuery,
        scope: RepositorySearchScope,
        policy: RepositoryProviderPolicy,
    ) -> tuple[list[RepositorySearchMatch], dict[str, int | bool | str | None]]:
        return self._search(query, scope, policy, {"file_name", "text", "symbol"})

    def _search(
        self,
        query: RepositorySearchQuery,
        scope: RepositorySearchScope,
        policy: RepositoryProviderPolicy,
        modes: set[str],
    ) -> tuple[list[RepositorySearchMatch], dict[str, int | bool | str | None]]:
        matches: list[RepositorySearchMatch] = []
        scanned = skipped = ignored = binary_skipped = 0
        output_chars = 0
        truncated = False
        truncation_reason: str | None = None
        terms = query.tokenized_terms or ([query.normalized_query_text] if query.normalized_query_text else [])
        if not terms:
            return matches, self._stats(scanned, skipped, ignored, binary_skipped, truncated, "empty_query", False)

        for path in self._iter_candidate_files(scope):
            if scanned >= scope.max_files_scanned:
                truncated = True
                truncation_reason = "max_files_scanned_exceeded"
                break
            if len(matches) >= scope.max_matches:
                truncated = True
                truncation_reason = "max_matches_exceeded"
                break
            if self._is_ignored_or_hidden(path, scope):
                ignored += 1
                skipped += 1
                continue
            if self._is_binary(path, scope, policy):
                binary_skipped += 1
                skipped += 1
                continue
            scanned += 1
            relative = self._relative(path)
            if "file_name" in modes and self._matches_text(path.name, terms):
                match = self._build_match(path, relative, "file_name", None, None, [], path.name, [], False)
                matches.append(match)
                output_chars += len(path.name)
            if len(matches) >= scope.max_matches:
                truncated = True
                truncation_reason = "max_matches_exceeded"
                break
            if ("text" in modes or "symbol" in modes) and query.normalized_query_text:
                new_matches, chars = self._scan_text_file(path, relative, query, scope, policy, "symbol" if "symbol" in modes and "text" not in modes else "text")
                for match in new_matches:
                    if len(matches) >= scope.max_matches:
                        truncated = True
                        truncation_reason = "max_matches_exceeded"
                        break
                    if output_chars + chars > policy.max_output_chars_default:
                        truncated = True
                        truncation_reason = "max_output_chars_exceeded"
                        break
                    matches.append(match)
                    output_chars += chars
            if truncated:
                break
        file_content_scanned = bool({"text", "symbol"} & modes)
        return matches, self._stats(scanned, skipped, ignored, binary_skipped, truncated, truncation_reason, file_content_scanned)

    def _iter_candidate_files(self, scope: RepositorySearchScope) -> list[Path]:
        try:
            paths = sorted(self.workspace_root.rglob("*"), key=lambda item: item.as_posix().lower())
        except OSError:
            return []
        files: list[Path] = []
        for path in paths:
            if not path.is_file() and not path.is_symlink():
                continue
            relative = self._relative(path)
            if scope.include_globs and not any(fnmatch(relative, pattern) for pattern in scope.include_globs):
                continue
            if any(fnmatch(relative, pattern) for pattern in scope.exclude_globs):
                continue
            suffix = path.suffix.lower()
            if scope.allowed_extensions and suffix not in {item.lower() for item in scope.allowed_extensions}:
                continue
            if suffix in {item.lower() for item in scope.denied_extensions}:
                files.append(path)
                continue
            files.append(path)
        return files

    def _scan_text_file(
        self,
        path: Path,
        relative: str,
        query: RepositorySearchQuery,
        scope: RepositorySearchScope,
        policy: RepositoryProviderPolicy,
        match_type: str,
    ) -> tuple[list[RepositorySearchMatch], int]:
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            return [], 0
        terms = query.tokenized_terms or [query.normalized_query_text]
        results: list[RepositorySearchMatch] = []
        char_count = 0
        context = max(0, min(policy.max_match_context_lines_default, 3))
        for index, line in enumerate(lines, start=1):
            if match_type == "symbol":
                matched = self._symbol_match(line, terms)
            else:
                matched = self._matches_text(line, terms)
            if not matched:
                continue
            before = lines[max(0, index - context - 1): index - 1]
            after = lines[index: index + context]
            redacted_line, redactions = self.sanitizer.redact_secret_like_content(line)
            before = [self.sanitizer.redact_secret_like_content(item)[0] for item in before]
            after = [self.sanitizer.redact_secret_like_content(item)[0] for item in after]
            secret_like = redactions > 0 or self.sanitizer.detect_secret_like_content(line)
            results.append(
                self._build_match(
                    path,
                    relative,
                    match_type,
                    index,
                    line.lower().find((terms[0] if terms else "").lower()) + 1 if terms else None,
                    before,
                    redacted_line,
                    after,
                    secret_like,
                )
            )
            char_count += len(redacted_line) + sum(len(item) for item in before + after)
        return results, char_count

    def _build_match(
        self,
        path: Path,
        relative: str,
        match_type: str,
        line_number: int | None,
        column_number: int | None,
        context_before: list[str],
        matched_line: str | None,
        context_after: list[str],
        secret_like: bool,
    ) -> RepositorySearchMatch:
        redacted = secret_like
        sanitized = self.sanitizer.sanitize_path(relative)
        return RepositorySearchMatch(
            match_id=f"repository_search_match:{_safe_id(relative)}:{match_type}:{line_number or 0}",
            root_id="workspace_root",
            relative_path=relative,
            sanitized_path=sanitized,
            extension=path.suffix.lower() or None,
            file_kind=_classify_file_kind(path, secret_like, False),
            match_type=match_type,
            line_number=line_number,
            column_number=column_number,
            score=None,
            context_before=context_before,
            matched_line=matched_line,
            context_after=context_after,
            content_redacted=redacted,
            secret_like_match=secret_like,
            binary_like_file=False,
            ignored=False,
            hidden=path.name.startswith("."),
            evidence_refs=[{"type": "repository_search_match", "path": sanitized}],
        )

    def _is_ignored_or_hidden(self, path: Path, scope: RepositorySearchScope) -> bool:
        relative_parts = self._relative(path).split("/")
        if not scope.include_hidden_files and any(part.startswith(".") for part in relative_parts):
            return True
        if not scope.include_ignored_files:
            if any(part.lower() in {item.lower() for item in self.ignore_policy.default_ignored_dirs} for part in relative_parts):
                return True
            if self.ignore_service.should_ignore_path(path, self.ignore_policy):
                return True
        if path.is_symlink() and not scope.follow_symlinks:
            return True
        return False

    def _is_binary(self, path: Path, scope: RepositorySearchScope, policy: RepositoryProviderPolicy) -> bool:
        if path.suffix.lower() in {item.lower() for item in scope.denied_extensions}:
            return True
        if not policy.binary_file_scan_enabled and self.sanitizer.block_binary_output(path):
            return True
        return False

    def _relative(self, path: Path) -> str:
        try:
            return path.resolve().relative_to(self.workspace_root).as_posix()
        except (OSError, ValueError):
            return path.name

    def _matches_text(self, text: str, terms: list[str]) -> bool:
        lowered = text.lower()
        return any(term.lower() in lowered for term in terms)

    def _symbol_match(self, text: str, terms: list[str]) -> bool:
        for term in terms:
            pattern = re.compile(rf"\b(class|def|function|const|let|var)\s+{re.escape(term)}\b", re.IGNORECASE)
            if pattern.search(text) or re.search(rf"\b{re.escape(term)}\b", text):
                return True
        return False

    def _stats(
        self,
        scanned: int,
        skipped: int,
        ignored: int,
        binary_skipped: int,
        truncated: bool,
        truncation_reason: str | None,
        file_content_scanned: bool,
    ) -> dict[str, int | bool | str | None]:
        return {
            "scanned_file_count": scanned,
            "skipped_file_count": skipped,
            "ignored_file_count": ignored,
            "binary_skipped_count": binary_skipped,
            "truncated": truncated,
            "truncation_reason": truncation_reason,
            "file_content_scanned_for_search": file_content_scanned,
        }


class RepositorySearchResultService:
    def build_result(
        self,
        query: RepositorySearchQuery,
        matches: list[RepositorySearchMatch],
        scan_stats: dict[str, int | bool | str | None],
    ) -> RepositorySearchResult:
        return RepositorySearchResult(
            result_id=f"repository_search_result:{query.query_id}",
            query=query,
            matches=matches,
            scanned_file_count=int(scan_stats.get("scanned_file_count") or 0),
            skipped_file_count=int(scan_stats.get("skipped_file_count") or 0),
            ignored_file_count=int(scan_stats.get("ignored_file_count") or 0),
            binary_skipped_count=int(scan_stats.get("binary_skipped_count") or 0),
            secret_like_match_count=sum(1 for item in matches if item.secret_like_match),
            redacted_match_count=sum(1 for item in matches if item.content_redacted),
            truncated=bool(scan_stats.get("truncated")),
            truncation_reason=scan_stats.get("truncation_reason") if isinstance(scan_stats.get("truncation_reason"), str) else None,
            file_content_scanned_for_search=bool(scan_stats.get("file_content_scanned_for_search")),
            evidence_refs=[{"type": "repository_search_query", "id": query.query_id}],
        )


class FileReadPolicyService:
    def build_file_read_policy(self) -> FileReadPolicy:
        return FileReadPolicy(evidence_refs=[{"type": "policy", "id": "file_read_policy:v0.24.3"}])


class FileReadWindowService:
    def build_window(self, request: FileReadRequest, policy: FileReadPolicy) -> FileReadWindow:
        max_bytes = request.max_bytes if request.max_bytes is not None else policy.max_bytes_per_read_default
        max_lines = request.max_lines if request.max_lines is not None else policy.max_lines_per_read_default
        end_line = request.end_line
        if request.start_line is not None and end_line is not None and end_line < request.start_line:
            status = "blocked"
        elif max_bytes <= 0 or max_lines <= 0:
            status = "blocked"
        else:
            status = "ready"
        return FileReadWindow(
            window_id=f"file_read_window:{_safe_id(request.relative_path)}",
            start_line=request.start_line,
            end_line=end_line,
            byte_offset=request.byte_offset,
            max_bytes=max_bytes,
            max_lines=max_lines,
            window_status=status,
            evidence_refs=[{"type": "file_read_request", "path": request.relative_path}],
        )


class FileReadService:
    def __init__(
        self,
        workspace_root: Path | None = None,
        ignore_service: WorkspaceIgnorePolicyService | None = None,
        sanitizer: FileReadSanitizationService | None = None,
    ) -> None:
        self.workspace_root = (workspace_root or Path.cwd()).resolve()
        self.ignore_service = ignore_service or WorkspaceIgnorePolicyService()
        self.sanitizer = sanitizer or FileReadSanitizationService()
        self.ignore_policy = self.ignore_service.build_ignore_policy()

    def read_excerpt(self, request: FileReadRequest, window: FileReadWindow, policy: FileReadPolicy) -> tuple[FileReadExcerpt | None, FileReadSanitizationReport | None, list[RepositoryFileProviderFinding]]:
        return self._read(request, window, policy, "excerpt")

    def read_bounded_file(self, request: FileReadRequest, window: FileReadWindow, policy: FileReadPolicy) -> tuple[FileReadExcerpt | None, FileReadSanitizationReport | None, list[RepositoryFileProviderFinding]]:
        return self._read(request, window, policy, "bounded_file")

    def _read(self, request: FileReadRequest, window: FileReadWindow, policy: FileReadPolicy, read_mode: str) -> tuple[FileReadExcerpt | None, FileReadSanitizationReport | None, list[RepositoryFileProviderFinding]]:
        findings: list[RepositoryFileProviderFinding] = []
        if request.include_raw_content:
            findings.append(_finding("critical", "unrestricted_file_read_attempted", "Raw content inclusion is not allowed in v0.24.3.", {"path": request.relative_path}))
            return None, None, findings
        path = self._resolve_relative(request.relative_path)
        sanitized_path = self.sanitizer.sanitize_path(request.relative_path)
        if path is None:
            findings.append(_finding("critical", "path_outside_workspace", "Requested path is outside the workspace root.", {"path": sanitized_path}))
            return None, None, findings
        if not path.exists() or not path.is_file():
            findings.append(_finding("error", "path_not_found", "Requested file was not found.", {"path": sanitized_path}))
            return None, None, findings
        if self._is_ignored_or_hidden(path):
            findings.append(_finding("warning", "ignored_path_skipped", "Requested path is ignored, hidden, or symlinked by policy.", {"path": sanitized_path}))
            return None, None, findings
        binary_like = self.sanitizer.block_binary_output(path)
        if binary_like or path.suffix.lower() in {item.lower() for item in policy.denied_extensions}:
            finding = _finding("error", "binary_raw_output_blocked", "Binary raw output is blocked.", {"path": sanitized_path})
            report = FileReadSanitizationReport(
                report_id=f"file_read_sanitization_report:{_safe_id(request.relative_path)}",
                file_ref={"path": sanitized_path},
                secret_like_content_detected=False,
                redaction_applied=False,
                redaction_count=0,
                private_path_sanitized=True,
                binary_output_blocked=True,
                raw_secret_output_blocked=True,
                sanitized_status="blocked",
                evidence_refs=[{"type": "file_read_policy", "id": policy.policy_id}],
            )
            return None, report, [finding]
        size = path.stat().st_size
        if size > policy.max_file_size_readable_default:
            findings.append(_finding("error", "file_too_large_for_read", "File exceeds bounded read policy size.", {"path": sanitized_path}))
            return None, None, findings
        if window.window_status == "blocked":
            findings.append(_finding("error", "unrestricted_file_read_attempted", "File read window is not bounded.", {"path": sanitized_path}))
            return None, None, findings
        lines, truncated = self._read_bounded_lines(path, request, window)
        redacted_lines: list[str] = []
        redaction_count = 0
        secret_detected = False
        for line in lines:
            secret_detected = secret_detected or self.sanitizer.detect_secret_like_content(line)
            redacted, count = self.sanitizer.redact_secret_like_content(line)
            redaction_count += count
            redacted_lines.append(redacted)
        excerpt = FileReadExcerpt(
            excerpt_id=f"file_read_excerpt:{_safe_id(request.relative_path)}",
            root_id=request.root_id or "workspace_root",
            relative_path=request.relative_path.replace("\\", "/"),
            sanitized_path=sanitized_path,
            read_mode=read_mode,
            line_start=request.start_line or 1,
            line_end=(request.start_line or 1) + len(redacted_lines) - 1 if redacted_lines else request.start_line,
            content_lines=redacted_lines,
            content_truncated=truncated,
            redacted=redaction_count > 0,
            redaction_count=redaction_count,
            secret_like_content_detected=secret_detected,
            binary_like_file=False,
            file_size_bytes=size,
            evidence_refs=[{"type": "bounded_file_read", "path": sanitized_path}],
        )
        sanitized_report = FileReadSanitizationReport(
            report_id=f"file_read_sanitization_report:{_safe_id(request.relative_path)}",
            file_ref={"path": sanitized_path},
            secret_like_content_detected=secret_detected,
            redaction_applied=redaction_count > 0,
            redaction_count=redaction_count,
            private_path_sanitized=True,
            binary_output_blocked=False,
            raw_secret_output_blocked=True,
            sanitized_status="warning" if redaction_count else "passed",
            evidence_refs=[{"type": "file_read_excerpt", "id": excerpt.excerpt_id}],
        )
        if redaction_count:
            findings.append(_finding("warning", "secret_like_content_redacted", "Secret-like content was redacted before output.", {"path": sanitized_path}))
        if truncated:
            findings.append(_finding("warning", "file_read_window_truncated", "File read window was truncated by policy.", {"path": sanitized_path}))
        return excerpt, sanitized_report, findings

    def _resolve_relative(self, relative_path: str) -> Path | None:
        candidate = (self.workspace_root / relative_path).resolve()
        try:
            candidate.relative_to(self.workspace_root)
        except ValueError:
            return None
        return candidate

    def _is_ignored_or_hidden(self, path: Path) -> bool:
        try:
            relative_parts = path.resolve().relative_to(self.workspace_root).as_posix().split("/")
        except ValueError:
            return True
        if any(part.startswith(".") for part in relative_parts):
            return True
        if any(part.lower() in {item.lower() for item in self.ignore_policy.default_ignored_dirs} for part in relative_parts):
            return True
        if self.ignore_service.should_ignore_path(path, self.ignore_policy):
            return True
        if path.is_symlink():
            return True
        return False

    def _read_bounded_lines(self, path: Path, request: FileReadRequest, window: FileReadWindow) -> tuple[list[str], bool]:
        try:
            all_lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            return [], False
        start = max((request.start_line or 1) - 1, 0)
        if request.end_line is not None:
            end = max(request.end_line, start)
        else:
            end = start + window.max_lines
        selected = all_lines[start:end]
        selected = selected[: window.max_lines]
        byte_total = 0
        bounded: list[str] = []
        truncated = len(selected) < (end - start)
        for line in selected:
            next_total = byte_total + len(line.encode("utf-8", errors="replace"))
            if next_total > window.max_bytes:
                truncated = True
                break
            bounded.append(line)
            byte_total = next_total
        return bounded, truncated


class RepositoryFileProviderFindingService:
    _MARKER_FINDINGS = {
        "missing_workspace_snapshot": ("warning", "missing_workspace_snapshot", "Workspace snapshot was not available."),
        "missing_repository_root": ("error", "missing_repository_root", "Repository root was missing."),
        "path_outside_workspace": ("critical", "path_outside_workspace", "Path escaped the workspace boundary."),
        "raw_secret_output": ("critical", "raw_secret_output_blocked", "Raw secret output is blocked."),
        "unrestricted_file_read": ("critical", "unrestricted_file_read_attempted", "Unrestricted file read is blocked."),
        "full_repository_dump": ("critical", "full_repository_dump_attempted", "Full repository dump is blocked."),
        "file_write": ("critical", "file_write_attempted", "File write is blocked."),
        "file_edit": ("critical", "file_edit_attempted", "File edit is blocked."),
        "file_delete": ("critical", "file_delete_attempted", "File delete is blocked."),
        "repository_mutation": ("critical", "repository_mutation_attempted", "Repository mutation is blocked."),
        "local_command_execution": ("critical", "local_command_execution_attempted", "Local command execution is blocked."),
        "provider_api_call": ("critical", "provider_api_call_performed", "Provider API calls are blocked."),
        "external_runtime_touched": ("critical", "external_runtime_touched", "External runtime touch is blocked."),
        "credential_exposure": ("critical", "credential_exposure_detected", "Credential exposure is blocked."),
        "vendor_hardcoding": ("critical", "vendor_hardcoding_detected", "Vendor-specific runtime logic is blocked."),
        "growthkernel_dependency": ("critical", "growthkernel_dependency_detected", "GrowthKernel active dependency is blocked."),
        "schumpeter_split": ("critical", "schumpeter_split_detected", "Schumpeter split is blocked."),
        "general_agent_usability": ("error", "general_agent_usability_premature", "General Agent UX remains deferred."),
        "llm_judge": ("critical", "llm_judge_detected", "LLM judge use is blocked."),
    }

    def build_findings(
        self,
        search_result_or_file_read_report: RepositorySearchResult | FileReadReport | None,
        policy: RepositoryProviderPolicy | FileReadPolicy,
        markers: list[str] | None = None,
    ) -> list[RepositoryFileProviderFinding]:
        findings: list[RepositoryFileProviderFinding] = []
        markers = markers or []
        for marker in markers:
            if marker in self._MARKER_FINDINGS:
                severity, finding_type, message = self._MARKER_FINDINGS[marker]
                findings.append(_finding(severity, finding_type, message, None))
        if isinstance(search_result_or_file_read_report, RepositorySearchResult):
            result = search_result_or_file_read_report
            if result.binary_skipped_count:
                findings.append(_finding("info", "binary_file_skipped", "Binary-like files were skipped.", None))
            if result.ignored_file_count:
                findings.append(_finding("info", "ignored_path_skipped", "Ignored or hidden files were skipped.", None))
            if result.truncated:
                if result.truncation_reason == "max_files_scanned_exceeded":
                    findings.append(_finding("warning", "max_files_scanned_exceeded", "Repository search reached max files scanned.", None))
                if result.truncation_reason == "max_matches_exceeded":
                    findings.append(_finding("warning", "max_matches_exceeded", "Repository search reached max matches.", None))
                findings.append(_finding("warning", "search_results_truncated", "Repository search result was truncated.", None))
            if result.redacted_match_count:
                findings.append(_finding("warning", "secret_like_content_redacted", "Secret-like match context was redacted.", None))
            if not findings:
                findings.append(_finding("info", "ok", "Repository/file provider boundary checks passed.", None))
        if isinstance(search_result_or_file_read_report, FileReadReport):
            findings.extend(search_result_or_file_read_report.findings)
            if not findings:
                findings.append(_finding("info", "ok", "File read provider boundary checks passed.", None))
        return findings


class RepositorySearchReportService:
    def __init__(
        self,
        workspace_root: Path | None = None,
        source_service: RepositoryFileProviderContractSourceService | None = None,
        policy_service: RepositoryProviderPolicyService | None = None,
        scope_service: RepositorySearchScopeService | None = None,
        query_service: RepositorySearchQueryService | None = None,
        search_service: RepositorySearchService | None = None,
        result_service: RepositorySearchResultService | None = None,
        finding_service: RepositoryFileProviderFindingService | None = None,
    ) -> None:
        self.workspace_root = (workspace_root or Path.cwd()).resolve()
        self.source_service = source_service or RepositoryFileProviderContractSourceService(self.workspace_root)
        self.policy_service = policy_service or RepositoryProviderPolicyService()
        self.scope_service = scope_service or RepositorySearchScopeService(self.workspace_root)
        self.query_service = query_service or RepositorySearchQueryService()
        self.search_service = search_service or RepositorySearchService(self.workspace_root)
        self.result_service = result_service or RepositorySearchResultService()
        self.finding_service = finding_service or RepositoryFileProviderFindingService()

    def build_report(self, request: RepositorySearchRequest | None = None, markers: list[str] | None = None) -> RepositorySearchReport:
        request = request or RepositorySearchRequest(query_text="provider", search_mode="mixed")
        policy = self.policy_service.build_search_policy()
        workspace_snapshot = self.source_service.load_workspace_snapshot_if_available()
        surface = self.source_service.load_repository_provider_surface()
        scope = self.scope_service.build_scope(request, workspace_snapshot, policy)
        scope_findings = self.scope_service.validate_scope(scope)
        query = self.query_service.build_query(request)
        if query.query_status == "blocked":
            matches: list[RepositorySearchMatch] = []
            stats = {"scanned_file_count": 0, "skipped_file_count": 0, "ignored_file_count": 0, "binary_skipped_count": 0, "truncated": False, "truncation_reason": "blocked_query", "file_content_scanned_for_search": False}
        elif request.search_mode == "file_name":
            matches, stats = self.search_service.search_file_names(query, scope, policy)
        elif request.search_mode == "text":
            matches, stats = self.search_service.search_text(query, scope, policy)
        elif request.search_mode == "symbol":
            matches, stats = self.search_service.search_symbols(query, scope, policy)
        else:
            matches, stats = self.search_service.search_mixed(query, scope, policy)
        result = self.result_service.build_result(query, matches, stats)
        findings = scope_findings + self.finding_service.build_findings(result, policy, markers)
        if surface is None:
            findings.append(_finding("error", "missing_repository_root", "Repository search provider surface is missing.", None))
        status = _status_from_findings(findings)
        return RepositorySearchReport(
            report_id="repository_search_report:v0.24.3",
            version=REPOSITORY_FILE_PROVIDER_VERSION,
            created_at=_utc_now(),
            request=request,
            result=result,
            findings=findings,
            report_status=status,
            ready_for_file_read=status in {"passed", "warning"},
            ready_for_v0_24_4=status in {"passed", "warning"},
            limitations=[
                "Search output is bounded sanitized match context, not raw repository content.",
                "Binary-like files, ignored paths, hidden paths, and secret-like paths are skipped or redacted by policy.",
            ],
            withdrawal_conditions=[
                "Withdraw if unrestricted file read, full repository dump, file mutation, local command execution, external provider calls, raw secrets, or private full paths are emitted.",
            ],
        )

    def render_report_cli(self, report: RepositorySearchReport, section: str = "report") -> str:
        common = [
            f"version={report.version}",
            f"provider={REPOSITORY_SEARCH_PROVIDER_ID}",
            "read_only=true",
            f"report_status={report.report_status}",
            f"repository_search_performed={str(report.repository_search_performed).lower()}",
            f"unrestricted_file_read_performed={str(report.unrestricted_file_read_performed).lower()}",
            f"full_repository_dump_performed={str(report.full_repository_dump_performed).lower()}",
            "file_write_performed=false",
            "file_edit_performed=false",
            "file_delete_performed=false",
            f"local_command_executed={str(report.local_command_executed).lower()}",
            "external_runtime_touched=false",
            f"credential_exposed={str(report.credential_exposed).lower()}",
            f"raw_secret_output={str(report.raw_secret_output).lower()}",
            f"private_full_paths_included={str(report.private_full_paths_included).lower()}",
            f"ready_for_v0_24_4={str(report.ready_for_v0_24_4).lower()}",
            f"ready_for_v0_25={str(report.ready_for_v0_25).lower()}",
            f"next_required_step={report.next_required_step}",
        ]
        if section == "findings":
            return "\n".join(["Repository/File Provider Findings", *common, *[f"- {item.severity}:{item.finding_type}:{item.message}" for item in report.findings]])
        if section == "matches":
            return "\n".join(["Repository Search Matches", *common, *[f"- {item.match_type}:{item.sanitized_path}:{item.line_number}:{item.matched_line}" for item in report.result.matches[:20]]])
        return "\n".join(
            [
                "Repository Search Provider Report",
                *common,
                f"query={report.result.query.normalized_query_text}",
                f"search_mode={report.result.query.search_mode}",
                f"scanned_file_count={report.result.scanned_file_count}",
                f"skipped_file_count={report.result.skipped_file_count}",
                f"ignored_file_count={report.result.ignored_file_count}",
                f"binary_skipped_count={report.result.binary_skipped_count}",
                f"match_count={len(report.result.matches)}",
                f"redacted_match_count={report.result.redacted_match_count}",
                f"truncated={str(report.result.truncated).lower()}",
                f"truncation_reason={report.result.truncation_reason or ''}",
            ]
        )


class FileReadReportService:
    def __init__(
        self,
        workspace_root: Path | None = None,
        source_service: RepositoryFileProviderContractSourceService | None = None,
        policy_service: FileReadPolicyService | None = None,
        window_service: FileReadWindowService | None = None,
        read_service: FileReadService | None = None,
        finding_service: RepositoryFileProviderFindingService | None = None,
    ) -> None:
        self.workspace_root = (workspace_root or Path.cwd()).resolve()
        self.source_service = source_service or RepositoryFileProviderContractSourceService(self.workspace_root)
        self.policy_service = policy_service or FileReadPolicyService()
        self.window_service = window_service or FileReadWindowService()
        self.read_service = read_service or FileReadService(self.workspace_root)
        self.finding_service = finding_service or RepositoryFileProviderFindingService()

    def build_report(self, request: FileReadRequest | None = None, markers: list[str] | None = None) -> FileReadReport:
        request = request or FileReadRequest(relative_path="README.md", read_mode="excerpt", max_lines=80)
        policy = self.policy_service.build_file_read_policy()
        window = self.window_service.build_window(request, policy)
        surface = self.source_service.load_file_read_provider_surface()
        if request.read_mode == "metadata_only":
            excerpt = None
            sanitization_report = FileReadSanitizationReport(
                report_id=f"file_read_sanitization_report:{_safe_id(request.relative_path)}",
                file_ref={"path": request.relative_path},
                secret_like_content_detected=False,
                redaction_applied=False,
                redaction_count=0,
                private_path_sanitized=True,
                binary_output_blocked=False,
                raw_secret_output_blocked=True,
                sanitized_status="passed",
            )
            read_findings: list[RepositoryFileProviderFinding] = []
        elif request.read_mode == "bounded_file":
            excerpt, sanitization_report, read_findings = self.read_service.read_bounded_file(request, window, policy)
        else:
            excerpt, sanitization_report, read_findings = self.read_service.read_excerpt(request, window, policy)
        placeholder = FileReadReport(
            report_id="file_read_report:v0.24.3",
            version=REPOSITORY_FILE_PROVIDER_VERSION,
            created_at=_utc_now(),
            request=request,
            policy=policy,
            read_window=window,
            excerpt=excerpt,
            sanitization_report=sanitization_report,
            findings=read_findings,
            report_status="passed",
            bounded_file_read_performed=request.read_mode == "bounded_file" and excerpt is not None,
            file_excerpt_read_performed=request.read_mode == "excerpt" and excerpt is not None,
            limitations=[],
            withdrawal_conditions=[],
        )
        findings = read_findings + self.finding_service.build_findings(placeholder, policy, markers)
        if surface is None:
            findings.append(_finding("error", "missing_repository_root", "File read provider surface is missing.", None))
        status = _status_from_findings(findings)
        placeholder.findings = findings
        placeholder.report_status = status
        placeholder.limitations = [
            "File read output is bounded sanitized excerpt content only.",
            "Binary-like files and ignored/hidden/symlinked paths are blocked or skipped by policy.",
        ]
        placeholder.withdrawal_conditions = [
            "Withdraw if full file dump, raw binary output, raw secret output, private full path output, file mutation, or local command execution occurs.",
        ]
        return placeholder

    def render_report_cli(self, report: FileReadReport, section: str = "report") -> str:
        common = [
            f"version={report.version}",
            f"provider={FILE_READ_PROVIDER_ID}",
            "read_only=true",
            f"report_status={report.report_status}",
            f"bounded_file_read_performed={str(report.bounded_file_read_performed).lower()}",
            f"file_excerpt_read_performed={str(report.file_excerpt_read_performed).lower()}",
            f"unrestricted_file_read_performed={str(report.unrestricted_file_read_performed).lower()}",
            f"full_file_dump_performed={str(report.full_file_dump_performed).lower()}",
            f"file_write_performed={str(report.file_write_performed).lower()}",
            f"file_edit_performed={str(report.file_edit_performed).lower()}",
            f"file_delete_performed={str(report.file_delete_performed).lower()}",
            f"local_command_executed={str(report.local_command_executed).lower()}",
            "external_runtime_touched=false",
            f"credential_exposed={str(report.credential_exposed).lower()}",
            f"raw_secret_output={str(report.raw_secret_output).lower()}",
            f"private_full_paths_included={str(report.private_full_paths_included).lower()}",
            f"ready_for_v0_24_4={str(report.report_status in {'passed', 'warning'}).lower()}",
            f"ready_for_v0_25=false",
            f"next_required_step={report.next_required_step}",
        ]
        if section == "excerpt" and report.excerpt:
            return "\n".join(["File Read Excerpt", *common, f"path={report.excerpt.sanitized_path}", *report.excerpt.content_lines])
        if section == "findings":
            return "\n".join(["File Read Findings", *common, *[f"- {item.severity}:{item.finding_type}:{item.message}" for item in report.findings]])
        return "\n".join(
            [
                "File Read Provider Report",
                *common,
                f"path={(report.excerpt.sanitized_path if report.excerpt else report.request.relative_path)}",
                f"read_mode={report.request.read_mode}",
                f"line_count={(len(report.excerpt.content_lines) if report.excerpt else 0)}",
                f"redaction_count={(report.excerpt.redaction_count if report.excerpt else 0)}",
                f"content_truncated={(str(report.excerpt.content_truncated).lower() if report.excerpt else 'false')}",
            ]
        )


class RepositoryFileProviderReportService:
    def __init__(self) -> None:
        self.finding_service = RepositoryFileProviderFindingService()

    def build_combined_report(
        self,
        search_reports: list[RepositorySearchReport] | None = None,
        file_read_reports: list[FileReadReport] | None = None,
    ) -> RepositoryFileProviderReport:
        search_reports = search_reports or []
        file_read_reports = file_read_reports or []
        findings: list[RepositoryFileProviderFinding] = []
        for report in search_reports:
            findings.extend(report.findings)
        for report in file_read_reports:
            findings.extend(report.findings)
        if not findings:
            findings.append(_finding("info", "ok", "Repository/file provider combined report passed.", None))
        status = _status_from_findings(findings)
        return RepositoryFileProviderReport(
            report_id="repository_file_provider_report:v0.24.3",
            version=REPOSITORY_FILE_PROVIDER_VERSION,
            created_at=_utc_now(),
            search_reports=search_reports,
            file_read_reports=file_read_reports,
            findings=findings,
            report_status=status,
            ready_for_v0_24_4=status in {"passed", "warning"},
            ready_for_v0_25=False,
            repository_search_performed=any(item.repository_search_performed for item in search_reports),
            bounded_file_read_performed=any(item.bounded_file_read_performed for item in file_read_reports),
            file_excerpt_read_performed=any(item.file_excerpt_read_performed for item in file_read_reports),
            limitations=["Combined report is a read-only aggregation of bounded search/read reports."],
            withdrawal_conditions=["Withdraw if mutation, local execution, external adapter, raw secret, private path, or unrestricted read behavior appears."],
        )

    def build_pig_report(self) -> dict[str, Any]:
        return {
            "version": REPOSITORY_FILE_PROVIDER_VERSION,
            "layer": REPOSITORY_FILE_PROVIDER_LAYER,
            "subject": "repository_search_file_read_provider",
            "principles": [
                "repository search is bounded observation, not full repository dump",
                "file read is bounded excerpt, not unrestricted content extraction",
                "secret-like content must be redacted before output",
                "binary files must not be emitted as raw text",
                "private paths must be sanitized",
                "no write/edit/delete operation is allowed",
                "no local command execution is allowed",
            ],
            "safety_boundary": {
                "repository_search_performed": True,
                "bounded_file_read_performed": "conditional",
                "file_excerpt_read_performed": "conditional",
                "unrestricted_file_read_performed": False,
                "full_repository_dump_performed": False,
                "raw_binary_output": False,
                "file_write_performed": False,
                "file_edit_performed": False,
                "file_delete_performed": False,
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
            "next_step": REPOSITORY_FILE_PROVIDER_NEXT_STEP,
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
            "state": REPOSITORY_FILE_PROVIDER_STATE,
            "version": REPOSITORY_FILE_PROVIDER_VERSION,
            "source_read_models": [
                "InternalProviderRegistryState",
                "InternalProviderCapabilitySurfaceState",
                "WorkspaceReadProviderState",
                "WorkspaceTreeState",
                "WorkspacePathSanitizationState",
            ],
            "target_read_models": [
                "RepositorySearchProviderState",
                "RepositorySearchResultState",
                "FileReadProviderState",
                "FileReadExcerptState",
                "FileReadSanitizationState",
                "V024ReadinessState",
            ],
            "effect_types": list(REPOSITORY_FILE_PROVIDER_EFFECT_TYPES),
        }


class RepositoryFileProviderService:
    def __init__(self, workspace_root: Path | None = None) -> None:
        self.workspace_root = (workspace_root or Path.cwd()).resolve()
        self.search_reports = RepositorySearchReportService(self.workspace_root)
        self.file_reports = FileReadReportService(self.workspace_root)

    def search_repository(self, request: RepositorySearchRequest) -> RepositorySearchReport:
        return self.search_reports.build_report(request)

    def read_file(self, request: FileReadRequest) -> FileReadReport:
        return self.file_reports.build_report(request)


def _classify_file_kind(path: Path, secret_like: bool, binary_like: bool) -> str:
    if secret_like:
        return "secret_like"
    if binary_like:
        return "binary"
    suffix = path.suffix.lower()
    name = path.name.lower()
    if name.startswith("test_") or "/tests/" in path.as_posix().lower():
        return "test"
    if suffix in {".md", ".rst", ".txt"}:
        return "docs"
    if suffix in {".toml", ".yaml", ".yml", ".json", ".ini", ".cfg"}:
        return "config"
    if suffix in {".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".go", ".rs", ".c", ".cpp", ".h"}:
        return "source"
    if path.as_posix().lower().startswith(("dist/", "build/")):
        return "generated"
    return "unknown"


def _finding(
    severity: str,
    finding_type: str,
    message: str,
    path_ref: dict[str, Any] | None,
) -> RepositoryFileProviderFinding:
    return RepositoryFileProviderFinding(
        finding_id=f"repository_file_provider_finding:{finding_type}",
        severity=severity,
        finding_type=finding_type,
        message=message,
        path_ref=path_ref,
        evidence_refs=[{"type": "repository_file_provider", "version": REPOSITORY_FILE_PROVIDER_VERSION}],
        withdrawal_condition="Withdraw if the boundary condition is no longer true.",
    )


def _status_from_findings(findings: list[RepositoryFileProviderFinding]) -> str:
    if any(item.severity == "critical" for item in findings):
        return "blocked"
    if any(item.severity == "error" for item in findings):
        return "failed"
    if any(item.severity == "warning" for item in findings):
        return "warning"
    return "passed"
