from __future__ import annotations

from dataclasses import dataclass
import pandas as pd

from src.db import DatabaseClient
from src.responder import ResultResponder
from src.schema_context import render_schema_context
from src.sql_generator import SQLGenerator
from src.sql_validator import validate_sql


@dataclass
class WorkflowResult:
    question: str
    sql: str
    answer: str
    dataframe: pd.DataFrame


class AnalyticsWorkflow:
    def __init__(self, database_url: str, model_name: str, api_key: str, query_timeout_seconds: int = 20):
        self.db = DatabaseClient(database_url, query_timeout_seconds=query_timeout_seconds)
        self.schema_context = render_schema_context()
        self.sql_generator = SQLGenerator(model_name=model_name, api_key=api_key)
        self.responder = ResultResponder(model_name=model_name, api_key=api_key)

    def run(self, question: str) -> WorkflowResult:
        sql = self.sql_generator.generate(question=question, schema_context=self.schema_context)
        validation = validate_sql(sql)
        if not validation.is_valid:
            raise ValueError(f"Generated SQL failed validation: {validation.message}\nSQL: {sql}")

        df = self.db.run_select(sql)
        answer = self.responder.summarize(question=question, sql=sql, df=df)
        return WorkflowResult(question=question, sql=sql, answer=answer, dataframe=df)
