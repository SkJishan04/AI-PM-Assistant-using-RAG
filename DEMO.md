# Demo Guide — AI PM Assistant

This guide walks through the included demo files (`demo_document.txt` and `demo_questions.txt`) question by question, showing what a correct, well-grounded answer should look like. Use this to verify your setup is working correctly, and to see the different retrieval behaviors the system is designed to demonstrate.

## Setup

1. Upload `demo_document.txt` via the Documents panel.
2. Click **Index documents** — you should see `Indexed 6 chunks.` (the document is ~3,900 characters after whitespace normalization; with `CHUNK_SIZE=900` and `CHUNK_OVERLAP=150`, the chunker advances in 750-character steps, producing 6 chunks).
3. Work through the questions below in order.

---

## Category 1: Simple Fact Lookup

These questions test whether the system retrieves the single chunk containing a specific fact and reports it accurately, without noise from unrelated sections.

**Q1: What is the default notification lead time?**
Expected answer: **30 minutes.** Found directly in Section 4, Key Requirement #2. This is the easiest case — the fact appears in one sentence, in one chunk.

**Q2: What are the customization options for notification lead time?**
Expected answer: **10 minutes, 30 minutes, 1 hour, 1 day** — from Section 4, Key Requirement #3. Tests whether the system retrieves a *list* correctly rather than just the first item.

**Q3: Who is the assignee for TASK-104?**
Expected answer: **Sam** (also blocked, waiting on the infrastructure team to provision a new queue). This question tests retrieval from the Jira export section specifically, which has a denser, more structured format than the prose sections — a good check that chunking didn't mangle the ticket list.

---

## Category 2: Summarization Across a Section

These questions require the system to synthesize multiple bullet points or sentences into a coherent answer, not just quote one line.

**Q4: What risks are mentioned in this PRD?**
Expected answer should cover all four risks from Section 5:
1. Notification delivery delays on Android due to battery optimization
2. Users disabling notifications at the OS level
3. Timezone handling bugs across devices
4. The personalization model feeling intrusive

If the answer only lists 1–2 of these, it may indicate `TOP_K` is too low to retrieve the full risks section, or the section spans a chunk boundary awkwardly.

**Q5: What were the main discussion points in the design review meeting?**
Expected answer should summarize three threads from Section 8: the debate over the 30-minute default lead time, the engineering estimate/timebox for cross-device sync, and the QA plan for timezone/DST edge cases.

**Q6: What is out of scope for v1?**
Expected answer: **location-based reminders, voice-activated reminder creation, and team-shared reminders** — from Section 10. A short, clean list — good sanity check that exclusion sections are retrieved correctly, not just "positive" requirements.

---

## Category 3: Multi-Fact Reasoning (Connecting Two Parts of the Document)

These are the most demanding questions — they require the retriever to pull chunks from two different sections and the LLM to connect them correctly.

**Q7: What action items came out of the design review, and who owns each one?**
Expected answer should pair each action item with its owner from Section 8:
- Alex → update onboarding flow mockups (by end of Week 1)
- Sam → scope the background sync job (by Monday of Week 2)
- Jordan → draft the timezone test plan (by Week 3)

**Q8: Which Jira tickets are blocked, and why?**
Expected answer: **TASK-104** is the only blocked ticket, blocked because the infrastructure team needs to provision a new queue. This tests whether the system correctly identifies status across *all* six tickets rather than just returning the first one it finds.

**Q9: What are the success metrics, and how do they relate to the goals?**
Expected answer should connect Section 6 (metrics: 25% reduction in overdue tasks, 40% adoption of reminders in week one, 15% acceptance of personalized suggestions) back to Section 2 (goals: reduce missed deadlines, increase daily active usage, keep setup simple). A strong answer explicitly draws the goal → metric connection rather than just listing both separately.

---

## Category 4: Reasoning Slightly Beyond a Single Sentence

**Q10: Why might the personalized lead-time suggestion feature be risky?**
Expected answer should combine the risk noted in Section 5 (*"could feel intrusive if it changes reminder times without clear explanation"*) with the feature description in Section 4 (*it adjusts defaults based on usage data after 2 weeks*) — a slightly deeper synthesis than pure lookup.

**Q11: What engineering risk was raised around cross-device sync, and how was it resolved?**
Expected answer: Sam flagged that syncing would need a new background job and take 3–4 extra engineering days; the team resolved it by timeboxing to 4 days and allowing near-real-time sync (within 5 minutes) instead of instant sync, if needed to hit the deadline. This spans Section 8 only, but requires connecting the problem statement to its resolution within the same meeting notes paragraph.

---

## Category 5: Grounding Checks (Should Say "I Don't Know")

This is the most important category to demonstrate, because it proves the system is *grounded* rather than hallucinating plausible-sounding answers.

**Q12: What is the budget for this project?**
**Q13: Who is the engineering manager overseeing this team?**
**Q14: What programming language is the app built in?**

None of these are answerable from `demo_document.txt`. A correct response says the information isn't available in the provided context — it should **not** invent a dollar figure, a name, or a tech stack. If your system confidently answers any of these, that's a signal the LLM is falling back on general knowledge instead of respecting the "answer only from context" instruction in `llm.py`, and the prompt or model may need adjustment.

---

## What This Demo Proves

Running through all 14 questions demonstrates, in order of increasing difficulty:
1. Basic single-fact retrieval works
2. Retrieval handles both prose and structured (ticket-style) text
3. The system can summarize multiple points from one section
4. The system can combine facts from *different* sections of the same document
5. The system correctly refuses to answer when the source document doesn't contain the answer

If all 14 questions behave as described above, the indexing, retrieval, and generation stages are all working correctly end to end.