"""Module for grade summary calculations."""
import statistics


def summary(scores: list[float]) -> dict:
    """Calculate min, max, mean, and median of scores.
    
    Raises:
        ValueError: If the scores list is empty.
    """
    if not scores:
        raise ValueError("Scores list cannot be empty")

    return {
        "min": min(scores),
        "max": max(scores),
        "mean": round(statistics.mean(scores), 2),
        "median": round(statistics.median(scores), 2),
    }


if __name__ == "__main__":
    assert summary([7.5, 9, 6, 8]) == {"min": 6, "max": 9, "mean": 7.62, "median": 7.75}
    assert summary([5])["median"] == 5
    print("grades.py: PASS")