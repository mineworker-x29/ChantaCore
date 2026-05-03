class WorkspaceError(Exception):
    """Base error for workspace inspection failures."""


class WorkspaceAccessError(WorkspaceError):
    """Raised when a workspace path is outside scope or blocked."""


class WorkspaceFileTooLargeError(WorkspaceError):
    """Raised when a file exceeds the configured read limit."""


class WorkspaceUnsupportedFileError(WorkspaceError):
    """Raised when a file cannot be safely read as text."""
