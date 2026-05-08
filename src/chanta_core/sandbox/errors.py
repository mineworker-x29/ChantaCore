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


class ShellNetworkRiskError(SandboxError):
    """Base error for shell/network risk pre-sandbox records."""


class ShellCommandIntentError(ShellNetworkRiskError):
    """Raised when a shell command intent is invalid."""


class NetworkAccessIntentError(ShellNetworkRiskError):
    """Raised when a network access intent is invalid."""


class ShellNetworkRiskAssessmentError(ShellNetworkRiskError):
    """Raised when a shell/network risk assessment is invalid."""


class ShellNetworkPreSandboxDecisionError(ShellNetworkRiskError):
    """Raised when a shell/network pre-sandbox decision is invalid."""


class ShellNetworkRiskViolationError(ShellNetworkRiskError):
    """Raised when a shell/network risk violation is invalid."""
