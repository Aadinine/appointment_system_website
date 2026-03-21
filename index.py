import os
import json
import math
import pymongo
import uuid
from datetime import datetime, timedelta
from flask import Flask, render_template, request
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

app = Flask(__name__)

# MongoDB Atlas connection
def get_atlas_connection():
    try:
        client = pymongo.MongoClient(os.getenv("ATLAS_CONNECTION_STRING"))
        db = client["appointment_system"]
        return db
    except:
        return None

# Load doctor data - try Atlas first, fallback to JSON
def load_doctor_data():
    atlas_db = get_atlas_connection()
    if atlas_db is not None:
        try:
            doctors = list(atlas_db["doctor"].find({"available": True}))
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

# Setup Gemini
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
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0]
    return text

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/health')
def health_check():
    return {"status": "healthy", "message": "Backend is working!"}

# Vercel serverless handler
def handler(environ, start_response):
    return app(environ, start_response)

if __name__ == "__main__":
    app.run(debug=True)
