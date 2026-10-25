def word_count(text: str) -> dict[str,int]:
    """Count case-insensitive words after replacing supported punctuation."""
    text = text.lower()

    for punct in ".,!?;:":
        text = text.replace(punct," ")

    words = text.split()
    count = {}
    for word in words:
        count[word] = count.get(word,0) +1

    return count

def top_k(text: str, k: int) -> list[tuple[str, int]]:
    """Return up to ``k`` words ordered by count then alphabetically."""
    count = word_count(text)

    sorted_item = sorted(count.items(), key = lambda x: (-x[1],x[0]))
    return sorted_item[:k]

