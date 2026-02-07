from fastapi import APIRouter
from app.utils.store import vector_store

router = APIRouter()

@router.post("/search-topic")
def search_topic(topic: str):
    results = vector_store.search(topic)
    return {
        "topic": topic,
        "results": results
    }
