#### This script load the vector store from the local file system

from typing import Annotated
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

def load_vector_store():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return FAISS.load_local("vectorstore", embeddings, allow_dangerous_deserialization=True)

# Load the FAISS vector store
vs = load_vector_store()

# # Print all documents
# with open("vectorstore_documents.txt", "w", encoding="utf-8") as f:
#     for i, doc_id in enumerate(vs.index_to_docstore_id.values(), start=1):
#         d = vs.docstore.search(doc_id)
#         f.write(f"Document {i}:\n")
#         f.write(d.page_content + "\n\n")