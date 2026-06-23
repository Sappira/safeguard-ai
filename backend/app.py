import json
import sys
import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from risk_engine import run_risk_scan
from rag_agent import answer_safety_query

FRONTEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frontend")
app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")
CORS(app)

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")


def load_json(filename):
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, "r") as f:
        return json.load(f)


def load_sensor_data(inject_critical_zone=None):
    sys.path.append(DATA_DIR)
    from sensor_simulation import get_all_zone_readings
    return get_all_zone_readings(inject_critical_zone=inject_critical_zone)


@app.route("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "running", "system": "SafeGuard AI"})


@app.route("/api/risk-scan", methods=["GET"])
def risk_scan():
    critical_zone = request.args.get("inject_critical")
    sensor_readings = load_sensor_data(inject_critical_zone=critical_zone)
    permits = load_json("permits.json")
    shifts = load_json("shift_logs.json")
    results = run_risk_scan(sensor_readings, permits, shifts)
    return jsonify(results)


@app.route("/api/sensor-readings", methods=["GET"])
def sensor_readings():
    critical_zone = request.args.get("inject_critical")
    readings = load_sensor_data(inject_critical_zone=critical_zone)
    return jsonify(readings)


@app.route("/api/permits", methods=["GET"])
def permits():
    data = load_json("permits.json")
    return jsonify(data)


@app.route("/api/ask", methods=["POST"])
def ask_copilot():
    body = request.get_json()
    question = body.get("question", "").strip()
    if not question:
        return jsonify({"error": "Question cannot be empty"}), 400
    result = answer_safety_query(question)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, port=5000)