# Lecture 1: Your First LLM Call

## Key concepts
- An **LLM call** needs 3 things: an **API key**, a **model** name, and a **message**.
- Client → sends request → LLM server (e.g. Groq) → returns a response.
- A message has a **role** (`user`, `assistant`, or `system`) and **content**.
- Without a role, the LLM has no way to know who's "speaking" — human conversation is context-related, and role is what encodes that context.
- **venv (virtual environment)**: isolates a project's dependencies so different projects can use different versions of the same library without conflicting with each other or with what's installed globally on your machine.

## Code
`hello_llm.py` — loads the API key from `.env`, creates a Groq client, sends a single user message, and prints the raw response object plus the extracted answer text (`response.choices[0].message.content`).
