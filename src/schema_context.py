from __future__ import annotations

import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT_DIR / "data" / "schema_dictionary.json"


def load_schema_dictionary() -> dict:
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def render_schema_context() -> str:
    schema = load_schema_dictionary()
    lines: list[str] = []
    lines.append(f"SQL dialect: {schema['dialect']}")
    for table in schema["tables"]:
        lines.append(f"\nTable: {table['name']}")
        lines.append(f"Purpose: {table['description']}")
        lines.append("Columns:")
        for col in table["columns"]:
            lines.append(
                f"- {col['name']} ({col['type']}): {col['description']}"
            )
        if table.get("business_rules"):
            lines.append("Business rules:")
            for rule in table["business_rules"]:
                lines.append(f"- {rule}")
    return "\n".join(lines)
