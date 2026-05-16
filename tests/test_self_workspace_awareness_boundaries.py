from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from chanta_core.self_awareness import (
    SelfWorkspaceInventoryService,
    SelfWorkspacePathPolicyService,
    WorkspaceInventoryRequest,
)
from chanta_core.skills.execution_gate import SkillExecutionGateService
from chanta_core.skills.invocation import ExplicitSkillInvocationService


@pytest.fixture
def workspace_root() -> Path:
    with tempfile.TemporaryDirectory() as directory:
        yield Path(directory)


def test_verify_path_blocks_traversal_variants(workspace_root: Path) -> None:
    service = SelfWorkspacePathPolicyService(workspace_root=workspace_root)

    for candidate in ["../", "..\\", "../../"]:
        resolution = service.resolve_path(candidate)
        assert resolution.blocked is True
        assert resolution.finding_type == "path_traversal"
        assert resolution.within_workspace is False


def test_verify_path_blocks_absolute_outside_workspace(workspace_root: Path) -> None:
    outside = workspace_root.parent / "outside.txt"
    service = SelfWorkspacePathPolicyService(workspace_root=workspace_root)

    resolution = service.resolve_path(str(outside))

    assert resolution.blocked is True
    assert resolution.finding_type == "absolute_path_not_allowed"


def test_verify_path_blocks_private_boundary_fixture(workspace_root: Path) -> None:
    (workspace_root / "private_zone").mkdir()
    service = SelfWorkspacePathPolicyService(
        workspace_root=workspace_root,
        private_boundary_names={"private_zone"},
    )

    resolution = service.resolve_path("private_zone")

    assert resolution.blocked is True
    assert resolution.finding_type == "private_boundary"


def test_inventory_returns_structured_blocked_report_for_traversal(workspace_root: Path) -> None:
    service = SelfWorkspaceInventoryService(
        path_policy_service=SelfWorkspacePathPolicyService(workspace_root=workspace_root)
    )

    report = service.build_inventory(WorkspaceInventoryRequest(relative_path="../"))

    assert report.blocked_count == 1
    assert report.entries == []
    assert report.findings[0].finding_type == "path_traversal"


def test_inventory_excludes_private_boundary_children(workspace_root: Path) -> None:
    (workspace_root / "private_zone").mkdir()
    (workspace_root / "visible").mkdir()
    service = SelfWorkspaceInventoryService(
        path_policy_service=SelfWorkspacePathPolicyService(
            workspace_root=workspace_root,
            private_boundary_names={"private_zone"},
        )
    )

    report = service.build_inventory(WorkspaceInventoryRequest(relative_path=".", max_depth=1))

    assert "visible" in {entry.relative_path for entry in report.entries}
    assert "private_zone" not in {entry.relative_path for entry in report.entries}
    assert report.excluded_count == 1


def test_symlink_path_is_blocked_by_default(workspace_root: Path) -> None:
    target = workspace_root / "target"
    target.mkdir()
    link = workspace_root / "link"
    try:
        link.symlink_to(target, target_is_directory=True)
    except OSError:
        return
    service = SelfWorkspacePathPolicyService(workspace_root=workspace_root)

    resolution = service.resolve_path("link")

    assert resolution.blocked is True
    assert resolution.finding_type == "symlink_blocked"


def test_gate_blocks_path_traversal_before_skill_invocation(workspace_root: Path) -> None:
    invocation = ExplicitSkillInvocationService()
    gate = SkillExecutionGateService(explicit_skill_invocation_service=invocation)

    result = gate.gate_explicit_invocation(
        skill_id="skill:self_awareness_workspace_inventory",
        input_payload={"root_path": str(workspace_root), "relative_path": "../"},
    )

    assert result.executed is False
    assert result.blocked is True
    assert gate.last_decision is not None
    assert gate.last_decision.decision_basis == "path_traversal"
    assert invocation.last_result is None
