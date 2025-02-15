# backend/app.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from query_agent import sql_agent

app = FastAPI()

# Add CORS middleware to allow requests from the frontend.
# You can restrict origins if needed (e.g., ["http://localhost:8501"])
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

@app.get("/")
def home():
    return {"message": "Welcome to the Startups Query Agent API!"}

@app.post("/query/")
def query_database(request: QueryRequest):
    try:
        # Generate SQL query and execute it via the SQL agent.
        response = sql_agent.invoke({"input": request.query})
        return {"query": request.query, "result": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
