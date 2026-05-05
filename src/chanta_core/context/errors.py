class ContextError(Exception):
    """Base error for context budget and compaction failures."""


class ContextBudgetError(ContextError):
    """Raised when a context budget is invalid."""


class ContextBudgetExceededWarning(ContextError):
    """Warning marker for context that cannot be compacted below budget."""


class ContextBlockValidationError(ContextError):
    """Raised when a context block cannot be constructed safely."""


class ContextCompactionError(ContextError):
    """Raised when context compaction fails."""
