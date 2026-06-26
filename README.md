# CareerCraft AI

CareerCraft AI is an explainable GenAI resume and job-description analysis platform.

## Current milestone

The first backend slice provides:

- FastAPI application structure
- Health endpoint
- Resume parsing endpoint: `POST /api/resume/parse`
- PDF, DOCX and TXT resume upload with text extraction
- Basic structured resume-section detection
- Deterministic resume-to-job skill matching baseline
- Explainable matched and missing skill output
- Automated tests

## Run locally

```bash
source .venv/bin/activate
make test
make run
```

Open:

- API documentation: `http://127.0.0.1:8000/docs`
- Health endpoint: `http://127.0.0.1:8000/api/health`

## Planned architecture

The production version will add structured resume parsing, section-aware evaluation,
embedding-based semantic matching, RAG evidence retrieval, configurable LLM adapters,
interview question generation, report export, evaluation datasets and a React frontend.
