"""Count and rank words after normalising case and basic punctuation."""


def word_count(text: str) -> dict[str, int]:
    """Count words separated by whitespace or common punctuation."""
    separators = str.maketrans(",.!?;:", "      ")
    words = text.lower().translate(separators).split()
    counts: dict[str, int] = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    return counts


def top_k(text: str, k: int) -> list[tuple[str, int]]:
    """Return up to k frequent words, breaking count ties alphabetically."""
    counts = word_count(text)
    ranked = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return ranked[: max(k, 0)]
