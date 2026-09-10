# A2A Multi-Agent System

A sophisticated multi-agent orchestration framework built on the A2A protocol with LangChain and Groq. This system enables intelligent task routing and execution across specialized AI agents for complex, multi-step workflows.

## 🎯 Overview

The A2A Multi-Agent System implements an **Agent-to-Agent (A2A)** communication protocol that allows:
- **Intelligent Routing**: Automatically routes queries to the most suitable agent
- **Multi-Step Orchestration**: Breaks complex tasks into steps and executes them sequentially
- **Specialized Agents**: Each agent has specific expertise and tools
- **Live Database Integration**: Query company data via HTTP API
- **Chat History & Session Management**: Track all conversations and outputs

## 🏗️ Architecture

### Core Components

```
┌─────────────────────────────────────────────────────┐
│         Orchestrator Agent (Port 9000)              │
│  Routes queries & plans multi-step executions       │
└────────────────┬────────────────────────────────────┘
                 │
        ┌────────┼────────┬──────────┬──────────┬──────────┐
        │        │        │          │          │          │
    🔬 (9001) 🧮 (9002) ✍️ (9003) 📄 (9004) 🛠️ (9005) 🗄️ (9006) 🌤️ (9007)
Research   Math    Writer   Summary  Tool     DB      Weather
Agent      Agent   Agent    Agent    Agent    Agent   Agent
```

### Agents

| Agent | Port | Description | Capabilities |
|-------|------|-------------|--------------|
| **Research Agent** 🔬 | 9001 | Answers factual questions | Q&A, Explanations, Research |
| **Math Agent** 🧮 | 9002 | Solves mathematical problems | Arithmetic, Statistics, Sequences |
| **Creative Writer Agent** ✍️ | 9003 | Creates content | Poetry, Stories, Emails, LinkedIn Posts |
| **Summary Agent** 📄 | 9004 | Condenses information | Text Summarization, Key Points |
| **Tool Agent** 🛠️ | 9005 | Executes tools | Metal Prices, In-Memory Storage |
| **DB Agent** 🗄️ | 9006 | Queries database | SQL Queries, Multi-Table Joins |
| **Weather Agent** 🌤️ | 9007 | Fetches live weather | Current Weather by City |

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- API Keys:
  - `GROQ_API_KEY` - For LangChain Groq integration
  - `OPENWEATHER_API_KEY` - For weather data

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/rajendradayma/A2A-Multi-Agent-system.git
   cd A2A-Multi-Agent-system
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Keys**
   - Edit `a2a_multi_agent.py` (lines 58-63) to add your API keys
   - Or set environment variables

4. **Run the system**
   ```bash
   python a2a_multi_agent.py
   ```

## 📚 Usage

### Single-Step Queries

The orchestrator routes simple queries to a single appropriate agent:

```
You → Orchestrator: "What is the capital of France?"
   ↓
   Orchestrator routes to Research Agent
   ↓
Research Agent: "The capital of France is Paris..."
```

**Examples:**
- `"What is the weather in London?"` → Weather Agent
- `"Calculate 10 + 20 + 30"` → Math Agent
- `"Write a poem about AI"` → Creative Writer Agent

### Multi-Step Queries

Complex queries are broken into steps with data chaining:

```
You: "Research quantum computing and summarize it"
   ↓
Step 1: Research Agent → Researches quantum computing
   ↓
Step 2: Summary Agent → Summarizes findings (using Step 1 output)
   ↓
Final Response: Summary of quantum computing
```

**Multi-Step Examples:**
- `"Find when moon landing happened, then write a LinkedIn post about it"` → Research → Writer
- `"Calculate Fibonacci(8), then write a poem inspired by that number"` → Math → Writer
- `"Get weather in Paris and write travel recommendations"` → Weather → Writer

### Interactive Mode

After demo queries complete, enter interactive mode:

```
You → Orchestrator (9000): What is gold price?
[Agent response]

You → Orchestrator (9000): history
[Shows last 5 conversations]

You → Orchestrator (9000): history stats
[Shows conversation statistics]

You → Orchestrator (9000): quit
[Exit program]
```

## 🛠️ Tools & Capabilities

### Metal Price Tool
```python
get_metal_price("gold")
# Returns: price per gram & per kg
# Supported: gold, silver, platinum, copper, aluminum, zinc
```

### In-Memory Storage
```python
save_data("Important note")
get_data()  # Retrieve all saved notes
```

### Database Queries
```
"List all employees"
"Who is on the AI Agents team?"
"Show active projects with employee names"
```

**Database Schema:**

**Employees Table:**
| id | name | role | team |
|----|------|------|------|
| 101 | Rajendra Dayma | Data Science Intern | AI Agents |
| 102 | Alice Smith | Senior Engineer | Backend |

**Projects Table:**
| id | title | assigned_to | status |
|----|-------|-------------|--------|
| A1 | Knowledge Graph Architecture | 101 | Active |

### Weather API
```
"What is the weather in Italy?"
# Automatically converts country to capital city (Italy → Rome)
```

## 📝 Chat History

