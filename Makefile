run-api:
	cd apps/api && uvicorn app.main:app --reload --port 8000

run-web:
	cd apps/web && npm run dev

test-api:
	cd apps/api && pytest

smoke:
	python scripts/smoke_test.py