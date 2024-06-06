import sys
import json
from surf_api import get_spot_id, get_surf_forecast
from utils import format_forecast_for_whatsapp

if __name__ == "__main__":
    if len(sys.argv) > 1:
        spot_name = sys.argv[1]
        spot_id = get_spot_id(spot_name)
        if spot_id:
            forecast_data = get_surf_forecast(spot_id)
            formatted_message = format_forecast_for_whatsapp(forecast_data)
            print(formatted_message)
        else:
            print("Unable to retrieve forecast without a valid spot ID.")
    else:
        print("No spot name provided.")