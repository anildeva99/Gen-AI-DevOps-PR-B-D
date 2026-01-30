import os

def review_pr_with_gemini(files, diff):
    api_key = os.environ.get("GOOGLE_API_KEY")

    if not api_key:
        return "❌ GOOGLE_API_KEY missing. Skipping AI review."

    try:
        import google.generativeai as genai

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = f"""
Review the following GitHub Pull Request.

Files:
{files}

Diff:
{diff}

Provide:
- Summary
- Risks
- Bugs
- Security issues
- Suggestions
"""

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"❌ Gemini error: {str(e)}"
