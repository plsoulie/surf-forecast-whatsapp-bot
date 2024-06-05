import sys
import json
import pysurfline
from datetime import datetime
from collections import Counter
from statistics import median

def serialize_weather(weather, current_time):
    return {
        "timestamp": str(current_time),
        "utcOffset": weather.utcOffset,
        "temperature": weather.temperature,
        "condition": weather.condition,
        "pressure": weather.pressure
    }

def serialize_wave(wave, current_time):
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
    spot_forecasts = pysurfline.get_spot_forecasts(spot_id)
    
    weather_data = [serialize_weather(weather, current_time) for weather in spot_forecasts.weather[:1]]
    
    wave_data = [serialize_wave(wave, current_time) for wave in spot_forecasts.waves[:1]]
    
    wind_data = [serialize_wind(wind, current_time) for wind in spot_forecasts.wind[:1]]

    tide_data = [serialize_tide(tide, current_time) for tide in spot_forecasts.tides[:1]]

    return {
        "spotId": spot_forecasts.spotId,
        "name": spot_forecasts.name,
        "weather": weather_data,
        "waves": wave_data,
        "wind": wind_data,
        "tides": tide_data
    }

if __name__ == "__main__":
    spot_id = sys.argv[1]
    forecast_data = get_surf_forecast(spot_id)
    print(json.dumps(forecast_data, indent=4))
