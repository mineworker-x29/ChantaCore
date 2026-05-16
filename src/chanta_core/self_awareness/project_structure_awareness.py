from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal
from uuid import uuid4

from chanta_core.self_awareness.workspace_awareness import (
    READ_ONLY_OBSERVATION_EFFECT,
    SelfWorkspaceInventoryService,
    SelfWorkspacePathPolicyService,
    WorkspaceInventoryEntry,
    WorkspaceInventoryRequest,
    WorkspacePathResolution,
)


PROJECT_STRUCTURE_EFFECTS = [READ_ONLY_OBSERVATION_EFFECT, "state_candidate_created"]
PROJECT_STRUCTURE_STATE = "project_surface_structure_awareness"
DEFAULT_PROJECT_MAX_DEPTH = 5
DEFAULT_PROJECT_MAX_ENTRIES = 2000
PROJECT_MAX_DEPTH_CAP = 10
PROJECT_MAX_ENTRIES_CAP = 5000

README_NAMES = {"readme", "readme.md", "readme.rst", "readme.txt"}
DOCS_DIR_NAMES = {"docs", "doc", "documentation"}
SOURCE_DIR_NAMES = {"app", "src", "lib", "packages", "services"}
TEST_DIR_NAMES = {"tests", "test", "specs", "spec"}
DEPENDENCY_MANIFEST_NAMES = {
    "pyproject.toml",
    "package.json",
    "requirements.txt",
    "poetry.lock",
    "pnpm-lock.yaml",
    "yarn.lock",
    "cargo.toml",
    "go.mod",
    "pom.xml",
    "build.gradle",
}
CONFIG_SUFFIXES = {".yaml", ".yml", ".toml", ".ini", ".cfg", ".json", ".jsonc"}
CONFIG_NAMES = {".env.example"}
ENTRYPOINT_NAMES = {"main.py", "app.py", "cli.py", "__main__.py", "index.ts", "index.js", "server.py"}
SCRIPT_SUFFIXES = {".ps1", ".sh", ".bat", ".cmd"}
CI_PATHS = {".github/workflows", ".gitlab-ci.yml", "azure-pipelines.yml"}


@dataclass(frozen=True)
class SelfProjectStructureRequest:
    root_id: str | None = None
    relative_path: str = "."
    max_depth: int = DEFAULT_PROJECT_MAX_DEPTH
    max_entries: int = DEFAULT_PROJECT_MAX_ENTRIES
    include_hidden: bool = False
    include_ignored: bool = False
    include_summary_candidates: bool = True
    include_candidate_surfaces: bool = True

    def normalized(self) -> "SelfProjectStructureRequest":
        return SelfProjectStructureRequest(
            root_id=self.root_id,
            relative_path=self.relative_path or ".",
            max_depth=min(max(0, int(self.max_depth)), PROJECT_MAX_DEPTH_CAP),
            max_entries=min(max(0, int(self.max_entries)), PROJECT_MAX_ENTRIES_CAP),
            include_hidden=bool(self.include_hidden),
            include_ignored=bool(self.include_ignored),
            include_summary_candidates=bool(self.include_summary_candidates),
            include_candidate_surfaces=bool(self.include_candidate_surfaces),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "root_id": self.root_id,
            "relative_path": self.relative_path,
            "max_depth": self.max_depth,
            "max_entries": self.max_entries,
            "include_hidden": self.include_hidden,
            "include_ignored": self.include_ignored,
            "include_summary_candidates": self.include_summary_candidates,
            "include_candidate_surfaces": self.include_candidate_surfaces,
        }


@dataclass(frozen=True)
class SelfProjectStructurePolicyDecision:
    allowed: bool
    blocked: bool
    finding_type: str
    reason: str | None
    root_id: str | None
    resolved_path: WorkspacePathResolution
    effective_max_depth: int
    effective_max_entries: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "allowed": self.allowed,
            "blocked": self.blocked,
            "finding_type": self.finding_type,
            "reason": self.reason,
            "root_id": self.root_id,
            "resolved_path": self.resolved_path.to_dict(),
            "effective_max_depth": self.effective_max_depth,
            "effective_max_entries": self.effective_max_entries,
        }


