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
├── Dockerfile           # Multi-stage container build setup
├── docker-compose.yml   # Multi-service local orchestrator configuration
├── requirements.txt     # Python dependency lockfile
└── README.md