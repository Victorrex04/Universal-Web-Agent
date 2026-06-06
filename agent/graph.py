from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from typing import TypedDict, Annotated
from agent.tools import browse_page

class AgentState(TypedDict):
    messages: Annotated[list, "add_messages"]
    url: str | None

# Use gpt-4o-mini for cheaper & faster testing
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
tools = [browse_page]
llm_with_tools = llm.bind_tools(tools)

async def agent_node(state: AgentState):
    response = await llm_with_tools.ainvoke(state["messages"])
    return {"messages": [response]}

def should_continue(state: AgentState):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END

workflow = StateGraph(AgentState)
workflow.add_node("agent", agent_node)
workflow.add_node("tools", lambda state: {"messages": [browse_page.invoke(state["messages"][-1].tool_calls[0]["args"])]})

workflow.set_entry_point("agent")
workflow.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
workflow.add_edge("tools", "agent")

def create_web_agent_graph():
    return workflow.compile()