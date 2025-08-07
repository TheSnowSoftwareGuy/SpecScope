# SpecScope MVP

AI-powered specification intelligence for construction estimators.

## Quick Start

1. Install Claude Code CLI:
   ```bash
   npm install -g @claude/cli
   ```

2. Start Claude Code session:
   ```bash
   claude --enable-architect
   ```

3. Initial development prompt:
   ```
   Initialize the SpecScope project with the structure defined in CLAUDE.md.
   Start by implementing the PDF upload and text extraction pipeline,
   ensuring we preserve page numbers and section information for citations.
   ```

## Development Workflow

- Use `/compact` between major features
- Run `/analyze` to test specification search
- Commit frequently with descriptive messages
- Update CLAUDE.md with new insights

## Key Features

- Multi-PDF upload and processing
- Hybrid search (keyword + semantic)
- 100% citation accuracy
- Conflict detection
- Export to CSV/PDF

## Tech Stack

- Backend: FastAPI + Python
- Frontend: React + Tailwind
- AI: OpenAI GPT-4 + Pinecone
- PDF: PyMuPDF
