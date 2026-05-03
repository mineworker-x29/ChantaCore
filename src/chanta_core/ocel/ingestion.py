from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from chanta_core.ocel.external_source import ExternalOCELSource


@dataclass(frozen=True)
class OCELIngestionBatch:
    batch_id: str
    source: ExternalOCELSource
    imported_at: str
    records_seen: int
    records_accepted: int
    records_rejected: int
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    batch_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "batch_id": self.batch_id,
            "source": self.source.to_dict(),
            "imported_at": self.imported_at,
            "records_seen": self.records_seen,
            "records_accepted": self.records_accepted,
            "records_rejected": self.records_rejected,
            "warnings": self.warnings,
            "errors": self.errors,
            "batch_attrs": self.batch_attrs,
        }


@dataclass(frozen=True)
class OCELIngestionResult:
    success: bool
    batch: OCELIngestionBatch
    accepted_record_ids: list[str]
    rejected_records: list[dict[str, Any]]
    result_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "success": self.success,
            "batch": self.batch.to_dict(),
            "accepted_record_ids": self.accepted_record_ids,
            "rejected_records": self.rejected_records,
            "result_attrs": self.result_attrs,
        }
