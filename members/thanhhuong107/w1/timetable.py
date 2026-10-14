"""Group and sort courses by weekday."""


def by_day(schedule: list[tuple[str, str]]) -> dict[str, list[str]]:
    """Return courses grouped by day, with each day's courses sorted."""
    result: dict[str, list[str]] = {}
    for course, day in schedule:
        result.setdefault(day, []).append(course)

    for courses in result.values():
        courses.sort()
    return result


if __name__ == "__main__":
    example = [("CSC10014", "Mon"), ("MTH00003", "Tue"), ("CSC10001", "Mon")]
    print(by_day(example))
