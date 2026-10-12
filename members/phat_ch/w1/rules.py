def can_register_thesis(credits: int, gpa: float) -> bool:
    return credits >= 120 and gpa >= 2.0


def missing(credits,gpa) -> list[str]:
    reason = []
    if credits < 120:
        reason.append(f"need {120 - credits} more credit(s)")
    if gpa < 2.0:
        reason.append(f"need GPA >= 2.0 (current: {gpa:.2f})")
    return reason
