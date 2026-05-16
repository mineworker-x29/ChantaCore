from __future__ import annotations

from dataclasses import dataclass, field
from fnmatch import fnmatch
from pathlib import Path
from typing import Any, Literal
from uuid import uuid4

from chanta_core.self_awareness.code_text_perception import (
    SelfCodeTextPerceptionSkillService,
    SelfTextReadPolicyService,
    SelfTextReadRequest,
    SelfTextRedactionFinding,
)
from chanta_core.self_awareness.workspace_awareness import (
    READ_ONLY_OBSERVATION_EFFECT,
    SelfWorkspaceInventoryService,
    SelfWorkspacePathPolicyService,
    WorkspaceInventoryRequest,
    WorkspacePathResolution,
)


SearchCandidateStatus = Literal["included", "skipped", "blocked"]

SEARCH_DEFAULT_MAX_FILES = 200
SEARCH_DEFAULT_MAX_MATCHES = 200
SEARCH_DEFAULT_MAX_MATCHES_PER_FILE = 20
SEARCH_DEFAULT_MAX_BYTES_PER_FILE = 65536
SEARCH_DEFAULT_MAX_TOTAL_BYTES = 1048576
SEARCH_MAX_QUERY_CHARS = 256
SEARCH_MAX_CONTEXT_LINES = 8
SEARCH_MAX_FILES_CAP = 1000
SEARCH_MAX_MATCHES_CAP = 1000
SEARCH_MAX_TOTAL_BYTES_CAP = 4 * 1024 * 1024
SEARCH_INVENTORY_MAX_DEPTH = 20
SEARCH_SKIPPED_CANDIDATE_LIMIT = 100


@dataclass(frozen=True)
class SelfWorkspaceSearchRequest:
    query: str
    root_id: str | None = None
    relative_path: str = "."
    include_globs: list[str] = field(default_factory=list)
    exclude_globs: list[str] = field(default_factory=list)
    case_sensitive: bool = False
    match_mode: str = "literal"
    context_lines: int = 2
    max_files: int = SEARCH_DEFAULT_MAX_FILES
    max_matches: int = SEARCH_DEFAULT_MAX_MATCHES
    max_matches_per_file: int = SEARCH_DEFAULT_MAX_MATCHES_PER_FILE
    max_bytes_per_file: int = SEARCH_DEFAULT_MAX_BYTES_PER_FILE
    max_total_bytes: int = SEARCH_DEFAULT_MAX_TOTAL_BYTES
    include_hidden: bool = False

    def normalized(self) -> "SelfWorkspaceSearchRequest":
        return SelfWorkspaceSearchRequest(
            query=str(self.query or ""),
            root_id=self.root_id,
            relative_path=self.relative_path or ".",
            include_globs=[str(item) for item in self.include_globs if str(item).strip()],
            exclude_globs=[str(item) for item in self.exclude_globs if str(item).strip()],
            case_sensitive=bool(self.case_sensitive),
            match_mode=str(self.match_mode or "literal"),
            context_lines=min(max(0, int(self.context_lines)), SEARCH_MAX_CONTEXT_LINES),
            max_files=min(max(1, int(self.max_files)), SEARCH_MAX_FILES_CAP),
            max_matches=min(max(1, int(self.max_matches)), SEARCH_MAX_MATCHES_CAP),
            max_matches_per_file=min(max(1, int(self.max_matches_per_file)), SEARCH_MAX_MATCHES_CAP),
            max_bytes_per_file=min(max(1, int(self.max_bytes_per_file)), SEARCH_DEFAULT_MAX_BYTES_PER_FILE),
            max_total_bytes=min(max(1, int(self.max_total_bytes)), SEARCH_MAX_TOTAL_BYTES_CAP),
            include_hidden=bool(self.include_hidden),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "query": self.query,
            "root_id": self.root_id,
            "relative_path": self.relative_path,
            "include_globs": list(self.include_globs),
            "exclude_globs": list(self.exclude_globs),
            "case_sensitive": self.case_sensitive,
            "match_mode": self.match_mode,
            "context_lines": self.context_lines,
            "max_files": self.max_files,
            "max_matches": self.max_matches,
            "max_matches_per_file": self.max_matches_per_file,
            "max_bytes_per_file": self.max_bytes_per_file,
            "max_total_bytes": self.max_total_bytes,
            "include_hidden": self.include_hidden,
        }


