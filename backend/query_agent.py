from langchain.agents import AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_cohere.chat_models import ChatCohere
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit

import os

# API Key for Cohere
os.environ["COHERE_API_KEY"] = "your_cohere_api_key"

# Database and LLM configuration
db = SQLDatabase.from_uri("sqlite:///data/database.db")
llm = ChatCohere(model="command-r-plus", temperature=0.1, verbose=True)
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# Agent setup
prompt = ChatPromptTemplate.from_template("{input}")
agent = toolkit.create_agent(prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=toolkit.get_tools(), verbose=True)

def execute_query(query):
    return agent_executor.invoke({"input": query})

if __name__ == "__main__":
    query = "List 10 startups in the medical domain."
    response = execute_query(query)
    print(response["output"])
