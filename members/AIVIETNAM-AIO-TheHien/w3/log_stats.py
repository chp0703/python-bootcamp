"""Summarise per-route request counts and nearest-rank p95 latency."""

from collections import Counter, defaultdict
from collections.abc import Iterable
from math import ceil, isfinite
from typing import TypedDict


class LogStats(TypedDict):
    """Request counts, p95 latencies, and the route with the highest p95."""

    counts: Counter[str]
    p95: dict[str, float]
    slowest: str | None


def analyse(pairs: Iterable[tuple[str, float]]) -> LogStats:
    """Group requests and select sorted latency at rank ceil(0.95 * count).

    Empty input has no slowest route. Tied routes keep first-seen order.
    Latencies must be finite and non-negative, in milliseconds.
    """
    counts: Counter[str] = Counter()
    latencies: defaultdict[str, list[float]] = defaultdict(list)
    for route, latency in pairs:
        if not isfinite(latency) or latency < 0:
            raise ValueError("latency must be finite and non-negative")
        counts[route] += 1
        latencies[route].append(latency)

    p95 = {
        route: sorted(values)[ceil(0.95 * len(values)) - 1]
        for route, values in latencies.items()
    }
    return {
        "counts": counts,
        "p95": p95,
        "slowest": max(p95, key=p95.__getitem__, default=None),
    }
