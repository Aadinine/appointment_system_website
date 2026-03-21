# MongoDB Atlas Setup Script
# Run this once to populate your Atlas database

import pymongo
import json
import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB Atlas connection string
# Get this from your Atlas dashboard: "Connect" → "Connect your application"
ATLAS_CONNECTION_STRING = os.getenv("ATLAS_CONNECTION_STRING", "mongodb+srv://username:password@cluster.mongodb.net/")

def setup_atlas_database():
    try:
        # Connect to MongoDB Atlas
        client = pymongo.MongoClient(ATLAS_CONNECTION_STRING)
        
        # Create/use database
        db = client["appointment_system"]
        
        # Create/use collection
        doctors_collection = db["doctor"]
        
        # Load current doctor data
        with open('data/doctors.json', 'r') as f:
            doctor_data = json.load(f)
        
        # Clear existing data and insert new data
        doctors_collection.delete_many({})
        doctors_collection.insert_many(doctor_data["specialists"])
        
        print(f"✅ Successfully inserted {len(doctor_data['specialists'])} doctors into Atlas!")
        
        # Verify insertion
        count = doctors_collection.count_documents({})
        print(f"📊 Total doctors in Atlas: {count}")
        
        # Show sample data
        print("\n📋 Sample doctor from Atlas:")
        sample = doctors_collection.find_one()
        print(f"Name: {sample['name']}")
        print(f"Specialty: {sample['specialty']}")
        print(f"Hospital: {sample['hospital']}")
        
        client.close()
        
    except Exception as e:
        print(f"❌ Error setting up Atlas: {e}")
        print("\n📝 Make sure to:")
        print("1. Set up MongoDB Atlas account")
        print("2. Create a cluster")
        print("3. Get your connection string")
        print("4. Add ATLAS_CONNECTION_STRING to .env file")

if __name__ == "__main__":
    setup_atlas_database()
