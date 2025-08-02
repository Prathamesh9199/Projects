import random

def register(mcp):
    @mcp.tool(name="rain", description="Tells the probability of rain in a given location.")
    def rain(location: str) -> float:
        """
        Tells the probability of rain in a given location.
        """

        return random.random() * 0.5 + 0.2
