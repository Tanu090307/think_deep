from fastapi import APIRouter, Query, HTTPException
from app.utils.store import vector_store
from app.utils.explainer import generate_explanation

router = APIRouter()


@router.post("/search-topic")
def search_topic(topic: str = Query(...)):

    chunks = vector_store.search(topic, k=5)

    print("DEBUG chunks:", type(chunks), chunks)

    if not chunks:
        return {"error": "No results found"}

    explanation = generate_explanation(topic, chunks)

    return {
        "topic": topic,
        "explanation": explanation,
        "references": chunks[:3]
    }