@dataclass(frozen=True)
class SelfWorkspaceSearchPolicyDecision:
    allowed: bool
    blocked: bool
    finding_type: str
    reason: str | None
    root_id: str | None
    resolved_path: WorkspacePathResolution
    effective_match_mode: str
    effective_max_files: int
    effective_max_matches: int
    effective_max_bytes_per_file: int
    effective_max_total_bytes: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "allowed": self.allowed,
            "blocked": self.blocked,
            "finding_type": self.finding_type,
            "reason": self.reason,
            "root_id": self.root_id,
            "resolved_path": self.resolved_path.to_dict(),
            "effective_match_mode": self.effective_match_mode,
            "effective_max_files": self.effective_max_files,
            "effective_max_matches": self.effective_max_matches,
            "effective_max_bytes_per_file": self.effective_max_bytes_per_file,
            "effective_max_total_bytes": self.effective_max_total_bytes,
        }


@dataclass(frozen=True)
class SelfSearchFileCandidate:
    root_id: str
    relative_path: str
    suffix: str | None
    size_bytes: int | None
    candidate_status: SearchCandidateStatus
    finding_type: str | None
    reason: str | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "root_id": self.root_id,
            "relative_path": self.relative_path,
            "suffix": self.suffix,
            "size_bytes": self.size_bytes,
            "candidate_status": self.candidate_status,
            "finding_type": self.finding_type,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class SelfSearchMatchSnippet:
    before: list[str]
    line: str
    after: list[str]
    redacted: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "before": list(self.before),
            "line": self.line,
            "after": list(self.after),
            "redacted": self.redacted,
        }


@dataclass(frozen=True)
class SelfSearchMatch:
    match_id: str
    root_id: str
    relative_path: str
    line_number: int
    column_start: int
    column_end: int
    snippet: SelfSearchMatchSnippet
    redaction_findings: list[SelfTextRedactionFinding]

    def to_dict(self) -> dict[str, Any]:
        return {
            "match_id": self.match_id,
            "root_id": self.root_id,
            "relative_path": self.relative_path,
            "line_number": self.line_number,
            "column_start": self.column_start,
            "column_end": self.column_end,
            "snippet": self.snippet.to_dict(),
            "redaction_findings": [item.to_dict() for item in self.redaction_findings],
        }


@dataclass(frozen=True)
class SelfWorkspaceSearchResult:
    result_id: str
    request: SelfWorkspaceSearchRequest
    policy_decision: SelfWorkspaceSearchPolicyDecision
    candidates_seen: int
    files_scanned: int
    files_skipped: int
    files_blocked: int
    matches: list[SelfSearchMatch]
    truncated: bool
    truncated_reason: str | None
    skipped_candidates: list[SelfSearchFileCandidate]
    evidence_refs: list[dict[str, Any]]
    blocked: bool
    warnings: list[str]
    result_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "result_id": self.result_id,
            "request": self.request.to_dict(),
            "policy_decision": self.policy_decision.to_dict(),
            "candidates_seen": self.candidates_seen,
            "files_scanned": self.files_scanned,
            "files_skipped": self.files_skipped,
            "files_blocked": self.files_blocked,
            "matches": [item.to_dict() for item in self.matches],
            "truncated": self.truncated,
            "truncated_reason": self.truncated_reason,
            "skipped_candidates": [item.to_dict() for item in self.skipped_candidates],
            "evidence_refs": [dict(item) for item in self.evidence_refs],
            "blocked": self.blocked,
            "warnings": list(self.warnings),
            "result_attrs": dict(self.result_attrs),
        }


