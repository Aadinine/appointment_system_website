import os
import sys
from flask import Flask

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import your app
from app import app

# Vercel serverless handler
def handler(request):
    return app(request.environ, request.start_response)

if __name__ == "__main__":
    app.run(debug=True)
