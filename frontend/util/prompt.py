import streamlit as st

def create_sql_querry_prompt(profile_name,user_input):
    # if st.session_state[profile_name]:
    #     metadata = st.session_state[profile_name].get_metadata()
    prompt = f"Q. Generate  a {profile_name if not st.session_state[profile_name] else st.session_state[profile_name].type} query :{user_input}."
    return prompt