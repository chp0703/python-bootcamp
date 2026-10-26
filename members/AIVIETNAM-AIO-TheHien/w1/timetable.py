"""Group course names by day."""


def by_day(pairs: list[tuple[str, str]]) -> dict[str, list[str]]:
    """Return alphabetically sorted courses for each observed day."""
    grouped: dict[str, list[str]] = {}
    for course, day in pairs:
        grouped.setdefault(day, []).append(course)
    return {day: sorted(courses) for day, courses in grouped.items()}