@dataclass(frozen=True)
class ProjectTreeNode:
    node_id: str
    root_id: str
    relative_path: str
    node_type: Literal["directory", "file"]
    depth: int
    suffix: str | None
    file_kind: str | None
    size_bytes: int | None
    children_count: int
    is_hidden: bool
    is_excluded: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "node_id": self.node_id,
            "root_id": self.root_id,
            "relative_path": self.relative_path,
            "node_type": self.node_type,
            "depth": self.depth,
            "suffix": self.suffix,
            "file_kind": self.file_kind,
            "size_bytes": self.size_bytes,
            "children_count": self.children_count,
            "is_hidden": self.is_hidden,
            "is_excluded": self.is_excluded,
        }


@dataclass(frozen=True)
class ProjectSurfaceCandidate:
    candidate_id: str
    candidate_type: Literal[
        "readme",
        "docs_root",
        "source_root",
        "test_root",
        "config_file",
        "dependency_manifest",
        "entrypoint_file",
        "package_root",
        "script_file",
        "ci_config",
    ]
    relative_path: str
    confidence: Literal["high", "medium", "low"]
    reason: str
    evidence_refs: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "candidate_type": self.candidate_type,
            "relative_path": self.relative_path,
            "confidence": self.confidence,
            "reason": self.reason,
            "evidence_refs": [dict(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class ProjectFileKindDistribution:
    total_files: int
    total_dirs: int
    by_suffix: dict[str, int]
    by_file_kind: dict[str, int]
    by_top_level_dir: dict[str, int]

    def to_dict(self) -> dict[str, Any]:
        return {
            "total_files": self.total_files,
            "total_dirs": self.total_dirs,
            "by_suffix": dict(self.by_suffix),
            "by_file_kind": dict(self.by_file_kind),
            "by_top_level_dir": dict(self.by_top_level_dir),
        }


@dataclass(frozen=True)
class SelfProjectStructureCandidate:
    candidate_id: str
    root_id: str
    relative_path: str
    tree_nodes: list[ProjectTreeNode]
    file_distribution: ProjectFileKindDistribution
    surface_candidates: list[ProjectSurfaceCandidate]
    linked_summary_candidate_ids: list[str]
    evidence_refs: list[dict[str, Any]]
    limitations: list[str]
    confidence: Literal["high", "medium", "low"]
    truncated: bool
    truncated_reason: str | None
    review_status: str = "candidate_only"
    canonical_promotion_enabled: bool = False
    promoted: bool = False
    policy_decision: SelfProjectStructurePolicyDecision | None = None
    candidate_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "root_id": self.root_id,
            "relative_path": self.relative_path,
            "tree_nodes": [item.to_dict() for item in self.tree_nodes],
            "file_distribution": self.file_distribution.to_dict(),
            "surface_candidates": [item.to_dict() for item in self.surface_candidates],
            "linked_summary_candidate_ids": list(self.linked_summary_candidate_ids),
            "evidence_refs": [dict(item) for item in self.evidence_refs],
            "limitations": list(self.limitations),
            "confidence": self.confidence,
            "truncated": self.truncated,
            "truncated_reason": self.truncated_reason,
            "review_status": self.review_status,
            "canonical_promotion_enabled": self.canonical_promotion_enabled,
            "promoted": self.promoted,
            "policy_decision": self.policy_decision.to_dict() if self.policy_decision else None,
            "candidate_attrs": dict(self.candidate_attrs),
        }


class SelfProjectStructurePolicyService:
    def __init__(self, *, path_policy_service: SelfWorkspacePathPolicyService | None = None) -> None:
        self.path_policy_service = path_policy_service or SelfWorkspacePathPolicyService()

    def decide(self, request: SelfProjectStructureRequest) -> SelfProjectStructurePolicyDecision:
        normalized = request.normalized()
        resolution = self.path_policy_service.resolve_path(normalized.relative_path, root_id=normalized.root_id)
        if resolution.blocked:
            return _project_policy_decision(normalized, resolution, resolution.finding_type, resolution.reason, False)
        target = Path(resolution.canonical_path)
        if not target.exists():
            return _project_policy_decision(normalized, resolution, "not_found", "Target path was not found.", False)
        if not target.is_dir():
            return _project_policy_decision(normalized, resolution, "not_directory", "Target path must be a directory.", False)
        return _project_policy_decision(normalized, resolution, "ok", None, True)


class ProjectTreeSnapshotService:
    def __init__(
        self,
        *,
        inventory_service: SelfWorkspaceInventoryService | None = None,
    ) -> None:
        self.inventory_service = inventory_service or SelfWorkspaceInventoryService()

    def build_tree(
        self,
        request: SelfProjectStructureRequest,
        policy_decision: SelfProjectStructurePolicyDecision,
    ) -> tuple[list[ProjectTreeNode], bool, str | None, int, int]:
        if policy_decision.blocked:
            return [], False, None, 0, 0
        inventory = self.inventory_service.build_inventory(
            WorkspaceInventoryRequest(
                root_id=request.root_id,
                relative_path=request.relative_path,
                max_depth=policy_decision.effective_max_depth,
                max_entries=policy_decision.effective_max_entries,
                include_hidden=request.include_hidden,
                include_ignored=request.include_ignored,
                include_files=True,
                include_dirs=True,
            )
        )
        if inventory.blocked_count:
            return [], False, "inventory_failed", inventory.total_entries_seen, inventory.total_entries_returned
        nodes = [_node_from_entry(item) for item in inventory.entries]
        child_counts = _child_counts(nodes)
        nodes = [
            ProjectTreeNode(
                **{
                    **node.to_dict(),
                    "children_count": child_counts.get(node.relative_path, 0),
                }
            )
            for node in nodes
        ]
        reason = "max_entries" if inventory.truncated else None
        return nodes, inventory.truncated, reason, inventory.total_entries_seen, inventory.total_entries_returned


class ProjectSurfaceCandidateDetector:
    def detect(self, tree_nodes: list[ProjectTreeNode]) -> list[ProjectSurfaceCandidate]:
        candidates: list[ProjectSurfaceCandidate] = []
        for node in tree_nodes:
            candidates.extend(_surface_candidates_for_node(node))
        return candidates


class ProjectFileKindDistributionService:
    def summarize(self, tree_nodes: list[ProjectTreeNode]) -> ProjectFileKindDistribution:
        total_files = sum(1 for item in tree_nodes if item.node_type == "file")
        total_dirs = sum(1 for item in tree_nodes if item.node_type == "directory")
        by_suffix: dict[str, int] = {}
        by_file_kind: dict[str, int] = {}
        by_top_level_dir: dict[str, int] = {}
        for node in tree_nodes:
            if node.node_type == "file":
                suffix = node.suffix or "<none>"
                by_suffix[suffix] = by_suffix.get(suffix, 0) + 1
            kind = node.file_kind or node.node_type
            by_file_kind[kind] = by_file_kind.get(kind, 0) + 1
            top = node.relative_path.split("/", 1)[0] if "/" in node.relative_path else "."
            by_top_level_dir[top] = by_top_level_dir.get(top, 0) + 1
        return ProjectFileKindDistribution(
            total_files=total_files,
            total_dirs=total_dirs,
            by_suffix=by_suffix,
            by_file_kind=by_file_kind,
            by_top_level_dir=by_top_level_dir,
        )


class SelfProjectStructureAwarenessService:
    def __init__(self, *, path_policy_service: SelfWorkspacePathPolicyService | None = None) -> None:
        self.path_policy_service = path_policy_service or SelfWorkspacePathPolicyService()
        self.policy_service = SelfProjectStructurePolicyService(path_policy_service=self.path_policy_service)
        self.tree_service = ProjectTreeSnapshotService(
            inventory_service=SelfWorkspaceInventoryService(path_policy_service=self.path_policy_service)
        )
        self.surface_detector = ProjectSurfaceCandidateDetector()
        self.distribution_service = ProjectFileKindDistributionService()

    def inspect_project_structure(self, request: SelfProjectStructureRequest) -> SelfProjectStructureCandidate:
        normalized = request.normalized()
        decision = self.policy_service.decide(normalized)
        if decision.blocked:
            return _blocked_candidate(normalized, decision)
        nodes, truncated, truncated_reason, seen, returned = self.tree_service.build_tree(normalized, decision)
        surfaces = self.surface_detector.detect(nodes) if normalized.include_candidate_surfaces else []
        distribution = self.distribution_service.summarize(nodes)
        limitations = ["metadata_only_surface_mapping", "no_architecture_inference", "no_dependency_or_import_resolution"]
        if truncated:
            limitations.append(f"truncated_by_{truncated_reason or 'inventory_limit'}")
        if not normalized.include_summary_candidates:
            limitations.append("summary_candidate_linking_disabled")
        return SelfProjectStructureCandidate(
            candidate_id=f"self_project_structure_candidate:{uuid4()}",
            root_id=decision.root_id or "workspace_root:primary",
            relative_path=decision.resolved_path.normalized_path,
            tree_nodes=nodes,
            file_distribution=distribution,
            surface_candidates=surfaces,
            linked_summary_candidate_ids=[],
            evidence_refs=[
                {"relative_path": decision.resolved_path.normalized_path},
                {"inventory_total_entries_seen": seen},
                {"inventory_total_entries_returned": returned},
            ],
            limitations=limitations,
            confidence="medium" if truncated else "high",
            truncated=truncated,
            truncated_reason=truncated_reason,
            policy_decision=decision,
            candidate_attrs=_candidate_attrs(),
        )


class SelfProjectStructureAwarenessSkillService:
    def __init__(self, *, path_policy_service: SelfWorkspacePathPolicyService | None = None) -> None:
        self.service = SelfProjectStructureAwarenessService(path_policy_service=path_policy_service)

    def inspect_project_structure(self, request: SelfProjectStructureRequest) -> SelfProjectStructureCandidate:
        return self.service.inspect_project_structure(request)


def _project_policy_decision(
    request: SelfProjectStructureRequest,
    resolution: WorkspacePathResolution,
    finding_type: str,
    reason: str | None,
    allowed: bool,
) -> SelfProjectStructurePolicyDecision:
    return SelfProjectStructurePolicyDecision(
        allowed=allowed,
        blocked=not allowed,
        finding_type=finding_type,
        reason=reason,
        root_id=resolution.root_id,
        resolved_path=resolution,
        effective_max_depth=request.max_depth,
        effective_max_entries=request.max_entries,
    )


def _blocked_candidate(
    request: SelfProjectStructureRequest,
    decision: SelfProjectStructurePolicyDecision,
) -> SelfProjectStructureCandidate:
    return SelfProjectStructureCandidate(
        candidate_id=f"self_project_structure_candidate:{uuid4()}",
        root_id=decision.root_id or "workspace_root:primary",
        relative_path=decision.resolved_path.normalized_path,
        tree_nodes=[],
        file_distribution=ProjectFileKindDistribution(0, 0, {}, {}, {}),
        surface_candidates=[],
        linked_summary_candidate_ids=[],
        evidence_refs=[{"finding_type": decision.finding_type}],
        limitations=[decision.reason or decision.finding_type],
        confidence="low",
        truncated=False,
        truncated_reason=None,
        policy_decision=decision,
        candidate_attrs=_candidate_attrs(blocked=True),
    )


def _node_from_entry(entry: WorkspaceInventoryEntry) -> ProjectTreeNode:
    node_type = "directory" if entry.entry_type == "directory" else "file"
    return ProjectTreeNode(
        node_id=f"project_tree_node:{uuid4()}",
        root_id=entry.root_id,
        relative_path=entry.relative_path,
        node_type=node_type,
        depth=entry.depth,
        suffix=entry.suffix or None,
        file_kind=_file_kind(entry.relative_path, node_type, entry.suffix),
        size_bytes=entry.size_bytes,
        children_count=0,
        is_hidden=entry.is_hidden,
        is_excluded=entry.is_excluded,
    )


def _child_counts(nodes: list[ProjectTreeNode]) -> dict[str, int]:
    paths = {node.relative_path for node in nodes if node.node_type == "directory"}
    counts = {path: 0 for path in paths}
    for node in nodes:
        parent = str(Path(node.relative_path).parent).replace("\\", "/")
        parent = "." if parent == "." else parent
        if parent in counts:
            counts[parent] += 1
    return counts


def _file_kind(relative_path: str, node_type: str, suffix: str | None) -> str | None:
    if node_type == "directory":
        return "directory"
    name = Path(relative_path).name.casefold()
    lowered = relative_path.casefold()
    if name in README_NAMES:
        return "readme"
    if name in DEPENDENCY_MANIFEST_NAMES:
        return "dependency_manifest"
    if name in ENTRYPOINT_NAMES:
        return "entrypoint_file"
    if _is_ci_path(lowered):
        return "ci_config"
    if suffix in {".py"}:
        return "python"
    if suffix in {".md", ".markdown", ".rst"}:
        return "markdown"
    if suffix in {".json", ".jsonc"}:
        return "json"
    if suffix in {".yaml", ".yml"}:
        return "yaml"
    if suffix == ".toml":
        return "toml"
    if suffix in SCRIPT_SUFFIXES:
        return "script"
    if suffix in CONFIG_SUFFIXES or name in CONFIG_NAMES:
        return "config"
    return "other"


def _surface_candidates_for_node(node: ProjectTreeNode) -> list[ProjectSurfaceCandidate]:
    name = Path(node.relative_path).name.casefold()
    lowered = node.relative_path.casefold()
    candidates: list[ProjectSurfaceCandidate] = []
    if node.node_type == "file" and name in README_NAMES:
        candidates.append(_surface_candidate("readme", node, "README filename pattern", "high"))
    if node.node_type == "directory" and name in DOCS_DIR_NAMES:
        candidates.append(_surface_candidate("docs_root", node, "docs directory name pattern", "high"))
    if node.node_type == "directory" and name in SOURCE_DIR_NAMES:
        candidates.append(_surface_candidate("source_root", node, "source directory name pattern", "medium"))
        if name == "packages":
            candidates.append(_surface_candidate("package_root", node, "package directory name pattern", "medium"))
    if node.node_type == "directory" and name in TEST_DIR_NAMES:
        candidates.append(_surface_candidate("test_root", node, "test directory name pattern", "high"))
    if node.node_type == "file" and name in DEPENDENCY_MANIFEST_NAMES:
        candidates.append(_surface_candidate("dependency_manifest", node, "dependency manifest filename pattern", "high"))
    if node.node_type == "file" and (node.suffix in CONFIG_SUFFIXES or name in CONFIG_NAMES):
        candidates.append(_surface_candidate("config_file", node, "configuration filename or suffix pattern", "medium"))
    if node.node_type == "file" and name in ENTRYPOINT_NAMES:
        candidates.append(_surface_candidate("entrypoint_file", node, "entrypoint filename heuristic", "medium"))
    if node.node_type == "file" and node.suffix in SCRIPT_SUFFIXES:
        candidates.append(_surface_candidate("script_file", node, "script suffix pattern", "medium"))
    if _is_ci_path(lowered):
        candidates.append(_surface_candidate("ci_config", node, "CI path/name pattern", "medium"))
    return candidates


def _surface_candidate(
    candidate_type: str,
    node: ProjectTreeNode,
    reason: str,
    confidence: str,
) -> ProjectSurfaceCandidate:
    return ProjectSurfaceCandidate(
        candidate_id=f"project_surface_candidate:{uuid4()}",
        candidate_type=candidate_type,  # type: ignore[arg-type]
        relative_path=node.relative_path,
        confidence=confidence,  # type: ignore[arg-type]
        reason=reason,
        evidence_refs=[
            {
                "relative_path": node.relative_path,
                "node_type": node.node_type,
                "file_kind": node.file_kind,
            }
        ],
    )


def _is_ci_path(lowered_relative_path: str) -> bool:
    return (
        lowered_relative_path.startswith(".github/workflows/")
        or lowered_relative_path in CI_PATHS
        or lowered_relative_path.endswith("/.gitlab-ci.yml")
        or lowered_relative_path.endswith("/azure-pipelines.yml")
    )


def _candidate_attrs(*, blocked: bool = False) -> dict[str, Any]:
    return {
        "effect_types": list(PROJECT_STRUCTURE_EFFECTS),
        "read_only": True,
        "policy_gated": True,
        "metadata_only_tree": True,
        "deterministic_surface_mapping": True,
        "llm_architecture_inference_used": False,
        "dependency_graph_created": False,
        "import_resolution_used": False,
        "runtime_introspection_used": False,
        "canonical_promotion_enabled": False,
        "promoted": False,
        "blocked": blocked,
        "workspace_write_used": False,
        "shell_execution_used": False,
        "network_access_used": False,
        "mcp_connection_used": False,
        "plugin_loading_used": False,
        "external_harness_execution_used": False,
        "memory_mutation_used": False,
        "persona_mutation_used": False,
        "overlay_mutation_used": False,
    }
