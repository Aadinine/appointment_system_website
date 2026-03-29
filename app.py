from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_session import Session
from pymongo import MongoClient
import json
import os
import math
from datetime import datetime, timedelta
import uuid
import hashlib
import secrets
import pymongo
from dotenv import load_dotenv

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

# Railway-safe client initialization - more aggressive approach
def init_groq_client():
    """Initialize Groq client safely for Railway environment"""
    try:
        from groq import Groq
        import os
        
        # Save and clear ALL environment variables that might cause issues
        original_env = os.environ.copy()
        
        # Clear all proxy-related variables
        proxy_vars = ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 'ALL_PROXY', 'all_proxy', 'NO_PROXY', 'no_proxy']
        for var in proxy_vars:
            os.environ.pop(var, None)
        
        # Also clear any Groq-specific env vars that Railway might set
        groq_vars = [k for k in os.environ.keys() if k.lower().startswith('groq')]
        for var in groq_vars:
            os.environ.pop(var, None)
        
        try:
            # Try with minimal parameters
            client = Groq(api_key=os.getenv("GROQ_API_KEY"))
            return client
        except Exception as e1:
            print(f"❌ Groq init attempt 1 failed: {e1}")
            try:
                # Try without any parameters
                client = Groq()
                # Set API key as attribute if possible
                if hasattr(client, 'api_key'):
                    client.api_key = os.getenv("GROQ_API_KEY")
                return client
            except Exception as e2:
                print(f"❌ Groq init attempt 2 failed: {e2}")
                return None
        finally:
            # Restore environment
            os.environ.clear()
            os.environ.update(original_env)
            
    except Exception as e:
        print(f"❌ Groq init failed: {e}")
        return None

def init_openai_client():
    """Initialize OpenAI client safely for Railway environment"""
    try:
        import openai
        import os
        
        # Save and clear ALL environment variables that might cause issues
        original_env = os.environ.copy()
        
        # Clear all proxy-related variables
        proxy_vars = ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 'ALL_PROXY', 'all_proxy', 'NO_PROXY', 'no_proxy']
        for var in proxy_vars:
            os.environ.pop(var, None)
        
        # Also clear any OpenAI-specific env vars that Railway might set
        openai_vars = [k for k in os.environ.keys() if k.lower().startswith('openai')]
        for var in openai_vars:
            os.environ.pop(var, None)
        
        try:
            # Try with minimal parameters
            client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            return client
        except Exception as e1:
            print(f"❌ OpenAI init attempt 1 failed: {e1}")
            try:
                # Try without any parameters
                client = openai.OpenAI()
                # Set API key as attribute if possible
                if hasattr(client, 'api_key'):
                    client.api_key = os.getenv("OPENAI_API_KEY")
                return client
            except Exception as e2:
                print(f"❌ OpenAI init attempt 2 failed: {e2}")
                return None
        finally:
            # Restore environment
            os.environ.clear()
            os.environ.update(original_env)
            
    except Exception as e:
        print(f"❌ OpenAI init failed: {e}")
        return None

# Simple Groq initialization - bypass Railway proxy issues
groq_client = None
groq_available = False

