import os

from config import MAX_HISTORY_TURNS


def build_prompt(question: str, context: str, history: list | None = None) -> str:
    history_text = ""
    if history:
        recent_turns = history[-MAX_HISTORY_TURNS:]
        formatted_turns = "\n".join(
            f"Q: {past_question}\nA: {past_answer}" for past_question, past_answer in recent_turns
        )
        history_text = (
            "Conversation so far (use this only to understand what the current "
            "question refers to, e.g. pronouns like 'it' or 'that' — not as a source of facts):\n"
            f"{formatted_turns}\n\n"
        )

    return (
        "Answer the question using only the context below. "
        "If the answer is not in the context, say you do not know.\n\n"
        f"{history_text}"
        f"Context:\n{context}\n\n"
        f"Question: {question}\n\n"
        "Answer:"
    )


def call_llm(question: str, context: str, history: list | None = None) -> str:
    prompt = build_prompt(question, context, history=history)

    if os.getenv("OPENAI_API_KEY"):
        from openai import OpenAI

        openai_client = OpenAI()
        response = openai_client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
        )
        return response.choices[0].message.content.strip()

    if os.getenv("GEMINI_API_KEY"):
        import google.generativeai as genai

        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel(os.getenv("GEMINI_MODEL", "gemini-1.5-flash"))
        response = model.generate_content(prompt)
        return response.text.strip()

    return (
        "No LLM API key found, so here are the most relevant retrieved notes:\n\n"
        f"{context}"
    )