"""Summarize request counts and latency percentiles by route."""

from collections import Counter, defaultdict
from collections.abc import Iterable
from math import ceil


def analyse(pairs: Iterable[tuple[str, float]]) -> dict[str, object]:
    """Return request counts, nearest-rank p95 values, and the slowest route.

    An empty input produces empty counts and percentiles with ``slowest`` set to
    ``None``. Ties for the highest p95 are resolved by route name.
    """
    latencies: dict[str, list[float]] = defaultdict(list)
    counts: Counter[str] = Counter()
    for route, latency_ms in pairs:
        if latency_ms < 0:
            raise ValueError("latency_ms must be non-negative")
        counts[route] += 1
        latencies[route].append(latency_ms)

    p95: dict[str, float] = {}
    for route, values in latencies.items():
        ordered = sorted(values)
        p95[route] = ordered[ceil(0.95 * len(ordered)) - 1]

    slowest = min(p95, key=lambda route: (-p95[route], route)) if p95 else None
    return {"counts": dict(counts), "p95": p95, "slowest": slowest}