def init_groq_simple():
    """Railway-safe Groq initialization"""
    try:
        from groq import Groq
        import os
        import sys
        
        # Debug: Check if API key exists
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            print("❌ GROQ_API_KEY not found in environment")
            return None
        
        print(f"🔑 GROQ_API_KEY found (length: {len(api_key)})")
        
        # Save original environment
        original_env = os.environ.copy()
        
        # Clear ALL environment variables that might interfere
        vars_to_clear = [
            'HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 
            'ALL_PROXY', 'all_proxy', 'NO_PROXY', 'no_proxy',
            'REQUESTS_CA_BUNDLE', 'CURL_CA_BUNDLE', 'SSL_CERT_FILE'
        ]
        
        # Also clear any variables that might contain proxy-related strings
        additional_vars = [k for k in os.environ.keys() if any(word in k.lower() for word in ['proxy', 'ca', 'cert', 'ssl'])]
        
        for var in vars_to_clear + additional_vars:
            if var in os.environ:
                del os.environ[var]
                print(f"🧹 Cleared environment variable: {var}")
        
        # Also clear any Groq-specific env vars that Railway might set EXCEPT the API key
        groq_vars = [k for k in os.environ.keys() if k.lower().startswith('groq') and k != 'GROQ_API_KEY']
        for var in groq_vars:
            if var in os.environ:
                del os.environ[var]
                print(f"🧹 Cleared Groq env var: {var}")
        
        try:
            print(f"🔧 Attempting to create Groq client with API key: {api_key[:10]}...")
            
            # Create a completely clean environment for the import
            import importlib
            importlib.reload(sys.modules.get('groq', sys.modules.get('groq._client', None)))
            
            client = Groq(api_key=api_key)
            print("✅ Groq client created successfully")
            return client
        except Exception as e:
            print(f"❌ Groq client creation failed: {type(e).__name__}: {str(e)}")
            print(f"❌ Full error details: {repr(e)}")
            
            # Try alternative approach - create client without any parameters
            try:
                print("🔄 Trying alternative Groq initialization...")
                
                # Clear environment again
                for var in vars_to_clear + additional_vars + groq_vars:
                    if var in os.environ:
                        del os.environ[var]
                
                client = Groq()
                print("✅ Groq client created without parameters")
                
                # Try to set API key through different methods
                if hasattr(client, 'api_key'):
                    client.api_key = api_key
                    print("✅ API key set via api_key attribute")
                elif hasattr(client, 'client'):
                    if hasattr(client.client, 'api_key'):
                        client.client.api_key = api_key
                        print("✅ API key set via client.api_key attribute")
                
                print("✅ Groq client created with alternative method")
                return client
            except Exception as e2:
                print(f"❌ Alternative Groq init failed: {type(e2).__name__}: {str(e2)}")
                print(f"❌ Full alternative error: {repr(e2)}")
                return None
        finally:
            # Restore original environment
            os.environ.clear()
            os.environ.update(original_env)
                
    except ImportError as e:
        print(f"❌ Groq library not installed: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected Groq init error: {e}")
        return None

# Try to initialize Groq as PRIMARY
try:
    if os.getenv("GROQ_API_KEY"):
        groq_client = init_groq_simple()
        if groq_client:
            groq_available = True
            print("✅ Groq available as PRIMARY service")
        else:
            groq_available = False
            print("❌ Groq failed to initialize")
    else:
        groq_available = False
        print("⚠️ Groq API key not found")
except Exception as e:
    groq_available = False
    print(f"❌ Groq error: {e}")

# OpenAI - keep disabled for now
openai_client = None
openai_available = False
print("❌ OpenAI disabled - focusing on Groq primary")

# Gemini as BACKUP - only initialize if Groq fails
gemini_available = False
if not groq_available:
    try:
        import google.generativeai as genai
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel('gemini-2.5-flash')
        # Test Gemini
        test_response = model.generate_content("test")
        if test_response.text:
            gemini_available = True
            print("✅ Gemini available as BACKUP service")
        else:
            gemini_available = False
            print("❌ Gemini test failed")
    except Exception as e:
        gemini_available = False
        print(f"❌ Gemini backup error: {e}")
else:
    print("ℹ️ Gemini backup not needed - Groq is working")

def get_groq_client():
    """Get Groq client - simple approach"""
    return groq_client is not None

