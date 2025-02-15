# frontend/app.py

import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"  # Ensure this matches your backend URL

st.title("Startups Query Agent")

user_query = st.text_input("Your Query:")

if st.button("Submit Query"):
    if user_query:
        try:
            st.info("Sending query to backend...")
            response = requests.post(f"{API_URL}/query/", json={"query": user_query})
            st.write("Status Code:", response.status_code)
            if response.status_code == 200:
                data = response.json()
                
                # Extract SQL query and results from the response
                result = data.get("result", {})
                sql_query = result.get("sql_query", "No SQL query returned")
                results = result.get("results", [])
                
                st.markdown("### Generated SQL Query")
                st.code(sql_query, language="sql")
                
                st.markdown("### Query Results")
                if isinstance(results, list) and results:
                    # Convert the results list to a DataFrame and display it as a table.
                    df = pd.DataFrame(results)
                    st.table(df)
                else:
                    st.write("No results returned.")
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Error connecting to API: {e}")
    else:
        st.warning("Please enter a query.")
