from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import pandas as pd

from src.prompts import SUMMARY_SYSTEM_PROMPT


class ResultResponder:
    def __init__(self, model_name: str, api_key: str):
        self.llm = ChatOpenAI(model=model_name, api_key=api_key, temperature=0)
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", SUMMARY_SYSTEM_PROMPT),
                (
                    "human",
                    "User question:\n{question}\n\nSQL used:\n{sql}\n\nResult preview:\n{result_preview}",
                ),
            ]
        )

    def summarize(self, question: str, sql: str, df: pd.DataFrame) -> str:
        if df.empty:
            return "No matching records were found for that question."
        preview = df.head(10).to_markdown(index=False)
        chain = self.prompt | self.llm
        response = chain.invoke(
            {"question": question, "sql": sql, "result_preview": preview}
        )
        return response.content.strip()
