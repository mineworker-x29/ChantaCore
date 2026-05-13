from pathlib import Path

from chanta_core.digestion import ExternalSkillStaticDigestionService
from chanta_core.ocpx.models import OCPXObjectView, OCPXProcessView
from chanta_core.pig.reports import PIGReportService


def test_static_risk_detects_shell_network_mcp_and_write(tmp_path: Path) -> None:
    skill_dir = tmp_path / "skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_bytes(
        b"""---
name: Risky Static Fixture
description: Uses shell command, http network access, mcp server, plugin, and write patch actions.
permissions: [shell, network, mcp, plugin, write]
---
# Risky Static Fixture
"""
    )

    service = ExternalSkillStaticDigestionService()
    report = service.create_static_digestion_report(root_path=str(tmp_path), relative_path="skill")
    risk = service.last_risk_profile

    assert report.status == "completed_with_findings"
    assert risk is not None
    assert risk.risk_class == "high"
    assert risk.declared_shell is True
    assert risk.declared_network is True
    assert risk.declared_mcp is True
    assert risk.declared_plugin is True
    assert risk.declared_write is True
    assert risk.execution_allowed_by_default is False
    assert {"shell_declared", "network_declared", "write_declared", "mcp_declared"}.issubset(
        {finding.finding_type for finding in service.last_findings}
    )


def test_candidate_and_adapter_hints_remain_non_executable(tmp_path: Path) -> None:
    skill_dir = tmp_path / "skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_bytes(b"# Generic Skill\n\nDescription: read summarize.\n")

    service = ExternalSkillStaticDigestionService()
    service.create_static_digestion_report(root_path=str(tmp_path), relative_path="skill")

    assert service.last_candidate is not None
    assert service.last_candidate.review_status == "pending_review"
    assert service.last_candidate.canonical_import_enabled is False
    assert service.last_candidate.execution_enabled is False
    assert service.last_adapter_hints
    assert service.last_adapter_hints[0].requires_review is True
    assert service.last_adapter_hints[0].execution_enabled is False


def test_pig_ocpx_static_digestion_counts_visible() -> None:
    view = OCPXProcessView(
        view_id="view:static-digest",
        source="test",
        session_id=None,
        events=[],
        objects=[
            OCPXObjectView(
                object_id="inventory:demo",
                object_type="external_skill_resource_inventory",
                object_attrs={"script_files": ["helper.py"]},
            ),
            OCPXObjectView(
                object_id="manifest:demo",
                object_type="external_skill_manifest_profile",
                object_attrs={"manifest_kind": "json"},
            ),
            OCPXObjectView(
                object_id="capability:demo",
                object_type="external_skill_declared_capability",
                object_attrs={"capability_category": "read_only"},
            ),
            OCPXObjectView(
                object_id="risk:demo",
                object_type="external_skill_static_risk_profile",
                object_attrs={"risk_class": "high", "declared_shell": True, "declared_network": True},
            ),
        ],
    )
    summary = PIGReportService._external_skill_static_digestion_summary(
        {
            "external_skill_resource_inventory": 1,
            "external_skill_manifest_profile": 1,
            "external_skill_declared_capability": 1,
            "external_skill_static_risk_profile": 1,
        },
        {},
        view,
    )

    assert summary["external_skill_resource_inventory_count"] == 1
    assert summary["external_skill_static_digest_by_manifest_kind"] == {"json": 1}
    assert summary["external_skill_static_digest_by_capability_category"] == {"read_only": 1}
    assert summary["external_skill_static_digest_by_risk_class"] == {"high": 1}
    assert summary["external_skill_static_digest_script_detected_count"] == 1
    assert summary["external_skill_static_digest_shell_declared_count"] == 1
    assert summary["external_skill_static_digest_network_declared_count"] == 1
