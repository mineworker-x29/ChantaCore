class MaterializedViewError(Exception):
    """Base error for generated materialized view failures."""


class MaterializedViewRenderError(MaterializedViewError):
    """Raised when a materialized view cannot be rendered."""


class MaterializedViewWriteError(MaterializedViewError):
    """Raised when a materialized view cannot be written."""
