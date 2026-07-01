# Contributing to CareerCraft AI

Thank you for helping improve CareerCraft AI.

## Local setup

```bash
git clone https://github.com/iTulsi/CareerCraft-AI.git
cd CareerCraft-AI

python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r backend/requirements.txt
```

## Development workflow

1. Create a focused branch from the latest `main`.
2. Keep each change limited to one problem.
3. Add or update tests for behavioural changes.
4. Run the complete verification commands.
5. Review the diff before opening a pull request.

```bash
python -m compileall -q backend/app
python -m pytest -q
git diff --check
```

## Pull requests

A pull request should explain:

- the problem being solved,
- why the change is necessary,
- which files changed,
- how the change was tested,
- any limitations or follow-up work.

Avoid unrelated formatting changes, generated files, committed virtual
environments, secrets, personal resume data, or unsupported accuracy claims.

## Commit messages

Use focused, descriptive commit messages such as:

```text
feat: add document validation
fix: handle unreadable PDF uploads
test: cover empty resume input
docs: explain benchmark limitations
```
