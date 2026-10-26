""" Member 1 - binary search on sorted vector."""

def binary_search(a: list[int], key: int) -> int:
    """Return the index of ``key`` in sorted ``a``, or ``-1`` when absent."""
    lo, hi = 0, len(a) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if a[mid] == key:
            return mid
        elif a[mid] < key:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
