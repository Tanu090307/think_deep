from fastapi import APIRouter, UploadFile, File
from app.utils.text_processing import clean_text, chunk_text
from app.utils.store import vector_store
import fitz  # PyMuPDF

router = APIRouter()


@router.post("/upload-book")
def upload_book(file: UploadFile = File(...)):

    # Optional: Skip rebuilding if index already exists
    if vector_store.load_index():
        return {
            "message": "Index already exists. Skipping rebuild."
        }

    if not file.filename.endswith(".pdf"):
        return {"error": "Only PDF files are allowed"}

    pdf_bytes = file.file.read()
    text = ""

    with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()

    cleaned_text = clean_text(text)
    chunks = chunk_text(cleaned_text)

    print("Total chunks before limiting:", len(chunks))

    # 🔥 Development limit (increase from 150)
    chunks = chunks[:600]

    print("Total chunks after limiting:", len(chunks))

    if not chunks:
        return {"error": "No readable text found in PDF"}

    vector_store.build_index(chunks)

    return {
        "filename": file.filename,
        "chunks_indexed": len(chunks),
        "preview_chunk": chunks[0][:150]
    }

