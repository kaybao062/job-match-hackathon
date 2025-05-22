### ---- This script runs agent to get job listings ----
# Set root folder as the project folder
import os
import sys
# os.getcwd()
os.chdir("/Users/kay/Desktop/job-match-hackathon")
# print("New directory:", os.getcwd())

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.tools import StructuredTool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor
from langchain.agents import create_tool_calling_agent

import getpass
from dotenv import load_dotenv

# Fix Python path to allow importing from `src`
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# from src.query_engine import QueryEngine
from typing import Annotated


# Initiate langsmith
def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")

# Load mistrial api
_set_env("MISTRAL_API_KEY")
os.environ['TOKENIZERS_PARALLELISM'] = 'true'

load_dotenv() # load env

def run_agent():

    # Initiate AI

    model = init_chat_model("mistral-small-latest", model_provider="mistralai")


    # Initiate tools

    def QueryEngine(resume: str) -> str:
        """Use this tool when user input a resume message to retrieve and rank jobs. """
        from src.query_engine import retrieve_jobs
        from src.load_data import load_vector_store
        
        # Load the vector store
        vector_store = load_vector_store()
        print('Vector store loaded')
        # load context
        context = retrieve_jobs(vector_store, resume)
        print(f'{len(context)} job documents retrieved.')

        return context


    # Wrap in tools
    query_engine_tool = StructuredTool.from_function(
        func=QueryEngine,
        name="QueryEngine",
        description="Use this tool to retrieve relevant job listings when a resume is provided to find top 3 matching jobs from the job listings database."
    )
    tools = [query_engine_tool]


    # # Load resume
    from langchain_community.document_loaders import Docx2txtLoader
    loader = Docx2txtLoader("resume.docx")

    data = loader.load()

    # Convert to a single string
    doc_text = "\n".join([doc.page_content for doc in data])

# doc_text 
# doc_text = ''
# Wrap up prompt to langchain acceptable template


    prompt_temp = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant for matching resumes to job listings. This is a resume. Please review it, use Query Engine tool to retrieve relevant job listings from job listings vector database, and select the top 3 matches based on the education, experience and skills on resume. Provide a rank score (out of 100) and explain your logic of ranking. If there's no resume submitted, just say you don't know. "),
        ("user", doc_text),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ])

    # Create agent
    agent = create_tool_calling_agent(model, tools, prompt_temp)
    agent_executor = AgentExecutor(agent=agent, tools=tools)

    # Running agent to get response
    print('Running agent...')
    response = agent_executor.invoke({'input': prompt_temp})

    # print(response)

    final_output = response.get("output")

    return final_output
    # print("Final output:", final_output)


    # if response:
    #     response.content
    #     response.tool_calls
    # else:
    #     print(response)


output = run_agent()

# Save final_output to a text file
with open("output.txt", "w", encoding="utf-8") as f:
    f.write(output)