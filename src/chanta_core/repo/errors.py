class RepoError(Exception):
    """Base error for read-only repository inspection failures."""


class RepoSearchError(RepoError):
    """Raised when repository text search cannot be completed."""


class RepoScanError(RepoError):
    """Raised when repository file scanning cannot be completed."""


class RepoSymbolScanError(RepoError):
    """Raised when lightweight symbol scanning cannot be completed."""
