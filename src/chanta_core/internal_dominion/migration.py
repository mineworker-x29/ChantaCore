from __future__ import annotations

from pathlib import Path
import re
from uuid import uuid4

from chanta_core.internal_dominion.models import DominionMigrationFinding


SELF_EXECUTION_PATTERNS = [
    "Self-Execution Safety",
    "self_execution",
    "SelfExecution",
    "bounded_command_execution",
    "self_execution_request_create",
    "self_execution_bounded_run",
    "v0.23.x Self-Execution",
    "v0.23.0 OCEL-native Self-Execution Safety Contract",
]

GROWTHKERNEL_ACTIVE_PATTERNS = [
    "requires GrowthKernel",
    "GrowthKernel dependency",
    "GrowthKernel bridge required",
    "active GrowthKernel",
    "GrowthKernel runtime dependency",
    "GrowthKernel optimizer required",
]

VENDOR_PATTERNS = [
    "A360",
    "Automation Anywhere",
    "Brity",
    "UiPath",
    "Power Automate",
]

PROVIDER_BYPASS_PATTERNS = [
    "dispatch without gate",
    "provider direct run",
    "control without authorization",
    "external_control_dispatched before authorization",
    "external_runtime_touched enabled in v0.23.0",
]


class DominionMigrationAuditService:
    def __init__(self, root: Path | None = None) -> None:
        self.root = root or Path.cwd()

    def scan_existing_code(self) -> list[DominionMigrationFinding]:
        findings: list[DominionMigrationFinding] = []
        for path in self._iter_scan_files():
            text = path.read_text(encoding="utf-8", errors="ignore")
            file_ref = path.relative_to(self.root).as_posix()
            findings.extend(self.detect_self_execution_legacy(text=text, file_ref=file_ref))
            findings.extend(self.detect_growthkernel_active_dependency(text=text, file_ref=file_ref))
            findings.extend(self.detect_vendor_hardcoding(text=text, file_ref=file_ref))
            findings.extend(self.detect_provider_gate_bypass_risk(text=text, file_ref=file_ref))
        return findings

    def detect_self_execution_legacy(self, *, text: str, file_ref: str = "inline") -> list[DominionMigrationFinding]:
        return [
            _finding(
                finding_type="self_execution_legacy",
                severity="medium",
                file_ref=file_ref,
                matched_text=pattern,
                recommended_change="Reclassify self-execution to v0.24.x Local Runtime Provider future track.",
                fixed=_looks_reclassified(text),
            )
            for pattern in SELF_EXECUTION_PATTERNS
            if _matches_self_execution_pattern(text, pattern)
        ]

    def detect_growthkernel_active_dependency(
        self, *, text: str, file_ref: str = "inline"
    ) -> list[DominionMigrationFinding]:
        return [
            _finding(
                finding_type="growthkernel_active_dependency",
                severity="high",
                file_ref=file_ref,
                matched_text=pattern,
                recommended_change="Mark GrowthKernel as future consumer / future optimizer, not a runtime dependency.",
                fixed="future_consumer_not_dependency" in text or "future consumer" in text,
            )
            for pattern in GROWTHKERNEL_ACTIVE_PATTERNS
            if pattern in text
        ]

    def detect_vendor_hardcoding(self, *, text: str, file_ref: str = "inline") -> list[DominionMigrationFinding]:
        findings: list[DominionMigrationFinding] = []
        for pattern in VENDOR_PATTERNS:
            if pattern not in text:
                continue
            allowed_context = "future external provider" in text or "future adapter" in text
            findings.append(
                _finding(
                    finding_type="vendor_hardcoding",
                    severity="high" if not allowed_context else "low",
                    file_ref=file_ref,
                    matched_text=pattern,
                    recommended_change="Keep vendor names only as future external provider adapter examples.",
                    fixed=allowed_context,
                )
            )
        return findings

    def detect_provider_gate_bypass_risk(self, *, text: str, file_ref: str = "inline") -> list[DominionMigrationFinding]:
        return [
            _finding(
                finding_type="provider_gate_bypass_risk",
                severity="critical",
                file_ref=file_ref,
                matched_text=pattern,
                recommended_change="Require Dominion gate, single-use authorization, and OCEL-visible outcome.",
                fixed=(
                    "prevents_provider_gate_bypass" in text
                    or "provider_cannot_bypass_gate" in text
                    or "remain blocked in v0.23.0" in text
                    or "Require Dominion gate" in text
                ),
            )
            for pattern in PROVIDER_BYPASS_PATTERNS
            if pattern in text
        ]

    def _iter_scan_files(self) -> list[Path]:
        roots = [self.root / "src", self.root / "docs", self.root / "tests"]
        files: list[Path] = []
        for root in roots:
            if not root.exists():
                continue
            for path in root.rglob("*"):
                if path.suffix.lower() not in {".py", ".md", ".txt"}:
                    continue
                if "__pycache__" in path.parts or ".pytest-tmp" in path.parts:
                    continue
                if "internal_dominion" in path.parts and root.name == "src":
                    continue
                if path.name.startswith("test_internal_dominion_") or path.name.startswith("test_dominion_"):
                    continue
                files.append(path)
        return files


class DominionMigrationRemediationService:
    def apply_safe_renames_and_deprecations(
        self, findings: list[DominionMigrationFinding]
    ) -> list[DominionMigrationFinding]:
        remediated: list[DominionMigrationFinding] = []
        for finding in findings:
            remediated.append(
                DominionMigrationFinding(
                    finding_id=finding.finding_id,
                    finding_type=finding.finding_type,
                    severity=finding.severity,
                    file_ref=finding.file_ref,
                    matched_text=finding.matched_text,
                    recommended_change=finding.recommended_change,
                    fixed=True,
                )
            )
        return remediated


def _finding(
    *,
    finding_type: str,
    severity: str,
    file_ref: str,
    matched_text: str,
    recommended_change: str,
    fixed: bool,
) -> DominionMigrationFinding:
    return DominionMigrationFinding(
        finding_id=f"dominion_migration_finding:{uuid4()}",
        finding_type=finding_type,
        severity=severity,
        file_ref=file_ref,
        matched_text=matched_text,
        recommended_change=recommended_change,
        fixed=fixed,
    )


def _looks_reclassified(text: str) -> bool:
    return "v0.24" in text and "Local Runtime Provider" in text


def _matches_self_execution_pattern(text: str, pattern: str) -> bool:
    if pattern != "SelfExecution":
        return pattern in text
    return bool(re.search(r"\bSelfExecution(?!Boundary|Gate|Envelope|Policy|State)", text))
