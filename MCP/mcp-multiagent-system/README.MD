# MCP Multi-Agent System

This project is a modular, local-first Multi-Agent system that implements the MCP (Multi-agent Communication Protocol) using JSON-RPC over `stdio`. It includes:

- **Math Server** – provides arithmetic tools.
- **Weather Server** – simulates weather queries.
- **Clients** – route requests between the host and servers.
- **Host** – orchestrates agents using LangGraph and Mistral 7B via Ollama.
- **Shared utilities** – standardize MCP interactions.

## 📁 Project Structure

```
mcp-multiagent-system/
├── clients/
│   ├── math_client/
│   │   ├── __init__.py
│   │   └── main.py
│   └── weather_client/
│       ├── __init__.py
│       └── main.py
├── host/
│   ├── __init__.py
│   ├── config.json
│   ├── graph/
│   │   ├── __init__.py
│   │   └── build_graph.py
│   ├── main.py
│   └── prompts.txt
├── servers/
│   ├── math_server/
│   │   ├── __init__.py
│   │   ├── config.json
│   │   ├── main.py
│   │   ├── prompts/prompts.txt
│   │   ├── resources/constants.py
│   │   └── tools/
│   │       ├── add.py
│   │       ├── area_of_circle.py
│   │       └── subtract.py
│   └── weather_server/
│       ├── __init__.py
│       ├── config.json
│       ├── main.py
│       ├── prompts/prompts.txt
│       ├── resources/city_list.py
│       └── tools/
│           ├── rain.py
│           └── temperature.py
├── shared/
│   └── utils.py
├── test/
│   └── test_math_server.py
├── requirements.txt
└── README.md
```

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/mcp-multiagent-system
cd mcp-multiagent-system
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate    # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 🚀 Running the System

> Make sure to run each component in a separate terminal window.

### 1. Start Math Server

```bash
python servers/math_server/main.py
```

### 2. Start Weather Server

```bash
python servers/weather_server/main.py
```

### 3. Start Math Client

```bash
python clients/math_client/main.py
```

### 4. Start Weather Client

```bash
python clients/weather_client/main.py
```

### 5. Start Host (LangGraph)

```bash
python host/main.py
```

## 🧠 Tools Provided

### Math Server

- `add(a: float, b: float) → float`
- `subtract(a: float, b: float) → float`
- `area_of_circle(radius: float) → float`

### Weather Server

- `temperature(location: str) → float`
- `rain(location: str) → float`

## 🧪 Testing

### Run the math server test

```bash
python test/test_math_server.py
```

This checks if the server responds correctly to an `initialize` + `add` request.

## 💡 Sample JSON-RPC Request

Request:

```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "method": "add",
  "params": {
    "a": 5,
    "b": 3
  }
}
```

Response:

```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "result": 8
}
```

## 📦 Requirements

```
fastmcp==2.11.0
langgraph==0.0.33
langchain==0.2.0
ollama==0.1.8
```

## 📚 Resources

- FastMCP SDK: https://github.com/monadfi/fastmcp
- LangGraph: https://github.com/langchain-ai/langgraph
- Ollama: https://ollama.com
- JSON-RPC Spec: https://www.jsonrpc.org/specification

## 📜 License

MIT License.