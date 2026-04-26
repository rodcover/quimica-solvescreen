FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libxrender1 libxext6 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/solvscreen ./src/solvscreen
COPY api ./api
COPY scripts ./scripts
COPY data/fixtures ./data/fixtures

ENV PYTHONPATH=/app/src
RUN mkdir -p models data/processed \
    && python scripts/run_etl.py data/fixtures/sample_mnsol_like.tsv -o data/processed/built.parquet \
    && python scripts/run_train.py data/processed/built.parquet -o models/baseline.joblib

ENV SOLVSCREEN_MODEL_PATH=/app/models/baseline.joblib

EXPOSE 8000
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
