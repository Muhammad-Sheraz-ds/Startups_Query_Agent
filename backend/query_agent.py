# backend/query_agent.py

import os
import re
import sqlite3
from types import SimpleNamespace
from ollama import chat

# Define the system prompt with chain-of-thought instructions.
SYSTEM_PROMPT = """
You are a knowledgeable SQL assistant. The database contains a table named 'startups' with the following columns:
company_id, company_name, short_description, long_description, batch, status, tags, location, country, year_founded, num_founders, founders_names, team_size, website, cb_url, linkedin_url.
When given a user's query, think step-by-step about how to build the SQL command.
Finally, output ONLY the final SQL query on a new line starting with "Final SQL Query:".
Do not include any extra commentary after that line.
"""

def execute_query(sql_query: str) -> list:
    """
    Executes the given SQL query against the SQLite database and returns the results as a list of dictionaries.
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
    The output must contain a line starting with "Final SQL Query:".
    """
    match = re.search(r"Final SQL Query:\s*(.+)", output, re.DOTALL)
    if match:
        # If the query spans multiple lines, take only the first line after the marker.
        final_line = match.group(1).strip().splitlines()[0]
        return final_line.strip()
    return ""

def invoke(params: dict) -> dict:
    """
    Accepts a dictionary with key "input" containing the user's natural language query.
    Iteratively prompts the assistant to generate a correct SQL query by providing its chain-of-thought reasoning.
    Once a final SQL query is extracted and successfully executed, returns only:
      - "sql_query": the final SQL query,
      - "results": the results from executing the query.
    """
    user_query = params.get("input", "")
    
    # Initial message list: system prompt plus user query.
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_query}
    ]
    
    max_attempts = 3
    last_error = ""
    
    for attempt in range(max_attempts):
        response = chat(
            model="llama3.2",
            messages=messages
        )
        output = response["message"]["content"].strip()
        final_query = parse_final_query(output)
        
        if not final_query:
            messages.append({"role": "assistant", "content": "Error: Could not extract a final SQL query. Please try again with a refined query."})
            continue
        
        try:
            results = execute_query(final_query)
            # Successful execution: return final query and results only.
            return {
                "sql_query": final_query,
                "results": results
            }
        except Exception as e:
            last_error = str(e)
            messages.append({"role": "assistant", "content": f"Error: {last_error}. Please refine your SQL query."})
    
    # If all attempts fail, return an error message with the last error.
    return {
        "error": f"Failed to generate a correct SQL query after {max_attempts} attempts. Last error: {last_error}"
    }

# Expose the invoke function as sql_agent.invoke for integration with other modules.
sql_agent = SimpleNamespace(invoke=invoke)

if __name__ == "__main__":
    # Example usage: Query startups founded in 2020.
    example_query = "List all startups founded in 2020"
    result = sql_agent.invoke({"input": example_query})
    print("Query Result:", result)
