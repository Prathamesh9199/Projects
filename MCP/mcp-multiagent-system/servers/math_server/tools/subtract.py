def register(mcp):
    @mcp.tool(name="subtract", description="Subtract 2 numbers")
    def subtract(a: float, b: float) -> float:
        """
        Subtracts two numbers.
        """
        print(f"[DEBUG] Subtract called with a={a}, b={b}", flush=True)
        return a - b