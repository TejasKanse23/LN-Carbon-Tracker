from geopy.geocoders import Nominatim
from geopy.distance import geodesic

geolocator = Nominatim(user_agent="carbon_tracker")


def get_route(origin, destination):

    loc1 = geolocator.geocode(origin)
    loc2 = geolocator.geocode(destination)

    coord1 = (loc1.latitude, loc1.longitude)
    coord2 = (loc2.latitude, loc2.longitude)

    distance = geodesic(coord1, coord2).km

    avg_speed = 50

    duration = distance / avg_speed

    return {
        "distance_km": distance,
        "duration_hrs": duration
    }