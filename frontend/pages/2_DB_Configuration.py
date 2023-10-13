import os
import streamlit as st
try:
    import pandas as pd
    import time
    # from util import PostgresqlConnector, MSAccessConnector
    from util.connectors import PostgresqlConnector, MSSqlConnector
except Exception as e:
    st.error(f"Import error:{e}")
st.session_state.update(st.session_state)

try:
# st page structure
    st.set_page_config(page_title="Database Profile Configuration", page_icon="nttdata.png", layout="centered", initial_sidebar_state="collapsed", menu_items=None)
    db_type = st.selectbox("Database type:",["MySQL", "Postgresql", "Oracle", "MS SQL Active Directory", "PySpark"])
    name = st.text_input("Name")
    hostname = st.text_input("Hostname")
    port = st.text_input("Port")
    username = st.text_input("Username")
    password = st.text_input("Password",type='password')
    database = st.text_input("Database")
    submitted = st.button("Submit")
    if submitted:
        st.session_state.profiles.append(name)
        if db_type == "Postgresql":
            st.session_state[name] = PostgresqlConnector(hostname,port,username,password,database)
        elif db_type == "MySQL":
            st.error("DB connector doesnt exist")
        elif db_type == "Oracle":
            st.error("DB connector doesnt exist")
        elif db_type == "MS SQL Active Directory":
            st.session_state[name] = MSSqlConnector(hostname,port,username,password,database,active_dir=True)
        elif db_type == "PySpark":
            st.error("DB connector doesnt exist")
        st.write(f"{name} created!!")
except Exception as e:
    st.error(f"Database config : {e}")

