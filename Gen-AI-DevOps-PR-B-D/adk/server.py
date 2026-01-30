import os
from flask import Flask, request, jsonify, send_from_directory
import vertexai
from vertexai.generative_models import GenerativeModel

app = Flask(__name__, static_folder="static")

PROJECT_ID = os.environ.get("PROJECT_ID", "testadi-459816")
REGION = "us-central1"

vertexai.init(project=PROJECT_ID, location=REGION)
model = GenerativeModel("models/gemini-2.0-flash")


# Serve browser UI
@app.route("/")
def index():
    return send_from_directory("static", "index.html")


# API endpoint
@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    response = model.generate_content(
        f"You are a DevOps assistant.\nUser: {user_message}"
    )

    return jsonify({"response": response.text})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

