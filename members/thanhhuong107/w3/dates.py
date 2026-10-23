"""Parse natural-language due dates relative to a supplied date."""

import re
from datetime import date, timedelta

_WEEKDAYS = {
    "mon": 0,
    "monday": 0,
    "tue": 1,
    "tues": 1,
    "tuesday": 1,
    "wed": 2,
    "wednesday": 2,
    "thu": 3,
    "thur": 3,
    "thurs": 3,
    "thursday": 3,
    "fri": 4,
    "friday": 4,
    "sat": 5,
    "saturday": 5,
    "sun": 6,
    "sunday": 6,
}


def parse_due(text: str, today: date) -> date:
    """Parse an ISO date, relative day expression, or next weekday occurrence."""
    normalized = text.strip().casefold()
    if normalized == "tomorrow":
        return today + timedelta(days=1)

    relative = re.fullmatch(r"in\s+(\d+)\s+days?", normalized)
    if relative:
        return today + timedelta(days=int(relative.group(1)))

    weekday = _WEEKDAYS.get(normalized)
    if weekday is not None:
        days_ahead = (weekday - today.weekday()) % 7 or 7
        return today + timedelta(days=days_ahead)

    try:
        return date.fromisoformat(normalized)
    except ValueError as exc:
        raise ValueError(f"unknown due date: {text!r}") from exc
