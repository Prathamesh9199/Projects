def register(mcp):
    @mcp.tool(name="add", description="Add two numbers")
    def add(a: float, b: float) -> float:
        """
        Adds two numbers.
        """
        print(f"[DEBUG] Add called with a={a}, b={b}", flush=True)
        return a + b