import re

def clean_text(raw_text: str) -> str:
    """
    Cleans textbook text for AI processing
    """

    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', raw_text)

    # Remove page numbers (simple heuristic)
    text = re.sub(r'\n?\s*\d+\s*\n?', ' ', text)

    # Remove common footer/header patterns
    text = re.sub(r'Copyright.*?reserved\.', ' ', text, flags=re.IGNORECASE)

    # Normalize newlines
    text = text.replace('\n', ' ').strip()

    return text

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100):
    """
    Splits text into overlapping chunks
    """

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks
