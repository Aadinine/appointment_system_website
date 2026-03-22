import os
import json
import pymongo
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# Connect to Atlas
connection_string = os.getenv("ATLAS_CONNECTION_STRING")
client = pymongo.MongoClient(connection_string)
db = client["appointment_system"]

# Load the new doctors from JSON file
with open('data/doctors.json', 'r') as f:
    doctors_data = json.load(f)

# Add doctors to Atlas collection
print("📥 Adding doctors to Atlas...")
added_count = 0
for doctor in doctors_data["specialists"]:
    try:
        # Add ObjectId for consistency
        doctor["_id"] = str(doctor.get("_id", f"doc_{datetime.now().timestamp()}"))
        
        # Insert into Atlas
        result = db["doctor"].insert_one(doctor.copy())
        print(f"✅ Added: {doctor['name']} - {doctor['specialty']}")
        added_count += 1
        
    except Exception as e:
        print(f"❌ Failed to add {doctor['name']}: {e}")

print(f"🎉 Successfully added {added_count} doctors to Atlas!")
print(f"📊 Total doctors in Atlas: {db['doctor'].count_documents({})}")

# Close connection
client.close()
