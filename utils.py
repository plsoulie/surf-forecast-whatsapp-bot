import re

def normalize_spot_name(spot_name):
    # Convert the spot name to lowercase
    spot_name = spot_name.lower()
    # Replace one or more whitespace characters with a single hyphen
    spot_name = re.sub(r'\s+', '-', spot_name)
    return spot_name

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

# Function to format message for Whatsapp

def format_forecast_for_whatsapp(forecast_data):
    message = f"Surf Forecast for {forecast_data['name']} (Spot ID: {forecast_data['spotId']}):\n\n"

    # Weather details
    weather = forecast_data['weather'][0]
    message += f"Weather: {weather.get('condition', 'Not available')} \n"
    message += f"Temperature: {weather.get('temperature', 'N/A')}°C \n"
    message += f"Pressure: {weather.get('pressure', 'N/A')} hPa \n"
    message += f"UTC Offset: {weather.get('utcOffset', 'N/A')} hours\n\n"

    # Waves details
    if forecast_data['waves']:
        wave = forecast_data['waves'][0]
        message += f"Waves: {wave.get('humanRelation', 'Not specified')} \n"
        message += f"Minimum Surf: {wave['surf'].get('min', 'N/A')}m, Maximum Surf: {wave['surf'].get('max', 'N/A')}m \n"
        message += f"Power: {wave.get('power', 'N/A')} with Probability: {wave.get('probability', 'N/A')}%\n"
        if wave['swells']:
            swell = wave['swells'][0]
            message += f"Swell Period: {swell.get('period', 'N/A')} seconds\n\n"
    else:
        message += "Waves data not available.\n\n"

    # Wind details
    if forecast_data['wind']:
        wind = forecast_data['wind'][0]
        message += f"Wind: {wind.get('directionType', 'N/A')} at {wind.get('speed', 'N/A')} m/s\n"
        message += f"Gusts up to: {wind.get('gust', 'N/A')} m/s\n"
        message += f"Direction: {wind.get('direction', 'N/A')} degrees\n\n"
    else:
        message += "Wind data not available.\n\n"

    # Tide details
    if forecast_data['tides']:
        tide = forecast_data['tides'][0]
        message += f"Tide Type: {tide.get('type', 'N/A')} \n"
        message += f"Tide Height: {tide.get('height', 'N/A')}m\n"
        message += f"UTC Offset: {tide.get('utcOffset', 'N/A')} hours\n"
    else:
        message += "Tide data not available.\n"

    return message