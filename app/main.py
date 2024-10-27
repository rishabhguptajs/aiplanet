from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import get_session
from .pdf_processing import extract_text_from_pdf
from .crud import create_pdf, get_pdf_by_id
from .nlp_processing import answer_question
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI application
app = FastAPI()

# Configure CORS middleware to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...), session: Session = Depends(get_session)):
    """
    Endpoint to upload a PDF file.
    Saves the file to the 'pdfs' directory and extracts text content.
    """
    # Ensure the 'pdfs' directory exists
    os.makedirs("pdfs", exist_ok=True)
    
    # Define the file location for saving the uploaded PDF
    file_location = f"pdfs/{file.filename}"
    
    # Save the uploaded file to the specified location
    with open(file_location, "wb") as f:
        f.write(file.file.read())

    # Extract text content from the uploaded PDF
    text_content = extract_text_from_pdf(file_location)

    # Create a PDF record in the database with the extracted text
    pdf_metadata = await create_pdf(session, filename=file.filename, text_content=text_content)

    # Return the filename and the ID of the created PDF record
    return {"filename": file.filename, "id": pdf_metadata.id}


@app.post("/ask-question/{pdf_id}")
async def ask_question(pdf_id: int, question: str = Body(..., embed=True), session: Session = Depends(get_session)):
    """
    Endpoint to ask a question about a specific PDF.
    Validates the question and retrieves the answer based on the PDF's text content.
    """
    # Validate the question input
    if not isinstance(question, str) or not question.strip():
        raise HTTPException(status_code=422, detail=[{
            "type": "string_type",
            "loc": ["body"],
            "msg": "Input should be a valid string",
            "input": {"question": question}
        }])
    
    # Retrieve the PDF record by its ID
    pdf = await get_pdf_by_id(session, pdf_id)
    
    # Raise an error if the PDF is not found
    if not pdf:
        raise HTTPException(status_code=404, detail="PDF not found")
    
    # Get the answer to the question based on the PDF's text content
    answer = answer_question(pdf.text_content, question)
    
    # Return the question and the corresponding answer
    return {"question": question, "answer": answer}

# Bind the FastAPI application to a specific port
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)