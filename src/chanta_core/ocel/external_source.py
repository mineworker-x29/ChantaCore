from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ExternalOCELSource:
    source_id: str
    source_name: str
    source_type: str
    source_format: str
    source_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_id": self.source_id,
            "source_name": self.source_name,
            "source_type": self.source_type,
            "source_format": self.source_format,
            "source_attrs": self.source_attrs,
        }
