def word_count(text: str) -> dict[str, int]:
    """Count words without case or common punctuation distinctions."""
    punc = ".,!?;:"

    for char in punc:
        text = text.replace(char, "")

    words = text.lower().split()
    counts = {}

    for word in words:
        counts[word] = counts.get(word, 0) + 1

    return counts

def top_k(text: str, k: int) -> list[tuple[str, int]]:
    """Return the most common words, breaking ties alphabetically."""
    counts = word_count(text)

    sorted_words = sorted(
        counts.items(),
        key=lambda item: (-item[1], item[0]),
    )

    return sorted_words[:k]
