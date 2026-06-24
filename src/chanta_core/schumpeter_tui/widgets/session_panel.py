"""Session panel rendering boundary."""

def session_panel_text(profile_id: str = "default-personal", provider: str = "configured") -> str:
    return f"SESSION\n{profile_id}\nprovider: {provider}"


__all__ = ["session_panel_text"]
