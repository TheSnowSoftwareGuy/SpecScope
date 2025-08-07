SpecScope MVP

Overview
SpecScope is an AI-powered specification intelligence system for construction estimators. This MVP focuses on trust, deterministic results, and 100% citation accuracy.

Stack
- Backend: Python 3.11, FastAPI, PyMuPDF, SQLite FTS5, OpenAI embeddings, optional Pinecone
- Frontend: React 18 + Tailwind
- Deployment: Vercel (frontend), Railway/Render (backend)

Quick start
1) Setup
- cp .env.example .env
- bash scripts/setup.sh

2) Run backend
- uvicorn backend.app.main:app --reload

3) Run frontend
- cd frontend && npm install && npm run dev

4) Test
- bash scripts/test_local.sh

API
- POST /upload: multipart PDFs; processes and indexes
- GET /documents
- GET /documents/{id}/pages/{n}
- POST /search: hybrid search
- POST /qa: QA (conservative MVP; strict citations to be enhanced)
- POST /export: CSV stub

Testing
- Pytest unit tests included for PDF processor and hybrid search.
- More tests, E2E, and QA/citation validation arrive in subsequent chunks.

Notes
- Embeddings fallback: if OPENAI_API_KEY is not set, a deterministic local embedding is used for tests/dev.
- Vector index fallback: in-memory index for local/dev. Pinecone integration will be added in a later chunk with the same interface.

Security
- Basic file validation for PDFs; stores under data/storage.
- CORS restricted by ALLOWED_ORIGINS.
- Do not log document text.

Roadmap next chunks
- Strict AI RAG with LangChain, JSON output schema, and citation validation enforcement.
- Conflict detection and export PDF.
- Frontend source viewer with highlight rectangles.
- CI, coverage 80%+, and deployment scripts completion.
```

What’s implemented in this chunk
- Full backend scaffolding with config, logging, and SQLite FTS5.
- PDF extraction with PyMuPDF and simple section header heuristics.
- Deterministic chunking with stable hashes.
- Embeddings with OpenAI + offline deterministic fallback.
- In-memory vector index and SQLite keyword index.
- Hybrid search with deterministic fusion and confidence mapping.
- Upload, documents listing, page retrieval, search, and basic QA endpoints.
- Initial React UI with upload, search, and QA.
- Pytest unit tests for PDF extraction and hybrid search.
- Dockerfile and docker-compose for backend, setup/test scripts, and .env.

Next steps (upcoming chunks)
- Integrate Pinecone client as an optional vector backend; keep in-memory for dev/tests.
- Implement LangChain RAG chain with strict output schema and citation validation; add tests for refusal when insufficient evidence.
- Implement conflict detection pipeline and CSV/PDF exports.
- Build source viewer highlights based on citation char ranges.
- Add more backend tests (citation_service, ai_service behaviors) and frontend tests (RTL, E2E with Playwright/Cypress).
- Performance tuning and caching of processed files/chunks by hash.