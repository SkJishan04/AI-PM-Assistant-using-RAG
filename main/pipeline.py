from vector_store import collection
from retriever import retrieve_context
from llm import call_llm


def answer_question(question: str, history: list | None = None) -> tuple[str, list]:
    history = history or []

    if not question.strip():
        return "Please enter a question.", history

    if collection.count() == 0:
        return "Please upload and index documents first.", history

    context, sources = retrieve_context(question)
    if not context:
        return "No relevant context found.", history

    answer = call_llm(question, context, history=history)
    source_text = "\n".join(f"- {source}" for source in sources)
    full_answer = f"{answer}\n\nSources:\n{source_text}"

    updated_history = history + [(question, answer)]
    return full_answer, updated_history