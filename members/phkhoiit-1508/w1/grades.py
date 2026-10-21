import statistics

def summary(scores: list[float]) -> dict:
    if not scores:
        raise ValueError("Scores list cannot be empty.")
    
    return {
        "min": min(scores),
        "max": max(scores),
        "mean": round(sum(scores) / len(scores), 2),
        "median": round(statistics.median(scores), 2),
    }