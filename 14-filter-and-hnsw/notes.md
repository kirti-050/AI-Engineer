# Day 14: Filters & HNSW

## 1. HNSW (Hierarchical Navigable Small World)

### The problem

Linear search checks vectors one by one. Fine for a small knowledge base, but with millions of vectors it becomes far too slow.

### The analogy

You are in Lucknow and want to find the "Nemo Fish" shop in CP, Delhi.

- **Linear search:** ask every shop in every lane of Lucknow, then every city on the way, all the way to Delhi. You will find it, but it takes forever.
- **HNSW:** don't ask anyone on the way. Get as close as possible first (Lucknow airport -> flight -> Delhi airport -> CP), and only then search the lanes of CP.

The idea: the world is small, everything is connected to something. Use those connections, take big hops, and get near the target before searching carefully.

### How it works for vectors

- Vectors are connected to other vectors (a graph).
- To answer a query, HNSW first finds the **region** where the closest vector is likely to be.
- Inside that region, it finds a smaller **sub-region**, and repeats until it reaches the nearest vector.
- Qdrant uses HNSW internally to find the top-k.

> We don't write any code for HNSW. Qdrant does it automatically. It is only here to understand why search stays fast.

## 2. Filters

### Why filters?

In production, data is JSON, not just text:

```json
{ "text": "24 days of leave", "category": "vacation", "is_active": true }
```

Without filters, Qdrant searches **all** vectors and returns the top-k. With filters, we can say "search only vectors where `category` = vacation and `is_active` = true".

Real-world example: an FAQ section on a website (leave, salary, departments). If the user is in the "leave" section, search only the leave category.

### Index (needed before filtering)

An index tells Qdrant to learn **in advance** which vectors fall under which payload value (like the index page of a book).

Example with 6 vectors:

- vacation -> vectors 1, 4
- work-life balance -> vectors 2, 3, 5

When we create the collection, we also create a payload index on the fields we want to filter on. Then Qdrant can filter quickly during search.

If we don't plan to filter on a field, no index is needed for it.

### Filter conditions

| Condition | Think of it as | Meaning |
|-----------|----------------|---------|
| `must` | AND | all conditions must be true |
| `must_not` | NOT | exclude this condition |
| `should` | OR | at least one condition should be true |

The filter is passed at search time.

## 3. Code Flow (Qdrant filter version)

| Part | What it does |
|------|--------------|
| 1 | Imports (new: `Filter`, `FieldCondition`, `MatchValue`, `MatchAny`, `PayloadSchemaType`, `json`) |
| 2 | Connect to Qdrant Cloud |
| 3 | Create collection `knowledge_filter` + create payload index on `category` (`PayloadSchemaType.KEYWORD`) |
| 4 | Load `knowledge.json` (list of dicts with `text`, `category`, `is_active`) |
| 5 | Embed only the `text` field of each document |
| 6 | Build points: payload is the **whole dict** (`documents[i]`), not only text |
| 7 | Upsert points |
| 8 | `search()` (no filter) and `search_with_filter()` (passes `query_filter`) |
| 9 | Test search with `reimbursement_filter` |
| 10-12 | Groq LLM + RAG pipeline, same as before |

### The filter used

```python
reimbursement_filter = Filter(
    must = [
        FieldCondition(
            key = "category",
            match = MatchValue(value = "reimbursement")
        )
    ]
)
```

## 4. Key Points to Remember

- HNSW = graph-based approximate search: jump close first, then search locally. Automatic in Qdrant.
- Store the full JSON as payload so filters have fields to work on.
- Create the payload index on the filter field (`category`) before filtering.
- `must` = AND, `must_not` = NOT, `should` = OR.
- `MatchValue` matches one exact value; `MatchAny` matches any value from a list.
- Filtering happens **together with** vector search: only vectors that pass the filter are compared.

## 5. Things to Check in the Code

- **Part 12 doesn't use the filter.** It calls `search(...)`, not `search_with_filter(...)`, so the final RAG answer is unfiltered. Use `search_with_filter(question, some_filter, top_k = 3)` there if you want filtered RAG.
- **Part 9 is a deliberate mismatch.** The query asks about vacation days but filters on `reimbursement`, so it returns only reimbursement results. Good for proving the filter works; for a real answer, filter on `leave` (that's the category in `knowledge.json`).
- **`is_active` has no index yet.** Only `category` is indexed. To filter on `is_active` too, create a second index with `PayloadSchemaType.BOOL`.
