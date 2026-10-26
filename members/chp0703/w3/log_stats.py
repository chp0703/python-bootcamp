from math import ceil
from typing import TypedDict


class LogStats(TypedDict):
    """Summary statistics grouped by request route."""

    counts: dict[str, int]
    p95: dict[str, float]
    slowest: str | None


def analyse(pairs: list[tuple[str, float]]) -> LogStats:
    """Return per-route counts, nearest-rank p95 values, and slowest route."""
    counts: dict[str, int] = {}
    latencies: dict[str, list[float]] = {}

    for route, latency in pairs:
        if route not in counts:
            counts[route] = 0
            latencies[route] = []

        counts[route] += 1
        latencies[route].append(latency)

    p95: dict[str, float] = {}

    for route, values in latencies.items():
        values.sort()

        index = ceil(0.95 * len(values)) - 1
        p95[route] = values[index]

    slowest = None
    highest_p95 = None

    for route, value in p95.items():
        if highest_p95 is None or value > highest_p95:
            highest_p95 = value
            slowest = route

    return {
        "counts": counts,
        "p95": p95,
        "slowest": slowest,
    }
