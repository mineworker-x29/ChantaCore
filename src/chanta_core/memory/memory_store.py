from __future__ import annotations

from chanta_core.memory.memory_record import MemoryRecord


class MemoryStore:
    """In-memory placeholder store; persistence is intentionally not implemented yet."""

    def __init__(self) -> None:
        self._records: list[MemoryRecord] = []

    def add(self, record: MemoryRecord) -> None:
        self._records.append(record)

    def list_records(self) -> list[MemoryRecord]:
        return list(self._records)