All conversations are saved to `chat_history.json`. The system tracks:
- Query text
- Steps executed
- Agent responses
- Execution mode (single/multi)
- Timestamp and session ID

### History Commands

```
history                    # Show last 5 conversations
history 10                 # Show last 10 conversations
history show 5             # Show full details of entry #5
history stats              # Display statistics
history search "keyword"   # Search conversations
history export             # Export current session
```

## 🐳 Docker Deployment

Build and run using Docker:

```bash
docker build -t a2a-multi-agent .
docker run -p 9000:9000 a2a-multi-agent
```

## 🔧 Configuration

Edit the `Config` class in `a2a_multi_agent.py`:

```python
@dataclass(frozen=True)
class Config:
    GROQ_API_KEY: str = "your-key-here"
    GROQ_MODEL: str = "llama-3.1-8b-instant"
    DB_API_URL: str = "http://127.0.0.1:8998"
    ORCHESTRATOR_PORT: int = 9000
    # ... other settings
```

### Configurable Ports

- **Database API**: 8998
- **Orchestrator**: 9000
- **Agents**: 9001-9007

## 📊 System Components

### A2A Protocol Implementation
- Agent Card Discovery
- JSON-RPC 2.0 Communication
- Skill Registration
- Multi-step Task Planning

### LangChain Integration
- Groq LLM Model (`llama-3.1-8b-instant`)
- Tool Binding
- Message History
- Retry Logic for Failed Requests

### Infrastructure
- Starlette Web Framework
- Uvicorn ASGI Server
- SQLite Database
- HTTP-based API Communication

## 🎓 Example Workflows

### Workflow 1: Research & Summarize
```
Query: "Research artificial intelligence and give me a summary"
├─ Step 1: Research Agent researches AI
└─ Step 2: Summary Agent condenses findings
Result: Concise AI summary
```

### Workflow 2: Calculate & Create
```
Query: "Calculate the 10th Fibonacci number, then write a poem about it"
├─ Step 1: Math Agent computes Fibonacci(10)
└─ Step 2: Writer Agent creates poem using that number
Result: Poem inspired by Fibonacci sequence
```

### Workflow 3: Database + Analysis
```
Query: "Get all employees in AI Agents team"
├─ Step 1: DB Agent queries employees table
└─ Step 2: Summary Agent creates report
Result: Formatted employee information
```

## 🔐 Security Notes

- API keys are hardcoded in the demo (configure via environment variables for production)
- Only SELECT queries allowed on database
- All queries logged to chat history
- No authentication required for demo mode

## 📦 Dependencies

```
a2a-sdk==1.0.1          # A2A Protocol implementation
langchain-groq           # Groq LLM integration
langchain-core           # LangChain core components
uvicorn                  # ASGI server
starlette                # Web framework
httpx                    # Async HTTP client
psutil                   # Process utilities
streamlit>=1.35.0        # UI framework
python-dotenv>=1.0.0     # Environment variables
```

## 📄 File Structure

```
A2A-Multi-Agent-system/
├── a2a_multi_agent.py          # Main orchestration system
├── streamlit_app.py             # Streamlit UI
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Docker configuration
├── railway.toml                 # Railway deployment config
├── A2A_Multi_Agent.ipynb        # Jupyter notebook demo
└── README.md                    # This file
```

## 🌟 Key Features

✅ **Intelligent Routing** - Automatically selects best agent for each query  
✅ **Multi-Step Orchestration** - Chains agents for complex workflows  
✅ **Live Tools** - Metal prices, weather, database access  
✅ **Conversation Memory** - Persistent chat history with search  
✅ **Error Handling** - Graceful fallbacks and retry logic  
✅ **Interactive Mode** - Real-time query execution  
✅ **JSON-RPC Protocol** - Standard A2A inter-agent communication  
✅ **Modular Design** - Easy to add new agents and tools  

## 🚨 Troubleshooting

### Port Already in Use
```bash
# Ports will be automatically freed on startup, but you can manually kill them:
lsof -i :9000  # Find process using port 9000
kill -9 <PID>  # Kill the process
```

### API Key Issues
```
⚠️ Ensure your GROQ_API_KEY and OPENWEATHER_API_KEY are valid
Check the Config class in a2a_multi_agent.py (lines 58-63)
```

### Database Connection Failed
```
Check if port 8998 is free
Verify SQLite is installed: python -m sqlite3 --version
```

## 📧 Contact & Support

Created by: **Rajendra Dayma**  
Repository: [rajendradayma/A2A-Multi-Agent-system](https://github.com/rajendradayma/A2A-Multi-Agent-system)

## 📜 License

This project is provided as-is for demonstration and educational purposes.

## 🎉 Demo Queries

The system comes with 19 pre-configured demo queries that showcase:

- **Single-step** queries (Research, Math, Writer, Tool, DB, Weather)
- **Multi-step** queries (Research→Writer, Math→Writer, DB→Summary, Weather→Writer)

Run `python a2a_multi_agent.py` to see the full demo!

---

**Built with** 🤖 A2A Protocol | 🦙 Groq LLM | ⛓️ LangChain | 🚀 Python
