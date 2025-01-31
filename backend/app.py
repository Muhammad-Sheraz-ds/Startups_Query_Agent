# app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from query_agent import setup_sql_agent

# Initialize FastAPI app
app = FastAPI()

# Define request model for user queries
class QueryInput(BaseModel):
    query: str

@app.post("/query/")
async def execute_query(query_input: QueryInput):
    """
    API endpoint to execute SQL queries using the agent.
    """
    try:
        # Initialize SQL Agent
        sql_agent = setup_sql_agent()

        # Execute the query via the agent
        result = sql_agent.invoke({"input": query_input.query})

        # Check if the agent was stopped due to iteration limit or timeout
        if 'Agent stopped due to iteration limit or time limit' in result.get('output', ''):
            raise HTTPException(status_code=408, detail="Request timed out or exceeded iteration limit.")
        
        return {"query": query_input.query, "result": result["output"]}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
