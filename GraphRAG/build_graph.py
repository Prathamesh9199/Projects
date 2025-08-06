from graphrag import KnowledgeGraphBuilder
import pandas as pd

# Load the CSV
df = pd.read_csv("finance_projects.csv")

# Load the unstructured text
with open("finance_summary.txt", "r", encoding="utf-8") as f:
    unstructured_text = f.read()

# Combine structured and unstructured content
documents = [
    {
        "content": df.to_csv(index=False),
        "metadata": {"type": "structured", "source": "finance_projects.csv"},
    },
    {
        "content": unstructured_text,
        "metadata": {"type": "unstructured", "source": "finance_summary.txt"},
    }
]

# Initialize the graph builder (Azure OpenAI chat + embedding models)
graph_builder = KnowledgeGraphBuilder.from_config()  # Reads from settings.yaml

# Build the graph
graph = graph_builder.build_knowledge_graph(documents)

# Save it
graph.save("finance_graph.json")

# Show info
print(f"✅ Graph built with {len(graph.nodes)} nodes and {len(graph.edges)} edges.")

# Print sample nodes
for node in list(graph.nodes)[:5]:
    print(f"Node: {node}")