class SelfWorkspaceSearchPolicyService:
    def __init__(self, *, path_policy_service: SelfWorkspacePathPolicyService | None = None) -> None:
        self.path_policy_service = path_policy_service or SelfWorkspacePathPolicyService()

    def decide(self, request: SelfWorkspaceSearchRequest) -> SelfWorkspaceSearchPolicyDecision:
        normalized = request.normalized()
        resolution = self.path_policy_service.resolve_path(normalized.relative_path, root_id=normalized.root_id)
        if not normalized.query.strip():
            return _search_decision(normalized, resolution, "empty_query", "Search query must not be empty.", False)
        if len(normalized.query) > SEARCH_MAX_QUERY_CHARS:
            return _search_decision(normalized, resolution, "query_too_long", "Search query exceeds policy limit.", False)
        if normalized.match_mode != "literal":
            return _search_decision(
                normalized,
                resolution,
                "unsupported_match_mode",
                "Only literal match mode is supported in v0.20.3.",
                False,
            )
        if resolution.blocked:
            return _search_decision(normalized, resolution, _map_path_finding(resolution.finding_type), resolution.reason, False)
        return _search_decision(normalized, resolution, "ok", None, True)


class SelfSearchCandidateService:
    def __init__(
        self,
        *,
        path_policy_service: SelfWorkspacePathPolicyService | None = None,
        inventory_service: SelfWorkspaceInventoryService | None = None,
        text_policy_service: SelfTextReadPolicyService | None = None,
    ) -> None:
        self.path_policy_service = path_policy_service or SelfWorkspacePathPolicyService()
        self.inventory_service = inventory_service or SelfWorkspaceInventoryService(
            path_policy_service=self.path_policy_service
        )
        self.text_policy_service = text_policy_service or SelfTextReadPolicyService(
            path_policy_service=self.path_policy_service
        )
        self.last_candidates_seen = 0
        self.last_files_skipped = 0
        self.last_files_blocked = 0
        self.last_truncated = False
        self.last_truncated_reason: str | None = None
        self.last_warnings: list[str] = []

    def collect_candidates(
        self,
        request: SelfWorkspaceSearchRequest,
        policy_decision: SelfWorkspaceSearchPolicyDecision,
    ) -> tuple[list[SelfSearchFileCandidate], list[SelfSearchFileCandidate]]:
        normalized = request.normalized()
        self.last_candidates_seen = 0
        self.last_files_skipped = 0
        self.last_files_blocked = 0
        self.last_truncated = False
        self.last_truncated_reason = None
        self.last_warnings = []
        if policy_decision.blocked:
            return [], []
        start_path = Path(policy_decision.resolved_path.canonical_path)
        if start_path.is_file():
            self.last_candidates_seen = 1
            return self._candidate_from_path(start_path, normalized, policy_decision)
        inventory = self.inventory_service.build_inventory(
            WorkspaceInventoryRequest(
                root_id=normalized.root_id,
                relative_path=normalized.relative_path,
                max_depth=SEARCH_INVENTORY_MAX_DEPTH,
                max_entries=max(normalized.max_files * 50, normalized.max_files),
                include_hidden=normalized.include_hidden,
                include_ignored=False,
                include_files=True,
                include_dirs=True,
            )
        )
        if inventory.blocked_count:
            self.last_files_blocked += inventory.blocked_count
            self.last_warnings.extend(inventory.warnings)
            return [], [
                SelfSearchFileCandidate(
                    root_id=policy_decision.root_id or "",
                    relative_path=normalized.relative_path,
                    suffix=None,
                    size_bytes=None,
                    candidate_status="blocked",
                    finding_type="workspace_inventory_failed",
                    reason="Workspace inventory failed before candidate collection.",
                )
            ]
        included: list[SelfSearchFileCandidate] = []
        skipped: list[SelfSearchFileCandidate] = []
        for entry in inventory.entries:
            if entry.entry_type != "file":
                continue
            self.last_candidates_seen += 1
            glob_reason = _glob_skip_reason(entry.relative_path, normalized.include_globs, normalized.exclude_globs)
            if glob_reason:
                self.last_files_skipped += 1
                _append_skipped(
                    skipped,
                    SelfSearchFileCandidate(
                        root_id=entry.root_id,
                        relative_path=entry.relative_path,
                        suffix=entry.suffix,
                        size_bytes=entry.size_bytes,
                        candidate_status="skipped",
                        finding_type=glob_reason,
                        reason="Candidate path did not satisfy search glob policy.",
                    ),
                )
                continue
            text_decision = self.text_policy_service.decide(
                SelfTextReadRequest(path=entry.relative_path, root_id=normalized.root_id, max_bytes=normalized.max_bytes_per_file)
            )
            if text_decision.blocked:
                self.last_files_blocked += 1
                _append_skipped(
                    skipped,
                    SelfSearchFileCandidate(
                        root_id=entry.root_id,
                        relative_path=entry.relative_path,
                        suffix=entry.suffix,
                        size_bytes=entry.size_bytes,
                        candidate_status="blocked",
                        finding_type=text_decision.finding_type,
                        reason=text_decision.reason,
                    ),
                )
                continue
            if len(included) >= policy_decision.effective_max_files:
                self.last_truncated = True
                self.last_truncated_reason = "max_files"
                break
            included.append(
                SelfSearchFileCandidate(
                    root_id=entry.root_id,
                    relative_path=entry.relative_path,
                    suffix=entry.suffix,
                    size_bytes=entry.size_bytes,
                    candidate_status="included",
                    finding_type=None,
                    reason=None,
                )
            )
        if inventory.truncated and not self.last_truncated:
            self.last_truncated = True
            self.last_truncated_reason = "candidate_inventory_limit"
        return included, skipped

    def _candidate_from_path(
        self,
        path: Path,
        request: SelfWorkspaceSearchRequest,
        policy_decision: SelfWorkspaceSearchPolicyDecision,
    ) -> tuple[list[SelfSearchFileCandidate], list[SelfSearchFileCandidate]]:
        relative_path = path.relative_to(self.path_policy_service.workspace_root).as_posix()
        glob_reason = _glob_skip_reason(relative_path, request.include_globs, request.exclude_globs)
        try:
            size_bytes = path.stat().st_size
        except OSError:
            size_bytes = None
        if glob_reason:
            self.last_files_skipped = 1
            return [], [
                SelfSearchFileCandidate(
                    root_id=policy_decision.root_id or "",
                    relative_path=relative_path,
                    suffix=path.suffix,
                    size_bytes=size_bytes,
                    candidate_status="skipped",
                    finding_type=glob_reason,
                    reason="Candidate path did not satisfy search glob policy.",
                )
            ]
        text_decision = self.text_policy_service.decide(
            SelfTextReadRequest(path=relative_path, root_id=request.root_id, max_bytes=request.max_bytes_per_file)
        )
        if text_decision.blocked:
            self.last_files_blocked = 1
            return [], [
                SelfSearchFileCandidate(
                    root_id=policy_decision.root_id or "",
                    relative_path=relative_path,
                    suffix=path.suffix,
                    size_bytes=size_bytes,
                    candidate_status="blocked",
                    finding_type=text_decision.finding_type,
                    reason=text_decision.reason,
                )
            ]
        return [
            SelfSearchFileCandidate(
                root_id=policy_decision.root_id or "",
                relative_path=relative_path,
                suffix=path.suffix,
                size_bytes=size_bytes,
                candidate_status="included",
                finding_type=None,
                reason=None,
            )
        ], []


