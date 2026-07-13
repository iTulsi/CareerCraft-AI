# API Contract Invariants

CareerCraft's API should remain predictable for the static frontend, external
API consumers, automated tests, and deployment health checks.

## Stable routes

| Method | Route | Contract |
|---|---|---|
| `GET` | `/` | Serves the application frontend. |
| `GET` | `/api/health` | Returns a small JSON health response without external model work. |
| `POST` | `/api/resume/parse` | Accepts a supported resume upload and returns normalized text and detected sections. |
| `POST` | `/api/analyze` | Accepts resume text and a job description and returns explainable matching results. |
| `POST` | `/api/report` | Validates an analysis payload and returns a downloadable text report. |
| `GET` | `/docs` | Serves FastAPI's generated API documentation. |

## Compatibility rules

1. Existing response fields should not be removed or silently renamed.
2. New response fields should be additive unless a versioned migration is
   intentionally introduced.
3. Validation failures should use FastAPI and Pydantic's structured error
   responses rather than custom plain-text errors.
4. File type and size failures should be explicit and testable.
5. The health route must not depend on optional semantic-model availability.
6. Report downloads must keep download-safe headers and `Cache-Control:
   no-store`.
7. Resume content and job descriptions must not be written to application logs.

## Review questions

Before changing an endpoint, verify:

- Does the current frontend depend on this field or status code?
- Is the change covered by both a success case and a failure case?
- Does the OpenAPI schema accurately describe the new behavior?
- Could the change expose resume content or other personal data?
- Can an older client continue to use the endpoint?
