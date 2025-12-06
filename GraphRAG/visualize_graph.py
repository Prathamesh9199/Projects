import lancedb
import networkx as nx
import matplotlib.pyplot as plt
import json

# Connect to LanceDB
db = lancedb.connect("output/lancedb")
table = db.open_table("default-text_unit-text")

# Load rows
df = table.to_pandas()

# print(df.columns)

# Preview the data
# print(df.head())

# Create a directed graph
G = nx.DiGraph()

# Print the first three rows of the 'attributes' column without truncation
print(df["attributes"].head(3).to_string(index=False))

# Unpack 'attributes' and build graph
for _, row in df.iterrows():
    attrs = row["attributes"]
    if isinstance(attrs, str):
        attrs = json.loads(attrs)
    
    subj = attrs.get("subject", "Unknown")
    pred = attrs.get("predicate", "related_to")
    obj = attrs.get("object", "Unknown")

    G.add_edge(subj, obj, label=pred)

# Draw graph
pos = nx.spring_layout(G, seed=42)
edge_labels = nx.get_edge_attributes(G, 'label')

plt.figure(figsize=(12, 8))
nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=2000, font_size=10, edge_color="gray")
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9)
plt.title("GraphRAG Knowledge Graph")
plt.show()