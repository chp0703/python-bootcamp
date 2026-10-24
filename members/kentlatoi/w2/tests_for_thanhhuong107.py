
import importlib

translate = importlib.import_module(
    "members.thanhhuong107.w1.translate"
)


def test_binary_search_negative_numbers():
    nums = [-10, -5, 0, 4, 9]
    target = -5
    expected = 1

    result = translate.binary_search(nums, target)

    assert result == expected


def test_insertion_sort_negative_and_duplicates():
    nums = [3, -1, 3, 0, -2]
    expected = [-2, -1, 0, 3, 3]

    result = translate.insertion_sort(nums)

    assert result == expected
    assert nums == [3, -1, 3, 0, -2]


def test_transpose_single_row():
    matrix = [[1, 2, 3]]
    expected = [[1], [2], [3]]

    result = translate.transpose(matrix)

    assert result == expected


def test_primes_up_to_two():
    limit = 2
    expected = [2]

    result = translate.primes_up_to(limit)

    assert result == expected


def test_two_sum_sorted_no_solution():
    nums = [1, 2, 4, 6]
    target = 20
    expected = [-1, -1]

    result = translate.two_sum_sorted(nums, target)

    assert result == expected

