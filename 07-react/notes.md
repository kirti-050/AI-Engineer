# Lecture 7: ReAct (Reasoning + Action)

## The problem
- An LLM is trained on historical data up to some cutoff date, so it has no way to know present/live info — today's weather, today's train schedule, today's product price, etc.
- Solution: give the LLM **tools** (APIs/functions) it can call to fetch present-day data, alongside its historical knowledge. So the LLM answers using two sources: what it already knows + what it can look up via tools.
- Once an agent has *many* tools (not just one), a new problem appears: **which tool to use, and when?** This can't be hardcoded with if-else, because the user's query comes in plain English and has near-infinite phrasing/complexity.

## Real-world shape of the problem
- e.g. Amazon's customer support AI Agent = LLM + Tools (order_status, track_delivery, return_item, refund_item, search_product, update_address, etc.)
- Not every tool is needed for every query — "Where is my order?" only needs `order_status` → `track_delivery`, not refund/return tools.
- Tools can also **chain**: the output of one tool becomes the input to the next (e.g. get an order ID → feed it into "track this order" → get status → feed that into something else).
- Because of this chaining and the sheer number of tool combinations possible, pre-determining the exact tool sequence in code isn't realistic — it has to be the LLM's job to decide what to use, when, how, and how much, based on reading and reasoning about the query itself.

## What ReAct is
**ReAct = Reasoning + Acting.** The LLM reads the prompt, reasons about what it needs to do, picks ONE tool, gets a result, feeds that result back in as more context, and reasons again — looping until it has a final answer.

Example: *"I want to buy an iPhone 17. I have 5000 rupees. If I buy it, how much money will I be left with?"*
1. Reasoning: need the current price of iPhone 17 (not historical → needs a tool).
2. Action: call a price-lookup tool → Observation: ₹2000.
3. Reasoning: now calculate 5000 − 2000.
4. Action: call a calculator tool → Observation: ₹3000.
5. Final Answer: ₹3000 left.

This read → reason → act → observe → reason again loop is the **ReAct loop**. The LLM decides the tool choice itself — nothing is hardcoded by the developer.

ReAct is essentially why modern AI agents are LLM + Tools, not just an LLM alone — a bare LLM with no tools can't function as a real-world agent today.

## The ReAct loop — rules
1. Decide what you need to do next.
2. Call ONLY ONE tool at a time.
3. After writing an Action, STOP immediately.
4. Never guess or invent a tool result.
5. Wait until you receive an Observation.
6. Then decide your next action.
7. When the task is complete, give the Final Answer.

## Code
`react_agent.py` — implements a minimal ReAct loop with two tools (`get_product_price`, `calculator`). The system prompt defines the tool-calling format (`Action: tool_name("argument")`) and the 7 loop rules. The agent loop:
- Sends the conversation so far to the LLM.
- If the response contains `Final Answer:`, stops.
- Otherwise, regex-parses out the `Action: tool_name(argument)` call, runs the matching Python function, and appends the result back into the conversation as an `Observation:` message.
- Repeats (up to 5 steps) until the LLM produces a Final Answer — demonstrating tool chaining (price lookup → calculator) driven entirely by the LLM's own reasoning.
