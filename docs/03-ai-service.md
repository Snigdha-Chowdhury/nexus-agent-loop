# 03 — AI Service

The AI service is the brain of the Nexus project. It runs the LLM agents and manages the workflow.

---

## What is the AI Service?

It is a Python application built with **FastAPI**. It receives a topic from the backend, runs it through a pipeline of AI agents, pauses for human review, and then completes the final action.

---

## Folder Structure

```
ai-service/
├── agents/
│   ├── researcher.py   # Agent 1 — researches the topic
│   ├── drafter.py      # Agent 2 — writes a structured summary
│   └── critic.py       # Agent 3 — finds weaknesses in the draft
├── graph/
│   └── workflow.py     # Wires all agents together into a pipeline
├── main.py             # FastAPI app — exposes the workflow as API endpoints
├── requirements.txt    # Python dependencies
└── .env                # API keys (never commit this)
```

---

## How the Pipeline Works

```
START
  ↓
[Researcher]  — takes the topic, returns research notes
  ↓
[Drafter]     — takes research notes, returns a structured draft
  ↓
[Critic]      — takes the draft, returns a critique
  ↓
⏸ INTERRUPT   — pauses and waits for a human to approve or reject
  ↓
[Final Action] — records the decision and completes the workflow
  ↓
END
```

---

## The Agents

Each agent is a simple Python function that:
1. Takes a string as input
2. Sends it to the LLM with a prompt
3. Returns the LLM's response as a string

**Example — researcher.py:**
```python
def research(topic: str) -> str:
    prompt = f"Research the following topic and provide detailed notes:\n\n{topic}"
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content
```

---

## The Workflow (LangGraph)

LangGraph is a library that lets you connect functions (called **nodes**) into a pipeline (called a **graph**).

### Key Concepts

| Concept | What it means |
|---------|---------------|
| **Node** | A function that receives state and returns updated state |
| **Edge** | A connection between two nodes |
| **GraphState** | A dictionary that holds all data as it flows through the graph |
| **MemorySaver** | Saves the state after each step so the graph can be paused and resumed |
| **interrupt()** | Pauses the graph and waits for human input |
| **Command(resume=...)** | Resumes the graph after an interrupt |

### GraphState

```python
class GraphState(TypedDict):
    topic: str          # the input topic
    research: str       # output from researcher agent
    draft: str          # output from drafter agent
    critique: str       # output from critic agent
    decision: str       # human's approve/reject decision
    final_action: str   # result of the final action node
```

### Node Example

Each node receives the full state and returns only the fields it updates:

```python
def research_node(state: GraphState) -> GraphState:
    return {"research": research(state["topic"])}
```

---

## The API (FastAPI)

Three endpoints expose the workflow:

### 1. Start the Workflow
```
POST /workflow/start
Body: { "topic": "climate change" }
```
- Starts the graph with the given topic
- Runs research → draft → critic
- Pauses at the interrupt
- Returns `thread_id` and the critique for human review

### 2. Check the Status
```
GET /workflow/status/{thread_id}
```
- Returns the current state of the workflow for a given `thread_id`
- Useful to see what stage the workflow is at

### 3. Resume the Workflow
```
POST /workflow/resume
Body: { "thread_id": "...", "decision": "approve" }
```
- Resumes the graph past the interrupt
- Runs the final action node
- Returns the final result

---

## LLM Provider

This project uses **Groq** as the LLM provider (free tier available).  
Model: `openai/gpt-oss-20b`

To switch models, update the `llm` line in each agent file:
```python
llm = ChatGroq(model="openai/gpt-oss-20b")
```

---

## Running the Service

```bash
cd ai-service
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

Then open **http://localhost:8000/docs** to test all endpoints interactively.

---

## Environment Variables

Create a `.env` file in `ai-service/`:
```
GROQ_API_KEY=your_key_here
```

Get a free API key at [console.groq.com](https://console.groq.com).