def analyze_with_openai(symptoms):
    """Analyze symptoms using OpenAI GPT (better free tier)"""
    if not openai_available or not openai_client:
        return None
        
    try:
        specialties = list(set([doc["specialty"] for doc in doctor_data["specialists"]]))
        specialties_list = ", ".join(specialties)
        
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a medical AI assistant. Respond ONLY with valid JSON. No explanations, no examples, just JSON."},
                {"role": "user", "content": f"""Analyze symptoms: "{symptoms}"

Available specialties: {specialties_list}

Return JSON format: {{"specialty": "specialty_name", "category": "URGENT/ROUTINE/NORMAL", "reason": "brief explanation", "timeline": "when to book"}}"""}
            ],
            temperature=0.1
        )
        
        text = response.choices[0].message.content.strip()
        
        # Clean up JSON if needed
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].strip()
        
        # Ensure it's valid JSON
        if not text.startswith('{'):
            import re
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                text = json_match.group(0)
        
        print(f"🤖 OpenAI Response: {text}")
        return text
        
    except Exception as e:
        print(f"❌ OpenAI error: {e}")
        return None

def analyze_with_groq(symptoms):
    """Analyze symptoms using Groq (fast and reliable)"""
    # Initialize client if needed
    if not get_groq_client():
        return None
        
    try:
        specialties = list(set([doc["specialty"] for doc in doctor_data["specialists"]]))
        specialties_list = ", ".join(specialties)
        
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a medical AI assistant. Respond ONLY with valid JSON. No explanations, no examples, just JSON."},
                {"role": "user", "content": f"""Analyze symptoms: "{symptoms}"

Available specialties: {specialties_list}

Return JSON format: {{"specialty": "specialty_name", "category": "URGENT/ROUTINE/NORMAL", "reason": "brief explanation", "timeline": "when to book"}}"""}
            ],
            temperature=0.1,
            max_tokens=200
        )
        
        text = response.choices[0].message.content.strip()
        
        # Clean up JSON if needed
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].strip()
        
        # Ensure it's valid JSON
        if not text.startswith('{'):
            import re
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                text = json_match.group(0)
        
        print(f"🤖 Groq Response: {text}")
        return text
        
    except Exception as e:
        print(f"❌ Groq error: {e}")
        return None

def analyze_with_gemini(symptoms):
    """Analyze symptoms using Gemini (fallback)"""
    try:
        specialties = list(set([doc["specialty"] for doc in doctor_data["specialists"]]))
        specialties_list = ", ".join(specialties)
        
        prompt = f"""You are a JSON API. Respond ONLY with JSON.

Symptoms: "{symptoms}"
Available specialties: {specialties_list}

Return JSON format: {{"specialty": "specialty_name", "category": "URGENT/ROUTINE/NORMAL", "reason": "brief explanation", "timeline": "when to book"}}"""
        
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        # Clean up JSON if needed
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].strip()
        
        # Remove any leading/trailing text
        if not text.startswith('{'):
            import re
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                text = json_match.group(0)
        
        # If still not JSON, create fallback response
        if not text.startswith('{') or not text.endswith('}'):
            symptoms_lower = symptoms.lower()
            if any(word in symptoms_lower for word in ['chest', 'heart', 'breathing']):
                text = '{"specialty": "Cardiologist", "category": "URGENT", "reason": "Chest or heart symptoms require immediate evaluation", "timeline": "Within 24 hours"}'
            elif any(word in symptoms_lower for word in ['skin', 'rash', 'acne']):
                text = '{"specialty": "Dermatologist", "category": "NORMAL", "reason": "Skin conditions can be evaluated by dermatologist", "timeline": "Within 1-2 weeks"}'
            elif any(word in symptoms_lower for word in ['brain', 'head', 'migraine', 'seizure']):
                text = '{"specialty": "Neurologist", "category": "URGENT", "reason": "Neurological symptoms require specialist evaluation", "timeline": "Within 24 hours"}'
            elif any(word in symptoms_lower for word in ['bone', 'joint', 'back', 'fracture']):
                text = '{"specialty": "Orthopedic", "category": "ROUTINE", "reason": "Musculoskeletal issues need orthopedic evaluation", "timeline": "Within 3-7 days"}'
            elif any(word in symptoms_lower for word in ['lung', 'breathing', 'asthma', 'cough']):
                text = '{"specialty": "Pulmonologist", "category": "ROUTINE", "reason": "Respiratory symptoms need lung specialist evaluation", "timeline": "Within 3-7 days"}'
            else:
                text = '{"specialty": "General Physician", "category": "ROUTINE", "reason": "General symptoms can be evaluated by primary care", "timeline": "Within 3-7 days"}'
        
        print(f"🤖 Gemini Response: {text}")
        return text
        
    except Exception as e:
        print(f"❌ Gemini error: {e}")
        return None

