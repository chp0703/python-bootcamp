def can_register_thesis(credits: int, gpa: float) -> bool:
    """Check whether the thesis credit and GPA thresholds are met."""
    return credits >= 120 and gpa >= 2.0


def missing(credits: int, gpa: float) -> list[str]:
    """Explain which thesis registration requirements are missing."""
    reasons = []
    if credits < 120:
        need = 120 - credits
        reasons.append(f"need {need} more credits")

    if gpa < 2.0:
        reasons.append("GPA must be at least 2.0")

    return reasons
