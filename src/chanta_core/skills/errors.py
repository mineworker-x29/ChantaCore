from __future__ import annotations


class SkillValidationError(ValueError):
    """Raised when a skill descriptor violates the dispatch contract."""


class SkillRegistryError(ValueError):
    """Raised when registry state would become ambiguous or inconsistent."""


class ExplicitSkillInvocationError(ValueError):
    """Raised when explicit skill invocation cannot proceed."""


class SkillProposalError(ValueError):
    """Raised when skill proposal cannot proceed."""


class SkillExecutionGateError(ValueError):
    """Raised when skill execution gate evaluation cannot proceed."""
