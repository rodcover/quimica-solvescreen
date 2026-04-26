from __future__ import annotations

import json
from pathlib import Path

import jsonschema
import pytest

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "confinement_dataset.schema.json"


@pytest.fixture(scope="module")
def schema():
    return json.loads(SCHEMA.read_text(encoding="utf-8"))


@pytest.mark.parametrize(
    "name",
    ["confinement_sample.json", "confinement_literature.json"],
)
def test_confinement_examples_validate(schema: dict, name: str):
    path = ROOT / "examples" / name
    instance = json.loads(path.read_text(encoding="utf-8"))
    jsonschema.validate(instance=instance, schema=schema)
