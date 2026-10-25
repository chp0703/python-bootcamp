def summary(scores: list[float]) -> dict[str, float]:
    """Return rounded minimum, maximum, mean, and median for non-empty scores."""
    if not (scores):
        raise ValueError ("Score must not be empty")

    ordered = sorted(scores)
    count = len(ordered)
    mid = count // 2

    if count %2 ==1:
        median = ordered[mid]
    else:
        median = (ordered[mid-1] + ordered[mid]) /2

    return{
    "min": ordered[0],
    "max": ordered[-1],
    "mean": round(sum(scores) / count, 2),
    "median": round(median, 2),
}
