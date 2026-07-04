from config import TOP_K
from vector_store import collection


def retrieve_context(question: str) -> tuple[str, list[str]]:
    results = collection.query(query_texts=[question], n_results=TOP_K)
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    context_parts = []
    sources = []
    for document, metadata in zip(documents, metadatas):
        source = metadata.get("source", "unknown")
        chunk = metadata.get("chunk", "?")
        label = f"{source} - chunk {chunk}"
        context_parts.append(f"Source: {label}\n{document}")
        sources.append(label)

    return "\n\n".join(context_parts), sources