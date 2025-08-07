# Project: SpecScope MVP - Construction Specification Intelligence System

## Mission
Build a production-ready MVP of SpecScope in 2 weeks - a specialized AI tool that helps construction estimators search and analyze project specifications with 100% citation accuracy. Unlike ChatGPT, every answer must include exact page references and source verification.

## Core Problem We're Solving
Construction estimators waste 4-8 hours per bid searching through 999+ page specifications. They've tried ChatGPT but can't trust it because:
1. It gives different answers each time
2. No citations or source verification
3. Misses critical requirements that could cost millions
4. Hallucinates information that doesn't exist

## Technical Requirements
- **Backend**: FastAPI with async Python
- **AI Pipeline**: OpenAI GPT-4 API with LangChain for RAG
- **Vector DB**: Pinecone for semantic search
- **Frontend**: React + Tailwind (minimal, functional UI)
- **PDF Processing**: PyMuPDF for robust extraction
- **Deployment**: Vercel (frontend) + Railway/Render (backend)

## MVP Features (Priority Order)
1. Multi-PDF upload and processing (specs, addenda, RFPs)
2. Hybrid search (keyword + semantic) with citations
3. Natural language Q&A with source highlighting
4. Conflict detection between documents
5. Export findings to CSV/PDF report

## Development Principles
- **Trust over Features**: Every answer must be verifiable
- **Speed over Perfection**: 2-week sprint to market
- **Construction-Specific**: Focus on patterns like "Division 01", "Addendum", "Alternate"
- **Show the Work**: Always display confidence scores and source text

## Success Metrics
- Process 1000+ page specification in under 30 seconds
- 100% citation accuracy (every claim linked to source)
- Save estimators 3+ hours per project
- Zero hallucinations or false information

## Architecture Decisions
- Use RAG (Retrieval Augmented Generation) to ensure accuracy
- Implement dual-index system: traditional search + vector embeddings
- Cache all processed documents to reduce costs
- Implement confidence scoring based on match quality

## File Structure Requirements
Keep the codebase modular and testable. Separate concerns clearly:
- API routes from business logic
- PDF processing from AI operations
- Search functionality from response generation

# CLAUDE.md - SpecScope Project Configuration

## Project Overview
SpecScope is a specification intelligence system for construction estimators. It uses AI to search and analyze construction documents with 100% citation accuracy.

## Core Principles
1. **Accuracy First**: Never generate information not explicitly in the documents
2. **Citations Required**: Every answer must link to exact page/section
3. **Conflict Detection**: Flag contradictions between documents
4. **Fast Processing**: Handle 1000+ page documents efficiently

## Technical Stack
- Python 3.11+ with FastAPI
- React 18 with Tailwind CSS
- OpenAI GPT-4 API for comprehension
- Pinecone for vector search
- PyMuPDF for PDF extraction

## Code Standards
- Use type hints for all Python functions
- Async/await for all I/O operations
- Comprehensive error handling with specific exceptions
- Test coverage minimum 80%
- Comments for complex business logic

## Construction Domain Knowledge
- Specifications follow CSI MasterFormat divisions
- Addenda supersede original specifications
- Look for patterns: "shall", "must", "required", "contractor responsible"
- Common searches: bonds, insurance, liquidated damages, submittals

## Testing Requirements
- Unit tests for all search functions
- Integration tests for PDF processing
- E2E tests for critical user flows
- Use sample construction specs for testing

## Git Workflow
- Commit after each completed feature
- Descriptive commit messages
- Branch naming: feature/[description]
- PR before merging to main

## Performance Targets
- PDF processing: < 10 seconds per 100 pages
- Search response: < 2 seconds
- 99% uptime
- Support 100 concurrent users

# Project Directory Structure

specscope/
├── .claude/
│   ├── commands/
│   │   ├── test.md          # Run all tests
│   │   ├── deploy.md        # Deploy to staging
│   │   └── analyze-spec.md  # Test spec analysis
│   └── settings.json
├── CLAUDE.md
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # FastAPI app entry
│   │   ├── config.py        # Environment config
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── document.py  # Document models
│   │   │   └── query.py     # Query/response models
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── routes/
│   │   │   │   ├── upload.py    # Document upload endpoints
│   │   │   │   ├── search.py    # Search endpoints
│   │   │   │   └── export.py    # Export endpoints
│   │   │   └── dependencies.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── pdf_processor.py  # PDF extraction
│   │   │   ├── text_chunker.py   # Document chunking
│   │   │   ├── embeddings.py     # Vector embeddings
│   │   │   └── search_engine.py  # Hybrid search
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── document_service.py
│   │   │   ├── search_service.py
│   │   │   ├── ai_service.py     # GPT-4 integration
│   │   │   └── citation_service.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── patterns.py       # Construction patterns
│   │       └── validators.py
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── test_pdf_processor.py
│   │   ├── test_search_engine.py
│   │   └── fixtures/
│   │       └── sample_spec.pdf
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── components/
│   │   │   ├── UploadZone.tsx
│   │   │   ├── SearchBar.tsx
│   │   │   ├── ResultsPanel.tsx
│   │   │   ├── SourceViewer.tsx
│   │   │   └── ExportButton.tsx
│   │   ├── hooks/
│   │   │   ├── useSearch.ts
│   │   │   └── useDocuments.ts
│   │   ├── services/
│   │   │   └── api.ts
│   │   └── types/
│   │       └── index.ts
│   ├── package.json
│   └── tailwind.config.js
├── scripts/
│   ├── setup.sh
│   ├── test_local.sh
│   └── deploy.sh
├── .env.example
├── docker-compose.yml
└── README.md