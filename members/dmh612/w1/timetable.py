"""Module for timetable grouping exercises for Week 1."""


def by_day(entries: list[tuple[str, str]]) -> dict[str, list[str]]:
    """Group courses by day and return a dict with sorted lists of courses.
    
    Args:
        entries: A list of (course, day) tuples.
        
    Returns:
        A dictionary mapping each day to a sorted list of courses.
    """
    result = {}
    for course, day in entries:
        result.setdefault(day, []).append(course)
    
    # Sắp xếp danh sách các khóa học của từng ngày theo thứ tự tăng dần
    return {day: sorted(courses) for day, courses in result.items()}


if __name__ == "__main__":
    # Test thử trực tiếp
    sample = [("CSC10014", "Mon"), ("MTH00003", "Tue"), ("CSC10001", "Mon")]
    res = by_day(sample)
    print("Kết quả:", res)
    assert res == {'Mon': ['CSC10001', 'CSC10014'], 'Tue': ['MTH00003']}
    print("Test PASS ngon lành!")