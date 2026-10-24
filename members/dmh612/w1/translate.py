"""W1.4: Bài của member 6 - Merge sorted merge."""


def merge_sorted_vectors(v1: list[int], v2: list[int]) -> list[int]:
    """Merge two already sorted lists/vectors into a single sorted list.
    
    Time Complexity: O(n + m)
    Space Complexity: O(n + m)
    """
    i = 0
    j = 0
    result = []
    
    # Dùng 2 con trỏ so sánh lần lượt từng phần tử
    while i < len(v1) and j < len(v2):
        if v1[i] <= v2[j]:
            result.append(v1[i])
            i += 1
        else:
            result.append(v2[j])
            j += 1
            
    # Gộp phần còn dư (nếu có)
    result.extend(v1[i:])
    result.extend(v2[j:])
    
    return result


merge_two_sorted_vectors = merge_sorted_vectors
merge_sorted = merge_sorted_vectors
merge = merge_sorted_vectors
