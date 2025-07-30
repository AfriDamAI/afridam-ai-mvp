# AfriDam AI - Hackathon MVP Backend
# Language: Python
# Framework: Flask
# VERSION 3: Added /check-ingredients endpoint.
#
# This script simulates the core functionality of the AfriDam AI analysis engine
# and the harmful ingredient detector.

# --- How to Run This Server ---
# 1. Ensure you are in your virtual environment (`source venv/bin/activate`).
# 2. Make sure you have Flask and Flask-Cors installed (`pip3 install Flask Flask-Cors`).
# 3. Save this file as `app.py`.
# 4. In your terminal, navigate to the folder where this file is saved.
# 5. Run the command: `flask run`

from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import os

# Initialize the Flask application
app = Flask(__name__)
CORS(app) # Enable Cross-Origin Resource Sharing

# --- Mock Database of Harmful Ingredients ---
# For the hackathon, we'll use a simple list. In a real app, this would be a large database.
HARMFUL_INGREDIENTS_DB = {
    "mercury": "A toxic heavy metal often used in skin lightening creams. It can cause kidney damage and skin rashes.",
    "hydroquinone": "A powerful depigmenting agent that can cause ochronosis (skin darkening and thickening) with long-term use.",
    "steroids": "Topical steroids can thin the skin, cause stretch marks, and lead to topical steroid withdrawal if overused.",
    "parabens": "Preservatives that can disrupt hormone function and have been linked to skin irritation.",
    "formaldehyde": "A known carcinogen and common allergen found in some cosmetics as a preservative."
}

# Create a directory to store uploaded images
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- API Endpoint for Image Analysis ---
@app.route('/analyze', methods=['POST'])
def analyze_skin_image():
    """Handles the image upload and analysis process."""
    print("Received a request to analyze a skin image...")
    # ... (rest of the image analysis code remains the same) ...
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No image selected"}), 400
    if file:
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
    time.sleep(3)
    mock_result = {
        "status": "success",
        "diagnosis": {
            "primary_condition": "Atopic Dermatitis (Eczema)",
            "confidence_score": 0.92,
            "severity_level": "Moderate",
            "description": "Our AI has identified patterns consistent with Atopic Dermatitis...",
            "recommendation_summary": "Proceed to view your personalized routine..."
        },
        "request_id": f"afridam-ai-{int(time.time())}"
    }
    return jsonify(mock_result)


# --- NEW: API Endpoint for Ingredient Checking ---
@app.route('/check-ingredients', methods=['POST'])
def check_ingredients():
    """
    Handles ingredient list submission and checks against the harmful database.
    Expects a JSON payload with a key "ingredients" which is a list of strings.
    e.g., {"ingredients": ["aqua", "glycerin", "hydroquinone", "parabens"]}
    """
    print("Received a request to check ingredients...")
    
    # Get the JSON data from the request
    data = request.get_json()

    # Basic validation
    if not data or 'ingredients' not in data or not isinstance(data['ingredients'], list):
        return jsonify({"error": "Invalid request. Please provide a JSON object with an 'ingredients' list."}), 400

    # Clean and process the submitted ingredients (convert to lowercase)
    submitted_ingredients = [ing.lower().strip() for ing in data['ingredients']]
    
    # Find which of the submitted ingredients are in our harmful database
    found_harmful = []
    for ingredient in submitted_ingredients:
        if ingredient in HARMFUL_INGREDIENTS_DB:
            found_harmful.append({
                "name": ingredient,
                "reason": HARMFUL_INGREDIENTS_DB[ingredient]
            })

    # Create the response
    response = {
        "status": "success",
        "submitted_count": len(submitted_ingredients),
        "harmful_found_count": len(found_harmful),
        "harmful_ingredients": found_harmful
    }

    print(f"Analysis complete. Found {len(found_harmful)} harmful ingredients.")
    
    return jsonify(response)


# --- Health Check Endpoint ---
@app.route('/')
def health_check():
    return "AfriDam AI Backend Server is running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