class SelfWorkspaceLiteralSearchService:
    def __init__(self, *, text_service: SelfCodeTextPerceptionSkillService | None = None) -> None:
        self.text_service = text_service or SelfCodeTextPerceptionSkillService()

    def search(
        self,
        request: SelfWorkspaceSearchRequest,
        policy_decision: SelfWorkspaceSearchPolicyDecision,
        candidates: list[SelfSearchFileCandidate],
    ) -> tuple[list[SelfSearchMatch], int, bool, str | None, list[str]]:
        normalized = request.normalized()
        matches: list[SelfSearchMatch] = []
        files_scanned = 0
        total_bytes = 0
        truncated = False
        truncated_reason: str | None = None
        warnings: list[str] = []
        query = normalized.query if normalized.case_sensitive else normalized.query.casefold()
        for candidate in candidates:
            if len(matches) >= policy_decision.effective_max_matches:
                truncated = True
                truncated_reason = "max_matches"
                break
            remaining_bytes = policy_decision.effective_max_total_bytes - total_bytes
            if remaining_bytes <= 0:
                truncated = True
                truncated_reason = "max_total_bytes"
                break
            read_limit = min(policy_decision.effective_max_bytes_per_file, remaining_bytes)
            result = self.text_service.read_text(
                SelfTextReadRequest(
                    path=candidate.relative_path,
                    root_id=normalized.root_id,
                    mode="preview",
                    max_bytes=read_limit,
                    max_lines=1000,
                )
            )
            if result.blocked or result.slice is None:
                warnings.append(result.policy_decision.finding_type)
                continue
            files_scanned += 1
            total_bytes += result.slice.bytes_read
            if result.slice.truncated and truncated_reason is None:
                truncated = True
                truncated_reason = "max_bytes_per_file"
            lines = result.slice.content.splitlines()
            per_file_matches = 0
            for index, line in enumerate(lines):
                search_line = line if normalized.case_sensitive else line.casefold()
                start = 0
                while True:
                    position = search_line.find(query, start)
                    if position < 0:
                        break
                    if len(matches) >= policy_decision.effective_max_matches:
                        truncated = True
                        truncated_reason = "max_matches"
                        break
                    if per_file_matches >= normalized.max_matches_per_file:
                        truncated = True
                        truncated_reason = "max_matches_per_file"
                        break
                    line_number = result.slice.start_line + index
                    snippet_lines = _snippet_lines(lines, index, normalized.context_lines)
                    snippet_findings = _findings_for_lines(
                        result.redaction_findings,
                        start_line=line_number - len(snippet_lines["before"]),
                        end_line=line_number + len(snippet_lines["after"]),
                    )
                    matches.append(
                        SelfSearchMatch(
                            match_id=f"self_workspace_search_match:{uuid4()}",
                            root_id=candidate.root_id,
                            relative_path=candidate.relative_path,
                            line_number=line_number,
                            column_start=position + 1,
                            column_end=position + len(normalized.query),
                            snippet=SelfSearchMatchSnippet(
                                before=snippet_lines["before"],
                                line=line,
                                after=snippet_lines["after"],
                                redacted=bool(snippet_findings),
                            ),
                            redaction_findings=snippet_findings,
                        )
                    )
                    per_file_matches += 1
                    start = position + max(1, len(query))
                if truncated and truncated_reason in {"max_matches", "max_matches_per_file"}:
                    break
            if total_bytes >= policy_decision.effective_max_total_bytes:
                truncated = True
                truncated_reason = truncated_reason or "max_total_bytes"
                break
        return matches, files_scanned, truncated, truncated_reason, warnings


