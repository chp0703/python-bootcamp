"""Summarise the study blocks produced by allocate()."""

from shared.contract import Block


def summarise_plan(
    blocks: list[Block],
    available_h: float,
) -> dict[str, int | float]:
    """Summarise allocated study hours."""
    planned_h = sum((block.hours for block in blocks), 0.0)
    return {
        "task_count": len(blocks),
        "planned_h": planned_h,
        "available_h": available_h,
        "remaining_h": available_h - planned_h,
    }
