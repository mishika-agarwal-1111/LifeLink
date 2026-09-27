from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import json
import os

app = Flask(__name__)
CORS(app)

DB_PATH = os.path.join(os.path.dirname(__file__), "lifelink.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS app_state (
            id INTEGER PRIMARY KEY,
            data TEXT NOT NULL
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM app_state")
    count = cursor.fetchone()[0]

    if count == 0:
        default_data = {
            "bloodBanks": [],
            "hospitals": [],
            "donors": [],
            "requests": [],
            "alerts": []
        }

        cursor.execute(
            "INSERT INTO app_state (id, data) VALUES (?, ?)",
            (1, json.dumps(default_data))
        )

    conn.commit()
    conn.close()


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "service": "LifeLink Python API",
        "database": "SQLite"
    })


@app.route("/api/data", methods=["GET"])
def get_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT data FROM app_state WHERE id = 1")
    row = cursor.fetchone()

    conn.close()

    if row:
        return jsonify(json.loads(row[0]))

    return jsonify({})


@app.route("/api/data", methods=["POST"])
def save_data():
    data = request.get_json()

    if data is None:
        return jsonify({
            "error": "No JSON data received"
        }), 400

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE app_state SET data = ? WHERE id = 1",
        (json.dumps(data),)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "status": "saved",
        "message": "LifeLink data saved successfully"
    })


@app.route("/api/reset", methods=["POST"])
def reset_data():
    default_data = {
        "bloodBanks": [],
        "hospitals": [],
        "donors": [],
        "requests": [],
        "alerts": []
    }

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE app_state SET data = ? WHERE id = 1",
        (json.dumps(default_data),)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "status": "reset",
        "message": "LifeLink data has been reset"
    })


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
