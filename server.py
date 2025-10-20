from flask import Flask, request, jsonify
from datetime import datetime
import random

app = Flask(__name__)

# -----------------------------
# Helper: Prime check
# -----------------------------
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# -----------------------------
# 1️⃣ Fixed-pattern GET
# -----------------------------
@app.route('/ping', methods=['GET'])
def ping_get():
    minutes = datetime.now().minute
    if minutes % 4 == 0:
        return jsonify({"error": "Bad request"}), 400
    elif minutes % 5 == 0:
        return jsonify({"error": "Internal server error"}), 500
    else:
        return jsonify({"received": "pong"}), 200

# 1️⃣ Fixed-pattern POST
@app.route('/ping-post', methods=['POST'])
def ping_post_fixed():
    minutes = datetime.now().minute
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 415
    data = request.get_json()

    if minutes % 4 == 0:
        return jsonify({"error": "Bad request"}), 400
    elif minutes % 5 == 0:
        return jsonify({"error": "Internal server error"}), 500
    else:
        return jsonify({"received": data, "status": "pong"}), 200


# -----------------------------
# 2️⃣ Randomized GET
# -----------------------------
@app.route('/ping-random', methods=['GET'])
def ping_random_get():
    minutes = datetime.now().minute
    chance = random.random()

    if chance < 0.1:
        return jsonify({"error": f"Bad request (chance={chance:.2f})"}), 400
    elif chance < 0.15:
        return jsonify({"error": f"Internal server error (chance={chance:.2f})"}), 500
    else:
        return jsonify({"received": f"pong at minute {minutes}"}), 200

# 2️⃣ Randomized POST
@app.route('/ping-random-post', methods=['POST'])
def ping_random_post():
    minutes = datetime.now().minute
    chance = random.random()
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 415
    data = request.get_json()

    if chance < 0.1:
        return jsonify({"error": f"Bad request (chance={chance:.2f})"}), 400
    elif chance < 0.15:
        return jsonify({"error": f"Internal server error (chance={chance:.2f})"}), 500
    else:
        return jsonify({"received": data, "chance": chance, "status": f"pong at minute {minutes}"}), 200


# -----------------------------
# 3️⃣ Dynamic Prime + Random GET
# -----------------------------
@app.route('/ping-dynamic', methods=['GET'])
def ping_dynamic_get():
    minutes = datetime.now().minute
    chance = random.random()
    if is_prime(minutes) or chance < 0.05:
        code = 500 if chance < 0.03 else 400
        return jsonify({
            "error": f"Unstable response at minute {minutes} (chance={chance:.2f})"
        }), code
    return jsonify({"received": f"pong at minute {minutes}"}), 200

# 3️⃣ Dynamic Prime + Random POST
@app.route('/ping-dynamic-post', methods=['POST'])
def ping_dynamic_post():
    minutes = datetime.now().minute
    chance = random.random()
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 415
    data = request.get_json()

    if is_prime(minutes) or chance < 0.05:
        code = 500 if chance < 0.03 else 400
        return jsonify({
            "error": f"Unstable response at minute {minutes} (chance={chance:.2f})"
        }), code

    return jsonify({"received": data, "status": f"pong at minute {minutes}"}), 200


# -----------------------------
# POST with Header Validation
# -----------------------------
@app.route('/pingHeader', methods=['POST'])
def ping_post_header():
    expected_header = "client-key"
    expected_value = "secret-key"

    header_value = request.headers.get(expected_header)
    if header_value != expected_value:
        return jsonify({"error": f"Missing or invalid {expected_header}"}), 400

    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 415

    data = request.get_json()
    return jsonify({"received": data, "header": header_value}), 200


# -----------------------------
# Global error handler
# -----------------------------
@app.errorhandler(Exception)
def handle_exceptions(e):
    return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(port=5000, debug=True)