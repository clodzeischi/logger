from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

def get_log_file():
    """Return the log file path for the current day."""
    date_str = datetime.utcnow().strftime("%Y-%m-%d")
    return f"{date_str}_audit.log"

@app.route("/audit", methods=["POST"])
def audit():
    try:
        data = request.get_json(force=True)
        timestamp = datetime.utcnow().isoformat()

        # Validate required fields
        required_fields = ["user", "app", "action", "entry", "result"]
        if not all(field in data for field in required_fields):
            log_file = get_log_file()
            with open(log_file, "a") as f:
                f.write(timestamp + ": Received incomplete logging request. \n")
            return jsonify({"error": "Missing required fields"}), 400

        # Build the audit message
        
        message = (
            f"{timestamp}: {data['user']} from the app {data['app']} attempted to "
            f"{data['action']} item {data['entry']}, resulting in Code {data['result']}"
        )

        # Append to log file
        log_file = get_log_file()
        with open(log_file, "a") as f:
            f.write(message + "\n")

        return jsonify({"status": "logged"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
