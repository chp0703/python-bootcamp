"""Module for thesis eligibility rules."""


def can_register_thesis(credits: int, gpa: float) -> bool:
    """Check if a student can register for thesis (credits >= 120 and gpa >= 2.0)."""
    return credits >= 120 and gpa >= 2.0


def missing(credits: int, gpa: float) -> list[str]:
    """Return human-readable reasons if conditions are not met."""
    reasons = []
    if credits < 120:
        reasons.append(f"need {120 - credits} more credits")
    if gpa < 2.0:
        reasons.append(f"need {round(2.0 - gpa, 2)} higher GPA")
    return reasons


if __name__ == "__main__":
    assert can_register_thesis(120, 2.0)
    assert not can_register_thesis(118, 3.1)
    assert missing(118, 3.1) == ["need 2 more credits"]
    assert missing(120, 2.0) == []
    assert len(missing(100, 1.5)) == 2
    print("rules.py: PASS")