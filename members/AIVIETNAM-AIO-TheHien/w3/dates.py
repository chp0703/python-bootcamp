"""Parse explicit and relative task deadlines."""

import re
from datetime import date, timedelta

WEEKDAYS = (
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
)


def parse_due(text: str, today: date) -> date:
    """Parse an ISO date, relative day, or the strictly next named weekday.

    Weekdays accept full names or three-letter abbreviations, ignoring case.
    Invalid or unrepresentable dates raise ValueError.
    """
    value = text.strip().lower()
    try:
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
            return date.fromisoformat(value)
        if value == "tomorrow":
            return today + timedelta(days=1)
        relative = re.fullmatch(r"in (\d+) days?", value)
        if relative:
            return today + timedelta(days=int(relative.group(1)))
        for index, weekday in enumerate(WEEKDAYS):
            if value in (weekday, weekday[:3]):
                return today + timedelta(days=(index - today.weekday()) % 7 or 7)
    except (ValueError, OverflowError) as error:
        raise ValueError(f"Invalid due date: {text!r}") from error
    raise ValueError(f"Unknown due date: {text!r}")
