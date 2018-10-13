import json

from geopy.geocoders import Nominatim
from geopy.distance import great_circle


def adress_to_coordinates(adress: str):
    geolocator = Nominatim(user_agent="tanieChlanie")
    location = geolocator.geocode(adress)
    cords = json.dumps((location.latitude, location.longitude))
    return tuple(cords)


<<<<<<< HEAD
def calculate_distance_in_km(coordinates1: tuple, coordinates2: tuple):
    return geopy.distance.vincenty(coordinates1, coordinates2).km
=======
def calculate_distance(coordinates1, coordinates2):
    print(coordinates1)
    print(coordinates2)
    coordinates1 = tuple(json.loads(coordinates1))
    coordinates2 = tuple(json.loads(coordinates2))
    return great_circle(coordinates1, coordinates2).km
>>>>>>> 1872a9e86460cc7aceb6498b111bed01853104c7
