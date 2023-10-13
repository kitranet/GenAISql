import os
import streamlit as st
try:
    import pandas as pd
    import time
    # from util import PostgresqlConnector, MSAccessConnector
    from util.connectors import MSAccessConnector
except Exception as e:
    st.error(f"Import error:{e}")
st.session_state.update(st.session_state)

try:
# st page structure
    st.set_page_config(page_title="Database Profile Configuration", page_icon="nttdata.png", layout="centered", initial_sidebar_state="collapsed", menu_items=None)
    st.title("Add new database connection")
    name = st.text_input("Name")
    db_file_path = st.text_input('Database File Path')
    submitted = st.button("Submit")
    if submitted:
        st.session_state.profiles.append(name)
        st.session_state[name] = MSAccessConnector(db_file_path)
        # display_pane.empty()
        st.write(f"{st.session_state.profiles} created!!")
    # st.experimental_rerun()
except Exception as e:
    st.error(f"Database config : {e}")

