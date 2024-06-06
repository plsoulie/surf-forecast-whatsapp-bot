import requests 
import pysurfline  # Assuming this module provides surf forecast data
from datetime import datetime
from utils import normalize_spot_name, serialize_tide, serialize_wave, serialize_weather, serialize_wind

def get_spot_id(spot_name):
    # Normalize the spot name
    normalized_spot_name = normalize_spot_name(spot_name)
    
    # Construct the Surfline search URL
    search_url = f"https://services.surfline.com/search/site?q={normalized_spot_name}"
    
    # Send a GET request to the search URL
    response = requests.get(search_url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        
        # Extract the spots with relevant information
        relevant_spots = [spot for entry in data for spot in entry['hits']['hits'] if 'name' in spot['_source']]
        
        if len(relevant_spots) == 0:
            print("Spot not found. Please try again.")
            return None
        
        # Display options if there are multiple matches
        if len(relevant_spots) > 1:
            print("Multiple matching spots found. Please select one:")
            for i, spot in enumerate(relevant_spots, start=1):
                print(f"{i}. {spot['_source']['name']}, {', '.join(spot['_source']['breadCrumbs'])}")
            
            # Prompt the user to select an option
            selection = int(input("Enter the number of the desired spot: "))
            if selection < 1 or selection > len(relevant_spots):
                print("Invalid selection.")
                return None
            else:
                spot_id = relevant_spots[selection - 1]['_id']
                return spot_id
        
        # If there is only one match, return its ID
        spot_id = relevant_spots[0]['_id']
        return spot_id
    else:
        print("Failed to fetch spot ID. Please try again.")
        return None
    
# Function to get surf forecast data for a given spot ID
def get_surf_forecast(spot_id):
    current_time = datetime.now()  # Get current time
    spot_forecasts = pysurfline.get_spot_forecasts(spot_id)  # Get forecast data for the spot
    
    # Serialize weather, wave, wind, and tide data
    weather_data = [serialize_weather(weather, current_time) for weather in spot_forecasts.weather[:1]]
    wave_data = [serialize_wave(wave, current_time) for wave in spot_forecasts.waves[:1]]
    wind_data = [serialize_wind(wind, current_time) for wind in spot_forecasts.wind[:1]]
    tide_data = [serialize_tide(tide, current_time) for tide in spot_forecasts.tides[:1]]

    # Return a dictionary containing forecast data
    return {
        "spotId": spot_forecasts.spotId,
        "name": spot_forecasts.name,
        "weather": weather_data,
        "waves": wave_data,
        "wind": wind_data,
        "tides": tide_data
    }
