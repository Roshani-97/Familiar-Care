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
CORS(app, resources={r"/*": {"origins": "*"}})

# Load sample encyclopedia data
sample_data = {
    "pets": [
        {
            "species": "Dog",
            "breed": "Labrador Retriever",
            "description": "Friendly, outgoing, and high-spirited companions who have more than enough affection to go around for a family.",
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
            "description": "Sweet, gentle cats that prefer a calm, quiet home where they can be the center of attention.",
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

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "message": "API server is running"})

@app.route('/api/encyclopedia/search', methods=['GET'])
def search_encyclopedia():
    try:
        query = request.args.get('query', '').lower().strip()
        logger.info(f"Encyclopedia search query: {query}")
        
        # Get all available species and breeds
        all_species = list(set(pet['species'] for pet in sample_data['pets']))
        all_breeds = list(set(pet['breed'] for pet in sample_data['pets']))
        
        # If no query, return all available species and breeds
        if not query:
            return jsonify({
                "results": sample_data['pets'],
                "species": all_species,
                "breeds": all_breeds
            })
        
        # Search for pets matching the query
        matching_pets = []
        for pet in sample_data['pets']:
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

@app.route('/api/encyclopedia/pet', methods=['GET'])
def get_pet_info():
    try:
        breed = request.args.get('breed', '').lower()
        species = request.args.get('species', '').lower()
        
        if not breed and not species:
            return jsonify({"error": "Please provide either breed or species"}), 400
        
        # Find matching pet
        for pet in sample_data['pets']:
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

@app.route('/api/chatbot', methods=['POST'])
def chatbot_query():
    try:
        data = request.get_json()
        if not data:
            logger.error("No JSON data received")
            return jsonify({"error": "No data provided"}), 400
            
        message = data.get('message', '')
        logger.info(f"Received message: {message[:50]}...")
        
        if not message:
            return jsonify({"error": "No message provided"}), 400
        
        # Simple response
        response = "Based on the symptoms described, your pet might be experiencing some discomfort. Please consult with a veterinarian for a proper diagnosis."
            
        return jsonify({
            "response": response
        })
    except Exception as e:
        logger.error(f"Error in chatbot_query: {str(e)}")
        return jsonify({
            "error": "Failed to generate response",
            "details": str(e)
        }), 500

if __name__ == '__main__':
    logger.info("Starting simplified Flask server on port 5001...")
    app.run(debug=True, host='0.0.0.0', port=5001) 