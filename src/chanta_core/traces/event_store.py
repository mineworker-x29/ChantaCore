from __future__ import annotations

import json
from pathlib import Path

from chanta_core.traces.event import AgentEvent


class AgentEventStore:
    def __init__(self, path: str | Path = "data/traces/agent_events.jsonl") -> None:
        self.path = Path(path)

    def append(self, event: AgentEvent) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as event_file:
            json.dump(event.to_dict(), event_file, ensure_ascii=False)
            event_file.write("\n")
