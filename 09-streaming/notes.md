# Lecture 9: Streaming

## What is streaming?
When you ask an LLM something, it doesn't generate the entire answer and dump it all at once — it generates line by line (word by word, really), continuously, until it reaches the end. Each piece that arrives as it's generated is called a **chunk**.

This is the same idea behind streaming on Netflix/YouTube: a video doesn't fully load before you watch it — it loads progressively while you watch the part that's already loaded, continuously, in chunks.

Analogy: a waiter bringing a 3-course order (starter, main course, dessert) one dish at a time instead of waiting for everything to be ready and bringing it all together.

## The `stream` parameter
LLM APIs have a `stream` setting, `False` by default:
- `stream = False` → the LLM generates the entire answer internally first, then dumps the whole thing at once.
- `stream = True` → the LLM sends back chunks of the response as they're generated, piece by piece.

## Why streaming matters
How fast/slow a service *feels* to a human is judged by **when the first item arrives**, not when the last one does.

Restaurant example: starter takes 10 min, main course 30 min, dessert 5 min (45 min total either way).
- If the waiter waits for everything and brings it all together → you wait 45 minutes with nothing, and the service feels terrible.
- If the waiter brings each dish as it's ready → your first dish arrives in 10 minutes, and you're already eating by the time the rest arrives. Total time is unchanged, but *perceived* wait time drops dramatically.

Same logic applies to an LLM generating a 1000-line essay that takes 5 minutes total: dumping it all at once makes the user wait 5 idle minutes and feel like the tool is slow. Streaming it line-by-line means the user sees progress immediately and can start reading while the rest is still being generated — much better human experience, even though total generation time is identical.

## When to use streaming vs. not
- **Use streaming** when the end-user is a **human** — e.g. a chatbot, since a person is reading the response as it comes in.
- **Don't use streaming** when the end-user is **code**, not a human — e.g. when the LLM is generating a JSON output that's consumed by another program. Streaming would deliver the JSON in pieces/line-by-line, which breaks the structure — a JSON object needs to be received whole/complete to be parsed correctly.

## Code

streaming.py — sends a single prompt with stream = True and iterates over the returned stream object. For each chunk, it reads chunk.choices[0].delta.content (the incremental piece of text for that chunk) and prints it immediately (end="", flush=True) so the response appears progressively in the terminal, the same way a chatbot UI would render it.
`streaming.py` — sends a single prompt with `stream = True` and iterates over the returned stream object. For each `chunk`, it reads `chunk.choices[0].delta.content` (the incremental piece of text for that chunk) and prints it immediately (`end=""`, `flush=True`) so the response appears progressively in the terminal, the same way a chatbot UI would render it.
