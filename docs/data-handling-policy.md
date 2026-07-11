# Data Handling Policy

CareerCraft AI processes resumes and job descriptions that may contain personal or confidential information.

## Collection

Process only the data needed to provide parsing, analysis, reporting, and interview-practice features.

## Storage

Avoid persistent storage unless a feature explicitly requires it. Temporary files should be scoped to one request and removed after processing.

## Logging

Do not log full resumes, job descriptions, generated reports, access tokens, or model credentials. Logs should contain operational metadata only when needed for diagnosis.

## Transmission

Production traffic must use HTTPS. External model or API integrations should receive only the minimum content required for the selected feature.

## User control

Validation errors should explain what must be corrected without exposing internal paths or stack traces.

## Development data

Use synthetic or intentionally anonymized fixtures in tests and examples. Never commit real applicant documents to the repository.

## Incident response

If sensitive information is exposed, stop further disclosure, rotate affected credentials, remove retained copies, document the scope, and publish a focused remediation change.
