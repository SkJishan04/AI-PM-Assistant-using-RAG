from vector_store import collection
from retriever import retrieve_context
from llm import call_llm


def answer_question(question: str) -> str:
    if not question.strip():
        return "Please enter a question."

    if collection.count() == 0:
        return "Please upload and index documents first."

    context, sources = retrieve_context(question)
    if not context:
        return "No relevant context found."

    answer = call_llm(question, context)
    source_text = "\n".join(f"- {source}" for source in sources)
    return f"{answer}\n\nSources:\n{source_text}"