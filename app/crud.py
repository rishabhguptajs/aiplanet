from sqlalchemy.future import select
from .models import PDFDocument

async def create_pdf(session, filename: str, text_content: str = None):
    """
    Create a new PDF document and save it to the database.

    Args:
        session: The database session to use for the operation.
        filename (str): The name of the PDF file.
        text_content (str, optional): The content of the PDF. Defaults to None.

    Returns:
        PDFDocument: The newly created PDF document instance.
    """
    # Create a new PDFDocument instance
    new_pdf = PDFDocument(filename=filename, text_content=text_content)
    
    # Add the new PDF document to the session
    session.add(new_pdf)
    
    # Commit the session to save the new document to the database
    await session.commit()
    
    # Refresh the instance to get the latest data from the database
    await session.refresh(new_pdf)
    
    return new_pdf

async def get_pdf_by_id(session, pdf_id: int):
    """
    Retrieve a PDF document by its ID.

    Args:
        session: The database session to use for the operation.
        pdf_id (int): The ID of the PDF document to retrieve.

    Returns:
        PDFDocument: The PDF document instance if found, otherwise None.
    """
    # Execute a query to select the PDF document with the given ID
    result = await session.execute(select(PDFDocument).filter(PDFDocument.id == pdf_id))
    
    # Return the first matching PDF document or None if not found
    return result.scalars().first()