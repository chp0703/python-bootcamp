"""Translate the insertion-sort exercise into Python."""


def insertion_sort(values: list[float]) -> list[float]:
    """Sort values in place and return the same list, without C++ references."""
    for index in range(1, len(values)):
        current = values[index]
        position = index - 1
        while position >= 0 and values[position] > current:
            values[position + 1] = values[position]
            position -= 1
        values[position + 1] = current
    return values
