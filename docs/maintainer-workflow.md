# Maintainer Workflow

This workflow keeps CareerCraft AI changes small, reviewable, and production-oriented.

## Before changing code

1. Reproduce the problem or confirm the requirement.
2. Read the current execution path before introducing new code.
3. Reuse existing modules, validation, and tests where possible.
4. Choose the smallest change that solves the verified problem.
5. Avoid new dependencies unless they clearly reduce complexity.

## During implementation

- Keep one concern per change.
- Preserve current public API behavior unless the change is intentional.
- Add or update tests for meaningful success and failure cases.
- Keep optional semantic-analysis paths separate from deterministic core behavior.
- Do not hide actionable errors behind broad exception handling.

## Before committing

Run the project verification command, review `git diff`, confirm only intended files changed, and use one focused commit message.

## Before release

Verify the health endpoint, API documentation, supported file parsing, analysis, reports, and any optional model-backed behavior enabled in production.
