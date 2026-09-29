# LLM Inference Orchestrator

An asynchronous, production-grade control plane and token-streaming gateway for large language models (LLMs). Built with Python, FastAPI, Async SQLAlchemy 2.0, and SQLite/PostgreSQL.

## Key Architectural Features

- **Real-Time Token Streaming:** Emits LLM token outputs using Server-Sent Events (SSE).
- **Asynchronous Data Persistence:** Tracks task lifecycles (`PENDING`, `PROCESSING`, `COMPLETED`, `FAILED`), prompts, completion timestamps, and latency using SQLAlchemy 2.0 and `aiosqlite`.
- **Decoupled Architecture:** Seamlessly routes requests to local GPU-accelerated inference engines (Ollama / vLLM / SGLang).
- **Containerized Deployment:** Fully packaged with Docker and Docker Compose for reproducible local and cloud environments.

---

## Directory Structure

```text
llm-inference-orchestrator/
├── src/
│   ├── database.py      # Async DB connection pools & session management
│   ├── models.py        # SQLAlchemy 2.0 ORM data models
│   ├── schemas.py       # Pydantic request/response data contracts
│   ├── services.py      # Core LLM streaming & async execution logic
│   ├── router.py        # REST API endpoints & SSE controllers
│   └── main.py          # FastAPI application entrypoint & lifespan context
├── .dockerignore        # Excludes virtual environments and build artifacts
├── .gitignore           # Ignores database files, caches, and secrets
├── Dockerfile           # Multi-stage container build setup
├── docker-compose.yml   # Multi-service local orchestrator configuration
├── requirements.txt     # Python dependency lockfile
└── README.md

```

---

## Getting Started

### Prerequisites

* **Python 3.11+**
* **Docker Desktop**
* **Ollama** installed and running locally (`ollama serve`) with a pulled model (e.g., `ollama pull llama3`)

---

### 1. Local Python Setup

```powershell
# Clone the repository
git clone [https://github.com/your-username/llm-inference-orchestrator.git](https://github.com/your-username/llm-inference-orchestrator.git)
cd llm-inference-orchestrator

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1   # On Windows PowerShell
# source venv/bin/activate    # On Linux/macOS

# Install dependencies
pip install -r requirements.txt

# Start the FastAPI server locally
uvicorn src.main:app --reload

```

---

### 2. Docker Setup (Recommended)

Run the entire orchestrator inside a containerized environment connected to your local host GPU/Ollama instance:

```powershell
# Build and launch the containerized orchestrator
docker compose up --build

```

---

## API Usage & Verification

Once running, interactive OpenAPI documentation is available at `http://127.0.0.1:8000/docs`.

### 1. Stream LLM Tokens in Real-Time (SSE)

```bash
curl -N -X POST "[http://127.0.0.1:8000/api/v1/chat/stream](http://127.0.0.1:8000/api/v1/chat/stream)" \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Explain GPU key-value caching in two sentences."}'

```

### 2. Query Task Execution Status & Metrics

```bash
curl "[http://127.0.0.1:8000/api/v1/tasks/](http://127.0.0.1:8000/api/v1/tasks/)<YOUR_TASK_ID>"

```

**Example Response:**

```json
{
  "task_id": "f42cf85d-6ac2-471c-b154-6b7852b53e81",
  "prompt": "Explain GPU key-value caching in two sentences.",
  "status": "COMPLETED",
  "created_at": "2026-09-29T12:00:00Z",
  "completed_at": "2026-09-29T12:00:03Z",
  "duration_seconds": 2.82
}

```