"""Command detail modal marker."""

def command_detail_text(command: str) -> str:
    return f"{command}\nUse /help commands for details."


__all__ = ["command_detail_text"]
