import importlib

translate = importlib.import_module(
    "members.phkhoiit-1508.w1.translate"
)


def test_transpose_square_matrix():
    matrix = [
        [1, 2],
        [3, 4]
    ]

    expected = [
        [1, 3],
        [2, 4]
    ]

    result = translate.transpose(matrix)

    assert result == expected


def test_transpose_single_row():
    matrix = [[1, 2, 3]]
    expected = [[1], [2], [3]]

    result = translate.transpose(matrix)

    assert result == expected


def test_transpose_single_column():
    matrix = [[1], [2], [3]]
    expected = [[1, 2, 3]]

    result = translate.transpose(matrix)

    assert result == expected


def test_transpose_empty_matrix():
    matrix = []
    expected = []

    result = translate.transpose(matrix)

    assert result == expected


def test_transpose_negative_and_zero():
    matrix = [
        [0, -1],
        [-2, 3]
    ]
    expected = [
        [0, -2],
        [-1, 3]
    ]

    result = translate.transpose(matrix)

    assert result == expected
