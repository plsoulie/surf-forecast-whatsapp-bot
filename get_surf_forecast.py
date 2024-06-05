import sys
import json
import pysurfline
from datetime import datetime

def average_weather_data(weather_data):
    # Calculate average temperature, pressure, and condition
    total_temperature = sum(weather['temperature'] for weather in weather_data)
    total_pressure = sum(weather['pressure'] for weather in weather_data)
    
    # Calculate average condition (by taking the most frequent condition)
    conditions = [weather['condition'] for weather in weather_data]
    most_frequent_condition = max(set(conditions), key=conditions.count)
    
    return {
        "timestamp": weather_data[0]['timestamp'],  # Use the timestamp from the first entry
        "utcOffset": weather_data[0]['utcOffset'],  # Use the utcOffset from the first entry
        "temperature": total_temperature / len(weather_data),
        "condition": most_frequent_condition,
        "pressure": total_pressure / len(weather_data)
    }

def serialize_weather(weather, current_time):
    return {
        "timestamp": str(current_time),
        "utcOffset": weather.utcOffset,
        "temperature": weather.temperature,
        "condition": weather.condition,
        "pressure": weather.pressure
    }

def serialize_wave(wave, current_time):
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
        "power": wave.power
    }

def serialize_wind(wind, current_time):
    return {
        "timestamp": str(current_time),
        "utcOffset": wind.utcOffset,
        "speed": wind.speed,
        "direction": wind.direction,
        "directionType": wind.directionType,
        "gust": wind.gust
    }

def serialize_tide(tide, current_time):
    return {
        "timestamp": str(current_time),
        "utcOffset": tide.utcOffset,
        "type": tide.type,
        "height": tide.height
    }

def get_surf_forecast(spot_id):
    current_time = datetime.now()  # Get current time
    spot_forecasts = pysurfline.get_spot_forecasts(spot_id, intervalHours=1, days=1)
    weather_data = [serialize_weather(weather, current_time) for weather in spot_forecasts.weather]
    aggregated_weather_data = average_weather_data(weather_data)
    wave_data = [serialize_wave(wave, current_time) for wave in spot_forecasts.waves]
    wind_data = [serialize_wind(wind, current_time) for wind in spot_forecasts.wind]
    tide_data = [serialize_tide(tide, current_time) for tide in spot_forecasts.tides]

    return {
        "spotId": spot_forecasts.spotId,
        "name": spot_forecasts.name,
        "weather": aggregated_weather_data,
        # "weather": weather_data,
        # "waves": wave_data,
        # "wind": wind_data,
        # "tides": tide_data
    }

if __name__ == "__main__":
    spot_id = sys.argv[1]
    forecast_data = get_surf_forecast(spot_id)
    print(json.dumps(forecast_data))
