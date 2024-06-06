import sys
from surf_api import get_surf_forecast

def main(spot_id):
    try:
        forecast = get_surf_forecast(spot_id)
        print(forecast)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <spot_id>")
    else:
        main(sys.argv[1])
