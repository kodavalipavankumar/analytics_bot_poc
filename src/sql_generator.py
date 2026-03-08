from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from src.prompts import SQL_SYSTEM_PROMPT


class SQLGenerator:
    def __init__(self, model_name: str, api_key: str):
        self.llm = ChatOpenAI(model=model_name, api_key=api_key, temperature=0)
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", SQL_SYSTEM_PROMPT),
                (
                    "human",
                    "Schema context:\n{schema_context}\n\nUser question:\n{question}\n\nReturn SQL only.",
                ),
            ]
        )

    def generate(self, question: str, schema_context: str) -> str:
        chain = self.prompt | self.llm
        response = chain.invoke({"schema_context": schema_context, "question": question})
        return response.content.strip()
