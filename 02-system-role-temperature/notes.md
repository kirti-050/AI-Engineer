# Lecture 2: System Role + Temperature

## System role
- The `system` role tells the LLM *who it is* / how it should behave for the rest of the conversation, before it even sees the user's message.
- The LLM reads the system message first, then the user message, and replies in character.
- Same user message + different system role → different response (e.g. "act as my girlfriend" vs "act as my colleague").
- Real-world use: a company can spin up multiple clients of the same base model (e.g. Claude), each with a different system role, to power different agents (architect, developer, manager, etc.) instead of getting one generalized response for everything.

## Temperature
- Temperature controls how "creative" vs "safe" the LLM's predictions are.
- Range (Groq API): 0 to 2. Default is 0.
- `temperature = 0` → safest, most predictable prediction (closest to the "obvious" answer).
- Higher temperature → more creative/random, LLM "explores" more before answering.
- LLMs are **prediction models**, not truth-telling machines — temperature tunes how much risk the prediction takes.
- Use case matters: an AI agent for a doctor needs low temperature (facts, safety). An AI agent for storytelling/content generation can use a higher temperature (creativity).

## Code
`sys_temp.py` — sends a system message (brand manager persona) + a user prompt asking for a one-word clothing brand name, with `temperature = 0` for a safe/consistent answer.
