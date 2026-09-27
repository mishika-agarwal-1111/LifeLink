import os
import json
from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SECRET_KEY = os.getenv("SUPABASE_SECRET_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_SECRET_KEY)

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

print(f"Blood bank migration completed: {len(blood_banks)} banks")
