# Lecture 3: Tokens

## What are tokens?
- Text is converted into numbers before an LLM can process it — these numeric chunks of text are called **tokens**. A token isn't always a whole word.
- Two earlier approaches that failed:
  1. Converting each letter to its ASCII value — works for a single word, but painfully slow/impractical for paragraphs or thousands of lines of text.
  2. Assigning every dictionary word a fixed number — fails because new/made-up words (names, brands, slang) constantly appear that aren't in any dictionary, so the vocabulary would need to grow infinitely.
- **Tokenizing**: common, reusable words/word-pieces are treated as a single token (e.g. "the", "in", "walk"). A rare/uncommon word (e.g. a name) gets broken into smaller known sub-pieces, each its own token, similar to how we learn English by learning base words and then extending them (walk → walking).
  - Example: "Bangalore" is common enough to be 1 token, but "Kirti" (a less common word) breaks into 2 tokens.
- Every LLM response changes based on tokens, not raw words.

## Why tokens matter
- **Cost**: Input tokens + Output tokens = Total tokens, and this is what determines the cost of an interaction.
- **Token limits**: `max_tokens` lets you cap how many tokens the model can generate — useful when you need a lightweight/limited AI agent (e.g. "keep responses under 100 tokens"). If the limit is hit, the response gets cut off mid-way.

## Code
`tokens.py` — sends 3 different prompts (varying in length/complexity) with `max_tokens = 50`, and prints prompt tokens, completion tokens, total tokens, and the finish reason for each — showing how token usage scales with prompt complexity.
