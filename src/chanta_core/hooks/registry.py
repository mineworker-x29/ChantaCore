from __future__ import annotations

from dataclasses import replace

from chanta_core.hooks.lifecycle import normalize_lifecycle_stage
from chanta_core.hooks.models import HookDefinition
from chanta_core.utility.time import utc_now_iso


class HookRegistry:
    def __init__(self) -> None:
        self._hooks_by_id: dict[str, HookDefinition] = {}

    def register(self, definition: HookDefinition) -> HookDefinition:
        self._hooks_by_id[definition.hook_id] = definition
        return definition

    def list_hooks(self) -> list[HookDefinition]:
        return self._sort_hooks(self._hooks_by_id.values())

    def get_hook(self, hook_id: str) -> HookDefinition | None:
        return self._hooks_by_id.get(hook_id)

    def find_by_stage(self, lifecycle_stage: str) -> list[HookDefinition]:
        normalized = normalize_lifecycle_stage(lifecycle_stage)
        return self._sort_hooks(
            hook
            for hook in self._hooks_by_id.values()
            if hook.lifecycle_stage == normalized
        )

    def disable_hook(self, hook_id: str) -> HookDefinition | None:
        hook = self._hooks_by_id.get(hook_id)
        if hook is None:
            return None
        disabled = replace(hook, status="disabled", updated_at=utc_now_iso())
        self._hooks_by_id[hook_id] = disabled
        return disabled

    def clear(self) -> None:
        self._hooks_by_id.clear()

    @staticmethod
    def _sort_hooks(hooks) -> list[HookDefinition]:
        return sorted(
            hooks,
            key=lambda hook: (
                1 if hook.priority is None else 0,
                -(hook.priority or 0),
                hook.hook_name,
                hook.hook_id,
            ),
        )
