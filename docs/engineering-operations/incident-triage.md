# Incident Triage Runbook

Use this sequence when the deployed application is unhealthy or a core workflow
has regressed.

## 1. Establish impact

Record:

- first known failure time,
- affected route or user workflow,
- whether all requests or one file type is affected,
- the deployed commit,
- a safe error identifier without resume content.

## 2. Check the smallest reliable signals

1. Request `/api/health`.
2. Inspect deployment status and startup logs.
3. Confirm the configured start command and Python dependency installation.
4. Reproduce with synthetic, non-personal input.
5. Compare the deployed commit with the last known good release.

## 3. Common symptom map

| Symptom | First checks |
|---|---|
| Health route unavailable | Process startup, port binding, dependency install, platform status. |
| Frontend loads but API fails | Browser network response, API logs, route validation. |
| One document type fails | Parser dependency, malformed fixture, MIME and extension validation. |
| Semantic option fails | Optional dependency availability and graceful fallback. |
| Report download fails | Payload validation, response headers, report serialization. |
| Scores changed unexpectedly | Scoring diff, skill vocabulary, normalization, benchmark output. |

## 4. Contain and recover

- Prefer rollback to a known good commit over editing production manually.
- Disable only the optional failing path when the deterministic core remains
  healthy and the behavior is explicit.
- Never copy real resume text into an issue, chat, or public log.
- Add a regression test before applying the permanent fix.

## 5. Closeout

Document the root cause, user impact, detection gap, fix, regression test, and
one concrete prevention action.
