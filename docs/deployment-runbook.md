# Deployment Runbook

CareerCraft AI is deployed as one web service: FastAPI serves both the API and
the static frontend.

## Build command

```bash
pip install -r backend/requirements.txt
```

## Start command

```bash
cd backend && uvicorn app.main:app --host 0.0.0.0 --port "$PORT"
```

## Health check

Configure the platform health-check path as:

```text
/api/health
```

## Pre-deployment checks

```bash
make test
make verify
git diff --check
```

## Post-deployment checks

1. Open `/api/health` and confirm a successful JSON response.
2. Open `/docs` and confirm the OpenAPI interface loads.
3. Load the frontend and complete one deterministic analysis.
4. Download one report and confirm it is readable.
5. Review platform logs for startup or dependency errors.

The base deployment intentionally excludes the optional semantic-model package
to keep memory and startup requirements predictable.
