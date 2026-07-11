# Observability Guide

CareerCraft AI should provide enough operational information to diagnose failures without exposing resume contents or other sensitive data.

## Logging principles

Record:

- request identifier;
- endpoint or operation name;
- response status;
- processing duration;
- safe error category; and
- external dependency status when relevant.

Do not record:

- complete resumes;
- full job descriptions;
- generated reports;
- access tokens;
- API keys;
- raw authorization headers; or
- model-provider credentials.

## Health monitoring

The health endpoint should confirm that the application process can serve requests. Optional model availability should be reported separately so a missing semantic model does not make the deterministic service appear unavailable.

## Useful metrics

Track, when the hosting platform supports them:

- request count;
- error rate;
- response latency;
- parsing failures by document type;
- report-generation failures;
- optional model failures; and
- deployment restarts.

## Diagnosing incidents

Start with the affected endpoint, deployment commit, request identifier, and safe error category. Reproduce with synthetic data before requesting user documents.

## Retention

Keep operational logs only as long as needed for reliability and security analysis. Apply stricter handling to any log that could contain personal information.
