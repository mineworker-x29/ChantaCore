from chanta_core.utility.time import utc_now_iso


def test_utc_now_iso_returns_z_suffixed_utc_string() -> None:
    value = utc_now_iso()

    assert isinstance(value, str)
    assert value.endswith("Z")
    assert "T" in value
    assert "+00:00" not in value


def test_utc_now_iso_multiple_calls_return_strings() -> None:
    first = utc_now_iso()
    second = utc_now_iso()

    assert isinstance(first, str)
    assert isinstance(second, str)
