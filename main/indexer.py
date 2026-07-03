from pathlib import Path
from typing import Iterable

from file_loader import read_file
from chunker import chunk_text
from vector_store import collection


def index_documents(files: Iterable) -> str:
    if not files:
        return "Please upload at least one document."

    added = 0
    for uploaded_file in files:
        file_path = uploaded_file.name
        file_name = Path(file_path).name
        text = read_file(file_path)
        chunks = chunk_text(text)

        if not chunks:
            continue

        ids = [f"{file_name}-{i}" for i in range(len(chunks))]
        metadatas = [{"source": file_name, "chunk": i + 1} for i in range(len(chunks))]
        collection.upsert(ids=ids, documents=chunks, metadatas=metadatas)
        added += len(chunks)

    return f"Indexed {added} chunks."