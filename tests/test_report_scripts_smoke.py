from scripts import (
    inspect_pi_substrate,
    report_process_instance,
    report_recent_pi,
    report_session_pi,
)


def test_report_script_modules_expose_main() -> None:
    assert callable(inspect_pi_substrate.main)
    assert callable(report_recent_pi.main)
    assert callable(report_process_instance.main)
    assert callable(report_session_pi.main)
