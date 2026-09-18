import json
from pathlib import Path

from jsonschema import validate

from app.models import WTMOutput


def test_wtm_output_matches_json_schema():
    schema_path = (
        Path(__file__).resolve().parents[1]
        / "schemas"
        / "wtm.output.json"
    )

    with schema_path.open("r", encoding="utf-8") as file:
        schema = json.load(file)

    output = WTMOutput(
        business="Empresa de prueba",
    )

    validate(
        instance=output.model_dump(mode="json"),
        schema=schema,
    )