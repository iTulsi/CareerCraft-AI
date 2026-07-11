# Incident Response Runbook

This runbook defines the minimum response for production failures or suspected data exposure.

## 1. Assess

Identify:

- affected feature or endpoint;
- first observed time;
- deployed commit;
- user impact;
- whether personal data or credentials may be involved; and
- whether the issue is ongoing.

## 2. Contain

Use the smallest effective action:

- disable an optional integration;
- roll back to the last known-good commit;
- revoke or rotate exposed credentials;
- restrict access to an affected endpoint; or
- pause deployment traffic when core safety is uncertain.

## 3. Investigate

Use request identifiers, safe logs, deployment events, and synthetic reproductions. Do not copy real resumes into issues or public discussions.

## 4. Recover

Deploy a focused fix with regression coverage. Verify health, parsing, deterministic analysis, reports, and affected optional features.

## 5. Document

Record:

- timeline;
- root cause;
- affected versions;
- containment action;
- remediation commit;
- verification results; and
- preventive follow-up.

## Security incidents

When personal data or credentials may have been exposed, prioritize containment and credential rotation before routine debugging. Preserve necessary evidence without increasing disclosure.
