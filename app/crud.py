from sqlalchemy.future import select
from .models import PDFDocument

async def create_pdf(session, filename: str, text_content: str = None):
    new_pdf = PDFDocument(filename=filename, text_content=text_content)
    session.add(new_pdf)
    await session.commit()
    await session.refresh(new_pdf)
    return new_pdf

async def get_pdf_by_id(session, pdf_id: int):
    result = await session.execute(select(PDFDocument).filter(PDFDocument.id == pdf_id))
    return result.scalars().first()