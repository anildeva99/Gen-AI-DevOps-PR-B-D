from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Day40 - AI Orchestrated CI/CD Pipeline Running Successfully!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
