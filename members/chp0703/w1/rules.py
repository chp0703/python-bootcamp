def can_register_thesis(credits: int, gpa: float) -> bool:
    """Return whether the student meets both thesis-registration thresholds."""
    return credits >= 120 and gpa >= 2.0


def missing(credits: int, gpa: float) -> list[str]:
    """List unmet thesis-registration requirements."""
    reason = []
    if credits < 120:
        reason.append(f"need {120 - credits} more credits")
    if gpa < 2.0:
        reason.append(f"need GPA >= 2.0 (current: {gpa:.2f})")
    return reason
