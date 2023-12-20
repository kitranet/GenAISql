import os
import streamlit as st
try:
    import pandas as pd
    import time
    from util.config import OpenAIConfig
except Exception as e:
    st.error(f"Import error:{e}")
st.session_state.update(st.session_state)

try:
# st page structure
    st.set_page_config(page_title="OpenAI Profile Configuration", page_icon="frontend/nttdata.png", layout="centered", initial_sidebar_state="collapsed", menu_items=None)

    # name = st.text_input("")
    # hostname = st.text_input("Hostname")
    # port = st.text_input("Port")
    # username = st.text_input("Username")
    api_key = st.text_input("API Key",type='password')
    temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.4, step=0.05, key='oai_temp')
    max_tokens = st.slider("Max Tokens", min_value=100, max_value=1000, value=300, step=1, key='oai_max_tok')
    top_p = st.slider("Top p", min_value=0.0, max_value=1.0, value=0.5, step=0.05, key='oai_top_p')
    frequency_penalty = st.slider("Frequency Penalty", min_value=0.0, max_value=1.0, value=0.0, step=0.05, key='oai_frequency_penalty')
    presence_penalty = st.slider("Presence Penalty", min_value=0.0, max_value=1.0, value=0.0, step=0.05, key='oai_presence_penalty')
    best_of = st.slider("Best Of", min_value=1, max_value=10, value=1, step=1, key='oai_best_of')
    # database = st.text_input("Database")
    submitted = st.button("Submit")
    if submitted:
        st.session_state['openai_config'] = OpenAIConfig(api_key, temperature, max_tokens, top_p, frequency_penalty, presence_penalty, best_of)
        st.write(f"OpenAI config created!!")
except Exception as e:
    st.error(f"OpenAI config : {e}")

