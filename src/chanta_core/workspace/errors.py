class WorkspaceError(Exception):
    """Base error for workspace inspection failures."""


class WorkspaceAccessError(WorkspaceError):
    """Raised when a workspace path is outside scope or blocked."""


class WorkspaceFileTooLargeError(WorkspaceError):
    """Raised when a file exceeds the configured read limit."""


class WorkspaceUnsupportedFileError(WorkspaceError):
    """Raised when a file cannot be safely read as text."""


class WorkspaceReadError(WorkspaceError):
    """Base error for explicit workspace read-only skill failures."""


class WorkspaceReadRootError(WorkspaceReadError):
    """Raised when a workspace read root is invalid."""


class WorkspaceReadBoundaryError(WorkspaceReadError):
    """Raised when a workspace read boundary is invalid."""


class WorkspacePathViolationError(WorkspaceReadError):
    """Raised when a requested path violates workspace read boundaries."""


class WorkspaceTextReadError(WorkspaceReadError):
    """Raised when a text file cannot be read safely."""


class WorkspaceBinaryFileError(WorkspaceTextReadError):
    """Raised when a requested file appears to be binary."""
