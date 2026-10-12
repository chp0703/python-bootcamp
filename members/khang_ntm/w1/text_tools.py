def word_count(text: str) -> dict:
    punc = ".,!?;:"

    for char in punc:
        text = text.replace(char, "")

    words = text.lower().split()
    counts = {}

    for word in words:
        counts[word] = counts.get(word, 0) + 1

    return counts

def top_k(text: str, k: int) -> list:
    counts = word_count(text)

    sortedWords = sorted(
        counts.items(),
        key=lambda item: (-item[1], item[0])
    )

    return sortedWords[:k]