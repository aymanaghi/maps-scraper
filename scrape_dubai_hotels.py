import requests
import pandas as pd
import os

# 🔑 YOUR GOOGLE MAPS API KEY GOES HERE
API_KEY = "*********************** "  # ← replace with your actual key

# 🌍 Dubai area bounds
LAT_START, LAT_END = 25.05, 25.30
LNG_START, LNG_END = 55.10, 55.40
STEP = 0.015      # smaller step = more tiles = more hotels
RADIUS = 2500     # meters per tile
MIN_RATING = 4.0
MIN_REVIEWS = 10

URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
DETAILS_URL = "https://maps.googleapis.com/maps/api/place/details/json"


def nearby_hotels(lat, lng, radius=RADIUS):
    """Fetch nearby hotels for a given lat/lng."""
    params = {"location": f"{lat},{lng}", "radius": radius, "type": "lodging", "key": API_KEY}
    results, next_token = [], None
    while True:
        if next_token:
            params["pagetoken"] = next_token
            time.sleep(2)
        res = requests.get(URL, params=params)
        data = res.json()
        results.extend(data.get("results", []))
        next_token = data.get("next_page_token")
        if not next_token:
            break
    return results


def get_details(pid):
    """Fetch detailed info for a single place."""
    params = {
        "place_id": pid,
        "fields": "name,formatted_address,geometry,rating,user_ratings_total,formatted_phone_number,website",
        "key": API_KEY,
    }
    res = requests.get(DETAILS_URL, params=params)
    return res.json().get("result", {})


def scrape_and_merge():
    hotels = []
    seen = set()

    # 🧾 load previous dataset if it exists
    existing_df = None
    if os.path.exists("dubai_hotels_cleaned.csv"):
        existing_df = pd.read_csv("dubai_hotels_cleaned.csv")
        print(f"📂 found old dataset with {len(existing_df)} hotels")
        for name in existing_df["name"].str.lower().str.strip():
            seen.add(name)

    lat = LAT_START
    tile_count = 0

    while lat <= LAT_END:
        lng = LNG_START
        while lng <= LNG_END:
            tile_count += 1
            print(f"🟨 scanning tile ({lat:.3f}, {lng:.3f})...")
            results = nearby_hotels(lat, lng)
            for r in results:
                name = (r.get("name") or "").lower().strip()
                if not name or name in seen:
                    continue
                pid = r.get("place_id")
                seen.add(name)
                details = get_details(pid)
                time.sleep(0.2)
                hotel = {
                    "name": details.get("name") or r.get("name"),
                    "address": details.get("formatted_address") or r.get("vicinity"),
                    "rating": details.get("rating"),
                    "reviews": details.get("user_ratings_total"),
                    "lat": details.get("geometry", {}).get("location", {}).get("lat")
                    if details.get("geometry") else None,
                    "lng": details.get("geometry", {}).get("location", {}).get("lng")
                    if details.get("geometry") else None,
                    "phone": details.get("formatted_phone_number"),
                    "website": details.get("website"),
                }
                hotels.append(hotel)
            print(f"✅ total collected so far: {len(hotels)}")
            lng += STEP
        lat += STEP

    print(f"🧭 finished scanning {tile_count} tiles")

    # 📊 merge with old data if available
    df = pd.DataFrame(hotels)
    if existing_df is not None:
        df = pd.concat([existing_df, df], ignore_index=True)

    # 🧹 clean + dedupe
    df["name_clean"] = df["name"].str.lower().str.strip()
    df.drop_duplicates(subset=["name_clean"], inplace=True)
    df.drop(columns=["name_clean"], inplace=True)
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce").fillna(0)
    df["reviews"] = pd.to_numeric(df["reviews"], errors="coerce").fillna(0)
    df = df[(df["rating"] >= MIN_RATING) & (df["reviews"] >= MIN_REVIEWS)]
    df = df.sort_values(by=["rating", "reviews"], ascending=[False, False])

    # 💾 save clean sheet
    df.to_csv("dubai_hotels_cleaned.csv", index=False)
    print(f"🎉 all done! unique hotels: {len(df)} saved to dubai_hotels_cleaned.csv")


if __name__ == "__main__":
    scrape_and_merge()
