import streamlit as st
import requests

# Define FastAPI backend URL
API_URL = "http://127.0.0.1:8000/query/"

st.title("🚀 Startups Query Agent")
st.markdown("Ask questions about startups, and get instant responses using OpenAI-powered SQL querying!")

# User input
query = st.text_area("Enter your question about startups:", "")

if st.button("Submit Query"):
    if query.strip():
        # Send query request to FastAPI backend
        response = requests.post(API_URL, json={"query": query})
        if response.status_code == 200:
            st.success(f"**Response:** {response.json()['result']}")
        else:
            st.error(f"Error: {response.json()['detail']}")
    else:
        st.warning("Please enter a query before submitting.")
