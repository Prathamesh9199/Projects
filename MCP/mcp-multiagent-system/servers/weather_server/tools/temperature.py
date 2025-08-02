import random

def register(mcp):
    @mcp.tool(name="temperature", description="Tells the temperature in a given location.")
    def temperature(location: str) -> float:
        """
        Tells the temperature of a given location.
        """

        return random.random() * 0.5 + 0.2