class InstructionError(Exception):
    """Base error for OCEL-native instruction substrate failures."""


class InstructionArtifactError(InstructionError):
    """Raised when an instruction artifact cannot be recorded."""


class ProjectRuleError(InstructionError):
    """Raised when a project rule cannot be recorded."""


class UserPreferenceError(InstructionError):
    """Raised when a user preference cannot be recorded."""
