# Lecture 8: Prompt Chaining

## Until now vs. now
Until now: one prompt → LLM → one output.
Now: real production work is rarely that simple — companies need complex, multi-step tasks solved (e.g. the resume parser: JD → extract skills, resume → extract skills, then match them). This is where **Prompt Chaining** comes in.

## Two ways to handle a complex task
1. **One big prompt** — write a single prompt covering the entire task start to finish, hand it to the LLM.
2. **Break it into smaller tasks (Prompt Chaining)** — split the complex task into small, simple steps. Send Task 1's prompt to the LLM → get its output → use that output to build Task 2's prompt → send to the LLM → get its output → and so on until the end.

Example (resume parser):
- Prompt 1 → extract skills from resume → LLM Call 1
- Prompt 2 → extract skills from JD → LLM Call 2
- Prompt 3 → match resume skills vs JD skills, generate a score (1–100) → LLM Call 3
- Prompt 4 → if score > 60 → notify HR, else → send rejection email → LLM Call 4

## Why chain instead of one big prompt?
1. **Debugging** — If a 2–3 page mega-prompt gives a wrong final result (e.g. a resume that should score ~90% comes back at 30%), there's no way to tell *where* it went wrong — you'd have to reread and debug the entire thing from scratch. With chaining, you can check each step's output individually and pinpoint exactly which step failed.
2. **Modularity** — Once you find the broken step, you only fix that one step instead of rewriting the whole prompt/program.
3. **Different models per step** — Some steps are harder than others. Use a stronger (and more expensive) model only for the genuinely complex steps, and a cheaper/free model for the easy ones — since tokens cost real money, this avoids wasting spend on simple steps.
4. **Retry individual steps** — You can re-run and refine just one step repeatedly until it meets expectations, without re-running the whole pipeline.

## Prompt Chaining vs. ReAct
They can feel similar (both involve multiple LLM calls/steps), but the key difference is **who decides the sequence**:
- **ReAct**: the developer only provides tools/functions (PDF reader, score function, extraction function, email function, etc.). The LLM itself decides what to call, in what order, based on reasoning about the prompt.
- **Prompt Chaining**: the developer decides the exact steps and their order in advance. The code calls Step 1, then explicitly feeds its output into Step 2, then Step 3, etc. — the LLM doesn't choose the sequence, it just executes each step it's given.

## Code
`prompt_chaining.py` — implements a 3-step prompt chain for resume/JD matching:
- `step1_res_extract()` — LLM call to extract skills from a hardcoded resume, returning only the skills.
- `step2_JD_extract()` — LLM call to extract required skills from a hardcoded job description, returning only the skills.
- `step3_match(candidate, jd)` — LLM call that takes the two extracted skill lists and produces a match score (1–100) plus a short fit verdict.
- The three steps run in sequence, each output explicitly fed into the next step's prompt — a `sleep(2)` between calls to avoid rate limits.
