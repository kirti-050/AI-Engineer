# Lecture 10: RAG (Retrieval Augmented Generation)

## The problem
LLMs like GPT, Claude, Gemini know publicly available/internet knowledge, but have no idea about an organization's internal information — how a company works, its internal codebases, docs, processes, etc. Asked about that, they either refuse to answer or hallucinate a wrong one.

Example: asking an LLM to evaluate your fit for a job — without any extra info it can't answer meaningfully, but if you also give it your resume, it can answer based on that. This is the core idea: when public knowledge isn't enough, give the LLM **additional context** to read and answer from.

## RAG = Retrieval Augmented Generation
The solution is to retrieve relevant information and feed it to the LLM as context before it answers.

## Evolution of approaches

1. **Mention it in the system prompt** — works for small amounts of info, but you can't fit "everything about how a whole company works" into a few lines of a system prompt.

2. **Dump everything into one giant PDF** — tell the LLM to read the whole PDF before answering. Breaks down fast: the PDF becomes huge, multiple companies'/projects' data gets mixed together, and feeding an LLM a company's entire document set (architecture docs, design docs, implementation docs, testing docs, usage docs, etc.) every time burns enormous numbers of tokens — very expensive.

3. **Retrieval (RAG's first iteration)** — instead of giving the LLM everything, build a small piece of software that:
   - Holds a knowledge base (PDF, JSON, dict, etc.)
   - Looks at the user's question, finds matching **keywords** in the knowledge base
   - Fetches only the matching lines/sections (the relevant context)
   - Hands just that retrieved context to the LLM, which reads it and answers

   Flow: **Knowledge base → software retrieves relevant info (context) → context given to LLM → LLM reads context and answers.** This retrieval-then-generation flow is why it's called Retrieval **Augmented** Generation — the LLM's generation is augmented with retrieved context.

## Why this first iteration isn't good enough today
This early retrieval approach is a **rigid, keyword-matching system**, so it breaks easily:
- "What is my age?" works if the knowledge base has an "age" key, but "How old am I?" (same meaning, different words) may fail to match and return "no information."
- A typo ("agee" instead of "age") breaks the keyword match entirely.
- Everyday LLM tools (ChatGPT, Claude) handle rephrasing and typos fine because they understand *meaning*, not just exact keywords — this rigid retrieval system doesn't.
- You can't realistically hand-write every possible phrasing/keyword variant to make the matching robust, and the knowledge base only grows over time, making the matching problem worse.

This is why modern RAG systems have moved to **Vector DBs, Embeddings, Chunking, and Tokenization** — to retrieve based on *meaning/similarity* rather than rigid keyword matching, which is the next stage of this topic.

## Code
`rag_basic.py` — implements the simplest possible RAG pattern:
- `knowledge_base` — a plain Python dict holding facts (age, school).
- `retrieve_info(question)` — rigid keyword-based retrieval: lowercases the question and checks if "age" or "school" appears in it, returning the matching fact or `None` if nothing matches.
- `ask_llm(question)` — builds a system prompt instructing the LLM to answer in one line, based only on the retrieved context, with no hallucination — then sends the system + user messages to the LLM and returns the answer.
- Demonstrates the full RAG loop end-to-end, including its current limitation: ask the question differently or with a typo, and `retrieve_info` returns `None`, so the LLM has no context to answer from.
