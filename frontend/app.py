import streamlit as st
import requests

# API URL
API_URL = "http://localhost:8000/query"

# Streamlit app
st.title("Startup Query System")
st.write("Ask questions about startups!")

query = st.text_input("Enter your query:")

if st.button("Submit"):
    response = requests.get(API_URL, params={"user_query": query}).json()
    if response["status"] == "success":
        st.write("**Result:**")
        st.write(response["data"])
    else:
        st.error(f"Error: {response['message']}")
