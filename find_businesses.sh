import requests
import pandas as pd

# Sign up at Radar to get your free API key: https://radar.com/
API_KEY = 'YOUR_FREE_RADAR_API_KEY_HERE'

def find_businesses(api_key, query, city="Saudi Arabia"):
    """
    Finds businesses using Radar's search API.
    """
    url = "https://api.radar.io/v1/search/autocomplete"
    headers = {
        'Authorization': api_key
    }
    params = {
        'query': f"{query} in {city}",
        'layers': 'place',
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raises an error for bad status codes
        data = response.json()
        
        businesses = []
        for place in data.get('addresses', []):
            business_info = {
                'Name': place.get('placeLabel', 'N/A'),
                'Address': place.get('formattedAddress', 'N/A'),
                'City': place.get('city', 'N/A'),
                'Latitude': place.get('latitude', 'N/A'),
                'Longitude': place.get('longitude', 'N/A'),
            }
            businesses.append(business_info)
            print(f"Found: {business_info['Name']}")
        
        return businesses

    except requests.exceptions.RequestException as e:
        print(f"An API error occurred: {e}")
        return []

def save_to_csv(business_data, filename='businesses_radar.csv'):
    """Saves the list of business data to a CSV file."""
    if business_data:
        df = pd.DataFrame(business_data)
        df.to_csv(filename, index=False)
        print(f"\nData successfully saved to '{filename}'.")
    else:
        print("\nNo data to save.")

if __name__ == '__main__':
    # === CONFIGURE YOUR SEARCH ===
    YOUR_API_KEY = API_KEY
    SEARCH_QUERY = "construction company"  # e.g., "logistics company", "warehousing"
    SEARCH_CITY = "Riyadh"  # Or Jeddah, Dammam, etc.
    
    if YOUR_API_KEY == 'YOUR_FREE_RADAR_API_KEY_HERE':
        print("Please set your actual Radar API key in the script.")
    else:
        listings = find_businesses(YOUR_API_KEY, SEARCH_QUERY, SEARCH_CITY)
        save_to_csv(listings)
