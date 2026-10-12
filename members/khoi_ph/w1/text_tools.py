import re

def word_count(text: str) -> dict[str, int]:
    cleaned = re.sub(r"[.,!?;:]", "", text.lower())
    words = cleaned.split()
    counts = {}
    for w in words:
        counts[w] = counts.get(w, 0) + 1
    return counts

def top_k(text: str, k: int) -> list[tuple[str, int]]:
    counts = word_count(text)
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:k]