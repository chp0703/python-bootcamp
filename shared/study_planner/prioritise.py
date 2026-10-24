from datetime import date

from shared.contract import Task


def prioritise(tasks: list[Task], today: date) -> list[Task]:
    return sorted(
        tasks,
        key=lambda task: task.importance / max((task.deadline - today).days, 1),
        reverse=True,
    )
