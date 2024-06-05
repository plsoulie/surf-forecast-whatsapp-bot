import requests

def normalize_spot_name(spot_name):
    # Convert the spot name to lowercase and remove whitespace
    return spot_name.lower().replace(" ", "-")

def get_spot_id(spot_name):
    # Normalize the spot name
    normalized_spot_name = normalize_spot_name(spot_name)
    
    # Construct the Surfline search URL
    search_url = f"https://services.surfline.com/search/site?q={normalized_spot_name}"
    
    # Send a GET request to the search URL
    response = requests.get(search_url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        
        # Extract the spots with relevant information
        relevant_spots = [spot for entry in data for spot in entry['hits']['hits'] if 'name' in spot['_source']]
        
        if len(relevant_spots) == 0:
            print("Spot not found. Please try again.")
            return None
        
        # Display options if there are multiple matches
        if len(relevant_spots) > 1:
            print("Multiple matching spots found. Please select one:")
            for i, spot in enumerate(relevant_spots, start=1):
                print(f"{i}. {spot['_source']['name']}, {', '.join(spot['_source']['breadCrumbs'])}")
            
            # Prompt the user to select an option
            selection = int(input("Enter the number of the desired spot: "))
            if selection < 1 or selection > len(relevant_spots):
                print("Invalid selection.")
                return None
            else:
                spot_id = relevant_spots[selection - 1]['_id']
                return spot_id
        
        # If there is only one match, return its ID
        spot_id = relevant_spots[0]['_id']
        return spot_id
    else:
        print("Failed to fetch spot ID. Please try again.")
        return None

# Test the function
spot_name = input("Enter the name of the surf spot: ")
spot_id = get_spot_id(spot_name)
print("Spot ID:", spot_id)
