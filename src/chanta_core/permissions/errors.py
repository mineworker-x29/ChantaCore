class PermissionModelError(Exception):
    """Base error for permission model records."""


class PermissionScopeError(PermissionModelError):
    """Raised when a permission scope is invalid."""


class PermissionRequestError(PermissionModelError):
    """Raised when a permission request is invalid."""


class PermissionDecisionError(PermissionModelError):
    """Raised when a permission decision is invalid."""


class PermissionGrantError(PermissionModelError):
    """Raised when a permission grant is invalid."""


class PermissionDenialError(PermissionModelError):
    """Raised when a permission denial is invalid."""


class PermissionPolicyNoteError(PermissionModelError):
    """Raised when a permission policy note is invalid."""


class SessionPermissionError(PermissionModelError):
    """Base error for session permission read-model records."""


class SessionPermissionContextError(SessionPermissionError):
    """Raised when a session permission context is invalid."""


class SessionPermissionSnapshotError(SessionPermissionError):
    """Raised when a session permission snapshot is invalid."""


class SessionPermissionResolutionError(SessionPermissionError):
    """Raised when a session permission resolution is invalid."""
