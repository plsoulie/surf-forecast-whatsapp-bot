# get_surf_forecast.py
import sys
import json
from pysurfline import Spots

def get_surf_forecast(spot_id):
    spot = Spots(spot_id)
    forecast = spot.get_report()
    return forecast

if __name__ == "__main__":
    spot_id = sys.argv[1]
    forecast_data = get_surf_forecast(spot_id)
    print(json.dumps(forecast_data))
