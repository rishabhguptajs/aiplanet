# Project Title

A brief description of your project goes here. This project is a FastAPI application that allows users to upload PDF files, extract text from them, and ask questions based on the extracted content.

## Features

- Upload PDF files
- Extract text from PDF documents
- Ask questions about the content of the PDFs
- Asynchronous database interactions using SQLAlchemy
- Integration with OpenRouter API for answering questions

## Requirements

- Python 3.7+
- FastAPI
- SQLAlchemy
- PyMuPDF
- Asyncpg
- Requests
- Dotenv

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and add your environment variables:
   ```plaintext
   POSTGRES_URL=<your_postgres_url>
   OPENROUTER_API_KEY=<your_openrouter_api_key>
   ```

## Usage

1. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
   ```

2. Access the API documentation at `http://127.0.0.1:8000/docs`.

3. Use the `/upload-pdf/` endpoint to upload a PDF file and extract its text.

4. Use the `/ask-question/{pdf_id}` endpoint to ask questions about the uploaded PDF.

## Frontend Instructions

1. ```bash
   cd frontend
   ```

2. ```bash
    npm install
    ```

3. ```bash
    npm start
    ```

4. Access the frontend at `http://localhost:3000/`.

Thank you for exploring this project!