"""Summarize a collection of numeric grades."""


def summary(scores: list[float]) -> dict[str, float | int]:
    """Return the minimum, maximum, mean, and median of non-empty scores."""
    if not scores:
        raise ValueError("Scores cannot be empty")

    ordered = sorted(scores)
    middle = len(ordered) // 2
    if len(ordered) % 2:
        median = ordered[middle]
    else:
        median = (ordered[middle - 1] + ordered[middle]) / 2

    return {
        "min": ordered[0],
        "max": ordered[-1],
        "mean": round(sum(ordered) / len(ordered), 2),
        "median": round(median, 2),
    }


if __name__ == "__main__":
    print(summary([7.5, 9, 6, 8]))
