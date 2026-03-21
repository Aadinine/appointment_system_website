from flask import Flask
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import your app
from app import app

# Vercel handler
def handler(request):
    return app(request.environ, start_response_status)
