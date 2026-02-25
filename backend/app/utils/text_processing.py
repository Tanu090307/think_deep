import re
import nltk

nltk.download("punkt")


def clean_text(text: str) -> str:
    #Cleans PDF-extracted textbook text.

    text = text.replace("-\n", "")
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"(C\s*H\s*A\s*P\s*T\s*E\s*R\s*\d+)", "", text)
    text = re.sub(r"\b\d{1,4}\b", "", text)
    text = re.sub(r"[\x00-\x1f\x7f-\x9f]", " ", text)

    return text.strip()


def chunk_text(
    text: str,
    max_length: int = 500,
    overlap: int = 100
):
    """
    Sentence-aware chunking with overlap.
    """

    sentences = nltk.sent_tokenize(text)

    chunks = []
    current_chunk = []

    current_length = 0

    for sentence in sentences:
        sentence_length = len(sentence)

        if current_length + sentence_length <= max_length:
            current_chunk.append(sentence)
            current_length += sentence_length
        else:
            # Save chunk
            chunk_text = " ".join(current_chunk)
            chunks.append(chunk_text)

            # Overlap logic
            overlap_sentences = []
            overlap_length = 0

            for sent in reversed(current_chunk):
                overlap_length += len(sent)
                overlap_sentences.insert(0, sent)
                if overlap_length >= overlap:
                    break

            current_chunk = overlap_sentences + [sentence]
            current_length = sum(len(s) for s in current_chunk)

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

