from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class RepoFileMatch:
    relative_path: str
    size_bytes: int | None
    match_reason: str
    attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "relative_path": self.relative_path,
            "size_bytes": self.size_bytes,
            "match_reason": self.match_reason,
            "attrs": self.attrs,
        }


@dataclass(frozen=True)
class RepoTextMatch:
    relative_path: str
    line_number: int
    line_text: str
    match_text: str
    attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "relative_path": self.relative_path,
            "line_number": self.line_number,
            "line_text": self.line_text,
            "match_text": self.match_text,
            "attrs": self.attrs,
        }


@dataclass(frozen=True)
class RepoSymbol:
    symbol_name: str
    symbol_kind: str
    relative_path: str
    line_number: int
    signature: str | None = None
    attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "symbol_name": self.symbol_name,
            "symbol_kind": self.symbol_kind,
            "relative_path": self.relative_path,
            "line_number": self.line_number,
            "signature": self.signature,
            "attrs": self.attrs,
        }


@dataclass(frozen=True)
class RepoSearchResult:
    query: str
    matches: list[RepoTextMatch] = field(default_factory=list)
    file_matches: list[RepoFileMatch] = field(default_factory=list)
    symbols: list[RepoSymbol] = field(default_factory=list)
    result_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "query": self.query,
            "matches": [item.to_dict() for item in self.matches],
            "file_matches": [item.to_dict() for item in self.file_matches],
            "symbols": [item.to_dict() for item in self.symbols],
            "result_attrs": self.result_attrs,
        }
