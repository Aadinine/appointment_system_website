import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Test API key
api_key = os.getenv("GEMINI_API_KEY")
print(f"API Key found: {'Yes' if api_key else 'No'}")
print(f"API Key starts with: {api_key[:10]}..." if api_key else "No API Key")

if not api_key or api_key == "YOUR_NEW_API_KEY_HERE":
    print("❌ Please update your API key in .env file")
    exit()

try:
    # Configure Gemini
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # Test simple generation
    response = model.generate_content("Hello, how are you?")
    print(f"AI Response: {response.text}")
    print("✅ AI is working!")
    
except Exception as e:
    print(f"❌ AI Error: {e}")
    print(f"Error Type: {type(e)}")
