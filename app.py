from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Any
import uvicorn

from summarization import run


app = FastAPI(title="Simple Summarization API",
    version="1.0.0",)

class SummaryResponse(BaseModel):
    summary: str = Field(..., description="The summarized text of the uploaded document.")

@app.post("/upload/", response_model=SummaryResponse)
async def upload_file(file: UploadFile = File(...)) -> SummaryResponse:
    """
    Uploads a .txt document and returns its summary if the document's size is within acceptable bounds.

    - **file**: UploadFile - A .txt file containing the document to be summarized.

    ### Response
    - **summary**: str - The summarized text of the uploaded document.
    """
    if not file.filename.endswith('.txt'):
        raise HTTPException(status_code=400, detail="File format not supported. Please upload a .txt file.")
    
    content = await file.read()
    text_to_process = content.decode("utf-8").strip()

    min_length, max_length = 100, 100000
    if len(text_to_process) < min_length:
        raise HTTPException(status_code=400, detail=f"Document too short. Summarization of that short document wouldn't make any sense. Minimum length is {min_length} characters.")
    if len(text_to_process) > max_length:
        raise HTTPException(status_code=400, detail=f"Document too long. Maximum length is {max_length} characters.")

    summary = run(text_to_process)
    
    return SummaryResponse(summary=summary)
