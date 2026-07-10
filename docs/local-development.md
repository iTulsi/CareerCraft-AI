# Local Development Guide

This guide covers the smallest reliable workflow for running CareerCraft AI locally.

## Prerequisites

- Python 3.10 or newer
- Git
- A POSIX-compatible shell

## Setup

```bash
git clone https://github.com/iTulsi/CareerCraft-AI.git
cd CareerCraft-AI
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r backend/requirements.txt
```

## Run the application

```bash
make run
```

The application is available at `http://127.0.0.1:8000`, and the interactive
API documentation is available at `http://127.0.0.1:8000/docs`.

## Validate a change

```bash
make test
make verify
git diff --check
```

Run these commands before committing. Optional semantic matching requires the
additional dependencies in `backend/requirements-ml.txt`.
