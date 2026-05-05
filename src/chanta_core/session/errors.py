class SessionError(Exception):
    """Base error for session substrate failures."""


class SessionNotFoundError(SessionError):
    """Raised when a requested session cannot be found."""


class ConversationTurnError(SessionError):
    """Raised when a conversation turn cannot be recorded."""


class SessionMessageError(SessionError):
    """Raised when a session message cannot be recorded."""
