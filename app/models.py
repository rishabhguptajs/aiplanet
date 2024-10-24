from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class PDFDocument(Base):
    __tablename__ = 'pdf_documents'

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    upload_date = Column(DateTime, default=datetime.datetime.utcnow)
    text_content = Column(String)