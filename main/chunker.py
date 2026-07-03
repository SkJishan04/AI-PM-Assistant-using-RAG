from config import CHUNK_SIZE, CHUNK_OVERLAP


def chunk_text(text: str) -> list[str]:
    clean_text = " ".join(text.split())
    chunks = []
    start = 0

    while start < len(clean_text):
        end = start + CHUNK_SIZE
        chunk = clean_text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks