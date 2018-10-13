import json

from geopy.geocoders import Nominatim
import geopy.distance


def adress_to_coordinates(adress: str):
    geolocator = Nominatim(user_agent="tanieChlanie")
    location = geolocator.geocode(adress)
    cords = json.dumps((location.latitude, location.longitude))
    return cords


def calculate_distance(coordinates1, coordinates2):
    coordinates1 = tuple(json.loads(coordinates1))
    coordinates2 = tuple(json.loads(coordinates2))
    return geopy.distance.vincenty(coordinates1, coordinates2).km
