from __future__ import annotations

from chanta_core.repo import RepoSymbolScanner
from chanta_core.workspace import WorkspaceInspector


def main() -> None:
    scanner = RepoSymbolScanner(WorkspaceInspector())
    symbols = scanner.scan_symbols(limit=20)
    print(f"Symbols: {len(symbols)}")
    for item in symbols[:10]:
        print(
            f"- {item.symbol_kind} {item.symbol_name} "
            f"{item.relative_path}:{item.line_number}"
        )


if __name__ == "__main__":
    main()
