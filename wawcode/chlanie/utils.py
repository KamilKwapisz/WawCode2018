import json

from geopy.geocoders import Nominatim
from geopy.distance import great_circle


def address_to_coordinates(adress: str):
    geolocator = Nominatim(user_agent="tanieChlanie")
    location = geolocator.geocode(adress)
    cords = json.dumps((location.latitude, location.longitude))
    return cords


def get_places_within_radius(lokale, user_coordinates, radius):
    for lokal in lokale:
        print(lokal.coordinates)
        dist = calculate_distance(lokal.coordinates, user_coordinates)
        if dist > radius:
            lokale = lokale.exclude(id=lokal.pk)
    return lokale


def calculate_distance(coordinates1, coordinates2):
    coordinates1 = tuple(json.loads(coordinates1))
    coordinates2 = tuple(json.loads(coordinates2))
    return great_circle(coordinates1, coordinates2).km
