"""Compute descriptive statistics for non-empty score lists."""


def summary(scores: list[float]) -> dict[str, float]:
    """Return minimum, maximum, mean, and median rounded to two decimals."""
    if not scores:
        raise ValueError("scores must not be empty")

    ordered = sorted(scores)
    count = len(ordered)
    middle = count // 2
    median = ordered[middle]
    if count % 2 == 0:
        median = (ordered[middle - 1] + ordered[middle]) / 2

    return {
        "min": ordered[0],
        "max": ordered[-1],
        "mean": round(sum(scores) / count, 2),
        "median": round(median, 2),
    }
