import os
import streamlit as st
try:
    import pandas as pd
    import time
    from util.connectors import MSSqlConnector
except Exception as e:
    st.error(f"Import error:{e}")
st.session_state.update(st.session_state)

try:
# st page structure
    st.set_page_config(page_title="Database Profile Configuration", page_icon="frontend/nttdata.png", layout="centered", initial_sidebar_state="collapsed", menu_items=None)
    db_type = st.selectbox("Database type:",["MS SQL Active Directory", "MySQL", "Postgresql", "Oracle", "PySpark"])
    name = st.text_input("Name", key = 'db_config_name')
    hostname = st.text_input("Hostname", key = 'db_config_hostname')
    port = st.text_input("Port", key = 'db_config_port')
    username = st.text_input("Username", key = 'db_config_username')
    password = st.text_input("Password",type='password')
    database = st.text_input("Database", key = 'db_config_database')
    submitted = st.button("Submit")
    if submitted:
        # with st.spinner("Creating DB Profile..."):
            # st.session_state.profiles.append(name)
        if db_type == "Postgresql":
            st.error("DB connector doesnt exist")
        elif db_type == "MySQL":
            st.error("DB connector doesnt exist")
        elif db_type == "Oracle":
            st.error("DB connector doesnt exist")
        elif db_type == "MS SQL Active Directory":
            with st.status("Creating DB Profile..."):
                st.write("Connecting to DB...")
                st.session_state[name] = MSSqlConnector(hostname,port,username,password,database,True,name)
                st.write("Extracting table structure information...")
                st.session_state[name].fetch_metadata()
                st.session_state.profiles = list(set(st.session_state.profiles+[name]))
                st.write(f"Profile {name} created.")
        elif db_type == "PySpark":
            st.error("DB connector doesnt exist")
        # st.write(f"{name} created!!")
except Exception as e:
    st.error(f"Database config : {e}")

