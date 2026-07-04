import os


def build_prompt(question: str, context: str) -> str:
    return (
        "Answer the question using only the context below. "
        "If the answer is not in the context, say you do not know.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {question}\n\n"
        "Answer:"
    )


def call_llm(question: str, context: str) -> str:
    prompt = build_prompt(question, context)

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