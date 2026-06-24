"""Architecture contract artifacts for Schumpeter v0.43.9."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any


class V0439TUIEngineKind(StrEnum):
    PURE_SNAPSHOT_RENDERER = "pure_snapshot_renderer"
    PROMPT_TOOLKIT_SHELL = "prompt_toolkit_shell"
    TEXTUAL_FULL_TUI = "textual_full_tui"
    RICH_STATIC_LAYOUT = "rich_static_layout"
    PLAIN_TERMINAL = "plain_terminal"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class V0439TUILibraryDecision:
    decision_id: str
    current_version_engine: str
    recommended_v0439_engine: str
    recommended_v04310_engine: str
    textual_dependency_added_now: bool
    prompt_toolkit_required_now: bool
    rich_required_now: bool
    reason: str
    production_certified: bool


@dataclass(frozen=True)
class V0439TUIArchitecturePolicy:
    policy_id: str
    runtime_core_separated_from_tui: bool
    runtime_adapter_required: bool
    ui_state_required: bool
    components_are_pure_renderers: bool
    renderers_separated_by_surface: bool
    snapshot_mode_required: bool
    no_side_effect_rendering_required: bool
    production_certified: bool


@dataclass(frozen=True)
class V04310StructuredTUIMVPHandoff:
    handoff_id: str
    target_version: str
    objective: str
    allowed_scope: tuple[str, ...]
    still_closed: tuple[str, ...]
    production_certified: bool


@dataclass(frozen=True)
class V0440ControlledWorkspaceReadDesignHandoff:
    handoff_id: str
    target_version: str
    objective: str
    allowed_scope: tuple[str, ...]
    closed_until_gate: tuple[str, ...]
    production_certified: bool


@dataclass(frozen=True)
class V0439IntegratedRestoreContextSnapshot:
    snapshot_id: str
    current_version: str
    current_track: str
    product_name: str
    contract_scope: str
    integrated_doc_path: str
    production_certified: bool


@dataclass(frozen=True)
class V0439IntegratedRestorePacket:
    packet_id: str
    snapshot: V0439IntegratedRestoreContextSnapshot
    required_sections: tuple[str, ...]
    restore_prompt: str
    production_certified: bool


@dataclass(frozen=True)
class V0439IntegratedRestoreDocumentManifest:
    manifest_id: str
    integrated_doc_path: str
    integrated_doc_required: bool
    separate_v0439_docs_allowed: bool
    separate_v0439_docs_created: bool
    required_sections_present: bool
    production_certified: bool


@dataclass(frozen=True)
class V04311UserFeedbackPolishHandoff:
    handoff_id: str
    target_version: str
    objective: str
    feedback_surfaces: tuple[str, ...]
    still_closed: tuple[str, ...]
    production_certified: bool


@dataclass(frozen=True)
class V04310IntegratedRestoreContextSnapshot:
    snapshot_id: str
    current_version: str
    current_track: str
    product_name: str
    mvp_scope: str
    integrated_doc_path: str
    production_certified: bool


@dataclass(frozen=True)
class V04310IntegratedRestorePacket:
    packet_id: str
    snapshot: V04310IntegratedRestoreContextSnapshot
    required_sections: tuple[str, ...]
    restore_prompt: str
    production_certified: bool


@dataclass(frozen=True)
class V04310IntegratedRestoreDocumentManifest:
    manifest_id: str
    integrated_doc_path: str
    integrated_doc_required: bool
    separate_v04310_docs_allowed: bool
    separate_v04310_docs_created: bool
    required_sections_present: bool
    production_certified: bool


REQUIRED_V0439_RESTORE_SECTIONS = (
    "Restore Purpose",
    "One-Screen Restore Summary",
    "Current Version and Track Identity",
    "v0.43.7 / v0.43.8 Baseline Requirements",
    "User UX Reference and Goal",
    "Structured TUI Architecture Principle",
    "Runtime Core vs TUI Shell Boundary",
    "RuntimeAdapter Contract",
    "UIState Model",
    "Component Boundary",
    "Renderer Boundary",
    "Layout Contract",
    "Display Width and Terminal Compatibility",
    "Command Palette Integration Contract",
    "Snapshot Mode Contract",
    "Golden Snapshot Acceptance",
    "No-Side-Effect Policy",
    "Forbidden Runtime Calls",
    "Still-Closed Capabilities",
    "Required Test Commands",
    "Manual Acceptance Commands",
    "Withdrawal Conditions",
    "v0.43.10 Structured TUI MVP Handoff",
    "v0.44 Controlled Workspace Read Design Gate",
    "Copy-Paste Restore Prompt for Future GPT/Codex Session",
)

REQUIRED_V04310_RESTORE_SECTIONS = (
    "Restore Purpose",
    "One-Screen Restore Summary",
    "Current Version and Track Identity",
    "v0.43.9 Architecture Baseline",
    "v0.43.10 Goal",
    "Structured TUI MVP Scope",
    "TUI Entrypoint Policy",
    "prompt_toolkit / Plain Fallback Policy",
    "RuntimeAdapter Contract",
    "TUI App State Model",
    "Sidebar Component",
    "Main Chat Component",
    "Input Box Component",
    "Status Bar / PI Monitor",
    "Slash Command Palette",
    "Renderer Boundary",
    "Snapshot Mode",
    "Manual UI Acceptance Guide",
    "No-Side-Effect Policy",
    "Safety Boundary",
    "Required Test Commands",
    "Manual Acceptance Commands",
    "Withdrawal Conditions",
    "v0.43.11 User Feedback Polish Handoff",
    "v0.44 Controlled Workspace Read Gate",
    "Copy-Paste Restore Prompt for Future GPT/Codex Session",
)


def create_v0439_tui_library_decision(**overrides: Any) -> V0439TUILibraryDecision:
    defaults = {
        "decision_id": "v0439-tui-library-decision",
        "current_version_engine": V0439TUIEngineKind.PLAIN_TERMINAL.value,
        "recommended_v0439_engine": V0439TUIEngineKind.PURE_SNAPSHOT_RENDERER.value,
        "recommended_v04310_engine": V0439TUIEngineKind.PROMPT_TOOLKIT_SHELL.value,
        "textual_dependency_added_now": False,
        "prompt_toolkit_required_now": False,
        "rich_required_now": False,
        "reason": "v0.43.9 opens the architecture and deterministic snapshot contract before a full interactive TUI.",
        "production_certified": False,
    }
    defaults.update(overrides)
    return V0439TUILibraryDecision(**defaults)


def create_v0439_tui_architecture_policy(**overrides: Any) -> V0439TUIArchitecturePolicy:
    defaults = {
        "policy_id": "v0439-tui-architecture-policy",
        "runtime_core_separated_from_tui": True,
        "runtime_adapter_required": True,
        "ui_state_required": True,
        "components_are_pure_renderers": True,
        "renderers_separated_by_surface": True,
        "snapshot_mode_required": True,
        "no_side_effect_rendering_required": True,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V0439TUIArchitecturePolicy(**defaults)


def create_v04310_structured_tui_mvp_handoff(**overrides: Any) -> V04310StructuredTUIMVPHandoff:
    defaults = {
        "handoff_id": "v04310-structured-tui-mvp-handoff",
        "target_version": "v0.43.10 Structured TUI MVP",
        "objective": "Build the first bounded interactive shell after the v0.43.9 snapshot contract is stable.",
        "allowed_scope": ("keyboard loop design", "focus model", "component composition", "non-provider command entry"),
        "still_closed": ("workspace read", "repo search", "shell/git", "file edit/apply", "provider tools", "subagents", "memory mutation", "production certification"),
        "production_certified": False,
    }
    defaults.update(overrides)
    return V04310StructuredTUIMVPHandoff(**defaults)


def create_v0440_controlled_workspace_read_design_handoff(**overrides: Any) -> V0440ControlledWorkspaceReadDesignHandoff:
    defaults = {
        "handoff_id": "v0440-controlled-workspace-read-design-handoff",
        "target_version": "v0.44.0 Controlled Workspace Read Design Gate",
        "objective": "Design workspace read only after TUI gates and explicit scope rules are accepted.",
        "allowed_scope": ("design", "scope contract", "risk register", "approval gate", "negative tests"),
        "closed_until_gate": ("workspace read implementation", "repo search", "arbitrary path read", "shell/git", "memory mutation"),
        "production_certified": False,
    }
    defaults.update(overrides)
    return V0440ControlledWorkspaceReadDesignHandoff(**defaults)


def create_v0439_integrated_restore_context_snapshot(**overrides: Any) -> V0439IntegratedRestoreContextSnapshot:
    defaults = {
        "snapshot_id": "v0439-integrated-restore-context",
        "current_version": "v0.43.9",
        "current_track": "Business Work Session Pilot & Process Intelligence Review Loop",
        "product_name": "Schumpeter",
        "contract_scope": "structured TUI architecture and deterministic snapshot harness",
        "integrated_doc_path": "docs/versions/v0.43/v0.43.9_schumpeter_structured_tui_architecture_restore.md",
        "production_certified": False,
    }
    defaults.update(overrides)
    return V0439IntegratedRestoreContextSnapshot(**defaults)


def create_v0439_integrated_restore_packet(**overrides: Any) -> V0439IntegratedRestorePacket:
    defaults = {
        "packet_id": "v0439-integrated-restore-packet",
        "snapshot": create_v0439_integrated_restore_context_snapshot(),
        "required_sections": REQUIRED_V0439_RESTORE_SECTIONS,
        "restore_prompt": "Restore Schumpeter v0.43.9 structured TUI architecture contract and keep all runtime side effects closed.",
        "production_certified": False,
    }
    defaults.update(overrides)
    return V0439IntegratedRestorePacket(**defaults)


def create_v0439_integrated_restore_document_manifest(**overrides: Any) -> V0439IntegratedRestoreDocumentManifest:
    defaults = {
        "manifest_id": "v0439-integrated-restore-document-manifest",
        "integrated_doc_path": "docs/versions/v0.43/v0.43.9_schumpeter_structured_tui_architecture_restore.md",
        "integrated_doc_required": True,
        "separate_v0439_docs_allowed": False,
        "separate_v0439_docs_created": False,
        "required_sections_present": True,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V0439IntegratedRestoreDocumentManifest(**defaults)


def create_v04311_user_feedback_polish_handoff(**overrides: Any) -> V04311UserFeedbackPolishHandoff:
    defaults = {
        "handoff_id": "v04311-user-feedback-polish-handoff",
        "target_version": "v0.43.11 User Feedback Visual Polish",
        "objective": "Collect manual TUI feedback and polish layout density, focus behavior, and transcript rendering.",
        "feedback_surfaces": ("sidebar", "main chat", "input", "status line", "command palette"),
        "still_closed": ("workspace read", "repo search", "shell/git", "edit/apply", "provider tools", "subagents", "memory mutation", "production certification"),
        "production_certified": False,
    }
    defaults.update(overrides)
    return V04311UserFeedbackPolishHandoff(**defaults)


def create_v04310_integrated_restore_context_snapshot(**overrides: Any) -> V04310IntegratedRestoreContextSnapshot:
    defaults = {
        "snapshot_id": "v04310-integrated-restore-context",
        "current_version": "v0.43.10",
        "current_track": "Business Work Session Pilot & Process Intelligence Review Loop",
        "product_name": "Schumpeter",
        "mvp_scope": "structured TUI preview entrypoint, plain/prompt_toolkit fallback loop, snapshot mode",
        "integrated_doc_path": "docs/versions/v0.43/v0.43.10_schumpeter_structured_tui_mvp_restore.md",
        "production_certified": False,
    }
    defaults.update(overrides)
    return V04310IntegratedRestoreContextSnapshot(**defaults)


def create_v04310_integrated_restore_packet(**overrides: Any) -> V04310IntegratedRestorePacket:
    defaults = {
        "packet_id": "v04310-integrated-restore-packet",
        "snapshot": create_v04310_integrated_restore_context_snapshot(),
        "required_sections": REQUIRED_V04310_RESTORE_SECTIONS,
        "restore_prompt": "Restore Schumpeter v0.43.10 structured TUI MVP and keep rendering/status/palette/snapshot side-effect-free.",
        "production_certified": False,
    }
    defaults.update(overrides)
    return V04310IntegratedRestorePacket(**defaults)


def create_v04310_integrated_restore_document_manifest(**overrides: Any) -> V04310IntegratedRestoreDocumentManifest:
    defaults = {
        "manifest_id": "v04310-integrated-restore-document-manifest",
        "integrated_doc_path": "docs/versions/v0.43/v0.43.10_schumpeter_structured_tui_mvp_restore.md",
        "integrated_doc_required": True,
        "separate_v04310_docs_allowed": False,
        "separate_v04310_docs_created": False,
        "required_sections_present": True,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V04310IntegratedRestoreDocumentManifest(**defaults)


__all__ = [name for name in globals() if name.startswith("V0439") or name.startswith("V04310") or name.startswith("V04311") or name.startswith("V0440") or name.startswith("create_v043")]
