# backend/query_agent.py

import os
import re
import sqlite3
from ollama import chat

# Define the system prompt instructing the assistant on the database schema and expected output.
SYSTEM_PROMPT = """
You are a knowledgeable SQL assistant. The database contains a table named 'startups' with the following columns:
company_id, company_name, short_description, long_description, batch, status, tags, location, country, year_founded, num_founders, founders_names, team_size, website, cb_url, linkedin_url.
When given a user's query, think step-by-step and generate the corresponding SQL query.
Output ONLY the final SQL query on a new line starting with "Final SQL Query:" and nothing else.
"""

def execute_query(sql_query: str) -> list:
    """
    Executes the given SQL query against the SQLite database
    and returns the results as a list of dictionaries.
    """
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/database.db"))
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description] if cursor.description else []
        results = [dict(zip(columns, row)) for row in rows]
    finally:
        conn.close()
    return results

def parse_final_query(output: str) -> str:
    """
    Extracts the final SQL query from the assistant's output.
    Expects a line starting with "Final SQL Query:".
    """
    match = re.search(r"Final SQL Query:\s*(.+)", output, re.DOTALL)
    if match:
        # If the query spans multiple lines, return only the first line.
        return match.group(1).strip().splitlines()[0]
    return ""

def invoke(params: dict) -> dict:
    """
    Accepts a dictionary with key "input" containing the user's natural language query.
    Uses the Ollama chat API to generate a SQL query, then executes the query against the database.
    Returns a dictionary with the final SQL query and its execution results.
    """
    user_query = params.get("input", "")
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_query},
        {"role": "assistant", "content": ""}
    ]
    
    response = chat(
        model="llama3.2",  # Adjust the model name if needed.
        messages=messages
    )
    
    output = response["message"]["content"].strip()
    final_sql = parse_final_query(output)
    
    try:
        results = execute_query(final_sql)
        return {"sql_query": final_sql, "results": results}
    except Exception as e:
        return {"error": str(e), "sql_query": final_sql}

# For local testing:
if __name__ == "__main__":
    sample_query = "List all startups founded in 2020"
    result = invoke({"input": sample_query})
    print("Query and Results:", result)
