from fastapi import FastAPI, Request
from data_processing import your_processing_function
from output_agent import your_output_function

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API is working"}

@app.post("/process")
def process_data(data: dict):
    result = your_processing_function(data)
    return {"result": result}

@app.post("/output")
def output_response(data: dict):
    response = your_output_function(data)
    return {"response": response}
