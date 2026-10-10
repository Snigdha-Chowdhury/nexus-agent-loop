# 00 — Project Overview

## What I'm Building

A multi-agent AI pipeline where a user types in any topic and a chain of AI agents handles the rest:

1. **Research Agent** — gathers information on the topic
2. **Draft Agent** — writes a structured summary from the research
3. **Critic Agent** — reviews the draft and flags weaknesses
4. **Human-in-the-Loop** — I (the user) read the draft and critique, then approve or reject
5. **Final Action Agent** — saves the approved output to a JSON file

The whole thing runs across three layers: a React frontend, a Node.js backend, and a Python AI service powered by LangGraph.

## Why I Built This

I built this project to learn multi-agent orchestration from scratch — by actually building something, not just reading about it.

If you're a beginner who wants to understand how AI agents work together in a real pipeline, this project is meant to be a practical reference. Every phase is documented step by step so you can follow along, understand the why behind each decision, and build it yourself.

## What Problem It Solves

Most tutorials show you a single LLM call. This project goes further — it shows you:

- How to break a task into specialized agents instead of one big prompt
- How to pause a workflow and wait for a human decision (human-in-the-loop)
- How to connect a Python AI service to a Node.js backend and a React UI
- How to think in terms of state machines, not just API calls

## Architecture at a Glance

```
Browser (React)
    ↓ HTTP
Node.js Backend (Express)
    ↓ HTTP
Python AI Service (FastAPI + LangGraph)
    ↓
Research → Draft → Critique → [INTERRUPT] → Final Action
```

## Test Topic Used in This Project

> "How to teach AI agent development to beginner developers"

This topic was chosen because it's directly relevant to what the project itself is trying to do — making agent development approachable for beginners.

## What I Expect to Learn

- LangGraph: graph state, nodes, edges, and interrupts
- How to design a polyglot architecture (Python + Node.js + React)
- How human-in-the-loop workflows actually work in practice
- How to document a project so others can learn from it
