"""Small text processing helpers."""


def word_count(text: str) -> dict[str, int]:
    """Count words case-insensitively after replacing common punctuation."""
    for mark in ".,!?:;":
        text = text.replace(mark, " ")

    counts: dict[str, int] = {}
    for word in text.lower().split():
        counts[word] = counts.get(word, 0) + 1
    return counts


def top_k(text: str, k: int) -> list[tuple[str, int]]:
    """Return up to k words ordered by descending count, then alphabetically."""
    if k <= 0:
        return []
    return sorted(word_count(text).items(), key=lambda item: (-item[1], item[0]))[:k]


if __name__ == "__main__":
    example = "Git is fun. Git is fast!"
    print(word_count(example))
    print(top_k(example, 2))
