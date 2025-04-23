from langchain.tools import StructuredTool
from pydantic import BaseModel

from src.query_engine import QueryEngine

template = """
    You are an assistant for job matching tasks. Based on how it align with the query (user's resume), order the retrieved jobs (context) and explain how you ranked. Returned a list of job titles of top 3 matches and their link. ”

    Resume: {resume}
    Jobs: {context} 
    Question: {question} 

    Answer:
    """


class JobMatchInput(BaseModel):
    resume: str
    question: str = "Which jobs match my education, skills and experience?"



job_match_tool = StructuredTool.from_function(
    name="JobMatch",
    description="Match resume to jobs with user demand.",
    func=lambda resume, question: QueryEngine(template, resume, question),
    args_schema=JobMatchInput
)



tools = [job_match_tool]