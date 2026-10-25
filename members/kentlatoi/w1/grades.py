def summary(scores: list[float]) -> dict[str, float]:
    """Return basic grade statistics rounded to two decimal places."""
    if not scores:
        raise ValueError("scores must not be empty")

    sorted_scores = sorted(scores)
    n = len(sorted_scores)
    mean = sum(sorted_scores) / n

    if n % 2 == 1:
        median = sorted_scores[n // 2]
    else:
        middle = n // 2
        median = (sorted_scores[middle - 1] + sorted_scores[middle]) / 2

    return {
        "min": min(scores),
        "max": max(scores),
        "mean": round(mean, 2),
        "median": round(median, 2),
    }
