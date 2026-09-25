# Lecture 6: Prompt Engineering

## Why prompt engineering?
- Ask an LLM the same thing twice and you can get different answers, in different formats, with different levels of detail — because nothing about the request was actually specified.
- Prompt engineering exists to make LLM answers **stable** (consistent every time) and to **limit the chatbot** to only the specific questions/details it's meant to handle (e.g. a Domino's chatbot should only answer order-related queries — not random coding questions, not internal/production details, not unrelated topics). This is also a real security/production concern, not just a nicety.

## The 6 steps to a secure, stable prompt

1. **Role** — Tell the LLM *who it is*. Should always be domain-related and responsibility-related.
   - Good: "You're a Senior Engineer responsible for reviewing code."
   - Bad: "You are a genius engineer, build GTA 7" — vague, not a real responsibility, doesn't work.

2. **Task** — Tell the LLM *exactly* what work it has to do. Needs to be a clear action with no ambiguity.
   - e.g. "Classification of issues" (not just "handle this").

3. **Constraints** — Give the LLM a boundary on the task.
   - e.g. "The issue should only be classified as one of 3 types: Billing, Technical, Return."

4. **Output Format** — Specify exactly what shape the answer should come back in.
   - e.g. "Answer in one word only."

5. **Zero-shot / One-shot / Few-shot** — Whether (and how many) examples you give the LLM to show it what you mean.
   - **One-shot**: give exactly one example. E.g. "I have more money deducted than my laptop's price → this is a Billing issue."
   - **Zero-shot**: no example given at all.
   - **Few-shot**: more than one example given.

6. **Fallback** — Tell the LLM what to do when the issue doesn't fit any given category, so it doesn't guess or misclassify.
   - e.g. "If the issue doesn't fit Billing/Technical/Return, return Others."
   - Without a fallback, the LLM can get confused or force-fit an unrelated issue into the closest category it can find, which produces wrong answers.

## Bad prompt vs. good prompt
- **Bad prompt example**: "This is a user complaint: My laptop is not working. Handle this." — too vague. No role, no real task, no constraints, no output format, no fallback. Every time you run it, you get a different style/format of answer.
- **Good prompt** uses all 6 steps together: gives the LLM a role (support assistant), a clear task (classify the issue), constraints (3 fixed categories), an output format (one word only), an example (one-shot), and a fallback (Others) — producing a consistent, predictable answer every time.

## Code
`prompt_eng.py` — compares a bad prompt (vague, no structure) against a good prompt that applies Role, Task, Constraints, Output Format, one-shot Example, and Fallback to reliably classify a support ticket into Billing / Technical / Return / Others.
