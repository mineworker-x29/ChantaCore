class EditingError(Exception):
    """Base error for edit proposal failures."""


class EditProposalError(EditingError):
    """Raised when an edit proposal cannot be created or loaded."""


class EditProposalValidationError(EditProposalError):
    """Raised when an edit proposal is invalid."""
