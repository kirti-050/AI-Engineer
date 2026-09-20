# Lecture 4: Pydantic + JSON (Structured Output)

## The problem
- By default, LLM responses are plain strings/paragraphs — great for humans to read, but hard for code to parse reliably.
- If code has to extract specific fields (name, email, issue, etc.) from a free-form string response, that string parsing is fragile and can easily break if the LLM adds extra words or phrases it differently each time.
- When an AI Agent's output feeds into *another* piece of code (not a human), that code needs a predictable, structured format — not a sentence.

## The solution: JSON + Pydantic
- **JSON (JavaScript Object Notation)**: a structured key-value output format that's easy for both humans to read and other programs to parse — no manual string parsing needed. Widely supported by extractor libraries in every language.
- **Pydantic**: a Python library used to define exactly what shape you want the output in.
  - Define a `class` (e.g. `Ticket(BaseModel)`) with typed fields (`name: str`, `email: str`, etc.) — this becomes the schema.
  - `Model.model_json_schema()` turns that class into a JSON schema you can hand to the LLM.
  - Tell the LLM (via system prompt) to return output matching that schema, in JSON format.
  - Use Groq's `response_format = {"type": "json_object"}` so the LLM's response is guaranteed to be valid JSON.
  - Parse the returned JSON string with `json.loads()`, then unpack it into the Pydantic class (`Ticket(**data)`) to get a typed, validated object you can safely use in code (e.g. `ticket.name`, `ticket.email`).

## Code
`json_pydantic.py` — defines a `Ticket` schema (name, email, issue), asks the LLM to extract those fields from a raw customer message into JSON, then loads and validates that JSON into a `Ticket` object.
