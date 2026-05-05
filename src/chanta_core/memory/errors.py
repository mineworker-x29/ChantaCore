class MemoryError(Exception):
    """Base error for OCEL-native memory substrate failures."""


class MemoryEntryError(MemoryError):
    """Raised when a memory entry cannot be created or changed."""


class MemoryRevisionError(MemoryError):
    """Raised when a memory revision cannot be recorded."""


class MemoryEntryNotFoundError(MemoryError):
    """Raised when a requested memory entry cannot be found."""
