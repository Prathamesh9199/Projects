from fastmcp import FastMCP
import os
import importlib.util
import json

def get_agent_details(config_path: str) -> dict:
    with open(config_path, "r") as f:
        config = json.load(f)
    return config

def load_all_tools(mcp):
    tools_dir = os.path.join(os.path.dirname(__file__), "tools")
    for fname in os.listdir(tools_dir):
        if fname.endswith(".py"):
            path = os.path.join(tools_dir, fname)
            spec = importlib.util.spec_from_file_location("tool_module", path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            if hasattr(mod, "register"):
                mod.register(mcp)

if __name__ == "__main__":
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    config = get_agent_details(config_path)
    AGENT_NAME = config["agent"]["name"]
    mcp = FastMCP(name=AGENT_NAME)
    load_all_tools(mcp)
    mcp.run(transport="http", host="0.0.0.0", port=8000, path="/mcp/")
