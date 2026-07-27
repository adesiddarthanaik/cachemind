# 🚀 CacheMind

> **Production-grade Semantic Caching Middleware for Large Language Models**

CacheMind is a high-performance semantic caching layer that sits between your application and any Large Language Model (LLM). Instead of sending every request to an LLM provider, CacheMind intelligently detects semantically similar prompts using vector embeddings and serves cached responses whenever possible.

This significantly reduces:

- ⚡ Response latency
- 💰 LLM API costs
- 📈 Infrastructure load

while remaining completely transparent to client applications.

---

## ✨ Features

- 🔍 Semantic similarity search using FAISS
- 🧠 Embedding-based intelligent cache lookup
- ⚡ Redis-backed response caching
- 🤖 Multi-provider architecture (OpenRouter, Ollama)
- 🌊 Streaming response support
- 🔐 API Key Authentication
- 🚦 Sliding Window Rate Limiting
- 🆔 Request ID Middleware
- 📊 Prometheus Metrics
- 📝 Structured Logging
- ✅ GitHub Actions CI/CD
- 🧪 Automated Testing with Pytest

---

## 🏗️ Tech Stack

| Layer | Technology |
|--------|------------|
| API Framework | FastAPI |
| Cache | Redis |
| Vector Search | FAISS |
| Embeddings | Sentence Transformers |
| LLM Providers | OpenRouter, Ollama |
| Monitoring | Prometheus |
| Testing | Pytest |
| CI/CD | GitHub Actions |
| Language | Python 3.12 |

---

## ❓ Why CacheMind?

Modern AI applications often send the same or semantically similar prompts to Large Language Models (LLMs) multiple times.

For example:

```
"What is semantic caching?"

"Explain semantic caching."

"Can you describe semantic caching?"
```

Although these prompts have different wording, they request the same information.

Traditional caching systems only detect **exact string matches**, causing every variation to be forwarded to the LLM provider, resulting in:

- Increased API costs
- Higher response latency
- Unnecessary GPU utilization
- Reduced application throughput

CacheMind solves this problem by using **vector embeddings** and **semantic similarity search**.

Instead of comparing text directly, CacheMind compares the **meaning** of prompts.

If a new prompt is semantically similar to a previously answered prompt, CacheMind instantly returns the cached response without contacting the LLM provider.

This enables AI applications to become faster, more cost-efficient, and significantly more scalable.

---

## 🧠 How It Works

```text
                User Request
                      │
                      ▼
             Generate Embedding
                      │
                      ▼
            Search Similar Vectors
                  (FAISS)
             ┌────────┴────────┐
             │                 │
      Cache Hit           Cache Miss
             │                 │
             ▼                 ▼
     Return Cached      Query LLM Provider
        Response               │
                               ▼
                    Store Response in Cache
                               │
                               ▼
                         Return Response
```

The entire caching process is transparent to client applications.
Applications continue sending requests normally while CacheMind automatically optimizes latency and cost behind the scenes.

---

## 🏛️ System Architecture

CacheMind follows a modular middleware architecture that separates concerns such as authentication, caching, embeddings, provider communication, and observability.

```text
                               Client
                                  │
                                  ▼
                      FastAPI REST API
                                  │
          ┌───────────────────────┴───────────────────────┐
          ▼                                               ▼
 Authentication                                 Rate Limiting
          │                                               │
          └───────────────────────┬───────────────────────┘
                                  ▼
                        Request ID Middleware
                                  │
                                  ▼
                           ChatService
                                  │
          ┌───────────────┬───────────────┬───────────────┐
          ▼               ▼               ▼
     Embeddings      Semantic Cache     Provider Factory
          │               │               │
          ▼               ▼               ▼
SentenceTransformer     Redis       OpenRouter / Ollama
          │
          ▼
        FAISS
                                  │
                                  ▼
                       Metrics & Observability
          ┌───────────────────────┴────────────────────────┐
          ▼                                                ▼
  Structured Logging                              Prometheus
```

---

## 📦 Core Components

### FastAPI

Provides REST APIs for interacting with CacheMind.

---

### Authentication Layer

Validates API keys before processing requests.

---

### Rate Limiter

Protects the API using a sliding-window rate limiting strategy.

---

### Request ID Middleware

Assigns a unique request identifier to every incoming request for tracing and debugging.

---

### ChatService

The central orchestration layer responsible for:

- Semantic cache lookup
- Provider routing
- Streaming responses
- Cache insertion
- Metrics collection

---

### Embedding Service

Generates vector embeddings for prompts using Sentence Transformers.

---

### FAISS Vector Store

Performs semantic similarity search using cosine similarity.

---

### Redis Cache

Stores cached responses and metadata for fast retrieval.

---

### Provider Layer

Supports multiple LLM providers through a common abstraction.

Current providers include:

- OpenRouter
- Ollama

Additional providers can be added without changing the API layer.

---

### Observability

CacheMind exposes operational metrics through Prometheus, including:

- Request count
- Cache hits
- Cache misses
- Provider requests
- Request latency
- Provider latency

Structured logs include request IDs to simplify debugging and traceability.

---

## 📂 Project Structure

