class SessionError(Exception):
    """Base error for session substrate failures."""


class SessionNotFoundError(SessionError):
    """Raised when a requested session cannot be found."""


class ConversationTurnError(SessionError):
    """Raised when a conversation turn cannot be recorded."""


class SessionMessageError(SessionError):
    """Raised when a session message cannot be recorded."""


class SessionContinuityError(SessionError):
    """Base error for session resume/fork failures."""


class SessionResumeError(SessionContinuityError):
    """Raised when a session resume operation cannot be recorded."""


class SessionForkError(SessionContinuityError):
    """Raised when a session fork operation cannot be recorded."""


class SessionContextReconstructionError(SessionContinuityError):
    """Raised when session context reconstruction fails."""
