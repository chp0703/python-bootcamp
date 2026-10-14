def transpose(matrix: list[list[int]]) -> list[list[int]]:
    """
    Transpose of a 2D matrix.
    Difference from C++: Uses Python's unpacking with zip(*matrix) 
    instead of pre-allocating vectors and using nested index loops.
    """
    if not matrix or not matrix[0]:
        return []
    return [list(row) for row in zip(*matrix)]