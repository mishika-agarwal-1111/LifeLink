import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client
import os

app = Flask(__name__)
CORS(app)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SECRET_KEY = os.getenv("SUPABASE_SECRET_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_SECRET_KEY)

app_data = {
    "bloodBanks": [],
    "hospitals": [],
    "donors": [],
    "requests": [],
    "alerts": []
}

@app.route("/api/migrate-hospitals", methods=["POST"])
def migrate_hospitals():
    try:
        with open(os.path.join(os.path.dirname(__file__), "hospitals.json"), "r", encoding="utf-8") as file:
            hospitals = json.load(file)

        for hospital in hospitals:
            data = {
                "id": hospital["id"],
                "name": hospital["name"],
                "city": hospital["city"],
                "distance_km": hospital["dist"],
                "blood_need": hospital["needs"],
                "verified": hospital["verified"]
            }

            supabase.table("hospitals").upsert(data).execute()

        return jsonify({
            "status": "success",
            "migrated": len(hospitals)
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "service": "LifeLink Python API",
        "database": "Supabase PostgreSQL"
    })


@app.route("/api/data", methods=["GET"])
def get_data():
    return jsonify(app_data)


@app.route("/api/data", methods=["POST"])
def save_data():
    global app_data

    data = request.get_json()

    if data is None:
        return jsonify({
            "error": "No JSON data received"
        }), 400

    app_data = data

    return jsonify({
        "status": "saved",
        "message": "LifeLink data saved successfully"
    })


@app.route("/api/reset", methods=["POST"])
def reset_data():
    global app_data

    app_data = {
        "bloodBanks": [],
        "hospitals": [],
        "donors": [],
        "requests": [],
        "alerts": []
    }

    return jsonify({
        "status": "reset",
        "message": "LifeLink data has been reset"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
