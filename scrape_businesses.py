# scrape_businesses.py
import googlemaps
import pandas as pd
from datetime import datetime

# You MUST replace this with your actual Google Maps API key
API_KEY = 'AIzaSyA67IIWQLEwSJmp_07JRwYbAgqBWyFmjvs'

def get_business_listings(api_key, location, keyword):
    """
    Fetches business listings from Google Maps for a specific location and search term.
    
    Args:
        api_key (str): Your Google Maps API key.
        location (str): The city/region to search in (e.g., 'Riyadh, Saudi Arabia').
        keyword (str): The type of business to search for (e.g., 'construction company').
    
    Returns:
        list: A list of dictionaries containing business information.
    """
    gmaps = googlemaps.Client(key=api_key)
    business_data = []
    
    try:
        # Step 1: Geocode the location to get its coordinates
        geocode_result = gmaps.geocode(location)
        if not geocode_result:
            print(f"Error: Could not find the location '{location}'.")
            return business_data
        
        location_geometry = geocode_result[0]['geometry']['location']
        location_lat_lng = (location_geometry['lat'], location_geometry['lng'])
        
        # Step 2: Use the Places API to search for nearby businesses
        places_result = gmaps.places_nearby(
            location=location_lat_lng,
            keyword=keyword,
            radius=20000,  # Search within a 20km radius. Adjust as needed.
        )
        
        # Step 3: Process the results
        for place in places_result.get('results', []):
            place_details = {
                'name': place.get('name'),
                'address': place.get('vicinity', 'N/A'),
                'rating': place.get('rating', 'N/A'),
                'place_id': place.get('place_id')
            }
            business_data.append(place_details)
            print(f"Found: {place_details['name']}")
        
        print(f"\nSuccessfully found {len(business_data)} businesses.")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return business_data

def save_to_csv(business_data, filename='business_listings.csv'):
    """Saves the list of business data to a CSV file."""
    if business_data:
        df = pd.DataFrame(business_data)
        df.to_csv(filename, index=False)
        print(f"\nData saved to '{filename}'.")
    else:
        print("\nNo data to save.")

if __name__ == '__main__':
    # === CONFIGURE YOUR SEARCH HERE ===
    YOUR_API_KEY = API_KEY  # Make sure to set your API key above
    SEARCH_LOCATION = "Riyadh, Saudi Arabia"
    SEARCH_KEYWORD = "construction company"
    # ===================================
    
    if YOUR_API_KEY == 'YOUR_GOOGLE_MAPS_API_KEY_HERE':
        print("Please set your actual Google Maps API key in the script.")
    else:
        listings = get_business_listings(YOUR_API_KEY, SEARCH_LOCATION, SEARCH_KEYWORD)
        save_to_csv(listings)
