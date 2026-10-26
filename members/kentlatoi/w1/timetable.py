def by_day(items: list[tuple[str, str]]) -> dict[str, list[str]]:
    """Group course names by weekday and sort each day's courses."""
    result = {}

    for course, day in items:
        if day not in result:
            result[day] = []

        result[day].append(course)

    for courses in result.values():
        courses.sort()

    return result
