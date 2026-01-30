import os
from flask import Flasking
#testing
app = Flask(__name__)

@app.route("/")
def home():
    return "Day38 Cloud Run Deployment Successful!"

@app.route("/test")
def test():
    return "Test route OK!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