class SelfCodeSearchAwarenessSkillService:
    def __init__(self, *, path_policy_service: SelfWorkspacePathPolicyService | None = None) -> None:
        self.path_policy_service = path_policy_service or SelfWorkspacePathPolicyService()
        self.policy_service = SelfWorkspaceSearchPolicyService(path_policy_service=self.path_policy_service)
        self.text_policy_service = SelfTextReadPolicyService(path_policy_service=self.path_policy_service)
        self.candidate_service = SelfSearchCandidateService(
            path_policy_service=self.path_policy_service,
            text_policy_service=self.text_policy_service,
        )
        self.search_service = SelfWorkspaceLiteralSearchService(
            text_service=SelfCodeTextPerceptionSkillService(path_policy_service=self.path_policy_service)
        )

    def search_workspace(self, request: SelfWorkspaceSearchRequest) -> SelfWorkspaceSearchResult:
        normalized = request.normalized()
        decision = self.policy_service.decide(normalized)
        if decision.blocked:
            return SelfWorkspaceSearchResult(
                result_id=f"self_workspace_search_result:{uuid4()}",
                request=normalized,
                policy_decision=decision,
                candidates_seen=0,
                files_scanned=0,
                files_skipped=0,
                files_blocked=0,
                matches=[],
                truncated=False,
                truncated_reason=None,
                skipped_candidates=[],
                evidence_refs=[{"finding_type": decision.finding_type}],
                blocked=True,
                warnings=[decision.reason] if decision.reason else [],
                result_attrs=_result_attrs(),
            )
        candidates, skipped = self.candidate_service.collect_candidates(normalized, decision)
        matches, files_scanned, search_truncated, search_truncated_reason, warnings = self.search_service.search(
            normalized,
            decision,
            candidates,
        )
        truncated = bool(search_truncated or self.candidate_service.last_truncated)
        truncated_reason = search_truncated_reason or self.candidate_service.last_truncated_reason
        return SelfWorkspaceSearchResult(
            result_id=f"self_workspace_search_result:{uuid4()}",
            request=normalized,
            policy_decision=decision,
            candidates_seen=self.candidate_service.last_candidates_seen,
            files_scanned=files_scanned,
            files_skipped=self.candidate_service.last_files_skipped,
            files_blocked=self.candidate_service.last_files_blocked,
            matches=matches,
            truncated=truncated,
            truncated_reason=truncated_reason,
            skipped_candidates=skipped,
            evidence_refs=[
                {"root_id": decision.root_id},
                {"candidate_count": len(candidates)},
                {"match_count": len(matches)},
            ],
            blocked=False,
            warnings=[*self.candidate_service.last_warnings, *warnings],
            result_attrs=_result_attrs(),
        )


