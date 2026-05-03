from __future__ import annotations

import re
from pathlib import Path

from chanta_core.repo.models import RepoSymbol
from chanta_core.repo.scanner import RepoScanner
from chanta_core.workspace import WorkspaceInspector
from chanta_core.workspace.errors import WorkspaceError


PYTHON_PATTERNS = [
    ("class", re.compile(r"^\s*class\s+([A-Za-z_][A-Za-z0-9_]*)\b.*")),
    ("function", re.compile(r"^\s*(?:async\s+)?def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(.*")),
]
JS_TS_PATTERNS = [
    ("function", re.compile(r"^\s*(?:export\s+)?function\s+([A-Za-z_$][A-Za-z0-9_$]*)\s*\(.*")),
    ("class", re.compile(r"^\s*(?:export\s+)?class\s+([A-Za-z_$][A-Za-z0-9_$]*)\b.*")),
    ("variable", re.compile(r"^\s*(?:export\s+)?(?:const|let)\s+([A-Za-z_$][A-Za-z0-9_$]*)\s*=.*")),
]
MARKDOWN_HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


class RepoSymbolScanner:
    def __init__(
        self,
        workspace_inspector: WorkspaceInspector,
        scanner: RepoScanner | None = None,
    ) -> None:
        self.workspace_inspector = workspace_inspector
        self.scanner = scanner or RepoScanner(workspace_inspector)

    def scan_symbols(self, path: str = ".", limit: int = 200) -> list[RepoSymbol]:
        files = self.scanner.candidate_code_files(limit=limit)
        symbols: list[RepoSymbol] = []
        for file_match in files:
            if path != "." and not file_match.relative_path.startswith(path.rstrip("/") + "/"):
                continue
            try:
                text_result = self.workspace_inspector.read_text_file(
                    file_match.relative_path
                )
            except WorkspaceError:
                continue
            suffix = Path(file_match.relative_path).suffix.lower()
            symbols.extend(
                self._scan_file(
                    relative_path=file_match.relative_path,
                    suffix=suffix,
                    text=str(text_result["text"]),
                    remaining=limit - len(symbols),
                )
            )
            if len(symbols) >= limit:
                break
        return symbols[:limit]

    def find_definitions_light(
        self,
        name: str,
        path: str = ".",
        limit: int = 100,
    ) -> list[RepoSymbol]:
        name_lower = name.lower()
        matches: list[RepoSymbol] = []
        for symbol in self.scan_symbols(path=path, limit=max(limit * 4, limit)):
            if symbol.symbol_name.lower() == name_lower:
                matches.append(symbol)
            elif name_lower in symbol.symbol_name.lower():
                matches.append(
                    RepoSymbol(
                        symbol_name=symbol.symbol_name,
                        symbol_kind=symbol.symbol_kind,
                        relative_path=symbol.relative_path,
                        line_number=symbol.line_number,
                        signature=symbol.signature,
                        attrs={**symbol.attrs, "confidence": "low"},
                    )
                )
            if len(matches) >= limit:
                break
        return matches

    def _scan_file(
        self,
        *,
        relative_path: str,
        suffix: str,
        text: str,
        remaining: int,
    ) -> list[RepoSymbol]:
        if remaining <= 0:
            return []
        patterns = []
        if suffix == ".py":
            patterns = PYTHON_PATTERNS
        elif suffix in {".js", ".jsx", ".ts", ".tsx"}:
            patterns = JS_TS_PATTERNS
        symbols: list[RepoSymbol] = []
        for line_number, line in enumerate(text.splitlines(), start=1):
            if suffix == ".md":
                markdown_match = MARKDOWN_HEADING.match(line)
                if markdown_match:
                    symbols.append(
                        RepoSymbol(
                            symbol_name=markdown_match.group(2).strip(),
                            symbol_kind="section",
                            relative_path=relative_path,
                            line_number=line_number,
                            signature=line.strip(),
                            attrs={
                                "parser": "lightweight_regex",
                                "confidence": "medium",
                                "heading_level": len(markdown_match.group(1)),
                            },
                        )
                    )
            else:
                for kind, pattern in patterns:
                    match = pattern.match(line)
                    if not match:
                        continue
                    symbols.append(
                        RepoSymbol(
                            symbol_name=match.group(1),
                            symbol_kind=kind,
                            relative_path=relative_path,
                            line_number=line_number,
                            signature=line.strip(),
                            attrs={
                                "parser": "lightweight_regex",
                                "confidence": "medium",
                            },
                        )
                    )
                    break
            if len(symbols) >= remaining:
                break
        return symbols
