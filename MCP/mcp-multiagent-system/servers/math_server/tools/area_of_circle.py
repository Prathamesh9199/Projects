from resources.constants import PI

def register(mcp):
    @mcp.tool(name="area_of_circle", description="Area of Circle")
    def area_of_circle(radius: float) -> float:
        """
        Calculates the area of a circle.
        """
        print(f"[DEBUG] area_of_circle called with radius={radius}", flush=True)
        return PI * radius ** 2