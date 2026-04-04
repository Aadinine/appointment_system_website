from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify
from flask_session import Session
from pymongo import MongoClient
import pymongo
import os
from datetime import datetime, timedelta
import uuid
import hashlib
import secrets
import json
from dotenv import load_dotenv
from bson.objectid import ObjectId

def calculate_distance(lat1, lng1, lat2, lng2):
    """Calculate distance between two coordinates in kilometers"""
    from math import radians, sin, cos, sqrt, atan2
    
    # Convert latitude and longitude from degrees to radians
    lat1, lng1, lat2, lng2 = map(radians, [lat1, lng1, lat2, lng2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlng = lng2 - lng1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    
    # Earth's radius in kilometers
    R = 6371
    distance = R * c
    
    return round(distance, 1)

load_dotenv()

app = Flask(__name__)

# Configure session management
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

# Initialize Flask-Session
Session(app)

# MongoDB Atlas connection
def get_atlas_connection():
    try:
        client = pymongo.MongoClient(os.getenv("ATLAS_CONNECTION_STRING"))
        db = client["appointment_system"]
        print("[loaded from atlas]")
        return db
    except Exception as e:
        print(f"❌ Atlas connection failed: {e}")
        return None

# Load doctor data from Atlas or fallback to mock data
def load_doctor_data():
    try:
        atlas_db = get_atlas_connection()
        if atlas_db is not None:
            doctors = list(atlas_db["doctor"].find({"available": True}))
            # Convert ObjectId to string for JSON serialization
            for doctor in doctors:
                doctor['_id'] = str(doctor['_id'])
            print("[loaded doctors from atlas]")
            return {"specialists": doctors}
    except Exception as e:
        print(f"❌ Atlas doctor loading failed: {e}")
    
    # Fallback to mock data
    print("[using mock doctor data]")
    return doctor_data

# Mock doctor data for testing
doctor_data = {
    "specialists": [
        {
            "_id": "doc1",
            "name": "Dr. Smith",
            "specialty": "Cardiologist",
            "hospital": "City Hospital",
            "location": {
                "lat": 28.6139, 
                "lng": 77.2090,
                "address": "123 Main Street, Delhi",
                "phone": "+91-98765-43210"
            },
            "available": True
        },
        {
            "_id": "doc2", 
            "name": "Dr. Johnson",
            "specialty": "Dermatologist",
            "hospital": "General Hospital",
            "location": {
                "lat": 28.6139, 
                "lng": 77.2090,
                "address": "456 Park Avenue, Delhi",
                "phone": "+91-87654-32109"
            },
            "available": True
        },
        {
            "_id": "doc3", 
            "name": "Dr. Williams",
            "specialty": "Neurologist",
            "hospital": "Medical Center",
            "location": {
                "lat": 28.6139, 
                "lng": 77.2090,
                "address": "789 Health Road, Delhi",
                "phone": "+91-76543-21098"
            },
            "available": True
        },
        {
            "_id": "doc4", 
            "name": "Dr. Brown",
            "specialty": "Orthopedic",
            "hospital": "Bone & Joint Clinic",
            "location": {
                "lat": 28.6139, 
                "lng": 77.2090,
                "address": "321 Ortho Street, Delhi",
                "phone": "+91-65432-10987"
            },
            "available": True
        }
    ]
}

# User Authentication Functions
def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    """Verify password against hash"""
    return hashlib.sha256(password.encode()).hexdigest() == hashed

def create_user(name, email, password, phone):
    """Create a new user in MongoDB"""
    atlas_db = get_atlas_connection()
    if atlas_db is None:
        return False, "Database connection failed"
    
    # Check if user already exists
    existing_user = atlas_db["users"].find_one({"email": email})
    if existing_user:
        return False, "User already exists with this email"
    
    # Create new user
    user_data = {
        "name": name,
        "email": email,
        "password": hash_password(password),
        "phone": phone,
        "created_at": datetime.now(),
        "is_active": True
    }
    
    try:
        result = atlas_db["users"].insert_one(user_data)
        return True, str(result.inserted_id)
    except Exception as e:
        return False, str(e)

def authenticate_user(email, password):
    """Authenticate user credentials"""
    atlas_db = get_atlas_connection()
    if atlas_db is None:
        return None, "Database connection failed"
    
    user = atlas_db["users"].find_one({"email": email})
    if not user:
        return None, "Invalid email or password"
    
    if not user.get("is_active", True):
        return None, "Account is deactivated"
    
    if verify_password(password, user["password"]):
        # Convert ObjectId to string for session storage
        user["_id"] = str(user["_id"])
        # Remove password from user data before storing in session
        user.pop("password", None)
        return user, "Login successful"
    else:
        return None, "Invalid email or password"

def get_user_appointments(user_id):
    """Get all appointments for a specific user"""
    atlas_db = get_atlas_connection()
    if atlas_db is None:
        return []
    
    try:
        appointments = list(atlas_db["appointments"].find({"patient_email": user_id}).sort("appointment_date", 1))
        # Convert ObjectId to string for JSON serialization
        for appointment in appointments:
            appointment["_id"] = str(appointment["_id"])
            # Generate appointment ID for display
            appointment["appointment_id"] = str(appointment["_id"])[-6:].upper()
            # Keep original date for parsing, add formatted date for display
            original_date = appointment['appointment_date']
            appointment["formatted_date"] = datetime.strptime(appointment['appointment_date'], '%Y-%m-%d').strftime('%B %d, %Y')
            
            # Format cancelled_at date if it exists
            if appointment.get('cancelled_at'):
                cancelled_at = appointment['cancelled_at']
                if isinstance(cancelled_at, str):
                    cancelled_at = datetime.fromisoformat(cancelled_at.replace('Z', '+00:00'))
                appointment["cancelled_at_formatted"] = cancelled_at.strftime('%B %d, %Y at %I:%M %p')
            else:
                appointment["cancelled_at_formatted"] = None
        return appointments
    except Exception as e:
        print(f"❌ Error getting user appointments: {e}")
        return []

def login_required(f):
    """Decorator to require login for routes"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Please log in to access this page', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# AI Client Status
def check_ai_status():
    """Check which AI services are available"""
    ai_status = {}
    
    # Check Groq
    try:
        if os.getenv("GROQ_API_KEY"):
            ai_status["Groq"] = "✅ Available"
        else:
            ai_status["Groq"] = "❌ No API key"
    except:
        ai_status["Groq"] = "❌ Error"
    
    # Check Gemini
    try:
        if os.getenv("GEMINI_API_KEY"):
            ai_status["Gemini"] = "✅ Available"
        else:
            ai_status["Gemini"] = "❌ No API key"
    except:
        ai_status["Gemini"] = "❌ Error"
    
    # Check OpenAI
    try:
        if os.getenv("OPENAI_API_KEY"):
            ai_status["OpenAI"] = "✅ Available"
        else:
            ai_status["OpenAI"] = "❌ No API key"
    except:
        ai_status["OpenAI"] = "❌ Error"
    
    return ai_status

# Simple symptom analysis with AI service tracking
def analyze_symptoms(symptoms):
    """Smart symptom analysis with fallback and AI service tracking"""
    symptoms_lower = symptoms.lower()
    
    # Try to use actual AI services first
    ai_service_used = "Keyword Analysis"
    
    # Debug environment variables
    print(f"🔍 Environment Check - Groq: {'✅' if os.getenv('GROQ_API_KEY') else '❌'}")
    print(f"🔍 Environment Check - Gemini: {'✅' if os.getenv('GEMINI_API_KEY') else '❌'}")
    print(f"🔍 Environment Check - OpenAI: {'✅' if os.getenv('OPENAI_API_KEY') else '❌'}")
    
    # Check Groq first
    if os.getenv("GROQ_API_KEY"):
        try:
            from groq import Groq
            client = Groq(api_key=os.getenv("GROQ_API_KEY"))
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a medical AI assistant. Provide helpful, natural responses in JSON format only. Focus on the most likely specialty based on symptoms."},
                    {"role": "user", "content": f"""Analyze these symptoms: "{symptoms}"

Available specialties: Cardiologist, Dermatologist, Neurologist, Orthopedic, Pulmonologist, General Physician, Gastroenterologist, Ophthalmologist, ENT Specialist, Gynecologist, Pediatrician, Psychiatrist

Return JSON format: {{"specialty": "specialty_name", "category": "URGENT/ROUTINE/NORMAL", "reason": "detailed explanation", "timeline": "specific timeframe"}}"""}
                ],
                temperature=0.3,
                max_tokens=150
            )
            result = response.choices[0].message.content.strip()
            print(f"🤖 [Groq responded]: {result}")
            return result
        except Exception as e:
            print(f"❌ Groq failed: {e}")
    
    # Check Gemini
    if os.getenv("GEMINI_API_KEY"):
        try:
            import google.generativeai as genai
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(f"""You are a medical AI assistant. Provide helpful, natural responses in JSON format only. Focus on the most likely specialty based on symptoms.

Analyze these symptoms: "{symptoms}"

Available specialties: Cardiologist, Dermatologist, Neurologist, Orthopedic, Pulmonologist, General Physician, Gastroenterologist, Ophthalmologist, ENT Specialist, Gynecologist, Pediatrician, Psychiatrist

Return JSON format: {{"specialty": "specialty_name", "category": "URGENT/ROUTINE/NORMAL", "reason": "detailed explanation", "timeline": "specific timeframe"}}""")
            result = response.text.strip()
            print(f"🤖 [Gemini responded]: {result}")
            ai_service_used = "Google Gemini"
            return result
        except Exception as e:
            print(f"❌ Gemini failed: {e}")
            print(f"🔍 Gemini API Key: {os.getenv('GEMINI_API_KEY')[:10] if os.getenv('GEMINI_API_KEY') else 'None'}")
    
    # Check OpenAI
    if os.getenv("OPENAI_API_KEY"):
        try:
            import openai
            client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a medical AI assistant. Provide helpful, natural responses in JSON format only. Focus on the most likely specialty based on symptoms."},
                    {"role": "user", "content": f"""Analyze these symptoms: "{symptoms}"

Available specialties: Cardiologist, Dermatologist, Neurologist, Orthopedic, Pulmonologist, General Physician, Gastroenterologist, Ophthalmologist, ENT Specialist, Gynecologist, Pediatrician, Psychiatrist

Return JSON format: {{"specialty": "specialty_name", "category": "URGENT/ROUTINE/NORMAL", "reason": "detailed explanation", "timeline": "specific timeframe"}}"""}
                ],
                temperature=0.3,
            )
            result = response.choices[0].message.content.strip()
            print(f"🤖 [OpenAI responded]: {result}")
            ai_service_used = "OpenAI"
            return result
        except Exception as e:
            print(f"❌ OpenAI failed: {e}")
            print(f"🔍 OpenAI API Key: {os.getenv('OPENAI_API_KEY')[:10] if os.getenv('OPENAI_API_KEY') else 'None'}")
    
    print(f"🔍 All AI services failed, using keyword analysis. Service used: {ai_service_used}")
    print(f"🔍 Environment variables loaded: Groq={bool(os.getenv('GROQ_API_KEY'))}, Gemini={bool(os.getenv('GEMINI_API_KEY'))}, OpenAI={bool(os.getenv('OPENAI_API_KEY'))}")
    
    # Fallback to keyword analysis
    specialties = [
        {"name": "Cardiologist", "keywords": ["heart", "chest pain", "palpitations", "shortness of breath", "blood pressure"]},
        {"name": "Dermatologist", "keywords": ["skin", "rash", "acne", "eczema", "moles", "sunburn"]},
        {"name": "Neurologist", "keywords": ["headache", "migraine", "seizure", "dizziness", "memory loss", "stroke"]},
        {"name": "Orthopedic", "keywords": ["bone", "joint", "fracture", "arthritis", "sprain", "back pain"]},
        {"name": "Pulmonologist", "keywords": ["lungs", "breathing", "cough", "asthma", "pneumonia", "bronchitis"]},
        {"name": "General Physician", "keywords": ["fever", "cold", "flu", "general checkup", "routine", "health"]},
        {"name": "Gastroenterologist", "keywords": ["stomach", "digestion", "acid reflux", "ulcer", "liver", "gallbladder"]},
        {"name": "Ophthalmologist", "keywords": ["eye", "vision", "cataract", "glaucoma", "retina", "blindness"]},
        {"name": "ENT Specialist", "keywords": ["ear", "nose", "throat", "sinus", "tonsils", "hearing loss"]},
        {"name": "Gynecologist", "keywords": ["women", "pregnancy", "menstrual", "uterus", "ovarian", "breast"]},
        {"name": "Pediatrician", "keywords": ["child", "baby", "infant", "pediatric", "kids", "children"]},
        {"name": "Psychiatrist", "keywords": ["mental", "depression", "anxiety", "stress", "bipolar", "schizophrenia"]}
    ]
    
    # Keyword fallback with better explanations
    if any(word in symptoms_lower for word in ['chest', 'heart', 'breathing']):
        result = '{"specialty": "Cardiologist", "category": "URGENT", "reason": "Chest pain and breathing difficulties may indicate serious heart or lung conditions requiring immediate medical attention", "timeline": "Within 24 hours"}'
    elif any(word in symptoms_lower for word in ['skin', 'rash', 'acne']):
        result = '{"specialty": "Dermatologist", "category": "NORMAL", "reason": "Skin issues like rashes and acne can be effectively treated by a dermatology specialist", "timeline": "Within 1-2 weeks"}'
    elif any(word in symptoms_lower for word in ['brain', 'head', 'migraine', 'seizure']):
        result = '{"specialty": "Neurologist", "category": "URGENT", "reason": "Headaches, migraines and seizures require neurological evaluation to rule out serious conditions", "timeline": "Within 24 hours"}'
    elif any(word in symptoms_lower for word in ['bone', 'joint', 'back', 'fracture']):
        result = '{"specialty": "Orthopedic", "category": "ROUTINE", "reason": "Bone, joint and back problems need orthopedic specialist evaluation for proper treatment", "timeline": "Within 3-7 days"}'
    elif any(word in symptoms_lower for word in ['lung', 'breathing', 'asthma', 'cough']):
        result = '{"specialty": "Pulmonologist", "category": "ROUTINE", "reason": "Respiratory symptoms including cough and asthma need lung specialist evaluation", "timeline": "Within 3-7 days"}'
    elif any(word in symptoms_lower for word in ['fever', 'cold', 'flu']):
        result = '{"specialty": "General Physician", "category": "ROUTINE", "reason": "Fever and cold symptoms can be managed by primary care physician", "timeline": "Within 3-7 days"}'
    elif any(word in symptoms_lower for word in ['stomach', 'digestive', 'acid', 'liver']):
        result = '{"specialty": "Gastroenterologist", "category": "ROUTINE", "reason": "Stomach and digestive issues require gastroenterology specialist for proper diagnosis", "timeline": "Within 3-7 days"}'
    elif any(word in symptoms_lower for word in ['eye', 'vision', 'cataract', 'glaucoma']):
        result = '{"specialty": "Ophthalmologist", "category": "ROUTINE", "reason": "Eye problems and vision changes need ophthalmology specialist evaluation", "timeline": "Within 1-2 weeks"}'
    elif any(word in symptoms_lower for word in ['ear', 'nose', 'throat', 'sinus']):
        result = '{"specialty": "ENT Specialist", "category": "ROUTINE", "reason": "Ear, nose and throat problems need ENT specialist for comprehensive care", "timeline": "Within 3-7 days"}'
    elif any(word in symptoms_lower for word in ['pregnancy', 'menstrual', 'women', 'fertility']):
        result = '{"specialty": "Gynecologist", "category": "ROUTINE", "reason": "Women\'s health issues including pregnancy and menstrual problems need gynecology care", "timeline": "Within 1-2 weeks"}'
    elif any(word in symptoms_lower for word in ['child', 'pediatric', 'baby', 'vaccine']):
        result = '{"specialty": "Pediatrician", "category": "ROUTINE", "reason": "Child health issues and vaccinations need pediatric specialist for age-appropriate care", "timeline": "Within 3-7 days"}'
    elif any(word in symptoms_lower for word in ['mental', 'depression', 'anxiety', 'stress']):
        result = '{"specialty": "Psychiatrist", "category": "URGENT", "reason": "Mental health concerns including depression and anxiety need immediate psychiatric evaluation", "timeline": "Within 24 hours"}'
    else:
        result = '{"specialty": "General Physician", "category": "ROUTINE", "reason": "General symptoms can be evaluated and treated by primary care physician", "timeline": "Within 3-7 days"}'
    
    print(f"🤖 [Keyword Analysis]: {result}")
    return result

# Routes
@app.route('/')
def home():
    print("🏠 Home route accessed")
    if 'user' in session:
        print("🔄 Redirecting to dashboard - user is logged in")
        return redirect(url_for('dashboard'))
    
    print("🏠 Showing homepage - user not logged in")
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        
        # Basic validation
        if not name or not email or not password or not phone:
            flash('All fields are required', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long', 'error')
            return render_template('register.html')
        
        success, message = create_user(name, email, password, phone)
        
        if success:
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash(f'Registration failed: {message}', 'error')
            return render_template('register.html')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        if not email or not password:
            flash('Email and password are required', 'error')
            return render_template('login.html')
        
        user, message = authenticate_user(email, password)
        
        if user:
            session['user'] = user
            flash(f'Welcome back, {user["name"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash(f'Login failed: {message}', 'error')
            return render_template('login.html')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out successfully', 'info')
    return redirect(url_for('home'))

@app.route('/health')
def health_check():
    """Health check endpoint for Railway deployment"""
    try:
        return jsonify({
            "status": "healthy",
            "service": "appointment-system",
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard showing their appointments"""
    user = session['user']
    user_id = user['email']
    
    # Get user's appointments
    appointments = get_user_appointments(user_id)
    
    # Separate upcoming and past appointments
    upcoming_appointments = []
    past_appointments = []
    
    for appointment in appointments:
        appointment_date = datetime.strptime(appointment['appointment_date'], '%Y-%m-%d').date()
        appointment_time = datetime.strptime(appointment['time_slot'], '%H:%M').time()
        current_datetime = datetime.now()
        current_time = current_datetime.time()
        current_date = current_datetime.date()
        
        # Debug logging
        print(f"🔍 Appointment Debug:")
        print(f"  Appointment Date: {appointment_date}")
        print(f"  Appointment Time: {appointment_time}")
        print(f"  Current Date: {current_date}")
        print(f"  Current Time: {current_time}")
        print(f"  Appointment Status: {appointment.get('status')}")
        
        # Check if appointment is today and time has passed
        if appointment_date == current_date:
            print(f"  📅 Appointment is today")
            if appointment_time >= current_time:
                print(f"  ⏰ Appointment time is in the future")
                if appointment.get('status') == 'cancelled':
                    print(f"  ❌ Appointment is cancelled - moving to past")
                    past_appointments.append(appointment)
                else:
                    print(f"  ✅ Appointment is upcoming")
                    upcoming_appointments.append(appointment)
            else:
                print(f"  ⏰ Appointment time has passed - moving to past")
                past_appointments.append(appointment)
        elif appointment_date > current_date:
            print(f"  📅 Appointment is in the future")
            if appointment.get('status') != 'cancelled':
                print(f"  ✅ Appointment is upcoming")
                upcoming_appointments.append(appointment)
            else:
                print(f"  ❌ Cancelled appointment - moving to past")
                past_appointments.append(appointment)
        else:
            print(f"  📅 Appointment is in the past - moving to past")
            past_appointments.append(appointment)
    
    return render_template('dashboard.html', 
                         user=user, 
                         upcoming_appointments=upcoming_appointments,
                         past_appointments=past_appointments)

@app.route('/book', methods=['GET', 'POST'])
@login_required
def book():
    if request.method == 'POST':
        symptoms = request.form['symptoms']
        user = session['user']
        name = user['name']
        ai_result = analyze_symptoms(symptoms)
        
        try:
            ai_data = json.loads(ai_result)
            doctors = load_doctor_data()
            # Find doctors matching recommended specialty
            recommended_specialty = ai_data.get("specialty", "General Physician")
            nearby_doctors = [doc for doc in doctors["specialists"] if doc["specialty"] == recommended_specialty]
            
            # If no doctors match the specialty, show all available doctors
            if not nearby_doctors:
                nearby_doctors = doctors["specialists"]
                print(f"⚠️ No doctors found for {recommended_specialty}, showing all {len(nearby_doctors)} available doctors")
            else:
                print(f"✅ Found {len(nearby_doctors)} doctors matching {recommended_specialty}")
            
            # Calculate distances for all doctors
            user_lat = 28.6139  # Delhi coordinates
            user_lng = 77.2090
            for doctor in nearby_doctors:
                if "location" in doctor and "lat" in doctor["location"] and "lng" in doctor["location"]:
                    doctor["distance"] = calculate_distance(user_lat, user_lng, doctor["location"]["lat"], doctor["location"]["lng"])
                else:
                    doctor["distance"] = 0
            
            # Sort doctors by distance (ascending)
            nearby_doctors.sort(key=lambda x: x.get("distance", float('inf')))
            
            return render_template('result.html', name=name, symptoms=symptoms, ai=ai_result, 
                                 ai_data=ai_data, nearby_doctors=nearby_doctors, user_location={"lat": 28.6139, "lng": 77.2090})
        except Exception as e:
            print(f"❌ Error parsing AI result: {e}")
            return render_template('result.html', name=name, symptoms=symptoms, ai=ai_result, ai_data=None)
    
    doctors = load_doctor_data()
    return render_template('book.html', specialists=doctors["specialists"])

@app.route('/specialists')
def specialists():
    doctors = load_doctor_data()
    return render_template('specialists.html', specialists=doctors["specialists"], user_location={"lat": 28.6139, "lng": 77.2090})

@app.route('/booking/<doctor_id>')
@login_required
def booking(doctor_id):
    """Show booking page for specific doctor"""
    doctors = load_doctor_data()
    doctor = next((doc for doc in doctors["specialists"] if doc["_id"] == doctor_id), None)
    
    if not doctor:
        flash('Doctor not found', 'error')
        return redirect(url_for('specialists'))
    
    user = session['user']
    return render_template('booking.html', doctor=doctor, user=user)

@app.route('/confirm_booking', methods=['POST'])
@login_required
def confirm_booking():
    """Confirm and save appointment booking"""
    user = session['user']
    
    # Get form data
    doctor_id = request.form.get('doctor_id')
    doctor_name = request.form.get('doctor_name')
    hospital = request.form.get('hospital')
    specialty = request.form.get('specialty', '')
    appointment_date = request.form.get('appointment_date')
    time_slot = request.form.get('time_slot')
    symptoms = request.form.get('symptoms', '')
    
    # Validate required fields
    if not all([doctor_id, doctor_name, hospital, appointment_date, time_slot]):
        flash('Please fill all required fields', 'error')
        return redirect(url_for('book'))
    
    try:
        # Save appointment to database
        atlas_db = get_atlas_connection()
        if atlas_db is not None:
            appointment_data = {
                "patient_email": user['email'],
                "patient_name": user['name'],
                "patient_phone": user['phone'],
                "doctor_id": doctor_id,
                "doctor_name": doctor_name,
                "hospital": hospital,
                "specialty": specialty,
                "appointment_date": appointment_date,
                "time_slot": time_slot,
                "symptoms": symptoms,
                "status": "confirmed",
                "created_at": datetime.now()
            }
            
            result = atlas_db["appointments"].insert_one(appointment_data)
            appointment_id = str(result.inserted_id)[-6:].upper()  # Last 6 digits, all caps
            
            # Add appointment_id to the database record
            atlas_db["appointments"].update_one(
                {"_id": result.inserted_id},
                {"$set": {"appointment_id": appointment_id}}
            )
            
            flash('Appointment booked successfully!', 'success')
            return render_template('confirmation.html', 
                                appointment=appointment_data, 
                                appointment_id=appointment_id)
        else:
            flash('Database connection error', 'error')
            return redirect(url_for('book'))
            
    except Exception as e:
        print(f"❌ Booking error: {e}")
        flash('Booking failed. Please try again.', 'error')
        return redirect(url_for('book'))

@app.route('/get_time_slots/<doctor_id>/<date>')
@login_required
def get_time_slots(doctor_id, date):
    """API endpoint to get available time slots for a doctor on a specific date"""
    try:
        # Validate date format
        if not date:
            return jsonify({"error": "Date is required"}), 400
        
        # Get current time
        now = datetime.now()
        selected_date = datetime.strptime(date, '%Y-%m-%d')
        
        # Don't allow booking for past dates
        if selected_date.date() < now.date():
            return jsonify({"error": "Cannot book appointments in the past"}), 400
        
        # Get existing appointments for this doctor and date
        atlas_db = get_atlas_connection()
        booked_slots = []
        if atlas_db is not None:
            try:
                appointments = list(atlas_db["appointments"].find({
                    "doctor_id": doctor_id,
                    "appointment_date": date,
                    "status": {"$ne": "cancelled"}  # Exclude cancelled appointments
                }))
                booked_slots = [apt["time_slot"] for apt in appointments]
            except:
                booked_slots = []
        
        # Generate time slots (9 AM to 9 PM, half-hour intervals)
        time_slots = []
        for hour in range(9, 22):  # 9 AM to 9 PM (last slot 20:30)
            for minute in [0, 30]:  # :00 and :30
                time_str = f"{hour:02d}:{minute:02d}"
                
                # Skip lunch break slots (12:30-14:00)
                if hour == 12 and minute == 30:
                    continue
                if hour == 13:
                    continue
                
                # Create datetime for this slot
                slot_datetime = datetime.strptime(f"{date} {time_str}", '%Y-%m-%d %H:%M')
                
                # Check if this slot is in the past (today)
                is_past = slot_datetime < now
                
                # Check if this slot is before current time on same day
                is_before_current_time = False
                if selected_date.date() == now.date() and slot_datetime <= now:
                    is_before_current_time = True
                
                # Check if this slot is already booked
                is_booked = time_str in booked_slots
                
                # Additional check: prevent double booking by checking if slot was recently booked by someone else
                is_double_booking = False
                if is_booked:
                    # Check if this slot was booked in the last 5 minutes (to prevent race conditions)
                    recent_appointments = list(atlas_db["appointments"].find({
                        "doctor_id": doctor_id,
                        "appointment_date": date,
                        "time_slot": time_str,
                        "created_at": {"$gte": (datetime.now() - timedelta(minutes=5)).isoformat()}
                    }))
                    if recent_appointments:
                        is_double_booking = True
                
                # Determine status
                if is_past:
                    status = 'past'
                elif is_before_current_time:
                    status = 'unavailable'
                elif is_booked or is_double_booking:
                    status = 'booked'
                else:
                    status = 'available'
                
                time_slots.append({
                    "time": time_str,
                    "available": status == 'available',
                    "status": status
                })
        
        return jsonify({"time_slots": time_slots})
    except Exception as e:
        print(f"❌ Time slots error: {e}")
        return jsonify({"error": "Failed to load time slots", "details": str(e)}), 500

@app.route('/cancel_appointment/<appointment_id>', methods=['POST'])
@login_required
def cancel_appointment(appointment_id):
    """Cancel an appointment"""
    user = session['user']
    
    try:
        # Get appointment from database
        atlas_db = get_atlas_connection()
        if atlas_db is None:
            return jsonify({"success": False, "message": "Database connection error"})
        
        appointment = atlas_db["appointments"].find_one({"_id": ObjectId(appointment_id)})
        
        if not appointment or appointment["patient_email"] != user['email']:
            return jsonify({"success": False, "message": "Appointment not found"})
        
        # Check if appointment is in the future (can only cancel upcoming appointments)
        appointment_datetime = datetime.strptime(f"{appointment['appointment_date']} {appointment['time_slot']}", '%Y-%m-%d %H:%M')
        if appointment_datetime <= datetime.now():
            return jsonify({"success": False, "message": "Cannot cancel past appointments"})
        
        # Update appointment status to cancelled
        result = atlas_db["appointments"].update_one(
            {"_id": ObjectId(appointment_id)},
            {"$set": {"status": "cancelled", "cancelled_at": datetime.now()}}
        )
        
        if result.modified_count > 0:
            print(f"✅ Appointment {appointment_id} cancelled by user {user['email']}")
            return jsonify({"success": True, "message": "Appointment cancelled successfully"})
        else:
            return jsonify({"success": False, "message": "Failed to cancel appointment"})
            
    except Exception as e:
        print(f"❌ Error cancelling appointment: {e}")
        return jsonify({"success": False, "message": "An error occurred while cancelling appointment"})

@app.route('/appointment_bill/<appointment_id>')
@login_required
def appointment_bill(appointment_id):
    """Show appointment bill/receipt"""
    user = session['user']
    
    try:
        # Get appointment from database
        atlas_db = get_atlas_connection()
        if atlas_db is None:
            flash('Database connection error', 'error')
            return redirect(url_for('dashboard'))
        
        appointment = atlas_db["appointments"].find_one({"_id": ObjectId(appointment_id)})
        
        if not appointment or appointment["patient_email"] != user['email']:
            flash('Appointment not found', 'error')
            return redirect(url_for('dashboard'))
        
        # Get doctor specialty from doctor data
        doctors = load_doctor_data()
        doctor = next((doc for doc in doctors["specialists"] if doc["_id"] == appointment["doctor_id"]), None)
        specialty = doctor["specialty"] if doctor else "Not specified"
        
        # Convert ObjectId to string and format
        appointment["_id"] = str(appointment["_id"])
        appointment["appointment_id"] = str(appointment["_id"])[-6:].upper()
        appointment["appointment_date"] = datetime.strptime(appointment['appointment_date'], '%Y-%m-%d').strftime('%B %d, %Y')
        
        # Format cancelled_at date if it exists
        if appointment.get('cancelled_at'):
            # Handle both string and datetime formats
            cancelled_at = appointment['cancelled_at']
            if isinstance(cancelled_at, str):
                cancelled_at = datetime.fromisoformat(cancelled_at.replace('Z', '+00:00'))
            appointment["cancelled_at_formatted"] = cancelled_at.strftime('%B %d, %Y at %I:%M %p')
        else:
            appointment["cancelled_at_formatted"] = None
        
        appointment["specialty"] = specialty
        
        return render_template('appointment_bill.html', appointment=appointment)
        
    except Exception as e:
        print(f"❌ Error loading appointment bill: {e}")
        flash('Error loading appointment details', 'error')
        return redirect(url_for('dashboard'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Starting appointment system on port {port}...")
    
    try:
        # Simple startup for Railway
        app.run(host='0.0.0.0', port=port, debug=False)
    except Exception as e:
        print(f"❌ Failed to start app: {e}")
        # Try to start with minimal configuration
        app.run(host='0.0.0.0', port=port, debug=False)
