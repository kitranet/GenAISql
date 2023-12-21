import os
import streamlit as st
try:
    # import pandas as pd
    # import time
    from util.config import OpenAIConfig
except Exception as e:
    st.error(f"Import error:{e}")
st.session_state.update(st.session_state)

try:
# st page structure
    st.set_page_config(page_title="DB Selector", page_icon="frontend/nttdata.png", layout="centered", initial_sidebar_state="collapsed", menu_items=None)
    page_url_params = st.experimental_get_query_params()
    if "db_profile" in page_url_params.keys():
        selected_db_profile = page_url_params["db_profile"]
    elif len(st.session_state.profiles):
        selected_db_profile = st.session_state.profiles[-1]
    else:
        st.error("No DB profiles exist!!")
    all_schemas, past_selected_schemas = st.session_state[selected_db_profile].get_selected_schema_names()
    selected_schemas = st.multiselect("Select schemas",all_schemas,default = past_selected_schemas)
    submitted = st.button("Submit")
    if submitted:
        st.session_state[selected_db_profile].set_selected_schema_names(selected_schemas)
        selected_profile_metadata = st.session_state[selected_db_profile].get_metadata()
        table_mapping_output_text = '\n|\n'.join([f"--{key}\n| |\n| -{','.join(selected_profile_metadata[key])}" for key in selected_profile_metadata])
        st.text(table_mapping_output_text)
except Exception as e:
    st.error(f"DB Object Selector config: {e}\nSelected Profile: {selected_db_profile}\n{st.session_state[selected_db_profile].get_selected_schema_names()}")

