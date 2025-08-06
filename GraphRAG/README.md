GraphRAG Quickstart & Visualization Guide
========================================

GraphRAG (Graph-based Retrieval-Augmented Generation) is an extension of traditional RAG that constructs a knowledge graph from documents to improve reasoning and answer quality. It integrates:

- Entity & relationship extraction
- Hierarchical community detection using clustering
- Summarization of communities
- Graph-augmented querying via Local, Global, and DRIFT search modes

## Requirements

GraphRAG requires Python 3.10 to 3.12 (GraphRAG is not compatible with 3.13+). To get started, install the graphrag Python package using pip:
```
pip install graphrag
```
## Initialization & Config Setup

Create a project directory and place your .txt, .csv, or other supported files under a folder named "input". Then, initialize GraphRAG in your project directory. This will create the necessary configuration files:\
```
graphrag init --root ./your_project
```
This will generate two files for you in your project directory:
- .env file for API credentials
- settings.yaml for config

If you're using Azure OpenAI, remember to update the 'model' section of the settings.yaml file to configure your model settings accordingly.
This will generate two files for you in your project directory:
- .env file for API credentials
- settings.yaml for config


If you're using Azure OpenAI, remember to update the 'model' section of the settings.yaml file to configure your model settings accordingly.

## Indexing (Build Knowledge Graph)

Run the following command in your terminal to build the index:\
```
graphrag index --root ./your_project
```

This performs:

Chunking of documents
Entity and relationship extraction\
Hierarchical community detection using clustering
Embedding generation
Artifacts are saved to ./your_project/output/

## Querying

Global Search:

Run the following command in your terminal to perform a global search:\
```
graphrag query --root ./your_project --method global --query "What are the top themes?"
```

Local Search:

Run the following command in your terminal to perform a local search:\
```
graphrag query --root ./your_project --method local --query "Who is Scrooge?"
```
DRIFT Search:

Run the following command in your terminal to perform a DRIFT search:\
```
graphrag query --root ./your_project --method drift --query "Explain the main topics around X"
```
Other available method: basic (vector-only search)

## Visualization Guide

To generate and visualize a GraphML file, follow these steps:

1. Enable snapshot generation in your settings.yaml file:\
<pre>
snapshots:
    graphml: true
embed_graph:
    enabled: true
umap:
    enabled: true
</pre>

2. Re-run graphrag index to generate the graph.graphml file in the output directory.

3. Open graph.graphml in Gephi or a similar tool.

4. Install the Leiden plugin and run statistics: Leiden + Average Degree.

5. Use ForceAtlas2 or OpenOrd for layout, resize by node degree, color by community, and enable labels if needed.

## Visualizer App (Optional)

You can use a browser-based visualizer (GraphRAG Visualizer) to interact with your graph:

1. Upload the .parquet files from the output directory.

2. It supports searching, graph navigation, and community exploration.

References:

https://dev.to/noworneverev/graphrag-visualizer-an-easy-way-to-visualize-microsofts-graphrag-artifacts-c0c

https://microsoft.github.io/graphrag/get_started/

## Prompt Tuning (Optional)

GraphRAG supports automatic and manual prompt tuning.

Prompts are stored in the prompts/ directory.

You can modify these to better reflect your domain.

Prompt tuning improves answer relevance and context alignment.

## When to Use GraphRAG

GraphRAG is useful when:

- Multi-hop reasoning is required
- The query needs summaries or patterns across documents
- You want structured, interpretable results

Use GraphRAG instead of plain vector RAG when your queries benefit from knowledge structure.

🛡 Limitations

- More resource intensive than vector RAG
- Quality depends on prompt design and entity extraction accuracy
- Inferred relationships can sometimes hallucinate

## References

Documentation: https://microsoft.github.io/graphrag/

Visualization Guide: https://microsoft.github.io/graphrag/visualization_guide/

Research Paper: https://arxiv.org/abs/2404.16130

Blogs:

https://medium.com/@zilliz_learn/graphrag-explained-enhancing-rag-with-knowledge-graphs-3312065f99e1

https://medium.com/data-science-collective/microsofts-graphrag-a-practical-guide-to-supercharging-rag-accuracy-08b4aafc8a46

https://dev.to/noworneverev/graphrag-visualizer-an-easy-way-to-visualize-microsofts-graphrag-artifacts-c0c
