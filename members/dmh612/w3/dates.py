"""Parse explicit dates and simple English deadline expressions."""

import re
from datetime import date, timedelta

WEEKDAYS = ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")


def parse_due(text: str, today: date) -> date:
    """Parse ISO dates, tomorrow, in N days, or the next named weekday.

    Weekday names are case-insensitive, abbreviated or full. A matching
    weekday means next week, never today. Unknown expressions raise ValueError.
    """
    value = text.strip().lower()
    try:
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
            return date.fromisoformat(value)
        if value == "tomorrow":
            return today + timedelta(days=1)
        match = re.fullmatch(r"in (\d+) days?", value)
        if match:
            return today + timedelta(days=int(match.group(1)))
        for index, weekday in enumerate(WEEKDAYS):
            if value in (weekday, weekday[:3]):
                offset = (index - today.weekday()) % 7 or 7
                return today + timedelta(days=offset)
    except (ValueError, OverflowError) as error:
        raise ValueError(f"Invalid due date: {text!r}") from error
    raise ValueError(f"Unknown due date: {text!r}")