def _search_decision(
    request: SelfWorkspaceSearchRequest,
    resolution: WorkspacePathResolution,
    finding_type: str,
    reason: str | None,
    allowed: bool,
) -> SelfWorkspaceSearchPolicyDecision:
    return SelfWorkspaceSearchPolicyDecision(
        allowed=allowed,
        blocked=not allowed,
        finding_type=finding_type,
        reason=reason,
        root_id=resolution.root_id,
        resolved_path=resolution,
        effective_match_mode=request.match_mode,
        effective_max_files=request.max_files,
        effective_max_matches=request.max_matches,
        effective_max_bytes_per_file=request.max_bytes_per_file,
        effective_max_total_bytes=request.max_total_bytes,
    )


def _glob_skip_reason(path: str, include_globs: list[str], exclude_globs: list[str]) -> str | None:
    if include_globs and not any(fnmatch(path, pattern) for pattern in include_globs):
        return "include_glob_skipped"
    if exclude_globs and any(fnmatch(path, pattern) for pattern in exclude_globs):
        return "exclude_glob_skipped"
    return None


def _append_skipped(items: list[SelfSearchFileCandidate], candidate: SelfSearchFileCandidate) -> None:
    if len(items) < SEARCH_SKIPPED_CANDIDATE_LIMIT:
        items.append(candidate)


def _map_path_finding(finding_type: str) -> str:
    if finding_type == "path_traversal":
        return "path_traversal"
    if finding_type == "outside_workspace" or finding_type == "absolute_path_not_allowed":
        return "outside_workspace"
    if finding_type == "private_boundary":
        return "private_boundary"
    if finding_type == "symlink_blocked":
        return "symlink_escape"
    return finding_type


def _snippet_lines(lines: list[str], index: int, context_lines: int) -> dict[str, list[str]]:
    start = max(0, index - context_lines)
    end = min(len(lines), index + context_lines + 1)
    return {
        "before": lines[start:index],
        "after": lines[index + 1 : end],
    }


def _findings_for_lines(
    findings: list[SelfTextRedactionFinding],
    *,
    start_line: int,
    end_line: int,
) -> list[SelfTextRedactionFinding]:
    return [item for item in findings if start_line <= item.line_number <= end_line]


def _result_attrs() -> dict[str, Any]:
    return {
        "effect_type": READ_ONLY_OBSERVATION_EFFECT,
        "read_only": True,
        "policy_gated": True,
        "bounded_search": True,
        "literal_match_only": True,
        "redaction_enabled": True,
        "workspace_write_used": False,
        "shell_execution_used": False,
        "network_access_used": False,
        "mcp_connection_used": False,
        "plugin_loading_used": False,
        "external_harness_execution_used": False,
        "memory_mutation_used": False,
        "persona_mutation_used": False,
        "overlay_mutation_used": False,
        "semantic_retrieval_used": False,
        "summary_used": False,
        "symbol_parse_used": False,
    }
