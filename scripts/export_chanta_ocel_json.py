from __future__ import annotations

import json
from pathlib import Path

from chanta_core.ocel.export import OCELExporter
from chanta_core.ocel.store import OCELStore


def main() -> None:
    target = Path("data/exports/chanta_ocel_export.json")
    exporter = OCELExporter(OCELStore())
    path = exporter.export_chanta_json(target)
    payload = json.loads(path.read_text(encoding="utf-8"))
    print(f"export_path={path}")
    print(f"events={len(payload.get('events') or [])}")
    print(f"objects={len(payload.get('objects') or [])}")
    print(f"relations={len(payload.get('relations') or [])}")


if __name__ == "__main__":
    main()
