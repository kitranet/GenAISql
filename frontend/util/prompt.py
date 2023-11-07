import streamlit as st

def create_sql_querry_prompt(profile_name,user_input):
    prompt = f"\nQ. Interpret user_input: {user_input} as a single {'SQL' if not st.session_state[profile_name] else st.session_state[profile_name].type} querry.\n"
    if st.session_state[profile_name]:
        metadata = st.session_state[profile_name].metadata
        prompt = metadata+prompt
    return prompt