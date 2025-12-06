from fastmcp import FastMCP
import os
import json
from graph.build_graph import build_langgraph

def get_agent_config(config_path: str) -> dict:
    with open(config_path, "r") as f:
        return json.load(f)

if __name__ == "__main__":
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    config = get_agent_config(config_path)

    AGENT_NAME = config["agent"]["name"]

    mcp = FastMCP(name=AGENT_NAME)

    # Register clients
    for client in config["clients"]:
        mcp.include(path=client["path"], name=client["name"])

    # Build orchestration graph
    graph = build_langgraph(mcp)
    mcp.include_graph(graph)

    mcp.run(transport="stdio")