```text
CacheMind/
│
├── app/
│   ├── auth/                  # API key authentication
│   ├── middleware/            # Request ID middleware
│   ├── metrics/               # Prometheus metrics
│   ├── providers/             # LLM provider implementations
│   ├── rate_limit/            # Sliding window rate limiter
│   ├── services/              # Core business logic
│   ├── utils/                 # Utility helpers
│   ├── exception_handlers.py  # Global exception handling
│   ├── exceptions.py          # Custom exception classes
│   ├── logger.py              # Structured logging
│   ├── config.py              # Configuration management
│   └── main.py                # FastAPI application entry point
│
├── data/
│   ├── faiss.index            # FAISS vector index
│   └── faiss_mapping.json     # Vector ID mapping
│
├── tests/                     # Automated test suite
│
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions CI pipeline
│
├── requirements.txt
├── pytest.ini
├── README.md
└── .gitignore
```

---

## 📁 Directory Overview

| Directory | Purpose |
|------------|---------|
| `app/auth` | Authentication and API key validation |
| `app/middleware` | Request lifecycle middleware |
| `app/providers` | Integrations with different LLM providers |
| `app/services` | Core application logic and orchestration |
| `app/rate_limit` | Request throttling and abuse prevention |
| `app/metrics` | Prometheus metrics definitions |
| `data` | Persistent semantic cache index and metadata |
| `tests` | Unit and integration tests |
| `.github/workflows` | Continuous Integration (CI) pipelines |

---

## 🚀 Quick Start

### 1️⃣ Clone the Repository

git clone https://github.com/adesiddarthanaik/cachemind.git

cd cachemind

---

### 2️⃣ Create a Virtual Environment

**Windows (PowerShell)**

```powershell
python -m venv venv

.\venv\Scripts\Activate
```

**Linux / macOS**

```bash
python3 -m venv venv

source venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Configure Environment Variables

Create a `.env` file in the project root.

Example:

```env
CACHEMIND_API_KEY=your-secret-api-key

REDIS_HOST=localhost
REDIS_PORT=6379

OPENROUTER_API_KEY=your-openrouter-api-key

EMBEDDING_MODEL=all-MiniLM-L6-v2

SIMILARITY_THRESHOLD=0.95
```

---

### 5️⃣ Start Redis

Make sure a Redis server is running locally.

Default:

```
localhost:6379
```

---

### 6️⃣ Start CacheMind

```powershell
uvicorn app.main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

---

### 7️⃣ Verify Installation

**Health Endpoint**

```
GET /health
```

**Expected Response**

```json
{
    "status": "healthy"
}
```

**Swagger UI**

```
http://127.0.0.1:8000/docs
```

**Prometheus Metrics**

```
http://127.0.0.1:8000/metrics
```

---

## 📡 API Reference

CacheMind exposes a simple REST API compatible with chat-based LLM workflows.

---

### Health Check

**Request**

```http
GET /health
```

**Response**

```json
{
  "status": "healthy"
}
```

---

### Chat Completions

Generate a response through CacheMind's semantic caching layer.

**Request**

```http
POST /v1/chat/completions
```

**Headers**

```http
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

**Request Body**

```json
{
  "provider": "openrouter",
  "model": "openai/gpt-4o-mini",
  "messages": [
    {
      "role": "user",
      "content": "Explain semantic caching."
    }
  ],
  "temperature": 0.7,
  "stream": false
}
```

---

### Cache Hit Response

```json
{
  "response": "...",
  "source": "semantic-cache"
}
```

---

### Provider Response

```json
{
  "response": "...",
  "source": "provider"
}
```

---

### Streaming Responses

Enable streaming by setting:

```json
{
  "stream": true
}
```

CacheMind forwards provider streaming responses while still collecting metrics and applying middleware.

---

### Metrics

Prometheus metrics endpoint:

```http
GET /metrics
```

Example metrics include:

- Total requests
- Cache hits
- Cache misses
- Provider requests
- Request latency
- Provider latency

---
## 📊 Performance

The following benchmark illustrates the expected improvements when semantic cache hits occur.

> **Note:** These numbers are illustrative placeholders. Real benchmark results will be added after deployment.

| Metric | Without Cache | Cache Hit |
|---------|--------------:|----------:|
| Response Time | ~2.1 s | ~45 ms |
| Provider API Calls | 1 | 0 |
| Redis Lookup | — | <5 ms |
| FAISS Similarity Search | — | <10 ms |
| Overall Latency | High | Very Low |

### Benefits

- ⚡ Faster responses for repeated and semantically similar prompts
- 💰 Lower LLM API costs
- 📈 Higher throughput
- 🚀 Better user experience
- 🔄 Transparent optimization with no client-side changes

---

## 🛣️ Roadmap

### ✅ Completed

- Semantic caching with FAISS
- Redis response cache
- Multi-provider architecture
- OpenRouter integration
- Ollama integration
- Streaming responses
- API Key authentication
- Sliding-window rate limiting
- Request ID middleware
- Structured logging
- Prometheus metrics
- GitHub Actions CI
- Automated testing

### 🚧 In Progress

- Docker support
- Production deployment
- Benchmark suite

### 🔮 Planned

- PostgreSQL metadata storage
- Admin dashboard
- Cache analytics UI
- Grafana integration
- Kubernetes deployment
- Multi-node cache synchronization
- Distributed FAISS support
- Provider auto-failover

---

## 🤝 Contributing

Contributions are welcome!

If you'd like to improve CacheMind:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a Pull Request

Please ensure:

- Code is formatted with **Black**
- Linting passes with **Ruff**
- All tests pass before submitting

---

## 📄 License

This project is licensed under the **MIT License**.

See the `LICENSE` file for more information.

---

## ⭐ Support

If you found CacheMind useful:

- ⭐ Star the repository
- 🐛 Report bugs through GitHub Issues
- 💡 Suggest new features
- 🤝 Contribute improvements

---

Built with ❤️ to make AI applications faster, smarter, and more cost-efficient.