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
from typing import Annotated
import requests




#### Webscraper function

# what
# where
# distance
# max_days_old
# sort_dir
# sort_by
# salary_min
# salary_max
# salary_include_unknown
# full_time
# part_time
# contract
# permanent
# company

# Define the endpoint and query parameters
def get_job_listings(app_id, app_key, what = None, where = None, distance = 5, max_days_old = None, sort_dir = 'up', sort_by = 'default', salary_min = 0, salary_max = 200000, salary_include_unknown = 1, full_time = None, part_time = None, contract = None, permanent = None, company = None):
    '''
    Get job listing with API
    '''


    # Define the endpoint and query parameters
    url = 'http://api.adzuna.com/v1/api/jobs/gb/search/1'

    # Define parameters: logic needed
    params = {
        'app_id': app_id,
        'app_key': app_key,
        'results_per_page': 20,
        'page': 10,
        'what': what, # job, company name, etc.
        'where': where, # city, state, postal codes etc.
        'distance': distance, # The distance in kilometres from the centre of the place described by the 'where' parameter. Defaults to 5km.
        'max_days_old': max_days_old, # in days
        'sort_dir': sort_dir, # up or down,
        'sort_by': sort_by, # sort by date, salary, relevance, default, hybrid
        'salary_min': salary_min, # minimum salary # what if hourly wage?
        'salary_max': salary_max, # maximum salary,
        'salary_include_unknown': salary_include_unknown, # 1 if salary is predicted, otherwise '',
        'full_time': full_time, # If set to "1", only full time jobs will be returned
        'part_time': part_time, # If set to "1", only part time jobs will be returned
        'contract': contract, # If set to "1", only contract jobs will be returned
        'permanent': permanent, # If set to "1", only permanent jobs will be returned
        'company': company, # company name
        # some other keywords good to include but not necessary:
        # 'what_and': 'data scientist, remote', # The keywords to search for, all keywords must be found.
        # 'what_or': 'data scientist, remote', The keywords to search for, any keywords may be found. Multiple terms may be space separated
        # 'what_exclude': 'internship', Keywords to exclude from the search. Multiple terms may be space separated.
        # 'title_only': Keywords to find, but only in the title. Multiple terms may be space separated.
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



#### Define job API call pipeline

def add_jobs_to_vectordb(
    what=None,
    where=None,
    distance=5,
    max_days_old=None,
    sort_dir='up',
    sort_by='default',
    salary_min=0,
    salary_max=200000,
    salary_include_unknown=1,
    full_time=None,
    part_time=None,
    contract=None,
    permanent=None,
    company=None,
):
    # load env
    # Get API
    load_dotenv()  # Loads variables from .env into environment

    app_id = os.getenv("app_id")
    app_key = os.getenv("app_key")
    

    # Initiate embedding model
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Initiate vector store model
    index = faiss.IndexFlatL2(len(embeddings.embed_query('hello')))

    vector_store = FAISS(
        embedding_function=embeddings,
        index=index,
        docstore=InMemoryDocstore(),
        index_to_docstore_id={},
    )

    # Call the function with user-provided arguments
    documents = get_job_listings(
        app_id = app_id,
        app_key = app_key, 
        what=what,
        where=where,
        distance=distance,
        max_days_old=max_days_old,
        sort_dir=sort_dir,
        sort_by=sort_by,
        salary_min=salary_min,
        salary_max=salary_max,
        salary_include_unknown=salary_include_unknown,
        full_time=full_time,
        part_time=part_time,
        contract=contract,
        permanent=permanent,
        company=company
    )

    if not documents:
        print("No documents returned.")
        return

    # Add to FAISS vector store
    uuids = [str(uuid4()) for _ in range(len(documents))]
    vector_store.add_documents(documents=documents, ids=uuids)

    # Save locally
    vector_store.save_local("vectorstore/job_listings_vectorstore")


add_jobs_to_vectordb(
    what=None,
    where=None,
    distance=5,
    max_days_old=None,
    sort_dir='up',
    sort_by='default',
    salary_min=0,
    salary_max=200000,
    salary_include_unknown=1,
    full_time=None,
    part_time=None,
    contract=None,
    permanent=None,
    company=None,
)


add_jobs_to_vectordb(what = 'Software Engineer', where='London')