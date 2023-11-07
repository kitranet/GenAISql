import os
import streamlit as st
import openai
import pandas as pd
import time
import pyodbc
# from util import PostgresqlConnector, MSAccessConnector
from util.connectors import PostgresqlConnector, MSAccessConnector
from util.prompt import create_sql_querry_prompt
import util.logging as ul
import logging
appLogger = logging.getLogger('frontend')
st.session_state.update(st.session_state)
# Configure OpenAI
openai.api_type = "azure"
openai.api_base = "https://generativetesing12.openai.azure.com/"
openai.api_version = "2023-09-15-preview"

st.set_page_config(page_title="SQL Query Generator", page_icon="nttdata.png", layout="centered", initial_sidebar_state="collapsed", menu_items=None)
if 'profiles' not in st.session_state:
    st.session_state['profiles'] = ['Demo - querry generation only']# ['Postgresql','MS Access']
for profile in st.session_state['profiles']:
    if profile not in st.session_state:
        st.session_state[profile] = None
# Streamlit app
             
generated_query = ""
try:
    st.selectbox("Select database profile",st.session_state.profiles,key='selected_profile')
    user_input = st.text_input("Enter a natural language query:",key="natural_querry")

    # Generate query
    if user_input and st.button("Generate SQL Query"):
        sqlquery_prompt = create_sql_querry_prompt(st.session_state['selected_profile'],user_input)
        appLogger.info(f'sqlquery_prompt:{sqlquery_prompt}')
        if 'openai_key' not in st.session_state:
            st.error("OpenAPI key not configured please configure it by going to the OpenAI Configuration page from the sidebar")
            appLogger.error("OpenAPI key not configured please configure it by going to the OpenAI Configuration page from the sidebar")
        else:
            openai.api_key=st.session_state.openai_key
            response = openai.Completion.create(
                engine="maltext",
                prompt=sqlquery_prompt,
                temperature=1,
                max_tokens=300,
                top_p=0.5,
                frequency_penalty=0,
                presence_penalty=0,
                best_of=1,
                stop=None
            )
            
            appLogger.info(f'response:{response}')
            # Extract generated email from response
            generated_query = response.choices[0].text.strip()
            st.write("Generated SQL Query")
            st.code(generated_query)
            conn_object = st.session_state[st.session_state["selected_profile"]]
            if conn_object:
                with st.spinner("Getting querry results..."):
                    try:
                        df = conn_object.get_results(generated_query)
                        st.write("Querry Results:")
                        st.dataframe(df)
                    except pyodbc.Error as e:
                        appLogger.exception(e)
                        import traceback
                        st.write(f"Error executing SQL query: {traceback.format_exc(chain=False)}")
                st.success("Querry results processed!")
except Exception as e:
    appLogger.exception(e)
    import traceback
    st.error(f"An error occurred: {traceback.format_exc(chain=False)}")


