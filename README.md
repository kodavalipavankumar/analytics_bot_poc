# Basic Analytics Bot POC - MySQL Version

A lightweight analytics chatbot built with **LangChain + Streamlit + SQLAlchemy + MySQL**.

This project is intentionally simple for a client POC:
- no LangSmith
- no agent loop
- no traceability dashboard
- no vector database
- no write access from the app workflow

The workflow is:

1. User asks a business question in natural language
2. The app sends schema context + question to the LLM
3. The LLM generates SQL
4. The app validates the SQL
5. The app executes the SQL against a MySQL analytics database
6. The app summarizes the result and renders a table/chart

## Project structure

```text
analytics_bot_poc/
├── app.py
├── requirements.txt
├── .env.example
├── README.md
├── data/
│   ├── demo_seed.py
│   └── schema_dictionary.json
├── src/
│   ├── config.py
│   ├── db.py
│   ├── prompts.py
│   ├── schema_context.py
│   ├── sql_generator.py
│   ├── sql_validator.py
│   ├── responder.py
│   ├── charts.py
│   └── workflow.py
└── tests/
    └── test_sql_validator.py
```

## Setup

### 1. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create your environment file

Copy `.env.example` to `.env` and update:
- `OPENAI_API_KEY`
- `DATABASE_URL`

Example `DATABASE_URL`:

```text
mysql+pymysql://analytics_user:analytics_password@localhost:3306/analytics_poc
```

### 4. Create the MySQL database

Run this once in MySQL:

```sql
CREATE DATABASE analytics_poc;
```

### 5. Seed the demo data into MySQL

```bash
python data/demo_seed.py
```

This creates and loads a demo `sales` table inside your MySQL database.

### 6. Run the app

```bash
streamlit run app.py
```

## Demo questions

- What were total sales by month in 2025?
- Show top 5 products by revenue in 2025.
- Compare sales by region for Q1 2025.
- What is the average order value by region?
- Which category had the highest units sold?

## Recommended production hardening

- use read-only credentials for the app user
- point the bot to curated views instead of raw tables
- add DB-side timeouts and connection controls
- log prompts and failures safely
- add authentication if multiple users will access it
- swap the demo `sales` table for your client schema dictionary and approved views

## Notes

This app generates SQL using the LLM, but only executes statements that pass validation.
It only allows `SELECT` queries against approved tables.
The seed script writes demo data, but the Streamlit app is read-only.
