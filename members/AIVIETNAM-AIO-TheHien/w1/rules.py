"""Check thesis-registration requirements."""


def can_register_thesis(credits: int, gpa: float) -> bool:
    """Require at least 120 credits and a GPA of 2.0."""
    return credits >= 120 and gpa >= 2.0


def missing(credits: int, gpa: float) -> list[str]:
    """Describe unmet credit and GPA requirements."""
    reasons: list[str] = []
    if credits < 120:
        reasons.append(f"need {120 - credits} more credits")
    if gpa < 2.0:
        reasons.append("need GPA at least 2.0")
    return reasons
