import googlemaps
from datetime import datetime
import json

def get_route(start, end):
    gmaps = googlemaps.Client(key="AIzaSyDO1zQVX5ZNS3yvtJt0M0fHqA_0x2tD2Wc")
    directions_result = gmaps.directions(start, end, mode="transit", departure_time=datetime.now(), transit_mode="subway")
    results = [(step["transit_details"]["departure_stop"]["name"], step["transit_details"]["arrival_stop"]["name"], step["transit_details"]["num_stops"]) 
        for step in directions_result[0]["legs"][0]["steps"] if step["travel_mode"] == "TRANSIT"]
    return results[0] if len(results) > 0 else ("", "", 0)

if __name__ == "__main__":
    print(get_route("111 8th Ave New York", "World Trade Center"))
