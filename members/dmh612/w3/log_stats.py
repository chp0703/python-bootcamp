"""Summarise route counts and nearest-rank p95 latency."""

from collections import Counter, defaultdict
from collections.abc import Iterable
from math import ceil, isfinite
from typing import TypedDict


class LogStats(TypedDict):
    """Result of analysing route/latency pairs."""

    counts: Counter[str]
    p95: dict[str, float]
    slowest: str | None


def analyse(pairs: Iterable[tuple[str, float]]) -> LogStats:
    """Count requests and compute p95 as sorted_values[ceil(0.95 * n) - 1].

    Ties for slowest are resolved alphabetically. Empty input returns empty
    mappings and None. Negative or non-finite latencies raise ValueError.
    """
    counts: Counter[str] = Counter()
    latencies: defaultdict[str, list[float]] = defaultdict(list)
    for route, latency in pairs:
        if not isfinite(latency) or latency < 0:
            raise ValueError("latency_ms must be finite and non-negative")
        counts[route] += 1
        latencies[route].append(latency)
    p95 = {
        route: sorted(values)[ceil(0.95 * len(values)) - 1]
        for route, values in latencies.items()
    }
    slowest = min(p95, key=lambda route: (-p95[route], route)) if p95 else None
    return {"counts": counts, "p95": p95, "slowest": slowest}
