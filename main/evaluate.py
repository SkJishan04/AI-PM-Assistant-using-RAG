"""Automated retrieval evaluation using recall@k.

Indexes the demo document, runs a labeled set of questions against the
retriever, and reports what fraction of questions had an expected answer
keyword present in the top-K retrieved chunks.

Usage:
    cd main
    python evaluate.py
"""

from pathlib import Path

from file_loader import read_file
from chunker import chunk_text
from vector_store import collection, clear_collection
from retriever import retrieve_context
from config import TOP_K

DEMO_DOC_PATH = Path(__file__).resolve().parent.parent / "demo_document.txt"

# Each case pairs a question with keywords that should appear in the
# retrieved context if the right chunk(s) were pulled. Any one keyword
# matching counts as a hit for that question.
EVAL_QUESTIONS = [
    {"question": "What is the default notification lead time?",
     "expected_keywords": ["30 minutes"]},
    {"question": "What are the customization options for notification lead time?",
     "expected_keywords": ["10 minutes", "1 hour", "1 day"]},
    {"question": "Who is the assignee for TASK-104?",
     "expected_keywords": ["Sam"]},
    {"question": "What risks are mentioned in this PRD?",
     "expected_keywords": ["battery optimization", "timezone"]},
    {"question": "What is out of scope for v1?",
     "expected_keywords": ["location-based", "voice-activated"]},
    {"question": "What action items came out of the design review?",
     "expected_keywords": ["Alex", "onboarding"]},
    {"question": "Which Jira tickets are blocked?",
     "expected_keywords": ["TASK-104", "queue"]},
    {"question": "What are the success metrics?",
     "expected_keywords": ["25%", "overdue"]},
    {"question": "What engineering risk was raised around cross-device sync?",
     "expected_keywords": ["background sync", "4 days"]},
]


def index_demo_document() -> None:
    clear_collection()
    text = read_file(str(DEMO_DOC_PATH))
    chunks = chunk_text(text)
    ids = [f"demo_document.txt-{i}" for i in range(len(chunks))]
    metadatas = [{"source": "demo_document.txt", "chunk": i + 1} for i in range(len(chunks))]
    collection.upsert(ids=ids, documents=chunks, metadatas=metadatas)


def recall_at_k() -> None:
    index_demo_document()

    hits = 0
    print(f"Running retrieval evaluation with TOP_K={TOP_K}\n")

    for case in EVAL_QUESTIONS:
        context, sources = retrieve_context(case["question"])
        context_lower = context.lower()
        found = any(keyword.lower() in context_lower for keyword in case["expected_keywords"])

        status = "PASS" if found else "FAIL"
        if found:
            hits += 1

        print(f"[{status}] {case['question']}")
        if not found:
            print(f"    expected one of: {case['expected_keywords']}")
            print(f"    retrieved sources: {sources}")

    total = len(EVAL_QUESTIONS)
    score = hits / total if total else 0.0
    print(f"\nRecall@{TOP_K}: {hits}/{total} = {score:.0%}")


if __name__ == "__main__":
    recall_at_k()