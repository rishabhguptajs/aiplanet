from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import get_session
from .pdf_processing import extract_text_from_pdf
from .crud import create_pdf, get_pdf_by_id
from .nlp_processing import answer_question
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...), session: Session = Depends(get_session)):
    # Ensure the 'pdfs' directory exists
    os.makedirs("pdfs", exist_ok=True)
    
    file_location = f"pdfs/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(file.file.read())

    text_content = extract_text_from_pdf(file_location)

    pdf_metadata = await create_pdf(session, filename=file.filename, text_content=text_content)

    return {"filename": file.filename, "id": pdf_metadata.id}


@app.post("/ask-question/{pdf_id}")
async def ask_question(pdf_id: int, question: str = Body(..., embed=True), session: Session = Depends(get_session)):
    if not isinstance(question, str) or not question.strip():
        raise HTTPException(status_code=422, detail=[{
            "type": "string_type",
            "loc": ["body"],
            "msg": "Input should be a valid string",
            "input": {"question": question}
        }])
    
    pdf = await get_pdf_by_id(session, pdf_id)
    
    if not pdf:
        raise HTTPException(status_code=404, detail="PDF not found")
    
    answer = answer_question(pdf.text_content, question)
    
    return {"question": question, "answer": answer}