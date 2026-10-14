def by_day(entries: list[tuple[str, str]]) -> dict[str, list[str]]:
    grouped: dict[str, list[str]] = {}
    for course, day in entries:
        grouped.setdefault(day, []).append(course)
    
    for day in grouped:
        grouped[day].sort()
        
    return grouped