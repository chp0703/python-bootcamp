def by_day(courses: list[tuple[str, str]]) -> dict[str, list[str]]:

    timetable = {}
    for course, day in courses:
        timetable.setdefault(day, []).append(course)

    return {day: sorted(day_courses) for day, day_courses in timetable.items()}

