import os
import json
import pymongo
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Connect to Atlas
connection_string = os.getenv("ATLAS_CONNECTION_STRING")
client = pymongo.MongoClient(connection_string)
db = client["appointment_system"]

print("🧹 Cleaning up duplicate doctors in Atlas...")

# Get all doctors currently in Atlas
existing_doctors = list(db["doctor"].find({}))
print(f"📊 Found {len(existing_doctors)} doctors in Atlas")

# Load our master doctor data
with open('data/doctors.json', 'r') as f:
    master_doctors = json.load(f)

print(f"📋 Master data has {len(master_doctors['specialists'])} doctors")

# Remove duplicates from Atlas
removed_count = 0
for master_doctor in master_doctors["specialists"]:
    # Check if doctor already exists in Atlas
    existing = db["doctor"].find_one({
        "name": master_doctor["name"],
        "specialty": master_doctor["specialty"],
        "hospital": master_doctor["hospital"]
    })
    
    if existing:
        # Remove duplicate
        result = db["doctor"].delete_one({"_id": existing["_id"]})
        if result.deleted_count > 0:
            removed_count += 1
            print(f"🗑️ Removed duplicate: {master_doctor['name']} - {master_doctor['specialty']} at {master_doctor['hospital']}")
        else:
            print(f"⚠️ Could not remove: {master_doctor['name']} - {master_doctor['specialty']}")

print(f"🎉 Successfully removed {removed_count} duplicate doctors from Atlas!")

# Add unique doctors to Atlas
added_count = 0
for master_doctor in master_doctors["specialists"]:
    # Check if doctor already exists in Atlas
    existing = db["doctor"].find_one({
        "name": master_doctor["name"],
        "specialty": master_doctor["specialty"],
        "hospital": master_doctor["hospital"]
    })
    
    if not existing:
        # Add new doctor with unique ObjectId
        doctor_to_add = master_doctor.copy()
        doctor_to_add["_id"] = str(doctor_to_add.get("_id", f"doc_{datetime.now().timestamp()}"))
        
        result = db["doctor"].insert_one(doctor_to_add)
        if result.inserted_id:
            added_count += 1
            print(f"✅ Added: {doctor_to_add['name']} - {doctor_to_add['specialty']} at {doctor_to_add['hospital']}")
        else:
            print(f"❌ Failed to add: {doctor_to_add['name']}")

print(f"🎉 Successfully added {added_count} new doctors to Atlas!")

# Final count
final_count = db["doctor"].count_documents({})
print(f"📊 Final doctor count in Atlas: {final_count}")

# Close connection
client.close()
