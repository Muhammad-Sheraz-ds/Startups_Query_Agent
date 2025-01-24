from fastapi import FastAPI, Query
from query_agent import execute_query

app = FastAPI()

@app.get("/query")
def query_startup(user_query: str = Query(..., description="Natural language query")):
    try:
        result = execute_query(user_query)
        return {"status": "success", "data": result["output"]}
    except Exception as e:
        return {"status": "error", "message": str(e)}
