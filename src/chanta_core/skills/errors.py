from __future__ import annotations


class SkillValidationError(ValueError):
    """Raised when a skill descriptor violates the dispatch contract."""


class SkillRegistryError(ValueError):
    """Raised when registry state would become ambiguous or inconsistent."""
