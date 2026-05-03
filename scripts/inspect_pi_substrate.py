from __future__ import annotations

from chanta_core.pig.inspector import PISubstrateInspector


def build_inspection(limit: int = 50):
    return PISubstrateInspector().inspect(limit=limit)


def main() -> None:
    inspection = build_inspection()
    print(inspection.inspection_text)
    print("warnings:", inspection.warnings)


if __name__ == "__main__":
    main()
