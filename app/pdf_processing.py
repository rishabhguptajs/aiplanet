import fitz  # Import the PyMuPDF library for PDF processing

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts text from a PDF file.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        str: The extracted text from the PDF.
    """
    doc = fitz.open(pdf_path)  # Open the PDF file
    text = ""  # Initialize an empty string to hold the extracted text

    # Iterate through each page in the PDF
    for page in doc:
        text += page.get_text()  # Append the text from the current page

    return text  # Return the complete extracted text