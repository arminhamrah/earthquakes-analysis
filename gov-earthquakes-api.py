import requests

def get_quake_count(min_mag, start_time, finish_time, lat, long, radius_in_km):
    url = "https://earthquake.usgs.gov/fdsnws/event/1/count"
    param_dictionary = {
        "format": "geojson",
        "starttime": start_time,
        "endtime": finish_time,
        "minmagnitude": min_mag,
        "latitude": lat,
        "longitude": long,
        "maxradiuskm": radius_in_km,
    }
    result = requests.get(url, params=param_dictionary)
    if result.status_code == 200:
        return result.json().get("count", 0)
    else:
        print(f"Error: {result.status_code}")
        return None

def get_quake_details(min_mag, start_time, finish_time, lat, long, radius_in_km):
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    param_dictionary = {
        "format": "geojson",
        "starttime": start_time,
        "endtime": finish_time,
        "minmagnitude": min_mag,
        "latitude": lat,
        "longitude": long,
        "maxradiuskm": radius_in_km,
    }
    result = requests.get(url, params=param_dictionary)
    if result.status_code == 200:
        return result.json().get("features", [])
    else:
        print(f"Error: {result.status_code}")
        return None

def Quake_loop():
    """Function to obtain and render earthquake data."""
    start_time = "2024-06-01"  # Let's check out June 2024
    finish_time = "2024-07-01"
    latitude = 34.0967  # Palo Alto coordinates
    longitude = -117.7198
    radius_in_km = 300

    # Loop over a range of minimum magnitudes
    min_magnitudes = [3.0 + i * 0.1 for i in range(15)]
    data = []

    for min_mag in min_magnitudes:
        quake_count = get_quake_count(min_mag, start_time, finish_time, latitude, longitude, radius_in_km)
        data.append((min_mag, quake_count))

    # Print results in a formatted chart
    print("Minimum Magnitude | Earthquake Count")
    print("----------------- | -----------------")
    for min_mag, count in data:
        print(f"{min_mag:.1f}               | {count}")

    return data

def Quake_compare(place1, place2):
    """Function to compare quakiness of two places."""
    start_time = "2024-01-01"
    finish_time = "2024-02-01"
    min_mag = 4.0
    radius_in_km = 100

    lat1, long1 = place1
    lat2, long2 = place2

    quakes1 = get_quake_details(min_mag, start_time, finish_time, lat1, long1, radius_in_km)
    quakes2 = get_quake_details(min_mag, start_time, finish_time, lat2, long2, radius_in_km)

    quake_count1 = len(quakes1)
    quake_count2 = len(quakes2)

    quakes1_sorted = sorted(quakes1, key=lambda x: x['properties']['mag'], reverse=True)
    quakes2_sorted = sorted(quakes2, key=lambda x: x['properties']['mag'], reverse=True)

    magnitudes1 = [quake['properties']['mag'] for quake in quakes1_sorted]
    magnitudes2 = [quake['properties']['mag'] for quake in quakes2_sorted]

    print(f"Results for the period {start_time} to {finish_time}, with minimum magnitude {min_mag} and radius {radius_in_km} km:")

    if quake_count1 == 0:
        print(f"Place 1 (Lat: {lat1}, Long: {long1}) had no earthquakes that fit these criteria during the specified time frame.")
    elif quake_count1 == 1:
        print(f"Place 1 (Lat: {lat1}, Long: {long1}): 1 earthquake — with a magnitude of {magnitudes1[0]}")
    else:
        print(f"Place 1 (Lat: {lat1}, Long: {long1}): {quake_count1} earthquakes — with magnitudes of {', '.join(map(str, magnitudes1))}")

    if quake_count2 == 0:
        print(f"Place 2 (Lat: {lat2}, Long: {long2}) had no earthquakes that fit these criteria during the specified time frame.")
    elif quake_count2 == 1:
        print(f"Place 2 (Lat: {lat2}, Long: {long2}): 1 earthquake — with a magnitude of {magnitudes2[0]}")
    else:
        print(f"Place 2 (Lat: {lat2}, Long: {long2}): {quake_count2} earthquakes — with magnitudes of {', '.join(map(str, magnitudes2))}")

    if quake_count1 > quake_count2:
        print(f"Place 1 was quakier between {start_time} and {finish_time} (i.e., within a {radius_in_km} km distance of each location for a minimum magnitude of {min_mag})!")
    elif quake_count2 > quake_count1:
        print(f"Place 2 was quakier between {start_time} and {finish_time} (i.e., within a {radius_in_km} km distance of each location for a minimum magnitude of {min_mag})!")
    else:
        print("Both places have the same quakiness.")

def main():
    print("Earthquake Count Analysis:")
    result = Quake_loop()

    print("\nReflection:")
    print("As the minimum magnitude threshold increases, the number of recorded earthquakes generally decreases. This is expected, as fewer earthquakes of higher magnitudes occur compared to those of lower magnitudes.")

    print("\nEarthquake Comparison Analysis:")
    place1 = (34.0967, -117.7198)  # Claremont, CA
    place2 = (37.7749, -122.4194)  # San Francisco, CA
    Quake_compare(place1, place2)

if __name__ == "__main__":
    main()