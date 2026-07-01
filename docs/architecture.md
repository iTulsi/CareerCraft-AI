# CareerCraft AI Architecture

CareerCraft AI uses a small, stateless web architecture.

## Request flow

```text
Browser frontend
      |
      v
FastAPI routes
      |
      +--> document parser
      +--> section parser
      +--> deterministic skill matcher
      +--> optional embedding matcher
      +--> evaluation comparison
      +--> interview-question generator
      +--> report generator
```

## Frontend

The frontend uses native HTML, CSS, and JavaScript. FastAPI serves the main
page and static assets, so the project does not require a separate frontend
build service.

## API layer

`backend/app/main.py` defines the application and coordinates resume parsing
and analysis. Pydantic response models keep the public API structure explicit.

## Document parsing

The parser accepts PDF, DOCX, and TXT documents. It validates the extension,
rejects empty and oversized uploads, extracts text, normalizes common document
artifacts, and reports malformed documents as validation errors.

## Analysis

The deterministic matcher identifies supported skills present in both the
resume and job description. Resume structure is evaluated separately. The
overall assessment combines explicit skill coverage and section coverage.

Optional semantic similarity is reported separately and is not silently mixed
into the deterministic score.

## Evaluation

The benchmark pipeline compares predicted scores with labelled examples and
reports error and correlation statistics. The included sample verifies the
pipeline but is not large enough to establish production accuracy.

## Data handling

The current application does not require a database. Requests are processed
by the API and returned to the caller without introducing a persistence layer.
