import os
import csv
import json
# %pip install -qU langchain-text-splitters

os.chdir("/Users/kay/Desktop/job-match-hackathon")
print("New directory:", os.getcwd())


# Load resume
from langchain_community.document_loaders import Docx2txtLoader
loader = Docx2txtLoader("resume.docx")

data = loader.load()

# Convert to a single string
doc_text = "\n".join([doc.page_content for doc in data])

# doc_text 


# Run agent
from agent import run_agent
output = run_agent(doc_text)

# Post-process or print
print(output)  

# parsing
output_dict = json.loads(output)
# Assuming `doc_list` is your list of Document objects
with open("job_matches.csv", "w", newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=output_dict[0].keys())
    writer.writeheader()
    writer.writerows(output_dict)
    
print("✅ CSV file 'job_matches.csv' created successfully.")