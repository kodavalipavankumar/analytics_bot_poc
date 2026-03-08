from __future__ import annotations

import re
from dataclasses import dataclass


FORBIDDEN_PATTERNS = [
    r"\bINSERT\b",
    r"\bUPDATE\b",
    r"\bDELETE\b",
    r"\bDROP\b",
    r"\bALTER\b",
    r"\bTRUNCATE\b",
    r"\bCREATE\b",
    r"\bATTACH\b",
    r"\bPRAGMA\b",
    r";",
    r"\bUNION\b",
]

ALLOWED_TABLES = {"sales"}


@dataclass
class ValidationResult:
    is_valid: bool
    message: str



def extract_tables(sql: str) -> set[str]:
    matches = re.findall(r"(?:FROM|JOIN)\s+([a-zA-Z_][a-zA-Z0-9_]*)", sql, flags=re.IGNORECASE)
    return {m.lower() for m in matches}



def validate_sql(sql: str) -> ValidationResult:
    stripped = sql.strip()
    if not stripped:
        return ValidationResult(False, "SQL is empty.")

    if not re.match(r"^SELECT\b", stripped, flags=re.IGNORECASE):
        return ValidationResult(False, "Only SELECT statements are allowed.")

    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, stripped, flags=re.IGNORECASE):
            return ValidationResult(False, f"Forbidden SQL pattern detected: {pattern}")

    tables = extract_tables(stripped)
    if not tables:
        return ValidationResult(False, "No table found in SQL.")

    disallowed = tables - ALLOWED_TABLES
    if disallowed:
        return ValidationResult(False, f"Disallowed tables referenced: {', '.join(sorted(disallowed))}")

    return ValidationResult(True, "SQL passed validation.")
