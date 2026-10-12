"""Week 1 search, sorting, matrix, and prime-number exercises."""


def two_sum_sorted(nums: list[int], target: int) -> list[int]:
    """Find two indices whose values add to target in a sorted list."""
    left, right = 0, len(nums) - 1
    while left < right:
        total = nums[left] + nums[right]
        if total == target:
            return [left, right]
        if total < target:
            left += 1
        else:
            right -= 1
    return [-1, -1]


def binary_search(nums: list[int], target: int) -> int:
    """Return the index of target in a sorted list, or -1 when absent."""
    left, right = 0, len(nums) - 1
    while left <= right:
        middle = (left + right) // 2
        if nums[middle] == target:
            return middle
        if nums[middle] < target:
            left = middle + 1
        else:
            right = middle - 1
    return -1


def insertion_sort(nums: list[int]) -> list[int]:
    """Return a sorted copy of nums using insertion sort."""
    result = nums.copy()
    for index in range(1, len(result)):
        value = result[index]
        position = index - 1
        while position >= 0 and result[position] > value:
            result[position + 1] = result[position]
            position -= 1
        result[position + 1] = value
    return result


def transpose(matrix: list[list[int]]) -> list[list[int]]:
    """Return the transpose of a rectangular matrix, including an empty one."""
    if not matrix:
        return []
    return [list(column) for column in zip(*matrix)]


def primes_up_to(limit: int) -> list[int]:
    """Return all prime numbers less than or equal to limit."""
    if limit < 2:
        return []
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for number in range(2, int(limit**0.5) + 1):
        if is_prime[number]:
            for multiple in range(number * number, limit + 1, number):
                is_prime[multiple] = False
    return [number for number, prime in enumerate(is_prime) if prime]


if __name__ == "__main__":
    print(two_sum_sorted([1, 2, 4, 6, 10], 8))
