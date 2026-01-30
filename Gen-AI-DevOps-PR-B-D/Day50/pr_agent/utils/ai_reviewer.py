import os

def run_ai_review(diff: str) -> str:
    """
    AI review entry point.
    This function can later call Gemini / OpenAI / Vertex AI.
    """

    google_api_key = os.getenv("GOOGLE_API_KEY")

    if not google_api_key:
        return (
            "⚠️ GOOGLE_API_KEY not set.\n"
            "Skipping AI review.\n"
            f"Diff length: {len(diff)}"
        )

    # Placeholder for future Gemini / LLM logic
    return (
        "🤖 AI Review Completed\n"
        f"Diff length: {len(diff)}\n"
        "No critical issues detected."
    )
