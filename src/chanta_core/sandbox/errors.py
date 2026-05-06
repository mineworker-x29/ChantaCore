class SandboxError(Exception):
    """Base error for sandbox records."""


class WorkspaceWriteSandboxError(SandboxError):
    """Base error for workspace write sandbox records."""


class WorkspaceRootError(WorkspaceWriteSandboxError):
    """Raised when a workspace root is invalid."""


class WorkspaceWriteBoundaryError(WorkspaceWriteSandboxError):
    """Raised when a workspace write boundary is invalid."""


class WorkspaceWriteIntentError(WorkspaceWriteSandboxError):
    """Raised when a workspace write intent is invalid."""


class WorkspaceWriteSandboxDecisionError(WorkspaceWriteSandboxError):
    """Raised when a workspace write sandbox decision is invalid."""


class WorkspaceWriteSandboxViolationError(WorkspaceWriteSandboxError):
    """Raised when a workspace write sandbox violation is invalid."""
