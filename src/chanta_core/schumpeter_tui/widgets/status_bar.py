"""Status bar text helper."""

STATUS_REGION_ID = "status-region"
STATUS_BAR_ID = "status-bar"


def status_bar_text() -> str:
    return "PI   Provider   Trace   Evidence   Safety       default-personal       v0.43.11"


__all__ = ["STATUS_REGION_ID", "STATUS_BAR_ID", "status_bar_text"]
