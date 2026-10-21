from shared.contract import Block, Task


def allocate(tasks: list[Task], hours: float) -> list[Block]:
    if hours < 0:
        raise ValueError("hours must be non-negative")

    blocks: list[Block] = []
    remaining = hours

    for task in tasks:
        if remaining <= 0:
            break

        allocated = min(task.effort_h, remaining)
        blocks.append(Block(task, allocated))
        remaining -= allocated

    return blocks
