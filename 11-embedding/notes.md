# Lecture 11: Embedding

## The problem with basic retrieval (recap from RAG)
RAG's first iteration relied on exact keyword matching in a knowledge base — if the wording didn't match exactly (synonym, typo, rephrasing), retrieval failed. "Happy" ≠ "joyful" to a rigid keyword search, even though they mean the same thing to a human.

Humans don't need exact words to understand each other — "There's a lot of jam on the main road" and "How much traffic is there?" share no common keywords, but people instantly understand they're about the same thing. Computers can't do this naturally — they only understand numbers, not meaning. **Embedding** exists to bridge that gap.

## What is embedding?
Embedding = converting any piece of knowledge (text, image, audio, file, etc.) into a **vector** (an array of numbers) based on a set of features/characteristics.

Simplified example: represent foods using 2 features — sweetness (0–10) and crunchiness (0–10):
- apple → [7, 8]
- cake → [10, 1]
- chips → [1, 9]

Each value is a score for that feature. In real embedding models, instead of 2 hand-picked features like "sweetness," there are hundreds of learned features (e.g. 384 or 768 dimensions) that the model has learned to represent meaning with — not something a human defines by hand.

## Comparing vectors — similarity
Once two pieces of text are vectors, you can measure how similar they are by comparing their arrays:
- cake [10, 1] vs chips [1, 9] → large differences on both features (9 and 8) → very different items.
- apple [7, 8] vs cake [10, 1] → smaller differences (3 and 7) → somewhat similar, but not identical.

The real technique used for this comparison is called **Cosine Similarity** (the simplified "take the difference" example above is just for intuition — real cosine similarity works differently, explained below).

The core goal of embeddings: bring words/sentences with similar *meaning* closer together in vector space — e.g. tea & coffee, dog & cat, table & chair end up numerically close, even with zero shared keywords (like the "jam" / "traffic" example).

## Cosine Similarity
A vector has both a **magnitude** and a **direction**. Cosine similarity cares about the *angle* between two vectors' directions, not their raw distance:
- Two vectors pointing in nearly the same direction (small angle) → high similarity.
- Two vectors pointing in very different directions (e.g. one along the y-axis, one along the x-axis) → little to no similarity.
- Two vectors pointing in opposite directions → negative similarity (very dissimilar).

Cosine similarity output generally ranges from about **1 (very similar)** → **0.5 (somewhat similar)** → **-0.5 or lower (not similar at all)**.

## What's new in the code for this lecture
- Embedding doesn't use a normal chat LLM — it needs a dedicated **embedding model**.
- **sentence-transformers** — a library/model specifically for turning sentences into vectors.
- **NumPy** — used to do the vector math (dot product, norms) for computing cosine similarity.

Embeddings are the stepping stone to **Vector DBs**, covered next.

## Code
`embedding.py`:
- `cosine_similarity(a, b)` — computes cosine similarity manually using NumPy: dot product of the two vectors divided by the product of their magnitudes (`np.linalg.norm`).
- Loads `all-MiniLM-L6-v2` from `sentence-transformers` — a lightweight model producing 384-dimension embeddings.
- Encodes two sentences (`model.encode(text)`) into vectors and compares them with `cosine_similarity`, showing how semantically related vs. unrelated sentences score very differently (e.g. two sentences about leaves/leave-days score higher than a sentence about leaves vs. one about a cat, despite shared words like "leaves" in the trickier pairing).
