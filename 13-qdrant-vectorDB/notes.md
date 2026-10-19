# Lecture 13: Vector Database (Qdrant)

## 1. Why a Vector DB?

As the knowledge base grows, three problems show up:

- **Time:** Linear search (line by line) for cosine similarity gets slow, and so does creating embeddings.
- **Persistence:** If the program stops or power goes out, all in-memory vectors are lost and embeddings must be recreated. A vector DB like Qdrant is persistent: once vectors are stored, they stay.
- **Memory:** More data means more space for vectors, and we can't keep everything on our own device.

## 2. Other Vector Databases

Weaviate, ChromaDB, FAISS, Pinecone, pgvector.

**Why Qdrant?** It is free (to learn) and easy to write and use.

## 3. What Is Qdrant?

A vector database made of **collections** (like tables in SQL). Each collection holds **points** (like rows).

A point stores three things:

1. **ID**: identifies the point
2. **Vector**: the embedding (array of numbers)
3. **Payload**: the actual data/text linked to the vector

```
Qdrant -> Collections -> Points -> (ID + Vector + Payload)
```

## 4. Why Store the Payload, Not Only the Vector?

The LLM is text-based and cannot read embedding arrays. We need the original text to give it as context, so the payload is stored next to the vector.

## 5. How Retrieval Works in RAG

1. Convert the knowledge base into embeddings.
2. Send ID + vector + payload to Qdrant (these points are the whole knowledge base).
3. Convert the user query into a vector (same embedding model).
4. Qdrant computes cosine similarity between the query vector and stored vectors.
5. It returns the top-k most similar points **with their payloads**.
6. Payload text goes to the LLM as context, and the LLM answers.

## 6. Complete RAG Workflow

```
Knowledge Base (text)
   -> Create Embeddings
   -> Store in Qdrant (ID + Vector + Payload)
   -> User Query -> Query Embedding
   -> Similarity Search (top-k payloads)
   -> LLM (query + retrieved context)
   -> Final Answer
```

## 7. Code Pipeline (qdrant.py)

| Part | What it does |
|------|--------------|
| 1 | Imports + load keys from `.env` (Qdrant URL/API key, Groq key) |
| 2 | Connect to Qdrant Cloud with `QdrantClient` |
| 3 | Create collection `knowledge` (vector size 384, cosine distance); delete it first if it exists |
| 4 | Load `knowledge.txt`, one non-empty line = one document |
| 5 | Embed documents with `all-MiniLM-L6-v2` (384 dimensions) |
| 6 | Build `PointStruct` per document (id, vector, payload `{"text": ...}`) |
| 7 | `upsert` points into the collection |
| 8 | `search()`: embed query, `query_points(...)` with `limit=top_k`, `with_payload=True` |
| 9 | Test search, print score + text |
| 10 | Connect to Groq |
| 11 | `ask_llm()`: prompt = "answer using only the context" + context + question |
| 12 | Full pipeline: search -> join payload texts -> LLM -> final answer |

## 8. Key Points to Remember

- Collection vector size **must match** the embedding model (MiniLM = 384).
- Use the **same embedding model** for documents and queries.
- `upsert` inserts new points or updates existing IDs.
- Deleting and recreating the collection each run keeps the demo clean but wipes persistence. Remove that step when you want data to persist.
- Search returns `score` (cosine similarity) + payload; only the payload text goes to the LLM.
- "Answer using only the information provided" in the prompt keeps the LLM grounded in the retrieved context.

## 9. Bug to Fix in Part 12

The context loop has a typo: `for resuslt in results` but uses `result.payload`. It should be `for result in results`, otherwise you get a `NameError`.
