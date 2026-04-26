# SolvScreen — alvos úteis (requer GNU Make: Git Bash, WSL, ou `choco install make`)
PYTHON ?= python
export PYTHONPATH := src

.PHONY: install install-dev etl-fixture train train-rf test api ui openapi schema examples clean

install:
	$(PYTHON) -m pip install -r requirements.txt

install-dev:
	$(PYTHON) -m pip install -r requirements.txt -r requirements-dev.txt
	pre-commit install

etl-fixture:
	$(PYTHON) scripts/run_etl.py data/fixtures/sample_mnsol_like.tsv -o data/processed/demo.parquet

train: etl-fixture
	$(PYTHON) scripts/run_train.py data/processed/demo.parquet -o models/baseline.joblib --metrics models/metrics.json

train-rf: etl-fixture
	$(PYTHON) scripts/run_train.py data/processed/demo.parquet -o models/baseline_rf.joblib --model-type rf --metrics models/metrics_rf.json

test:
	pytest tests/ -q

api:
	SOLVSCREEN_MODEL_PATH=models/baseline.joblib $(PYTHON) -m uvicorn api.main:app --reload --host 127.0.0.1 --port 8000

ui:
	$(PYTHON) scripts/run_streamlit.py

openapi:
	$(PYTHON) scripts/export_openapi.py

schema:
	$(PYTHON) -c "import json, jsonschema; from pathlib import Path; s=json.load(open('schemas/confinement_dataset.schema.json')); [jsonschema.validate(json.load(open(p)), s) for p in Path('examples').glob('confinement*.json')]"

benchmark:
	$(PYTHON) scripts/benchmark_literature.py models/metrics.json

examples: etl-fixture train benchmark

clean:
	$(RM) -rf data/processed/*.parquet models/*.joblib models/*.json docs/openapi.json __pycache__ .pytest_cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
