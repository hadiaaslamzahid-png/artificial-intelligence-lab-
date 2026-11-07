import re


def word_spans(text):
    """Return start/end character positions for whitespace-separated words."""
    return [(match.start(), match.end()) for match in re.finditer(r"\S+", text)]


def windows(text, size=40, overlap=10, offset=0):
    if size <= 0 or not 0 <= overlap < size:
        raise ValueError("Use size > 0 and 0 <= overlap < size.")

    spans = word_spans(text)
    chunks = []
    step = size - overlap

    for start_index in range(0, len(spans), step):
        end_index = min(start_index + size, len(spans))
        chunks.append((
            offset + spans[start_index][0],
            offset + spans[end_index - 1][1]
        ))
        if end_index == len(spans):
            break
    return chunks


def sentence_chunks(text, size=40):
    if size <= 0:
        raise ValueError("Chunk size must be positive.")

    # A simple teaching splitter: punctuation followed by whitespace.
    boundaries = [0]
    boundaries += [
        match.end() for match in re.finditer(r"[.!?]\s+", text)
    ]
    boundaries.append(len(text))

    result = []
    pending = None
    pending_words = 0

    for start, end in zip(boundaries, boundaries[1:]):
        segment = text[start:end]
        count = len(segment.split())
        if count == 0:
            continue

        if count > size:
            if pending is not None:
                result.append(pending)
            result.extend(windows(segment, size, 0, start))
            pending, pending_words = None, 0
        elif pending is not None and pending_words + count <= size:
            pending = (pending[0], end)
            pending_words += count
        else:
            if pending is not None:
                result.append(pending)
            pending, pending_words = (start, end), count

    if pending is not None:
        result.append(pending)
    return result


def make_chunks(documents, strategy):
    chunks = []
    for doc_id, source_text in documents.items():
        if strategy == "sentence":
            spans = sentence_chunks(source_text, 40)
        elif strategy in ("0", "10"):
            spans = windows(source_text, 40, int(strategy))
        else:
            raise ValueError("Strategy must be 0, 10, or sentence.")

        for number, (start, end) in enumerate(spans):
            chunks.append({
                "id": f"{doc_id}:{number}",
                "doc": doc_id,
                "start": start,
                "end": end,
                "text": source_text[start:end]
            })
    return chunks


if __name__ == "__main__":
    assert windows("") == []
    assert windows("short text") == [(0, 10)]

    try:
        windows("a b", 2, 2)
    except ValueError:
        pass
    else:
        raise AssertionError("Invalid overlap was accepted.")

    long_sentence = " ".join(["word"] * 95) + "."
    assert all(
        len(long_sentence[start:end].split()) <= 40
        for start, end in sentence_chunks(long_sentence)
    )

    print("Chunking boundary tests passed.")
    print("A long sentence is split into safe-size fallback chunks.")
