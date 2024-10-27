from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

# Create a base class for declarative class definitions
Base = declarative_base()

class PDFDocument(Base):
    __tablename__ = 'pdf_documents'  # Name of the table in the database

    # Unique identifier for each PDF document
    id = Column(Integer, primary_key=True, index=True)
    
    # Name of the PDF file
    filename = Column(String, index=True)
    
    # Date and time when the PDF was uploaded, defaults to the current UTC time
    upload_date = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Text content extracted from the PDF
    text_content = Column(String)