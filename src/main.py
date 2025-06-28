# backend/main.py

from fastapi import FastAPI
from utils.supabase_client import supabase

app = FastAPI()

@app.get("/resume/{user_id}")
def get_resume(user_id: str):
    file_path = f"{user_id}/resume.docx"  # Adjust as needed

    try:
        file_response = supabase.storage.from_("user-resume").download(file_path)
        return {
            "success": True,
            "content": file_response.decode("utf-8")  # or stream/download it as needed
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }