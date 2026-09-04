"""Parse bank/Open Finance datetimes down to seconds (no milliseconds).

Providers send ISO-8601 instants, Unix epochs, or a calendar day with no clock.
The ledger keeps `date` as that calendar day (bill cycles, grouping) and stores
the instant separately when the source actually has a time.
"""
from __future__ import annotations

from datetime import date, datetime, timezone
from typing import Optional


def truncate_to_seconds(value: datetime) -> datetime:
    """UTC instant with the sub-second part dropped."""
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc).replace(microsecond=0)


def parse_provider_datetime(value: object) -> tuple[Optional[date], Optional[datetime]]:
    """Return (calendar_day, occurred_at).

    Calendar day follows the ISO date prefix (`YYYY-MM-DD…`) so it matches what
    Securo already stored from Pluggy via `value[:10]`. `occurred_at` is set
    only when the string includes a clock time, truncated to seconds.
    """
    if value is None:
        return None, None
    raw = str(value).strip()
    if not raw:
        return None, None

    calendar: Optional[date] = None
    if len(raw) >= 10 and raw[4] == "-" and raw[7] == "-":
        try:
            calendar = date.fromisoformat(raw[:10])
        except ValueError:
            calendar = None

    has_clock = "T" in raw or (len(raw) > 10 and " " in raw[10:])
    if not has_clock:
        return calendar, None

    iso = raw.replace("Z", "+00:00")
    try:
        occurred = truncate_to_seconds(datetime.fromisoformat(iso))
    except ValueError:
        return calendar, None
    if calendar is None:
        calendar = occurred.date()
    return calendar, occurred
