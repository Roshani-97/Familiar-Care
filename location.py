import requests
import webbrowser
from geopy.geocoders import Nominatim

# Replace with your Google API key
GOOGLE_API_KEY = "YOUR_GOOGLE_API_KEY"

def get_current_location():
    """Get the user's current location using Geopy."""
    try:
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode("Your City, Country")  # Default fallback
        if location:
            return location.latitude, location.longitude
        else:
            print("Could not determine location. Using a default location.")
            return 28.6139, 77.2090  # Default: New Delhi, India
    except Exception as e:
        print(f"Error getting location: {e}")
        return 28.6139, 77.2090  # Default location

def find_nearby_vets(latitude, longitude):
    """Find nearby vet agencies using Google Places API."""
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{latitude},{longitude}",
        "radius": 5000,  # Search within 5 km
        "type": "veterinary_care",
        "key": GOOGLE_API_KEY
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        results = response.json().get("results", [])
        if results:
            print("\nNearby Veterinary Clinics:")
            for i, place in enumerate(results[:5], start=1):
                print(f"{i}. {place['name']} - {place['vicinity']}")
            return results
        else:
            print("No veterinary clinics found nearby.")
    else:
        print("Error fetching vet clinics.")
    return []

def open_google_maps(latitude, longitude):
    """Open Google Maps with nearby veterinary clinics."""
    maps_url = f"https://www.google.com/maps/search/veterinary+clinic/@{latitude},{longitude},14z"
    webbrowser.open(maps_url)
    print("\nGoogle Maps has been opened with vet clinic search results.")

if __name__ == "__main__":
    lat, lon = get_current_location()
    vets = find_nearby_vets(lat, lon)
    open_google_maps(lat, lon)
