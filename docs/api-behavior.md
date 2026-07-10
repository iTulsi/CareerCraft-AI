# API Behavior Reference

CareerCraft AI exposes a small HTTP API through FastAPI.

## Health check

`GET /api/health` returns the service status and application version. Deployment
platforms can use this endpoint as a lightweight health check.

## Resume parsing

`POST /api/resume/parse` accepts PDF, DOCX, and TXT resumes. The service rejects
unsupported formats and files above the configured upload limit. Parsed text is
returned to the caller for review before analysis.

## Resume analysis

`POST /api/analyze` compares resume text with a job description. Deterministic
skill coverage is the default signal. Semantic comparison is optional and may
be unavailable when the extra machine-learning dependencies are not installed.

## Report generation

`POST /api/report` validates an analysis payload and returns a downloadable text
report. Generated reports should not be treated as official employer ATS output.

## Error responses

Invalid request bodies, unsupported documents, and malformed report payloads
return explicit client errors rather than silently producing partial results.
Use the interactive documentation at `/docs` for the current request schemas.
