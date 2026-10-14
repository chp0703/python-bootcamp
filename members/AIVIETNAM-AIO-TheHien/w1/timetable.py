def by_day(pairs: list[tuple[str, str]]) -> dict[str, list[str]]:
    grouped = {}
    for course, day in pairs:
        grouped.setdefault(day, []).append(course)
    return {day: sorted(courses) for day, courses in grouped.items()}
