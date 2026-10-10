# AI Engineer — Learning Log

My daily learning log following the **"AI Engineer"**. Each folder holds the notes + code for one lecture (or milestone project), in order.

## Log

| # | Topic | Folder |
|---|-------|--------|
| 1 | Your first LLM call — API key, model, message, roles, venv | [`01-llm-call`](./01-llm-call) |
| 2 | System role + Temperature | [`02-system-role-temperature`](./02-system-role-temperature) |
| 3 | Tokens — what they are, why they matter, cost & limits | [`03-tokens`](./03-tokens) |
| 4 | Structured output with Pydantic + JSON | [`04-pydantic-json`](./04-pydantic-json) |
| 5 | Mini project: Resume ↔ Job Description matcher | [`05-resume-parser`](./05-resume-parser) |
| 6 | Prompt Engineering — Role, Task, Constraints, Output Format, Few-shot, Fallback | [`06-prompt-engineering`](./06-prompt-engineering) |
| 7 | ReAct (Reasoning + Action) — LLM + Tools, the ReAct loop, tool chaining | [`07-react`](./07-react) |
| 8 | Prompt Chaining — breaking complex tasks into ordered LLM steps, vs. ReAct | [`08-prompt-chaining`](./08-prompt-chaining) |
| 9 | Streaming — chunks, stream=True, when to stream vs. not (human vs. code consumers) | [`09-streaming`](./09-streaming) |
| 10 | RAG (Retrieval Augmented Generation) — knowledge base, keyword retrieval, why it breaks | [`10-rag`](./10-rag) |
| 11 | Embedding — vectors, semantic meaning vs. keyword matching, cosine similarity | [`11-embedding`](./11-embedding) |
| 12 | Build Your First RAG System — combining retrieval + embedding into a working pipeline | [`12-first-rag-system`](./12-first-rag-system) |


## Setup

Each script expects a `.env` file (not committed) with:

```
GROQ_API_KEY=your_key_here
```

Install dependencies as you go — this repo doesn't pin a single requirements file yet since it's growing lecture by lecture. Rough list so far: `groq`, `python-dotenv`, `pydantic`, `pypdf`, `python-docx`, `numpy`, `sentence_transformers`.

## About

Built while learning — code and notes reflect where I was in the course on the day I wrote them, warts and all. Each folder's `notes.md` has a plain-English summary of the concept plus what the code does.
