import sys
import json
import pysurfline  # Assuming this module provides surf forecast data
from datetime import datetime
from collections import Counter
from statistics import median

# Function to serialize weather data
def serialize_weather(weather, current_time):
    return {
        "timestamp": str(current_time),
        "utcOffset": weather.utcOffset,
        "temperature": weather.temperature,
        "condition": weather.condition,
        "pressure": weather.pressure
    }

# Function to serialize wave data
def serialize_wave(wave, current_time):
    # Serialize only the first swell for simplicity
    serialized_swells = [{"period": swell.period} for swell in wave.swells[:1]]

    return {
        "timestamp": str(current_time),
        "probability": wave.probability,
        "surf": {
            "min": wave.surf.min,
            "max": wave.surf.max,
            "optimalScore": wave.surf.optimalScore,
            "plus": wave.surf.plus,
            "humanRelation": wave.surf.humanRelation
        },
        "power": wave.power,
        "swells": serialized_swells
    }

# Function to serialize wind data
def serialize_wind(wind, current_time):
    return {
        "timestamp": str(current_time),
        "utcOffset": wind.utcOffset,
        "speed": wind.speed,
        "direction": wind.direction,
        "directionType": wind.directionType,
        "gust": wind.gust
    }

# Function to serialize tide data
def serialize_tide(tide, current_time):
    return {
        "timestamp": str(current_time),
        "utcOffset": tide.utcOffset,
        "type": tide.type,
        "height": tide.height
    }

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

# Main entry point of the program
if __name__ == "__main__":
    spot_id = sys.argv[1]  # Get spot ID from command-line argument
    forecast_data = get_surf_forecast(spot_id)  # Get forecast data for the spot
    print(json.dumps(forecast_data, indent=4))  # Print the forecast data in JSON format
