# Security Policy

## Reporting a vulnerability

Please do not disclose suspected vulnerabilities in a public issue.

Report security problems through GitHub's private security-advisory feature.
Include:

- the affected endpoint or component,
- steps to reproduce the problem,
- the expected and actual behaviour,
- the potential impact,
- a suggested remediation when available.

Do not include real resumes, access tokens, private keys, passwords, or other
personal information in a report.

## Supported version

Security fixes are applied to the latest version of the `main` branch.

## Scope

Relevant reports include:

- unsafe document-upload handling,
- denial-of-service risks,
- path traversal,
- accidental information disclosure,
- dependency vulnerabilities,
- injection flaws,
- exposed secrets or credentials.

CareerCraft AI is a decision-support project. Scoring disagreements without a
security impact should be reported as normal product issues.
