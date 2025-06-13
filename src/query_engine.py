import sys
import os

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


#### This script loads the vector store and sets up the query engine for the LLM.
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

# from src.load_data import load_vector_store

from langchain.tools import tool

def load_template():
    template = """
     You are an AI assistant for job ranking tasks. Based on how well the context (a list of job descriptions) aligns with the query (user's resume input), order the retrieved jobs (context) and explain how you ranked them. Return a list of the top 3 matching job titles and their links.
        Resume: {resume}
        Context: {context}
        Answer:
        
        """
    
    return ChatPromptTemplate.from_template(template)

def create_query_engine(template):
    """Creates a query engine using an LLM and a prompt template."""
    # Set up the LLM
    llm = OllamaLLM(model="llama3.2")

    # Create a Retrieval-based QA chain
    # prompt = ChatPromptTemplate.from_template(template)
    chain = template | llm
    
    return chain

def retrieve_jobs(vector_store, resume):
    """Retrieve the most relevant jobs from the vector store based on the resume."""
    retrieve_documents = vector_store.similarity_search(resume, k=5)
    # retrieve_documents[0]

    context = "\n\n".join([doc.page_content for doc in retrieve_documents])

    return context


@tool("QueryEngine", return_direct=True)
def QueryEngine(resume: str) -> str:
# def QueryEngine(resume): 
    """Use this tool when user input a resume message to retrieve and rank jobs. """
    from src.query_engine import load_template, retrieve_jobs, create_query_engine
    from src.load_data import load_vector_store
    
    # load the template
    template = load_template()
    print('Template loaded')
    # Load the vector store
    vector_store = load_vector_store()
    print('Vector store loaded')
    # load context
    context = retrieve_jobs(vector_store, resume)
    print('Context retrieved')
    # print("Context:", context)
   
    # add prompt
    # prompt = template.format(context=context, resume=resume)

    # Initialize the query engine
    chain = create_query_engine(template)
    # print(chain)

    # # input question or use default question
    # question = user_question if user_question else "Which jobs match my education, skills and experience based on this resume?"

    # Run the query engine

    result = chain.invoke({'resume': resume, "context": context})
    
    
    return result





# Call with no custom question (defaults to the preset question)
# from langchain_community.document_loaders import Docx2txtLoader
# loader = Docx2txtLoader("resume.docx")

# data = loader.load()

# # Convert to a single string
# doc_text = "\n".join([doc.page_content for doc in data])

 
# result = QueryEngine(doc_text)

# print("Response:", result)