import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Get API key from .env
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not set in environment variables")

# Create Gemini client (force correct API version)
client = genai.Client(
    api_key=api_key,
    http_options={"api_version": "v1"}
)


def generate_explanation(topic: str, context_chunks: list[str]) -> str:
    """
    Generates explanation using Gemini.
    Uses only retrieved textbook context.
    """

    try:
        if not context_chunks:
            return "No relevant content found."

        # Limit to top 3 chunks for stability
        context = "\n\n".join(context_chunks[:3])

        prompt = f"""
You are an AI Concept Coach, not a content generator.

Your goal is to help a student understand the topic step-by-step.

Rules:
- Use ONLY the textbook excerpts below.
- Do NOT introduce outside knowledge.
- Do NOT provide assignment-style final answers.
- Focus on conceptual clarity and reasoning.

Respond strictly in JSON format:

{{
  "definition": "...",
  "intuition": "...",
  "stepwise_explanation": [
    "Step 1: ...",
    "Step 2: ...",
    "Step 3: ..."
  ],
  "example": "...",
  "check_understanding_question": "Ask the student one conceptual question to test understanding."
}}

Textbook excerpts:
{context}

Explanation:
"""
        available_models = list(client.models.list())
        if not available_models:
            return "No models available."
        model_name = available_models[0].name

        response = client.models.generate_content(
            model=model_name,
            contents=prompt
        )

        import json
        import re

        raw_text = response.text.strip()

        clean_text = re.sub(r"^```json", "", raw_text)
        clean_text = re.sub(r"```$", "", clean_text)
        clean_text = clean_text.strip()

        try:
            return json.loads(clean_text)
        except Exception as e:
            print("Explanation JSON Parse Error:", e)
            print("Raw Explanation:", raw_text)
        return {
        "definition": raw_text,
        "intuition": "",
        "stepwise_explanation": [],
        "example": "",
        "check_understanding_question": ""
        }

    except Exception as e:
        # Prevent backend crash
        print("Gemini Error:", e)
        return "Explanation could not be generated at this time."
    
def generate_hint(topic: str, context_chunks: list[str], level: int):
    context = "\n\n".join(context_chunks[:3])

    hint_styles = {
        1: "Give only a subtle directional hint. Do NOT explain fully.",
        2: "Give a conceptual clue but do NOT reveal full reasoning.",
        3: "Give strong guidance but do NOT give final answer directly."
    }

    instruction = hint_styles.get(level, hint_styles[1])

    prompt = f"""
You are an AI Concept Coach.

Topic: {topic}

{instruction}

Use ONLY the textbook excerpts below.

Textbook excerpts:
{context}
"""

    available_models = list(client.models.list())
    model_name = available_models[0].name

    response = client.models.generate_content(
        model=model_name,
        contents=prompt
    )

    return response.text
def generate_quiz(topic: str, context_chunks: list[str]):
    """
    Generates structured quiz questions using Gemini.
    """

    if not context_chunks:
        return {"error": "No relevant content found."}

    context = "\n\n".join(context_chunks[:3])

    prompt = f"""
You are an AI Concept Coach.

Generate:
- 3 conceptual questions
- 2 application-based questions

about the topic "{topic}".

Use ONLY the textbook excerpts below.

Respond strictly in JSON format:

{{
  "conceptual": ["q1", "q2", "q3"],
  "application": ["q4", "q5"]
}}

Textbook excerpts:
{context}
"""

    available_models = list(client.models.list())
    model_name = available_models[0].name

    response = client.models.generate_content(
        model=model_name,
        contents=prompt
    )

    import json
    import re

    raw_text = response.text.strip()

    clean_text = re.sub(r"^```json|```$", "", raw_text).strip()

    try:
        return json.loads(clean_text)
    except Exception as e:
        print("JSON Parse Error:", e)
        print("Raw Response:", raw_text)
        return {"error": raw_text}

def evaluate_quiz(user_answers: list[str], correct_answers: list[str]):
    """
    Simple mastery evaluation.
    """

    if len(user_answers) != len(correct_answers):
        return {"error": "Answer count mismatch"}

    score = 0

    for user, correct in zip(user_answers, correct_answers):
        if user.strip().lower() in correct.lower():
            score += 1

    percentage = (score / len(correct_answers)) * 100

    if percentage >= 80:
        level = "Strong"
    elif percentage >= 50:
        level = "Moderate"
    else:
        level = "Needs Revision"

    return {
        "score": score,
        "total": len(correct_answers),
        "percentage": percentage,
        "mastery_level": level
    }