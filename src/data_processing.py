#### This scripts takes Adzuna API job listings and saves them to a FAISS vector store




# from langchain_community.document_loaders import SeleniumURLLoader
# from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.vectorstores.faiss import InMemoryDocstore
from langchain_community.vectorstores import FAISS
import faiss
from uuid import uuid4
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document
from langchain_community.document_loaders import Docx2txtLoader
from dotenv import load_dotenv
import os

import requests


#### Initiate embedding model
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

#### Initiate vector store model
index = faiss.IndexFlatL2(len(embeddings.embed_query('hello')))

vector_store = FAISS(
    embedding_function=embeddings,
    index=index,
    docstore=InMemoryDocstore(),
    index_to_docstore_id={},
)

#### Get API
load_dotenv()  # Loads variables from .env into environment

app_id = os.getenv("app_id")
app_key = os.getenv("app_key")

#### Webscraper function

# Define the endpoint and query parameters
def get_job_listings():
    '''
    Get job listing with API
    '''


    # Define the endpoint and query parameters
    url = 'http://api.adzuna.com/v1/api/jobs/gb/search/1'

    params = {
        'app_id': app_id,
        'app_key': app_key,
        'results_per_page': 20,
        'what': 'data scientist, remote',
        'content-type': 'application/json'
    }

    # Make the GET request
    response = requests.get(url, params=params)

    # initiate langchain documents
    documents = []

    # Check if it worked
    if response.status_code == 200:
        data = response.json()  # Parse JSON response
        for job in data.get('results', []):
            content = f"Title: {job.get('title')}\n\nDescription: {job.get('description')}"
            metadata = {
                "id": job.get("id"),
                "company": job.get("company", {}).get("display_name"),
                "location": job.get("location", {}).get("display_name"),
                "salary_min": job.get("salary_min"),
                "salary_max": job.get("salary_max"),
                "url": job.get("redirect_url")
            }

            documents.append(Document(page_content=content, metadata=metadata))
        # documents now contains LangChain Document objects
        print(f"Loaded {len(documents)} job listings as LangChain Documents.")
        return documents
        
    else:
        print("Error:", response.status_code, response.text)

# Call the function to get job listings
documents = get_job_listings()
# print(documents)
#### Add to FAISS vector store
# Generate unique IDs
uuids = [str(uuid4()) for _ in range(len(documents))]

# Add documents with custom IDs
vector_store.add_documents(documents=documents, ids=uuids)


#### Write vector store to local
vector_store.save_local("vectorstore/job_listings_vectorstore")