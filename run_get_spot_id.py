from surf_api import get_spot_id

def main(spot_name):
    spots_list = get_spot_id(spot_name)
    if spots_list:
        print(spots_list)
    else:
        print("No spots found or an error occurred.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python run_get_spot_id.py <spot_name>")
    else:
        main(sys.argv[1])
