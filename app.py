from __future__ import annotations

import streamlit as st

from src.charts import build_chart
from src.config import get_settings
from src.workflow import AnalyticsWorkflow

st.set_page_config(page_title='Analytics Bot POC', layout='wide')

settings = get_settings()

st.title('Analytics Bot POC')
st.caption('Natural language to MySQL analytics demo built with LangChain')

with st.sidebar:
    st.subheader('Setup')
    st.write('1. Add your OpenAI key and MySQL connection in `.env`')
    st.write('2. Create the MySQL database and run `python data/demo_seed.py`')
    st.write('3. Run `streamlit run app.py`')
    st.subheader('Sample questions')
    samples = [
        'What were total sales by month in 2025?',
        'Show top 5 products by revenue in 2025.',
        'Compare sales by region for Q1 2025.',
        'What is the average order value by region?',
        'Which category had the highest units sold?',
    ]
    for s in samples:
        st.code(s)

if 'messages' not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])
        if message.get('sql'):
            with st.expander('Generated SQL'):
                st.code(message['sql'], language='sql')
        if message.get('dataframe') is not None:
            st.dataframe(message['dataframe'], use_container_width=True)
            chart = build_chart(message['dataframe'])
            if chart:
                st.plotly_chart(chart, use_container_width=True)

question = st.chat_input('Ask an analytics question')

if question:
    st.session_state.messages.append({'role': 'user', 'content': question})
    with st.chat_message('user'):
        st.markdown(question)

    with st.chat_message('assistant'):
        if not settings.openai_api_key:
            st.error('Missing OPENAI_API_KEY in .env file.')
        else:
            workflow = AnalyticsWorkflow(
                database_url=settings.database_url,
                model_name=settings.llm_model,
                api_key=settings.openai_api_key,
                query_timeout_seconds=settings.query_timeout_seconds,
            )
            try:
                result = workflow.run(question)
                st.markdown(result.answer)
                with st.expander('Generated SQL'):
                    st.code(result.sql, language='sql')
                st.dataframe(result.dataframe, use_container_width=True)
                chart = build_chart(result.dataframe)
                if chart:
                    st.plotly_chart(chart, use_container_width=True)

                st.session_state.messages.append(
                    {
                        'role': 'assistant',
                        'content': result.answer,
                        'sql': result.sql,
                        'dataframe': result.dataframe,
                    }
                )
            except Exception as exc:
                error_message = f'I could not answer that question. {exc}'
                st.error(error_message)
                st.session_state.messages.append(
                    {'role': 'assistant', 'content': error_message}
                )
