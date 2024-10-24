from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_session
from .pdf_processing import extract_text_from_pdf
from .crud import create_pdf, get_pdf_by_id
from .nlp_processing import answer_question

app = FastAPI()

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...), session: Session = Depends(get_session)):
    file_location = f"pdfs/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(file.file.read())

    #extract text from pdf
    text_content = "extract_text_from_pdf(file_location)"

    #store pdf metadata and extracted text in database
    pdf_metadata = await create_pdf(session, filename=file.filename, text_content=text_content)

    return { "filename": file.filename, "id": pdf_metadata.id }


@app.post("/ask-question/{pdf_id}")
async def ask_question(pdf_id: int, question: str, session: Session = Depends(get_session)):
    pdf = await get_pdf_by_id(session, pdf_id)
    
    if not pdf:
        raise HTTPException(status_code=404, detail="PDF not found")
    
    # Use LangChain to answer the question based on the PDF content
    answer = answer_question(pdf.text_content, question)
    
    return {"question": question, "answer": answer}