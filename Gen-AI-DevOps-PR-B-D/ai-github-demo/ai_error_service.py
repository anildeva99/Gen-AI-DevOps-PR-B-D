from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/analyze", methods=["POST"])
def analyze_log():
    try:
        logs = request.data.decode("utf-8")

        # Check for ZeroDivisionError
        if "ZeroDivisionError" in logs:
            return jsonify({
                "status": "error_detected",
                "issue": "ZeroDivisionError",
                "root_cause": "Code attempts to divide a number by zero.",
                "suggested_fix": "Ensure the divisor is not zero before dividing."
            }), 200

        return jsonify({
            "status": "no_error_detected",
            "details": "Log analyzed successfully."
        }), 200

    except Exception as e:
        return jsonify({
            "status": "failed",
            "error": str(e)
        }), 500


# IMPORTANT: Run on 0.0.0.0 so Cloud Shell preview can access it
if __name__ == "__main__":
    print("🚀 AI Error Service starting on port 5000...")
    app.run(host="0.0.0.0", port=5000)

