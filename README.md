# CareerCraft AI

CareerCraft AI is an explainable resume and job-description analysis platform built with FastAPI and a lightweight browser frontend.

It extracts resume text, evaluates skill alignment, identifies missing qualifications, checks resume structure, generates tailored interview questions, and exports a downloadable analysis report.

> CareerCraft provides decision-support signals. Its scores are not employer ATS scores, hiring probabilities, or guarantees of selection.

## Features

- Parse PDF, DOCX, and TXT resumes
- Validate file types, file size, and malformed documents
- Detect standard resume sections
- Measure explicit job-skill coverage
- Explain matched and missing skills
- Compare deterministic and optional semantic similarity scores
- Generate technical, learning-gap, and behavioural interview questions
- Download a plain-text analysis report
- Evaluate matching approaches against labelled benchmark data
- Serve the frontend and API from one FastAPI application
- Automated tests for parsing, scoring, reports, API behaviour, frontend delivery, and benchmarking

## Explainable scoring

The deterministic assessment combines:

- **75% skill coverage** — recognised skills shared by the resume and job description
- **25% resume structure** — presence of expected resume sections

Semantic similarity is shown separately when the optional embedding model is installed. It is not silently included in the overall score.

## Technology

- Python
- FastAPI
- Pydantic
- Uvicorn
- pdfplumber and pypdf
- python-docx
- Vanilla HTML, CSS, and JavaScript
- pytest
- Optional sentence-transformers embeddings

The frontend intentionally uses native browser features and does not require a JavaScript build pipeline.


## API endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/` | Serve the CareerCraft web application |
| `GET` | `/api/health` | Check service health and version |
| `POST` | `/api/resume/parse` | Extract and structure uploaded resume text |
| `POST` | `/api/analyze` | Generate the complete resume-to-job analysis |
| `POST` | `/api/report` | Download an analysis report |
| `GET` | `/docs` | Open the interactive API documentation |


## Run locally

Clone the repository:

    git clone https://github.com/iTulsi/CareerCraft-AI.git
    cd CareerCraft-AI

Create and activate the virtual environment:

    python3 -m venv .venv
    source .venv/bin/activate

Install dependencies:

    pip install -r backend/requirements.txt

Verify the complete project:

    make verify

Start the application:

    make run

Then open:

- Web application: `http://127.0.0.1:8000`
- API documentation: `http://127.0.0.1:8000/docs`
- Health endpoint: `http://127.0.0.1:8000/api/health`


## Benchmarking

CareerCraft includes a labelled sample dataset and a benchmark CLI for evaluating deterministic and optional semantic matching.

Run the benchmark:

    make benchmark

The report is written to:

    /tmp/careercraft-benchmark.json

The benchmark reports mean absolute error, Pearson correlation, Spearman correlation, and individual prediction results.

The included four-pair dataset verifies the evaluation pipeline. It is not large enough to claim production-level model accuracy. See `docs/dataset-design.md` for the dataset and annotation design.

## Deployment

The repository includes a Render Blueprint in `render.yaml`.

The deployment:

- Installs dependencies from `backend/requirements.txt`
- Starts Uvicorn using Render's assigned port
- Serves the frontend and API from one service
- Uses `/api/health` for health checks

The default deployment excludes the optional sentence-transformers model to keep memory and build requirements manageable.

## Current limitations

- Deterministic matching only recognises supported skill vocabulary.
- Semantic comparison requires optional machine-learning dependencies.
- The sample benchmark dataset should be expanded with independently reviewed labels.
- CareerCraft does not reproduce any employer's private ATS logic.
- Analysis results should support, not replace, human review.

## License

Released under the [MIT License](LICENSE).
