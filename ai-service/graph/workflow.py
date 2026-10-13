from dotenv import load_dotenv
load_dotenv()
from typing import TypedDict 
from langgraph.graph import StateGraph, START
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt, Command
from agents.researcher import research
from agents.drafter import draft
from agents.critic import critic

class GraphState(TypedDict):
    topic: str 
    research: str 
    draft: str 
    critique: str
    decision: str 
    final_action: str

def research_node(state: GraphState) -> GraphState:
    return {"research": research(state["topic"])}

def drafter_node(state: GraphState) -> GraphState:
    return {"draft": draft(state["research"])}

def critic_node(state: GraphState) -> GraphState:
    return {"critique": critic(state["draft"])}

def human_review_node(state: GraphState) -> GraphState:
    decision = interrupt("Review the critique and decide: approve or reject?")
    return {"decision": decision}

def final_action_node(state:GraphState) -> GraphState:
    result=f"Action taken based on decision:{state['decision']}"
    return {"final_action": result}

# Build Workflow
workflow = StateGraph(GraphState)

# Add nodes
workflow.add_node("research", research_node)
workflow.add_node("draft", drafter_node)
workflow.add_node("critic", critic_node)
workflow.add_node("human_review", human_review_node)
workflow.add_node("final_action", final_action_node)

workflow.add_edge(START, "research")
workflow.add_edge("research", "draft")
workflow.add_edge("draft", "critic")
workflow.add_edge("critic", "human_review")
workflow.add_edge("human_review", "final_action")

checkpointer = InMemorySaver()
app = workflow.compile(checkpointer=checkpointer)