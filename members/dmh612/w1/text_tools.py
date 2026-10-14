"""Module for text processing tools."""
import re


def word_count(text: str) -> dict[str, int]:
    """Count occurrences of each word, ignoring punctuation .,!?;:."""
    cleaned = re.sub(r"[.,!?;:]", "", text.lower())
    words = cleaned.split()
    counts = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    return counts


def top_k(text: str, k: int) -> list[tuple[str, int]]:
    """Return top k words sorted by count descending, then alphabetically."""
    counts = word_count(text)
    # Sắp xếp: số lần xuất hiện giảm dần (-count), từ ngữ tăng dần theo bảng chữ cái (word)
    sorted_words = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return sorted_words[:k]


if __name__ == "__main__":
    assert word_count("Git is fun. Git is fast!") == {"git": 2, "is": 2, "fun": 1, "fast": 1}
    assert top_k("Git is fun. Git is fast!", 2) == [("git", 2), ("is", 2)]
    assert top_k("", 3) == []
    print("text_tools.py: PASS")