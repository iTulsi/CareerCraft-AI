# Deployment Verification Runbook

CareerCraft is deployed as one Render web service.

## Expected configuration

```text
Build: pip install -r backend/requirements.txt
Start: cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
Health path: /api/health
```

## Pre-deployment

1. Start from a clean branch based on current `main`.
2. Run the complete test suite.
3. Run syntax compilation and the deterministic benchmark.
4. Review the final diff for generated files, secrets, and accidental data.
5. Confirm base requirements do not include the optional semantic model unless
   the target infrastructure is sized for it.
6. Confirm no environment-specific URL or secret is committed.

## Post-deployment smoke test

Verify:

- `/api/health` returns a successful JSON response,
- `/` loads the static frontend,
- `/docs` loads the OpenAPI interface,
- a small TXT resume can be parsed,
- deterministic analysis returns matched and missing skills,
- an invalid upload receives a structured client error,
- report generation returns a downloadable response with `no-store`,
- logs do not contain submitted resume or job-description text.

## Rollback trigger

Rollback when the health route fails, core endpoints return repeatable server
errors, parsing behavior regresses, report headers expose cacheable personal
data, or the release cannot be explained by the reviewed diff.
