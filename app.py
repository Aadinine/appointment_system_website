from flask import Flask, render_template, request
import google.generativeai as genai
import os
import json
import math
import pymongo
import uuid
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# MongoDB Atlas connection
def get_atlas_connection():
    try:
        client = pymongo.MongoClient(os.getenv("ATLAS_CONNECTION_STRING"))
        db = client["appointment_system"]
        return db
    except:
        # Fallback to JSON if Atlas is not available
        return None

# Load doctor data - try Atlas first, fallback to JSON
def load_doctor_data():
    atlas_db = get_atlas_connection()
    if atlas_db is not None:
        try:
            doctors = list(atlas_db["doctor"].find({"available": True}))
            # Convert ObjectId to string for JSON serialization
            for doctor in doctors:
                doctor['_id'] = str(doctor['_id'])
            print("[loaded from atlas]")
            return {"specialists": doctors}
        except:
            pass
    
    # Fallback to JSON file
    with open('data/doctors.json', 'r') as f:
        print("[loaded from json]")
        return json.load(f)

doctor_data = load_doctor_data()

# Generate time slots for a doctor
def generate_time_slots(doctor_id, date):
    # Standard clinic hours: 9:00 AM to 5:00 PM
    slots = []
    start_time = datetime.strptime("09:00", "%H:%M")
    end_time = datetime.strptime("17:00", "%H:%M")
    
    current_time = start_time
    while current_time < end_time:
        time_str = current_time.strftime("%H:%M")
        
        # Check if slot is already booked
        is_booked = is_time_slot_booked(doctor_id, date, time_str)
        
        # Check if slot is in the past
        is_past = is_time_slot_past(date, time_str)
        
        # Slot is available if not booked AND not in the past
        is_available = not is_booked and not is_past
        
        slots.append({
            "time": time_str,
            "available": is_available,
            "status": "booked" if is_booked else ("past" if is_past else "available")
        })
        
        # Add 30 minutes for each slot
        current_time += timedelta(minutes=30)
    
    return slots

# Check if a time slot is already booked
def is_time_slot_booked(doctor_id, date, time):
    atlas_db = get_atlas_connection()
    if atlas_db is not None:
        try:
            # Debug: Print the query parameters
            print(f"🔍 Checking booking for doctor_id: {doctor_id}, date: {date}, time: {time}")
            
            existing = atlas_db["appointments"].count_documents({
                "doctor_id": doctor_id,
                "appointment_date": date,
                "time_slot": time,
                "status": "confirmed"
            })
            
            print(f"📊 Found {existing} existing bookings for this slot")
            return existing > 0
        except Exception as e:
            # If appointments collection doesn't exist or other error, return False
            print(f"❌ Error checking booking: {e}")
            return False
    else:
        print("⚠️ Atlas connection not available")
        return False

# Check if a time slot is in the past
def is_time_slot_past(date, time):
    try:
        # Parse the appointment date and time
        appointment_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
        current_datetime = datetime.now()
        
        # Return True if the appointment time is in the past
        is_past = appointment_datetime < current_datetime
        print(f"⏰ Checking if {date} {time} is in the past: {is_past}")
        return is_past
    except Exception as e:
        print(f"❌ Error checking past time: {e}")
        return False

# Calculate distance between two coordinates (Haversine formula)
def calculate_distance(lat1, lng1, lat2, lng2):
    R = 6371  # Earth's radius in kilometers
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lng = math.radians(lng2 - lng1)
    
    a = (math.sin(delta_lat/2)**2 + 
         math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lng/2)**2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    return R * c

# Get user location (for demo, using Delhi center)
def get_user_location():
    # In production, you'd use browser geolocation API
    # For now, defaulting to Delhi center
    return {"lat": 28.6139, "lng": 77.2090, "address": "Delhi, India"}

# Sort doctors by distance from user
def get_nearby_doctors(specialty_name, user_location):
    nearby_doctors = []
    
    for doctor in doctor_data["specialists"]:
        if doctor["specialty"] == specialty_name and doctor.get("available", True):
            distance = calculate_distance(
                user_location["lat"], user_location["lng"],
                doctor["location"]["lat"], doctor["location"]["lng"]
            )
            doctor_with_distance = doctor.copy()
            doctor_with_distance["distance"] = round(distance, 2)
            nearby_doctors.append(doctor_with_distance)
    
    return sorted(nearby_doctors, key=lambda x: x["distance"])

# Setup Gemini
import google.generativeai as genai
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')

