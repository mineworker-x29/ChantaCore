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


class SessionContextError(SessionError):
    """Base error for bounded session context projection failures."""


class SessionContextPolicyError(SessionContextError):
    """Raised when a session context policy is invalid."""


class SessionContextProjectionError(SessionContextError):
    """Raised when a session context projection cannot be assembled."""


class SessionPromptRenderError(SessionContextError):
    """Raised when a session prompt render cannot be produced."""
