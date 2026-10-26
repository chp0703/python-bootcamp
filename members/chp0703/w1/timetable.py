def by_day(courses: list[tuple[str, str]]) -> dict[str, list[str]]:
    """Group course codes by day and sort each day's course codes."""

    timetable = {}
    for course, day in courses:
        timetable.setdefault(day, []).append(course)

    return {day: sorted(day_courses) for day, day_courses in timetable.items()}

