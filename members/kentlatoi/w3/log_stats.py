"""Summarise request latency by route."""

from collections import Counter, defaultdict
from math import ceil


def analyse(pairs: list[tuple[str, float]]) -> dict:
    """Return counts, nearest-rank p95 per route, and its slowest route.

    The nearest-rank index is ceil(0.95 * n) in sorted order. For empty
    input, counts and p95 are empty and slowest is None. Ties use the first
    route seen in the input.
    """
    counts = Counter(route for route, _ in pairs)
    latencies: dict[str, list[float]] = defaultdict(list)
    for route, latency in pairs:
        latencies[route].append(latency)

    p95 = {
        route: sorted(values)[ceil(0.95 * len(values)) - 1]
        for route, values in latencies.items()
    }
    slowest = max(p95, key=p95.__getitem__) if p95 else None
    return {"counts": dict(counts), "p95": p95, "slowest": slowest}
