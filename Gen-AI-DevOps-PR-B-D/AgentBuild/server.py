from flask import Flask, request, jsonify, send_from_directory
from agent import run_agent

app = Flask(__name__)

@app.route("/")
def home():
    return send_from_directory("static", "index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    user_input = data.get("message", "")

    if not user_input:
        return jsonify({"response": "No input provided"}), 400

    reply = run_agent(user_input)
    return jsonify({"response": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

