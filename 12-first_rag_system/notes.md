# Lecture 12: Build Your First RAG System

## Combining RAG + Embedding
The last two lectures covered RAG (retrieving relevant context for an LLM to answer from) and Embedding (turning text into vectors so similarity can be measured by meaning, not exact keywords). This lecture combines both into one working end-to-end RAG system.

## The two halves of RAG
- **(R) Retrieval** → uses embedding to pull out the best-matching data from a knowledge base for a given query.
- **Augmented Generation** → the LLM reads that retrieved data and answers the question using it.

## Why this simple version isn't enough for real use
The example knowledge base here is only 5 short sentences (~7 KB, checked via `sys.getsizeof(document_embeddings)`), so:
- **Retrieval is brute-force**: every document's embedding gets compared against the query embedding, one by one, then sorted to find the best match. With only 5-6 documents this is trivially fast and scalable enough.
- Real company knowledge bases are nowhere near this small — they're GBs or TBs of data, with lakhs/millions of lines. Scoring every single line one-by-one against a query at that scale is not feasible.

This is exactly the gap **Vector DB** (next lecture) fills — it solves two problems at once:
1. **Space** — efficiently storing huge numbers of vectors.
2. **Searching** — finding the best-matching vectors quickly, without brute-force comparing against everything.

## How this RAG system works, step by step
1. Define a small `documents` list (the knowledge base) — plain text strings (e.g. leave policy, WFH policy, reimbursements, notice period).
2. Embed all documents at once into `document_embeddings` using the sentence-transformer model.
3. Embed the incoming user `query` the same way.
4. `retrieve(query_embedding)` — loops through every document embedding, computes cosine similarity against the query embedding, collects `(score, document)` pairs, sorts them descending, and returns the single best match.
5. `ask_llm(question, context)` — sends a system prompt instructing the LLM to answer in one line, using only the retrieved context, with no hallucination — then returns the LLM's answer.
6. End-to-end: query → embed → retrieve best-matching document → pass as context to the LLM → get a grounded answer.

## Code
`first_rag_system.py` — implements the full pipeline above: a 5-sentence company-policy knowledge base, embedding + cosine-similarity retrieval to find the single most relevant policy line for a query (e.g. "How much vacation do I get?" → retrieves the paid-leave policy), then an LLM call that answers strictly from that retrieved context.
