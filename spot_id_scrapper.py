import requests

def normalize_spot_name(spot_name):
    # Convert the spot name to lowercase and remove whitespace
    return spot_name.lower().replace(" ", "-")

def get_spot_id(spot_name):
    # Construct the Surfline search URL
    search_url = f"https://services.surfline.com/search/site?q={spot_name}"
    
    # Send a GET request to the search URL
    response = requests.get(search_url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        print(data)
        
        # Extract the spot ID from the response
        for entry in data:
            # Check if the current entry contains spot information
            if 'hits' in entry and 'hits' in entry['hits'] and len(entry['hits']['hits']) > 0:
                spot_id = entry['hits']['hits'][0]['_id']
                return spot_id
        print("Spot not found. Please try again.")
        return None
    else:
        print("Failed to fetch spot ID. Please try again.")
        return None

# Example usage
spot_name = input("Enter the name of the surf spot: ")
spot_id = get_spot_id(spot_name)
if spot_id:
    print(f"The spot ID for {spot_name} is: {spot_id}")
