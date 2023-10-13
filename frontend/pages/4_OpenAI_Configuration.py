import os
import streamlit as st
try:
    import pandas as pd
    import time
    # from util import PostgresqlConnector, MSAccessConnector
    from util.connectors import PostgresqlConnector
except Exception as e:
    st.error(f"Import error:{e}")
st.session_state.update(st.session_state)

try:
# st page structure
    st.set_page_config(page_title="OpenAI Profile Configuration", page_icon="nttdata.png", layout="centered", initial_sidebar_state="collapsed", menu_items=None)

    # name = st.text_input("")
    # hostname = st.text_input("Hostname")
    # port = st.text_input("Port")
    # username = st.text_input("Username")
    api_key = st.text_input("API Key",type='password')
    # database = st.text_input("Database")
    submitted = st.button("Submit")
    if submitted:
        st.session_state['openai_key'] = api_key
        st.write(f"key created!!")
except Exception as e:
    st.error(f"OpenAI config : {e}")

