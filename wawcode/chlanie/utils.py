import json

from geopy.geocoders import Nominatim
import geopy.distance


def adress_to_coordinates(adress: str):
    geolocator = Nominatim(user_agent="tanieChlanie")
    location = geolocator.geocode(adress)
    cords = json.dumps((location.latitude, location.longitude))
    return tuple(cords)


def calculate_distance_in_km(coordinates1: tuple, coordinates2: tuple):
    return geopy.distance.vincenty(coordinates1, coordinates2).km
