from __future__ import annotations


class PersonaError(Exception):
    """Base error for persona loading records."""


class SoulIdentityError(PersonaError):
    """Raised when a soul identity record is invalid."""


class PersonaProfileError(PersonaError):
    """Raised when a persona profile record is invalid."""


class PersonaInstructionArtifactError(PersonaError):
    """Raised when a persona instruction artifact is invalid."""


class AgentRoleBindingError(PersonaError):
    """Raised when an agent role binding is invalid."""


class PersonaLoadoutError(PersonaError):
    """Raised when a persona loadout cannot be built."""


class PersonaProjectionError(PersonaError):
    """Raised when a persona projection cannot be rendered."""
