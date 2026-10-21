def by_day(items: list[tuple[str, str]]) -> dict[str, list[str]]:
    result = {}

    for course, day in items:
        if day not in result:
            result[day] = []

        result[day].append(course)

    for day in result:
        result[day].sort()

    return result