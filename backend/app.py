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
@app.route("/api/migrate-blood-banks", methods=["POST"])
@app.route("/api/migrate-donors", methods=["POST"])
def migrate_donors():
    try:
        with open(os.path.join(os.path.dirname(__file__), "donors.json"), "r", encoding="utf-8") as file:
            donors = json.load(file)

        for donor in donors:
            donor_data = {
                "id": donor["id"],
                "name": donor["name"],
                "blood_group": donor["group"],
                "city": donor["city"],
                "available": donor["available"],
                "last_donation": donor["lastDonation"]
            }

            supabase.table("donors").upsert(donor_data).execute()

        return jsonify({
            "status": "success",
            "migrated": len(donors)
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
def migrate_blood_banks():
    try:
        with open(os.path.join(os.path.dirname(__file__), "blood_banks.json"), "r", encoding="utf-8") as file:
            blood_banks = json.load(file)

        for bank in blood_banks:
            bank_data = {
                "id": bank["id"],
                "name": bank["name"],
                "city": bank["city"],
                "verified": bank["verified"]
            }

            supabase.table("blood_banks").upsert(bank_data).execute()

            inventory = bank.get("inventory", {})

            for blood_group, units in inventory.items():
                inventory_data = {
                    "blood_bank_id": bank["id"],
                    "blood_group": blood_group,
                    "units": units
                }

                supabase.table("blood_inventory").upsert(
                    inventory_data
                ).execute()

        return jsonify({
            "status": "success",
            "migrated": len(blood_banks)
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
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
    hospitals = supabase.table("hospitals").select("*").execute().data
    blood_banks = supabase.table("blood_banks").select("*").execute().data
    inventory_rows = supabase.table("blood_inventory").select("*").execute().data
    donors = supabase.table("donors").select("*").execute().data
    requests = supabase.table("blood_requests").select("*").execute().data
    alerts = supabase.table("alerts").select("*").execute().data

    inventory_map = {}

    for row in inventory_rows:
        bank_id = row["blood_bank_id"]
        group = row["blood_group"]
        units = row["units"]

        if bank_id not in inventory_map:
            inventory_map[bank_id] = {}

        inventory_map[bank_id][group] = units

    formatted_banks = []

    for bank in blood_banks:
        formatted_banks.append({
            "id": bank["id"],
            "name": bank["name"],
            "city": bank["city"],
            "dist": [4, 11, 7, 18, 3, 14, 9, 22, 6, 16, 28, 12, 35, 8, 19, 25, 5, 31, 13, 21, 10, 27, 17, 33, 15, 24, 38, 20, 29, 42, 7, 34, 11, 26, 18, 45, 9, 23, 32, 14, 37, 6, 28, 16, 41, 12, 30, 21, 36][len(formatted_banks)],
            "inventory": inventory_map.get(bank["id"], {}),
            "verified": bank["verified"]
        })

    formatted_hospitals = []

    for hospital in hospitals:
        formatted_hospitals.append({
            "id": hospital["id"],
            "name": hospital["name"],
            "city": hospital["city"],
            "dist": hospital["distance_km"] or 0,
            "needs": hospital["blood_need"],
            "verified": hospital["verified"]
        })

    return jsonify({
        "banks": formatted_banks,
        "hospitals": formatted_hospitals,
        "donors": donors,
        "requests": requests,
        "alerts": alerts,
        "transfers": [],
        "expiryUnits": [],
        "notifications": [],
        "activity": [],
        "sos": [],
        "myDonor": 1
    })
@app.route("/api/data", methods=["POST"])
def save_data():
    data = request.get_json()

    if not data:
        return jsonify({
            "status": "error",
            "message": "No data received"
        }), 400

    return jsonify({
        "status": "received",
        "message": "Data received by LifeLink API"
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
