import streamlit as st
import requests

# Backend API URL
BACKEND_URL = "http://127.0.0.1:8000/query"

st.title("Startups Query Agent")

# Input query from the user
user_query = st.text_input("Enter your query:", placeholder="e.g., Show me the first 10 startups in the database.")

if st.button("Run Query"):
    if user_query.strip():
        # Send request to backend
        try:
            with st.spinner("Querying the database..."):
                response = requests.post(BACKEND_URL, json={"query": user_query})
                if response.status_code == 200:
                    result = response.json().get("result", "No result found.")
                    st.success("Query successful!")
                    st.write(f"### Query Result:\n{result}")
                else:
                    st.error(f"Error: {response.status_code}, {response.json().get('detail')}")
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to connect to the backend: {e}")
    else:
        st.warning("Please enter a query to proceed!")

