from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import logging
import json
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Load encyclopedia data
try:
    # Try to load from Backend directory
    encyclopedia_data_path = os.path.join('Backend', 'encyclopedia_data.json')
    if os.path.exists(encyclopedia_data_path):
        with open(encyclopedia_data_path, 'r') as f:
            encyclopedia_data = json.load(f)
            logger.info("Successfully loaded encyclopedia data from Backend directory")
    else:
        # If not found, create sample data
        encyclopedia_data = {
            "pets": [
                {
                    "species": "Dog",
                    "breed": "Labrador Retriever",
                    "description": "Friendly, outgoing, and high-spirited companions who have more than enough affection to go around for a family looking for a medium-to-large dog.",
                    "do": [
                        "Regular exercise (at least 1 hour daily)",
                        "Consistent training from an early age",
                        "Regular grooming to manage shedding",
                        "Regular vet check-ups",
                        "Provide plenty of toys for mental stimulation"
                    ],
                    "dont": [
                        "Don't overfeed as they are prone to obesity",
                        "Don't skip socialization during puppyhood",
                        "Don't leave alone for long periods",
                        "Don't ignore dental hygiene",
                        "Don't skip regular exercise"
                    ]
                },
                {
                    "species": "Cat",
                    "breed": "Persian",
                    "description": "Sweet, gentle cats that prefer a calm, quiet home where they can be the center of attention. Known for their long, luxurious coat and peaceful personality.",
                    "do": [
                        "Daily grooming to prevent matting",
                        "Regular face cleaning",
                        "Keep indoors",
                        "Provide scratching posts",
                        "Regular vet check-ups"
                    ],
                    "dont": [
                        "Don't skip grooming sessions",
                        "Don't expose to extreme temperatures",
                        "Don't forget regular eye care",
                        "Don't ignore dental hygiene",
                        "Don't leave grooming tools within reach"
                    ]
                },
                {
                    "species": "Bird",
                    "breed": "Budgerigar",
                    "description": "Small, social parakeets that are popular as pets. They are relatively easy to care for and can learn to mimic human speech.",
                    "do": [
                        "Provide plenty of cage space",
                        "Regular social interaction",
                        "Varied diet with fresh vegetables",
                        "Clean cage regularly",
                        "Regular vet check-ups with an avian specialist"
                    ],
                    "dont": [
                        "Don't use non-stick cookware around them",
                        "Don't expose to drafts",
                        "Don't place cage in direct sunlight",
                        "Don't use scented candles or air fresheners",
                        "Don't feed avocado or chocolate"
                    ]
                }
            ]
        }
        logger.warning("Using sample encyclopedia data")
except Exception as e:
    logger.error(f"Error loading encyclopedia data: {str(e)}")
    # Create sample data if loading fails
    encyclopedia_data = {
        "pets": [
            {
                "species": "Dog",
                "breed": "Labrador Retriever",
                "description": "Friendly, outgoing, and high-spirited companions.",
                "do": ["Regular exercise", "Consistent training"],
                "dont": ["Don't overfeed", "Don't skip socialization"]
            },
            {
                "species": "Cat",
                "breed": "Persian",
                "description": "Sweet, gentle cats with long, luxurious coats.",
                "do": ["Daily grooming", "Regular face cleaning"],
                "dont": ["Don't skip grooming", "Don't expose to extreme temperatures"]
            }
        ]
    }

# Configure CORS with more specific settings
CORS(app, resources={r"/*": {"origins": "*"}})

def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

@app.after_request
def after_request(response):
    return add_cors_headers(response)

# Simple pet disease database
pet_diseases = {
    'vomit': {
        'disease': 'Gastroenteritis',
        'symptoms': 'vomiting, diarrhea, lethargy, decreased appetite',
        'treatment': 'Fluid therapy to prevent dehydration, temporarily withholding food, bland diet, medication to control vomiting and diarrhea.'
    },
    'diarrhea': {
        'disease': 'Gastroenteritis or Colitis',
        'symptoms': 'loose or watery stool, increased frequency of bowel movements, lethargy, dehydration',
        'treatment': 'Fluid therapy, fasting for 12-24 hours, followed by bland diet, probiotics, and anti-diarrheal medication if prescribed by a vet.'
    },
    'cough': {
        'disease': 'Kennel Cough',
        'symptoms': 'dry hacking cough, retching, nasal discharge',
        'treatment': 'Rest, isolation from other dogs, cough suppressants, antibiotics if bacterial infection is present.'
    },
    'itch': {
        'disease': 'Allergic Dermatitis',
        'symptoms': 'itching, scratching, red skin, rashes, hair loss',
        'treatment': 'Identifying and removing the allergen, antihistamines, corticosteroids, special shampoos.'
    },
    'scratch': {
        'disease': 'Allergic Dermatitis or Flea Infestation',
        'symptoms': 'excessive scratching, red skin, visible fleas or flea dirt, skin lesions',
        'treatment': 'Flea treatment, antihistamines, medicated baths, and environmental control.'
    },
    'fever': {
        'disease': 'Infection',
        'symptoms': 'elevated body temperature, lethargy, decreased appetite, shivering',
        'treatment': 'Veterinary examination to identify the underlying cause, antibiotics if bacterial infection, anti-inflammatories, and supportive care.'
    },
    'limp': {
        'disease': 'Arthritis or Injury',
        'symptoms': 'difficulty walking, favoring a limb, swelling, pain upon touch',
        'treatment': 'Rest, pain management, anti-inflammatory medication, and physical therapy. Severe cases may require surgery.'
    },
    'eye': {
        'disease': 'Conjunctivitis',
        'symptoms': 'redness in the eyes, discharge, squinting, pawing at eyes',
        'treatment': 'Cleaning the affected eye, antibiotic eye drops or ointment, treating any underlying causes.'
    },
    'ear': {
        'disease': 'Ear Infection',
        'symptoms': 'head shaking, ear scratching, odor from ears, redness in ear canal',
        'treatment': 'Cleaning the ears, topical medications, oral antibiotics or antifungals if needed.'
    }
}

