.PHONY: run test

run:
	cd backend && ../.venv/bin/python -m uvicorn app.main:app --reload --port 8000

test:
	cd backend && ../.venv/bin/python -m pytest -q
