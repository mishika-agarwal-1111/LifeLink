import os
import json
from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SECRET_KEY = os.getenv("SUPABASE_SECRET_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_SECRET_KEY)

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

print(f"Donor migration completed: {len(donors)} donors")
