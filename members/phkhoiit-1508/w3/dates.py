"""Parse common study-task due-date expressions."""

import re
from datetime import date, timedelta

_WEEKDAYS = ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")


def parse_due(text: str, today: date) -> date:
    """Return the date described by an ISO date, relative expression, or weekday."""
    value = text.strip().lower()
    try:
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
            return date.fromisoformat(value)
        if value == "tomorrow":
            return today + timedelta(days=1)
        match = re.fullmatch(r"in (\d+) days?", value)
        if match:
            return today + timedelta(days=int(match.group(1)))
        for index, weekday in enumerate(_WEEKDAYS):
            if value in (weekday, weekday[:3]):
                offset = (index - today.weekday()) % 7 or 7
                return today + timedelta(days=offset)
    except (ValueError, OverflowError) as error:
        raise ValueError(f"Invalid due date: {text!r}") from error
    raise ValueError(f"Unknown due date: {text!r}")