def analyze_symptoms(symptoms):
    specialties = list(set([doc["specialty"] for doc in doctor_data["specialists"]]))
    specialties_list = ", ".join(specialties)
    
    prompt = f"""
    Analyze these symptoms: "{symptoms}"
    
    Return ONLY this JSON format:
    {{"specialty": "specialty name", "category": "URGENT/ROUTINE/NORMAL", "reason": "one sentence", "timeline": "when to book"}}
    
    Available specialties: {specialties_list}
    """
    response = model.generate_content(prompt)
    text = response.text
    # Clean up JSON if needed
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0]
    return text

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/specialists')
def specialists():
    user_location = get_user_location()
    specialists_with_distance = []
    
    for specialist in doctor_data["specialists"]:
        if specialist["available"]:
            distance = calculate_distance(
                user_location["lat"], user_location["lng"],
                specialist["location"]["lat"], specialist["location"]["lng"]
            )
            specialist_copy = specialist.copy()
            specialist_copy["distance"] = round(distance, 2)
            specialists_with_distance.append(specialist_copy)
    
    # Sort by distance
    specialists_with_distance.sort(key=lambda x: x["distance"])
    
    return render_template('specialists.html', specialists=specialists_with_distance, user_location=user_location)

@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        symptoms = request.form['symptoms']
        name = request.form['name']
        ai_result = analyze_symptoms(symptoms)
        
        # Parse AI result to get specialty
        try:
            ai_data = json.loads(ai_result)
            user_location = get_user_location()
            nearby_doctors = get_nearby_doctors(ai_data.get("specialty", "General Physician"), user_location)
            
            return render_template('result.html', name=name, symptoms=symptoms, ai=ai_result, 
                                 ai_data=ai_data, nearby_doctors=nearby_doctors, user_location=user_location)
        except:
            return render_template('result.html', name=name, symptoms=symptoms, ai=ai_result, ai_data=None)
    
    return render_template('book.html', specialists=doctor_data["specialists"])

@app.route('/booking/<doctor_id>')
def booking(doctor_id):
    # Find doctor by ID
    doctor = None
    for specialist in doctor_data["specialists"]:
        if specialist["_id"] == doctor_id:
            doctor = specialist
            break
    
    if not doctor:
        return "Doctor not found", 404
    
    # Get today's date for default
    today = datetime.now().strftime("%Y-%m-%d")
    time_slots = generate_time_slots(doctor_id, today)
    
    return render_template('booking.html', doctor=doctor, time_slots=time_slots, today=today)

@app.route('/confirm_booking', methods=['POST'])
def confirm_booking():
    # Get form data
    doctor_id = request.form['doctor_id']
    doctor_name = request.form['doctor_name']
    hospital = request.form['hospital']
    patient_name = request.form['patient_name']
    patient_email = request.form['patient_email']
    patient_phone = request.form['patient_phone']
    appointment_date = request.form['appointment_date']
    time_slot = request.form['time_slot']
    symptoms = request.form.get('symptoms', '')
    
    # Check if the slot is already booked (server-side validation)
    if is_time_slot_booked(doctor_id, appointment_date, time_slot):
        # Slot is already booked, show error message
        return render_template('booking_error.html', 
                             doctor_name=doctor_name,
                             appointment_date=appointment_date,
                             time_slot=time_slot,
                             message="This time slot is already booked. Please choose a different time.")
    
    # Find doctor specialty
    doctor = None
    for specialist in doctor_data["specialists"]:
        if specialist["_id"] == doctor_id:
            doctor = specialist
            break
    
    # Generate appointment ID
    appointment_id = str(uuid.uuid4())[:8].upper()
    
    # Create appointment record
    appointment = {
        "appointment_id": appointment_id,
        "doctor_id": doctor_id,
        "doctor_name": doctor_name,
        "hospital": hospital,
        "specialty": doctor["specialty"] if doctor else "General Physician",
        "patient_name": patient_name,
        "patient_email": patient_email,
        "patient_phone": patient_phone,
        "appointment_date": appointment_date,
        "time_slot": time_slot,
        "symptoms": symptoms,
        "status": "confirmed",
        "created_at": datetime.now().isoformat()
    }
    
    # Save to Atlas
    atlas_db = get_atlas_connection()
    if atlas_db is not None:
        try:
            atlas_db["appointments"].insert_one(appointment)
        except:
            pass
    
    return render_template('confirmation.html', appointment=appointment)

@app.route('/get_time_slots/<doctor_id>/<date>')
def get_time_slots(doctor_id, date):
    time_slots = generate_time_slots(doctor_id, date)
    return {"time_slots": time_slots}

@app.route('/health')
def health_check():
    return {"status": "healthy", "message": "Backend is working!"}

@app.route('/debug')
def debug_info():
    return {
        "environment_variables": {
            "GEMINI_API_KEY": "✅ Set" if os.getenv("GEMINI_API_KEY") else "❌ Missing",
            "ATLAS_CONNECTION_STRING": "✅ Set" if os.getenv("ATLAS_CONNECTION_STRING") else "❌ Missing"
        },
        "database_connection": "✅ Connected" if get_atlas_connection() else "❌ Failed",
        "doctor_data_count": len(doctor_data.get("specialists", []))
    }

if __name__ == '__main__':
    app.run(debug=True)
else:
    # Production configuration for Vercel
    app.config['DEBUG'] = False

# Vercel serverless handler
def handler(environ, start_response):
    return app(environ, start_response)