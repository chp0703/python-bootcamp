def insertion_sort(values: list) -> list:
    """Python sửa trực tiếp list mà không cần tham số tham chiếu & như C++."""
    for index in range(1, len(values)):
        current = values[index]
        position = index - 1
        while position >= 0 and values[position] > current:
            values[position + 1] = values[position]
            position -= 1
        values[position + 1] = current
    return values
