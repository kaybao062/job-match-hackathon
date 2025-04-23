#### This script loads the vector store and sets up the query engine for the LLM.
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

from src.load_data import load_vector_store



def create_query_engine(template):
    """Creates a query engine using an LLM and a prompt template."""
    # Set up the LLM (you can use OpenAI, HuggingFace, or others)
    llm = OllamaLLM(model="llama3.2")

    # Create a Retrieval-based QA chain
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm
    
    return chain

def retrieve_jobs(resume):
    """Retrieve the most relevant jobs from the vector store based on the resume."""
    retrieve_documents = vector_store.similarity_search(resume, k=5)
    # retrieve_documents[0]

    context = "\n\n".join([doc.page_content for doc in retrieve_documents])

    return context

def QueryEngine(template, resume, user_question=None):
    """Retrieve jobs and return the response using the query engine."""
    # Load the vector store
    vector_store = load_vector_store()
    print('Vector store loaded')
    
    print('Query engine initialized')

    # Retrieve the context
    context = retrieve_jobs(resume)
    print('Context retrieved')


    # Initialize the query engine
    chain = create_query_engine(template)

    # input question or use default question
    question = user_question if user_question else "Which jobs match my education, skills and experience based on my resume?"

    # Run the query engine

    result = chain.invoke({'resume': resume, "context": context, "question": question})
    return result

# # Example usage
# resume = "..."  # Example resume text to query against the vector store

# # Call with a custom question
# result = return_response(resume, user_question="What are the top 3 jobs for a software engineer?")
# print("Response:", result)

# # Call with no custom question (defaults to the preset question)
# result = return_response(resume)
# print("Response:", result)