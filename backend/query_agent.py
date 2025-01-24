from langchain_ollama import ChatOllama
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.base import create_sql_agent, SQLDatabaseToolkit

# Set up the LLM
llm = ChatOllama(model="llama3.2", temperature=0.1)

import os
from langchain_community.utilities.sql_database import SQLDatabase

# Construct absolute path to the database
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/database.db"))
db = SQLDatabase.from_uri(f"sqlite:///{db_path}")

# Set up the SQL toolkit
toolkit = SQLDatabaseToolkit(db=db, llm=llm)


from langchain.agents import AgentExecutor

agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    max_iterations=20,  # Increase the iteration limit (default is 15)
    max_execution_time=60,  # Set time limit in seconds
    verbose=True
)

# Create the SQL Agent
def setup_sql_agent():
    return create_sql_agent(toolkit=toolkit, llm=llm, verbose=True)
