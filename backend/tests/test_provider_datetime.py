from datetime import date, datetime, timezone

from app.core.provider_datetime import parse_provider_datetime, truncate_to_seconds


def test_pluggy_zulu_drops_milliseconds_keeps_utc_calendar_day():
    day, occurred = parse_provider_datetime("2026-09-04T13:14:07.693Z")
    assert day == date(2026, 9, 4)
    assert occurred == datetime(2026, 9, 4, 13, 14, 7, tzinfo=timezone.utc)
    assert occurred.microsecond == 0


def test_date_only_has_no_occurred_at():
    day, occurred = parse_provider_datetime("2026-09-04")
    assert day == date(2026, 9, 4)
    assert occurred is None


def test_offset_datetime_converts_to_utc_seconds():
    day, occurred = parse_provider_datetime("2026-09-04T10:14:07-03:00")
    assert day == date(2026, 9, 4)
    assert occurred == datetime(2026, 9, 4, 13, 14, 7, tzinfo=timezone.utc)


def test_space_separated_datetime_has_clock():
    day, occurred = parse_provider_datetime("2026-09-04 13:14:07.693+00:00")
    assert day == date(2026, 9, 4)
    assert occurred == datetime(2026, 9, 4, 13, 14, 7, tzinfo=timezone.utc)

    assert parse_provider_datetime(None) == (None, None)
    assert parse_provider_datetime("") == (None, None)
    assert parse_provider_datetime("not-a-date") == (None, None)


def test_truncate_naive_assumes_utc():
    naive = datetime(2026, 9, 4, 13, 14, 7, 123456)
    assert truncate_to_seconds(naive) == datetime(2026, 9, 4, 13, 14, 7, tzinfo=timezone.utc)
