from __future__ import annotations

from chanta_core.missions.mission import Mission


class MissionRuntime:
    """Placeholder mission runtime; orchestration is intentionally deferred."""

    def prepare(self, mission: Mission) -> Mission:
        return mission
