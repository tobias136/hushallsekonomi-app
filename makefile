# Makefile för hushallsekonomi-app

# Variabler
PYTHON=python3

# Kommandon
reset:
	$(PYTHON) scripts/reset_test_data.py

test:
	pytest tests/

run-import:
	$(PYTHON) app/CLI/main.py importera csv/test_bank.csv

format:
	black app/ scripts/ tests/

lint:
	ruff app/ scripts/ tests/

.PHONY: reset test run-import format lint