def analyze_symptoms(symptoms):
    """Smart symptom analysis with Groq PRIMARY, Gemini BACKUP"""
    
    # Try Groq first as PRIMARY service
    groq_result = analyze_with_groq(symptoms)
    if groq_result:
        print("🎯 Using Groq as PRIMARY AI service")
        return groq_result
    
    # Use Gemini as BACKUP if Groq fails
    gemini_result = analyze_with_gemini(symptoms)
    if gemini_result:
        print("🔄 Using Gemini as BACKUP AI service")
        return gemini_result
    
    # Try OpenAI (disabled but keeping for structure)
    openai_result = analyze_with_openai(symptoms)
    if openai_result:
        return openai_result
    
    # Final keyword-based fallback (always works)
    print("🔄 Using keyword fallback as all AI services failed")
    symptoms_lower = symptoms.lower()
    if any(word in symptoms_lower for word in ['chest', 'heart', 'breathing']):
        return '{"specialty": "Cardiologist", "category": "URGENT", "reason": "Chest or heart symptoms require immediate evaluation", "timeline": "Within 24 hours"}'
    elif any(word in symptoms_lower for word in ['skin', 'rash', 'acne']):
        return '{"specialty": "Dermatologist", "category": "NORMAL", "reason": "Skin conditions can be evaluated by dermatologist", "timeline": "Within 1-2 weeks"}'
    elif any(word in symptoms_lower for word in ['brain', 'head', 'migraine', 'seizure']):
        return '{"specialty": "Neurologist", "category": "URGENT", "reason": "Neurological symptoms require specialist evaluation", "timeline": "Within 24 hours"}'
    elif any(word in symptoms_lower for word in ['bone', 'joint', 'back', 'fracture']):
        return '{"specialty": "Orthopedic", "category": "ROUTINE", "reason": "Musculoskeletal issues need orthopedic evaluation", "timeline": "Within 3-7 days"}'
    elif any(word in symptoms_lower for word in ['lung', 'breathing', 'asthma', 'cough']):
        return '{"specialty": "Pulmonologist", "category": "ROUTINE", "reason": "Respiratory symptoms need lung specialist evaluation", "timeline": "Within 3-7 days"}'
    elif any(word in symptoms_lower for word in ['fever', 'cold', 'flu']):
        return '{"specialty": "General Physician", "category": "ROUTINE", "reason": "Fever and cold symptoms can be evaluated by primary care", "timeline": "Within 3-7 days"}'
    elif any(word in symptoms_lower for word in ['stomach', 'digestive', 'acid', 'liver']):
        return '{"specialty": "Gastroenterologist", "category": "ROUTINE", "reason": "Digestive symptoms need gastroenterology evaluation", "timeline": "Within 3-7 days"}'
    elif any(word in symptoms_lower for word in ['eye', 'vision', 'cataract', 'glaucoma']):
        return '{"specialty": "Ophthalmologist", "category": "ROUTINE", "reason": "Eye and vision problems need ophthalmology evaluation", "timeline": "Within 1-2 weeks"}'
    elif any(word in symptoms_lower for word in ['ear', 'nose', 'throat', 'sinus']):
        return '{"specialty": "ENT Specialist", "category": "ROUTINE", "reason": "Ear, nose, and throat symptoms need ENT evaluation", "timeline": "Within 3-7 days"}'
    elif any(word in symptoms_lower for word in ['pregnancy', 'menstrual', 'women', 'fertility']):
        return '{"specialty": "Gynecologist", "category": "ROUTINE", "reason": "Women\'s health issues need gynecology evaluation", "timeline": "Within 1-2 weeks"}'
    elif any(word in symptoms_lower for word in ['child', 'pediatric', 'baby', 'vaccine']):
        return '{"specialty": "Pediatrician", "category": "ROUTINE", "reason": "Child health issues need pediatric evaluation", "timeline": "Within 3-7 days"}'
    elif any(word in symptoms_lower for word in ['mental', 'depression', 'anxiety', 'stress']):
        return '{"specialty": "Psychiatrist", "category": "ROUTINE", "reason": "Mental health issues need psychiatry evaluation", "timeline": "Within 1-2 weeks"}'
    else:
        return '{"specialty": "General Physician", "category": "ROUTINE", "reason": "General symptoms can be evaluated by primary care", "timeline": "Within 3-7 days"}'

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

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard showing their appointments"""
    user = session['user']
    user_id = user['email']  # Using email as user identifier for appointments
    
    # Get user's appointments
    appointments = get_user_appointments(user_id)
    
    # Separate upcoming and past appointments
    upcoming_appointments = []
    past_appointments = []
    
    for appointment in appointments:
        appointment_date = datetime.strptime(appointment['appointment_date'], '%Y-%m-%d')
        if appointment_date >= datetime.now().date():
            upcoming_appointments.append(appointment)
        else:
            past_appointments.append(appointment)
    
    return render_template('dashboard.html', 
                         user=user, 
                         upcoming_appointments=upcoming_appointments,
                         past_appointments=past_appointments)

@app.route('/')
def home():
    # Check if user is logged in
    if 'user' in session:
        return redirect(url_for('dashboard'))
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
@login_required
def book():
    if request.method == 'POST':
        symptoms = request.form['symptoms']
        user = session['user']
        name = user['name']  # Use logged-in user's name
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
@login_required
def confirm_booking():
    # Get logged-in user info
    user = session['user']
    
    # Get form data
    doctor_id = request.form['doctor_id']
    doctor_name = request.form['doctor_name']
    hospital = request.form['hospital']
    patient_name = user['name']  # Use logged-in user's name
    patient_email = user['email']  # Use logged-in user's email
    patient_phone = user['phone']  # Use logged-in user's phone
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
    import os
    
    # Get detailed Groq info
    groq_key = os.getenv("GROQ_API_KEY")
    groq_key_info = {
        "exists": "✅ Set" if groq_key else "❌ Missing",
        "length": len(groq_key) if groq_key else 0,
        "starts_with_gsk": groq_key.startswith("gsk_") if groq_key else False
    }
    
    # Check for proxy variables
    proxy_vars = ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 
                 'ALL_PROXY', 'all_proxy', 'NO_PROXY', 'no_proxy']
    proxy_info = {}
    for var in proxy_vars:
        if var in os.environ:
            proxy_info[var] = "✅ Set"
        else:
            proxy_info[var] = "❌ Not Set"
    
    return {
        "environment_variables": {
            "GEMINI_API_KEY": "✅ Set" if os.getenv("GEMINI_API_KEY") else "❌ Missing",
            "OPENAI_API_KEY": "✅ Set" if os.getenv("OPENAI_API_KEY") else "❌ Missing",
            "GROQ_API_KEY": groq_key_info,
            "ATLAS_CONNECTION_STRING": "✅ Set" if os.getenv("ATLAS_CONNECTION_STRING") else "❌ Missing"
        },
        "proxy_variables": proxy_info,
        "api_status": {
            "OpenAI": "✅ Available" if openai_available else "❌ Not Available",
            "Groq": "✅ Available" if groq_available else "❌ Not Available",
            "Gemini": "✅ Available" if gemini_available else "❌ Not Available"
        },
        "database_connection": "✅ Connected" if get_atlas_connection() is not None else "❌ Failed",
        "doctor_data_count": len(doctor_data.get("specialists", []))
    }

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
else:
    # Production configuration for Vercel
    app.config['DEBUG'] = False

# Vercel serverless handler
def handler(environ, start_response):
    return app(environ, start_response)