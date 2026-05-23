import os
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI

# 1. Define the state representing the workflow
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], "The history of messages in the workflow"]
    current_agent: str
    decision: str

# 2. Mock Agent Nodes (Will interface with Ollama or OpenAI)
def planner_agent(state: AgentState):
    """Determines what research or analysis needs to be done."""
    messages = state.get("messages", [])
    print("[Planner] Analyzing request:", messages[-1].content)
    
    # In a real app, this invokes an LLM
    response = AIMessage(content="Generated plan: 1. Research phase, 2. Analysis phase.")
    return {"messages": messages + [response], "current_agent": "Planner", "decision": "ROUTE_RESEARCH"}

def research_agent(state: AgentState):
    """Executes search or data retrieval operations."""
    messages = state.get("messages", [])
    print("[Research] Executing search...")
    response = AIMessage(content="Gathered necessary documentation and vector embeddings.")
    return {"messages": messages + [response], "current_agent": "Research", "decision": "ROUTE_ANALYST"}

def analyst_agent(state: AgentState):
    """Synthesizes the research into actionable data."""
    messages = state.get("messages", [])
    print("[Analyst] Crunching data...")
    response = AIMessage(content="Data synthesized into core insights.")
    return {"messages": messages + [response], "current_agent": "Analyst", "decision": "ROUTE_WRITER"}

def writer_agent(state: AgentState):
    """Formats the final response for the user."""
    messages = state.get("messages", [])
    print("[Writer] Drafting final report...")
    response = AIMessage(content="Final operational report compiled successfully.")
    return {"messages": messages + [response], "current_agent": "Writer", "decision": "END"}

# 3. Router Function
def routing_logic(state: AgentState) -> str:
    decision = state.get("decision", "END")
    if decision == "ROUTE_RESEARCH": return "research"
    if decision == "ROUTE_ANALYST": return "analyst"
    if decision == "ROUTE_WRITER": return "writer"
    return END

# 4. Build the LangGraph Workflow
def build_workflow():
    workflow = StateGraph(AgentState)
    
    workflow.add_node("planner", planner_agent)
    workflow.add_node("research", research_agent)
    workflow.add_node("analyst", analyst_agent)
    workflow.add_node("writer", writer_agent)
    
    workflow.set_entry_point("planner")
    
    workflow.add_conditional_edges("planner", routing_logic)
    workflow.add_conditional_edges("research", routing_logic)
    workflow.add_conditional_edges("analyst", routing_logic)
    workflow.add_conditional_edges("writer", routing_logic)
    
    return workflow.compile()

# Singleton instance
engine = build_workflow()

def execute_chat_workflow(prompt: str):
    """Helper method to invoke the engine from a FastAPI endpoint."""
    input_state = {"messages": [HumanMessage(content=prompt)]}
    final_state = engine.invoke(input_state)
    return final_state
