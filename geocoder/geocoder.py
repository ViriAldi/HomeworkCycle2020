from geopy.geocoders import Nominatim


def locate(name):
    geolocator = Nominatim(user_agent=__name__)
    location = geolocator.geocode(name)

    return location.latitude, location.longitude


def decode(coords):
    geolocator = Nominatim(user_agent=__name__)
    country = geolocator.reverse(coords, zoom=5)
    address = geolocator.reverse(coords)

    return country, address

