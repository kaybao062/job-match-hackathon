# backend/main.py

from fastapi import FastAPI
from utils.supabase_client import supabase
from output_agent import agent_output_process_from_bytes

app = FastAPI()

@app.get("/resume/{user_id}")
def get_resume(user_id: str):
    file_path = f"{user_id}/resume.docx"  # Adjust as needed

    try:
        file_response = supabase.storage.from_("user-resume").download(file_path)
        
        df = agent_output_process_from_bytes(file_response)
        return {
            "success": True,
            "data": fdf.to_dict() if df is not None else None  # or stream/download it as needed
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# def get_resume2(user_id: str):
#     file_path = f"{user_id}/resume.docx"  # Adjust as needed

#     try:
#         file_response = supabase.storage.from_("user-resume").create_signed_url(file_path, 60)
#         signed_url = file_response.get("signedURL")
        
#         if not signed_url:
#             raise ValueError("Failed to generate signed URL")
#         return {
#             "success": True,
#             "url": signed_url
#         }
#     except Exception as e:
#         return {
#             "success": False,
#             "error": str(e)
#         }