from fastapi import APIRouter, HTTPException, File, UploadFile 
from .services import generate_response_api, generate_response_local

router = APIRouter( 
   prefix="/api",  
   tags=["VLM Chat API"]  
) 

@router.get("/")
async def root():
    """Root endpoint for the VLM Chat API"""
    return {"message": "VLM Chat API", "status": "running"}

@router.post("/generate-response-local", status_code=200, response_model=dict)
async def generate_response_local(input_img: UploadFile = File(...), query: str, chat_history: str):
    """Generate response using local model"""
    try:
        result = generate_response_local(input_img, query, True, chat_history)
        if result["db_insert"] != "Successfully inserted log":
            raise HTTPException(status_code=500, detail=result["db_insert"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-response-api", status_code=200, response_model=dict)
async def generate_response_api(input_img: UploadFile = File(...), query: str, chat_history: str):
    """Generate response using HF Inference API"""
    try:
        result = generate_response_api(input_img, query, False, chat_history)
        if result["db_insert"] != "Successfully inserted log":
            raise HTTPException(status_code=500, detail=result["db_insert"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))