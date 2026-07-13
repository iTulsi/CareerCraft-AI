# Privacy Threat Model

CareerCraft processes resumes and job descriptions, which may contain names,
contact details, employment history, education details, and other personal
information.

## Data flow

1. A user uploads a resume to the FastAPI service.
2. The service validates and extracts text in memory for the active request.
3. A user submits resume text and a job description for analysis.
4. The service returns scores, gaps, recommendations, and interview questions.
5. A report may be generated and returned as a download.
6. The application does not intentionally persist request content in an
   application-managed database.

## Main threats and controls

| Threat | Control |
|---|---|
| Sensitive text appears in logs | Log request metadata and error categories, not document bodies. |
| Oversized upload causes resource pressure | Enforce the documented upload limit before expensive parsing. |
| Malformed document crashes the service | Catch parser-specific failures and return structured errors. |
| Report response is cached | Keep `Cache-Control: no-store`. |
| Original filename becomes a filesystem path | Treat filenames as display metadata only. |
| Optional model sends data externally | Keep external processing disabled unless explicitly designed and disclosed. |
| Error response leaks internals | Return safe client errors and keep tracebacks server-side. |
| Public deployment is mistaken for private storage | Clearly state the request-scoped processing model and limitations. |

## Review checklist

- No resume or job-description body is logged.
- No temporary file survives beyond the request unless explicitly required.
- New analytics avoid collecting document content.
- Third-party services are documented before receiving user data.
- Dependency updates are reviewed for parser and upload-related advisories.
- Tests cover malformed files, oversized files, and report cache headers.
