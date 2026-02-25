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
You are an AI Concept Coach.

Using ONLY the textbook excerpts below, explain the topic "{topic}"
clearly and simply for an undergraduate engineering student.

Structure your response as:
1. Definition
2. Step-by-step explanation
3. Simple example
4. Common misconception (if applicable)

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

        return response.text

    except Exception as e:
        # Prevent backend crash
        print("Gemini Error:", e)
        return "Explanation could not be generated at this time."