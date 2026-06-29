.PHONY: run test benchmark

run:
	cd backend && ../.venv/bin/python -m uvicorn app.main:app --reload --port 8000

test:
	cd backend && ../.venv/bin/python -m pytest -q

benchmark:
	cd backend && ../.venv/bin/python -m app.benchmark \
		--dataset ../data/benchmark_sample.csv \
		--output /tmp/careercraft-benchmark.json
