from fastapi import APIRouter, Query, HTTPException
from app.utils.store import vector_store
from app.utils.explainer import evaluate_quiz, generate_explanation, generate_hint, generate_quiz

router = APIRouter()


@router.post("/concept-coach")
def concept_coach(topic: str = Query(...)):

    try:
        chunks = vector_store.search(topic, k=5)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not chunks:
        return {"error": "No relevant content found for this topic."}

    # Generate guided explanation
    explanation = generate_explanation(topic, chunks)

    # Add reflection question
    reflection_question = (
        f"Think about this: Why is '{topic}' important in solving real-world engineering problems?"
    )

    return {
        "topic": topic,
        "guided_explanation": explanation,
        "reflection_question": reflection_question,
        "references": chunks[:3]
    }
@router.post("/hint")
def get_hint(topic: str, level: int):
    chunks = vector_store.search(topic)
    hint = generate_hint(topic, chunks, level)
    return {"hint_level": level, "hint": hint}

@router.post("/generate-quiz")
def create_quiz(topic: str):
    chunks = vector_store.search(topic)
    quiz = generate_quiz(topic, chunks)
    return {"topic": topic, "quiz": quiz}

@router.post("/evaluate-quiz")
def evaluate(user_answers: list[str], correct_answers: list[str]):
    result = evaluate_quiz(user_answers, correct_answers)
    return result