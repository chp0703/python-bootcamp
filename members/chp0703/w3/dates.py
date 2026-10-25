from datetime import date, timedelta


def parse_due(text: str, today: date) -> date:
    """Parse a supported due-date expression relative to ``today``.

    Supported expressions are ISO dates, ``tomorrow``, ``in N days``, and
    three-letter weekday names. A weekday always means its next occurrence.
    """
    text = text.strip().lower()

    if text == "tomorrow":
        return today + timedelta(days=1)

    parts = text.split()

    if len(parts) == 3 and parts[0] == "in" and parts[2] == "days":
        days = int(parts[1])
        return today + timedelta(days=days)

    weekdays = {
        "mon": 0,
        "tue": 1,
        "wed": 2,
        "thu": 3,
        "fri": 4,
        "sat": 5,
        "sun": 6,
    }
    if text in weekdays:
        days_until = (weekdays[text] - today.weekday()) % 7
        return today + timedelta(days=days_until or 7)

    try:
        return date.fromisoformat(text)
    except ValueError as error:
        raise ValueError("Invalid date format") from error
