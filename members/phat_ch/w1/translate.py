""" Member 1 - binary search on sorted vector."""

def binary_search(a: list[int], key: int) -> int:
    """
    Difference from C++ version:
    In C++, vector size management uses `a.size()` and manual integer casting, 
    whereas Python provides `len()` function and dynamic typing. 
    Additionally, Python uses `//` for explicit integer division to avoid float conversion. 
    """
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