"""PI monitor widget text boundary."""


def pi_monitor_text(provider_status: str = "ready") -> str:
    return f"PI MONITOR\n● PI       available\n● Provider {provider_status}\n● Trace    active\n○ Evidence none\n● Safety   protected"


__all__ = ["pi_monitor_text"]
