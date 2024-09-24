import sys
import requests
import pysurfline
from datetime import datetime
from utils import normalize_spot_name, serialize_tide, serialize_wave, serialize_weather, serialize_wind, format_forecast_for_whatsapp

def get_spot_id(spot_name):
    normalized_spot_name = normalize_spot_name(spot_name)
    search_url = f"https://services.surfline.com/search/site?q={normalized_spot_name}"
    response = requests.get(search_url)

    if response.status_code == 200:
        data = response.json()
        relevant_spots = [spot for entry in data for spot in entry['hits']['hits'] if 'name' in spot['_source']]
        
        if len(relevant_spots) == 0:
            return None
        
        spots_list = [{"id": spot['_id'], "name": spot['_source']['name'], "location": ", ".join(spot['_source']['breadCrumbs'])} for spot in relevant_spots]
        
        # Print the spots_list to the terminal in a parseable format
        for spot in spots_list:
            print(f"{spot['id']}|{spot['name']}|{spot['location']}")
        
        return spots_list
    else:
        print("Failed to fetch spots")
        return None

def get_surf_forecast(spot_id):
    current_time = datetime.now()
    print(current_time)
    spot_forecasts = pysurfline.get_spot_forecasts(spot_id)
    
    weather_data = [serialize_weather(weather, current_time) for weather in spot_forecasts.weather[:1]]
    wave_data = [serialize_wave(wave, current_time) for wave in spot_forecasts.waves[:1]]
    wind_data = [serialize_wind(wind, current_time) for wind in spot_forecasts.wind[:1]]
    tide_data = [serialize_tide(tide, current_time) for tide in spot_forecasts.tides[:1]]

    # Prepare the forecast data dictionary
    forecast_data = {
        "spotId": spot_forecasts.spotId,
        "name": spot_forecasts.name,
        "weather": weather_data,
        "waves": wave_data,
        "wind": wind_data,
        "tides": tide_data
    }

    # Format the forecast message for WhatsApp using the utility function
    formatted_forecast = format_forecast_for_whatsapp(forecast_data)

    return formatted_forecast

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python surf_api.py <function> <argument>")
    else:
        function_name = sys.argv[1]
        argument = sys.argv[2]
        if function_name == "get_spot_id":
            get_spot_id(argument)
        elif function_name == "get_surf_forecast":
            get_surf_forecast(argument)
        else:
            print(f"Unknown function: {function_name}")