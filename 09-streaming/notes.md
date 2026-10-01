# Lecture 9: Streaming

## What is streaming?
When you ask an LLM something, it doesn't generate the full answer and dump it all at once — it generates the answer continuously, piece by piece, until it's done. Each continuous piece is called a **chunk**. This piece-by-piece delivery is called **Streaming**.

Same idea as:
- Netflix/YouTube — a video doesn't fully load before you watch it; it loads in chunks while you watch the part that's already loaded.
- A waiter bringing a multi-course order one dish at a time instead of waiting for everything to be ready before bringing it all together.

## The `stream` parameter
LLM APIs have a `stream` setting, `False` by default:
- `stream = False` → the LLM generates the entire answer first, then dumps it all at once.
- `stream = True` → the LLM sends the answer piece by piece (in chunks) as it's generated.

## Why streaming matters (the restaurant example)
How fast/slow a service *feels* to a human user is judged by **when the first item arrives**, not when the last one does.

Example: you order starters (10 min), main course (30 min), dessert (5 min) — total 30+ min either way.
- If the waiter waits for everything and brings it all together: you wait 30+ min for anything at all → feels slow.
- If the waiter brings things as they're ready (starter at 10 min, main at 30 min, dessert last): you get your first dish in just 10 min → feels much faster, even though the *total* time is identical.

Same with an LLM generating a 1000-line essay that takes 5 minutes total:
- Without streaming: you stare at nothing for 5 minutes, then get it all at once — feels painfully slow.
- With streaming: you start reading lines almost immediately while the rest keeps generating — feels fast, even though the total generation time hasn't changed.

**The total time is the same in both cases — streaming only reduces perceived wait time**, which is why LLM companies use it to improve human experience.

## When to use streaming vs. not
- **Use streaming** when the end-user is a **human** — e.g. a chatbot, since a person is reading the output live.
- **Don't use streaming** when the end-user is **code**, not a human — e.g. when the LLM is generating a JSON response that gets passed to another program. Streaming would send the JSON line-by-line/piece-by-piece, breaking the format, since the receiving code needs the JSON as one complete, valid object, not partial fragments.

So streaming isn't a "default always-on" setting for every AI product — it depends on who's actually consuming the output.

## Code
`streaming.py` — sends a prompt with `stream = True`, then iterates over the returned stream object. Each `chunk.choices[0].delta.content` is one small piece of the answer; printed immediately (`end=""`, `flush=True`) as it arrives, producing the live, line-by-line output effect instead of waiting for the full response.
