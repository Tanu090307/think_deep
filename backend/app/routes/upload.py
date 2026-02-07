from fastapi import APIRouter, UploadFile, File
from app.utils.text_processing import clean_text, chunk_text
from app.utils.store import vector_store
import fitz  # PyMuPDF

router = APIRouter()


@router.post("/upload-book")
async def upload_book(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        return {"error": "Only PDF files are allowed"}

    pdf_bytes = await file.read()
    text = ""

    with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()

    cleaned_text = clean_text(text)
    chunks = chunk_text(cleaned_text)
    vector_store.build_index(chunks)

    return {
    "filename": file.filename,
    "chunks_indexed": len(chunks),
    "preview_chunk": chunks[0][:500]
}
