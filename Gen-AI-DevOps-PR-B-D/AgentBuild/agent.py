from vertexai import init
from vertexai.generative_models import GenerativeModel

init(project="testadi-459816", location="us-central1")

MODEL_NAME = "models/gemini-2.0-flash"

model = GenerativeModel(MODEL_NAME)

def run_agent(user_input: str) -> str:
    try:
        response = model.generate_content(user_input)
        return response.text or "No response"
    except Exception as e:
        return f"ERROR: {str(e)}"