@app.route('/api/health', methods=['GET', 'OPTIONS'])
def health_check():
    if request.method == 'OPTIONS':
        return add_cors_headers(make_response()), 200
    return jsonify({"status": "ok", "message": "API server is running"})

@app.route('/api/chatbot', methods=['POST', 'OPTIONS'])
def chatbot_query():
    if request.method == 'OPTIONS':
        return add_cors_headers(make_response()), 200
        
    try:
        data = request.get_json()
        if not data:
            logger.error("No JSON data received")
            return jsonify({"error": "No data provided"}), 400
            
        message = data.get('message', '')
        logger.info(f"Received message: {message[:50]}...")
        
        if not message:
            return jsonify({"error": "No message provided"}), 400
        
        # Check if message contains any of our known symptoms
        message_lower = message.lower()
        matched_symptom = None
        
        # Find the most relevant symptom match
        for symptom in pet_diseases.keys():
            if symptom in message_lower:
                matched_symptom = symptom
                break
                
        if matched_symptom:
            disease_info = pet_diseases[matched_symptom]
            response = f"Based on the symptoms described, your pet might be experiencing {disease_info['disease']}. "
            response += f"This condition typically presents with {disease_info['symptoms']}. "
            response += f"\n\nRecommended treatment approach: {disease_info['treatment']} "
            response += f"\n\nPlease consult with a veterinarian for proper diagnosis and treatment. "
            response += f"This is only an AI-based assessment."
        else:
            response = "I couldn't identify a specific condition based on those symptoms. Please provide more details about your pet's symptoms (such as vomiting, diarrhea, coughing, itching, limping, etc.) or consult with a veterinarian for a proper diagnosis."
            
        return jsonify({
            "response": response
        })
    except Exception as e:
        logger.error(f"Error in chatbot_query: {str(e)}")
        return jsonify({
            "error": "Failed to generate response",
            "details": str(e)
        }), 500

# Enhanced Encyclopedia API
@app.route('/api/encyclopedia/search', methods=['GET', 'OPTIONS'])
def search_encyclopedia():
    if request.method == 'OPTIONS':
        return add_cors_headers(make_response()), 200
    
    try:
        query = request.args.get('query', '').lower().strip()
        logger.info(f"Encyclopedia search query: {query}")
        
        # Get all available species and breeds
        all_species = list(set(pet['species'] for pet in encyclopedia_data['pets']))
        all_breeds = list(set(pet['breed'] for pet in encyclopedia_data['pets']))
        
        # If no query, return all available species and breeds
        if not query:
            return jsonify({
                "results": encyclopedia_data['pets'],
                "species": all_species,
                "breeds": all_breeds
            })
        
        # Search for pets matching the query
        matching_pets = []
        for pet in encyclopedia_data['pets']:
            if (query in pet['species'].lower() or 
                query in pet['breed'].lower() or 
                query in pet['description'].lower()):
                matching_pets.append(pet)
        
        # Get unique species and breeds from matching pets
        matching_species = list(set(pet['species'] for pet in matching_pets))
        matching_breeds = list(set(pet['breed'] for pet in matching_pets))
        
        return jsonify({
            "results": matching_pets,
            "species": matching_species,
            "breeds": matching_breeds
        })
    except Exception as e:
        logger.error(f"Error in search_encyclopedia: {str(e)}")
        return jsonify({
            "error": "Failed to search pets",
            "details": str(e)
        }), 500

@app.route('/api/encyclopedia/pet', methods=['GET', 'OPTIONS'])
def get_pet_info():
    if request.method == 'OPTIONS':
        return add_cors_headers(make_response()), 200
    
    try:
        breed = request.args.get('breed', '').lower()
        species = request.args.get('species', '').lower()
        
        if not breed and not species:
            return jsonify({"error": "Please provide either breed or species"}), 400
        
        # Find matching pet
        for pet in encyclopedia_data['pets']:
            if (breed and pet['breed'].lower() == breed) or \
               (species and pet['species'].lower() == species):
                return jsonify(pet)
        
        return jsonify({"error": "Pet not found"}), 404
    except Exception as e:
        logger.error(f"Error in get_pet_info: {str(e)}")
        return jsonify({
            "error": "Failed to get pet information",
            "details": str(e)
        }), 500

# Add support for locations API
@app.route('/api/locations', methods=['GET', 'OPTIONS'])
def get_locations():
    if request.method == 'OPTIONS':
        return add_cors_headers(make_response()), 200
    
    # Return sample location data
    return jsonify({
        "vets": [
            {
                "name": "Sample Veterinary Clinic",
                "address": "123 Main St",
                "rating": 4.5,
                "location": {
                    "lat": 40.7128,
                    "lng": -74.0060
                }
            }
        ],
        "userLocation": {
            "lat": 40.7128,
            "lng": -74.0060
        }
    })

if __name__ == '__main__':
    logger.info("Starting simplified Flask server on port 5000...")
    app.run(debug=True, host='0.0.0.0', port=5000) 