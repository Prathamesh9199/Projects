from langgraph.graph import StateGraph
from fastmcp import FastMCP
import json

class HostState:
    def __init__(self):
        self.results = []

def decide_branch(state: HostState) -> str:
    last_result = state.results[-1]
    if "temperature" in last_result["name"] or "rain" in last_result["name"]:
        return "weather"
    return "math"

def invoke_math_client(state: HostState, mcp) -> HostState:
    result = mcp.invoke_tool("math_client", name=state.results[-1]["name"], arguments=state.results[-1]["arguments"])
    state.results.append(result)
    return state

def invoke_weather_client(state: HostState, mcp) -> HostState:
    result = mcp.invoke_tool("weather_client", name=state.results[-1]["name"], arguments=state.results[-1]["arguments"])
    state.results.append(result)
    return state

def build_langgraph(mcp: FastMCP):
    builder = StateGraph(HostState)
    
    builder.add_node("router", lambda state: decide_branch(state))
    builder.add_node("math", lambda state: invoke_math_client(state, mcp))
    builder.add_node("weather", lambda state: invoke_weather_client(state, mcp))

    builder.set_entry_point("router")
    builder.add_conditional_edges("router", decide_branch, {
        "math": "math",
        "weather": "weather"
    })

    return builder.compile()
