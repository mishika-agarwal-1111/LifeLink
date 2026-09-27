import os
import json
from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SECRET_KEY = os.getenv("SUPABASE_SECRET_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_SECRET_KEY)

with open("hospitals.json", "r", encoding="utf-8") as file:
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

print("Hospital migration completed successfully.")
