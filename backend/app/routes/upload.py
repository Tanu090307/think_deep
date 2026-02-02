from fastapi import APIRouter, UploadFile, File
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

    return {
        "filename": file.filename,
        "characters_extracted": len(text),
        "preview": text[:500]
    }
