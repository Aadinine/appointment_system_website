# Setup Appointments Collection
# This script creates the appointments collection and adds some sample bookings

import pymongo
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

def setup_appointments_collection():
    try:
        # Connect to MongoDB Atlas
        client = pymongo.MongoClient(os.getenv("ATLAS_CONNECTION_STRING"))
        db = client["appointment_system"]
        
        # Get actual doctor IDs from Atlas
        doctors_collection = db["doctor"]
        doctors = list(doctors_collection.find({"available": True}))
        
        # Create appointments collection with sample data
        appointments_collection = db["appointments"]
        
        # Find Dr. Rajesh Kumar and Dr. Priya Sharma IDs
        dr_rajesh_id = None
        dr_priya_id = None
        
        for doctor in doctors:
            if "Rajesh Kumar" in doctor.get("name", ""):
                dr_rajesh_id = str(doctor["_id"])
            elif "Priya Sharma" in doctor.get("name", ""):
                dr_priya_id = str(doctor["_id"])
        
        # Sample appointments to demonstrate the booking system
        sample_appointments = []
        today = datetime.now().strftime("%Y-%m-%d")
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        
        if dr_rajesh_id:
            sample_appointments.extend([
                {
                    "appointment_id": "SAMPLE001",
                    "doctor_id": dr_rajesh_id,
                    "doctor_name": "Dr. Rajesh Kumar",
                    "hospital": "City General Hospital",
                    "specialty": "General Physician",
                    "patient_name": "John Doe",
                    "patient_email": "john.doe@email.com",
                    "patient_phone": "9876543210",
                    "appointment_date": tomorrow,
                    "time_slot": "09:00",
                    "symptoms": "Fever and headache",
                    "status": "confirmed",
                    "created_at": datetime.now().isoformat()
                },
                {
                    "appointment_id": "SAMPLE002",
                    "doctor_id": dr_rajesh_id,
                    "doctor_name": "Dr. Rajesh Kumar",
                    "hospital": "City General Hospital",
                    "specialty": "General Physician",
                    "patient_name": "Jane Smith",
                    "patient_email": "jane.smith@email.com",
                    "patient_phone": "9876543211",
                    "appointment_date": today,
                    "time_slot": "09:30",
                    "symptoms": "Regular checkup",
                    "status": "confirmed",
                    "created_at": datetime.now().isoformat()
                }
            ])
        
        if dr_priya_id:
            sample_appointments.append({
                "appointment_id": "SAMPLE003",
                "doctor_id": dr_priya_id,
                "doctor_name": "Dr. Priya Sharma",
                "hospital": "Apollo Hospital",
                "specialty": "Cardiologist",
                "patient_name": "Robert Johnson",
                "patient_email": "robert.j@email.com",
                "patient_phone": "9876543212",
                "appointment_date": today,
                "time_slot": "14:00",
                "symptoms": "Chest pain consultation",
                "status": "confirmed",
                "created_at": datetime.now().isoformat()
            })
        
        # Clear existing sample data and insert new samples
        appointments_collection.delete_many({"appointment_id": {"$regex": "^SAMPLE"}})
        if sample_appointments:
            appointments_collection.insert_many(sample_appointments)
        
        print(f"✅ Successfully created appointments collection with {len(sample_appointments)} sample bookings!")
        
        # Verify collection exists and show data
        count = appointments_collection.count_documents({})
        print(f"📊 Total appointments in Atlas: {count}")
        
        # Show sample appointments
        print("\n📋 Sample appointments:")
        for appointment in appointments_collection.find({"appointment_id": {"$regex": "^SAMPLE"}}):
            print(f"  - {appointment['appointment_id']}: {appointment['doctor_name']} - {appointment['appointment_date']} at {appointment['time_slot']} (Doctor ID: {appointment['doctor_id']})")
        
        client.close()
        
    except Exception as e:
        print(f"❌ Error setting up appointments collection: {e}")

if __name__ == "__main__":
    setup_appointments_collection()
