### This script takes resume as argument, runs the agent, output response and store as csv


import os

import json
import pandas as pd
# %pip install -qU langchain-text-splitters

os.chdir("/Users/kay/Desktop/job-match-hackathon")
print("New directory:", os.getcwd())


# Load resume

from langchain_community.document_loaders import Docx2txtLoader
loader = Docx2txtLoader("resume.docx")

data = loader.load()

# Convert to a single string
resume = "\n".join([doc.page_content for doc in data])

resume


from agent import run_agent

def parse_json(output):
    '''
    parse json output to dictionary
    '''
    try:
        output_dict = json.loads(output)
        return output_dict
    
    except json.JSONDecodeError as e:
        print("Initial JSON decode failed:", e)
        try:
            # Try fallback: remove intro text before JSON
            json_str = output.split("\n\n", 1)[1]
            output_dict = json.loads(json_str)

            return output_dict

        except Exception as fallback_e:
            print("Fallback decode failed due to incorrect json format:", fallback_e)
            return None
        

def agent_output_process(resume):
# def agent_output_process():
    '''
    Run full agent pipeline
    '''



    # Run agent
    # from agent import run_agent
    output = run_agent(resume)
    # output = run_agent(doc_text)

    # Post-process or print
    print(output)  

    # parsing
    if output:
        output_dict = parse_json(output)
        print(output_dict)
    else:
        output_dict = None
        print('None object returned. ')

    # transform and output dataframe
    df = pd.DataFrame(output_dict)
    print(df)

    return df
    # # Assuming `doc_list` is your list of Document objects
    # with open("job_matches.csv", "w", newline='', encoding='utf-8') as f:
    #     writer = csv.DictWriter(f, fieldnames=output_dict[0].keys())
    #     writer.writeheader()
    #     writer.writerows(output_dict)
        
    # print("✅ CSV file 'job_matches.csv' created successfully.")


df = agent_output_process(resume)

# df.to_csv('output_test.csv')