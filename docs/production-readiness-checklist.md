# Production Readiness Checklist

## Application

- Core analysis works without optional ML dependencies.
- Supported PDF and DOCX inputs are validated.
- Empty, malformed, encrypted, and oversized inputs fail safely.
- API contracts match the generated OpenAPI schema.
- Reports and interview questions are generated from validated analysis results.

## Security

- Secrets are stored outside the repository.
- Production CORS is restricted.
- Request sizes are bounded.
- Sensitive document contents are excluded from logs.
- Temporary files are removed.
- Dependencies are reviewed and intentionally constrained.

## Reliability

- Tests pass from a clean checkout.
- The health endpoint reports service availability.
- Optional external integrations degrade without breaking core features.
- Deployment and rollback steps are documented.
- A known-good rollback commit is identified.

## Operations

- Production start commands are documented.
- Hosting configuration matches the supported Python version.
- Smoke checks cover frontend, API docs, parsing, analysis, and reports.
- Error logs provide actionable context without exposing user data.
- The deployed commit SHA is recorded after every release.
