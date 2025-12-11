from fastapi import APIRouter, UploadFile, File, HTTPException
from app.schemas.bill import BillExtractionResponse
from app.services.llm_service import llm_service

router = APIRouter()

@router.post("/extract", response_model=BillExtractionResponse)
async def extract_bill(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        contents = await file.read()
        result = llm_service.extract_bill_data(contents)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
