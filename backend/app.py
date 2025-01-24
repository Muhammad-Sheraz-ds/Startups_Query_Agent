from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from query_agent import setup_sql_agent

app = FastAPI()

# Initialize the SQL agent
sql_agent = setup_sql_agent()


class QueryRequest(BaseModel):
    query: str


@app.get("/")
async def root():
    return {"message": "Welcome to the Startups Query Agent Backend!"}


@app.post("/query")
async def query_database(request: QueryRequest):
    try:
        result = sql_agent.run(request.query)
        return {"query": request.query, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
