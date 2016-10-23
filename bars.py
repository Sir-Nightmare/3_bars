import sys
import json
from math import radians, sin, cos, sqrt, atan2, pow


def load_bars_data(filepath):
    with open(filepath, 'r', encoding="utf8") as input_file:
        data = json.load(input_file)
    return data


def get_biggest_bar(data):
    biggest_bar = max(data, key=lambda i: i['Cells']['SeatsCount'])
    return (biggest_bar['Cells']['Name'], biggest_bar['Cells']['SeatsCount'])


def get_smallest_bar(data):
    smallest_bar = min(data, key=lambda i: i['Cells']['SeatsCount'])
    return (smallest_bar['Cells']['Name'], smallest_bar['Cells']['SeatsCount'])


def distance(current_longitude, current_latitude, bar_longitude, bar_latitude):
    '''
    Parameters: coordinates of the bar in degrees

    :return: distance in metres

    See more info about this function in readme

    '''

    # sin and cos of latitudes
    cosl1 = cos(radians(current_latitude))
    cosl2 = cos(radians(bar_latitude))
    sinl1 = sin(radians(current_latitude))
    sinl2 = sin(radians(bar_latitude))
    # sin and cos of longitude difference
    longitude_delta = radians(bar_longitude - current_longitude)
    cos_delta = cos(longitude_delta)
    sin_delta = sin(longitude_delta)
    # haversine formula
    numerator = sqrt(pow(cosl2 * sin_delta, 2) + pow(cosl1 * sinl2 - sinl1 * cosl2 * cos_delta, 2))
    denominator = sinl1 * sinl2 + cosl1 * cosl2 * cos_delta
    angular_disparity = atan2(numerator, denominator)  # result of haversine formula(angle)

    earth_radius = 6372795  # in metres
    distance = angular_disparity * earth_radius
    return distance


def get_closest_bar(data, longitude, latitude):
    closest_bar = min(data, key=lambda i: distance(
        longitude, latitude,
        i['Cells']['geoData']['coordinates'][0],
        i['Cells']['geoData']['coordinates'][1]))

    distance_to_closest_bar = round(distance(
        longitude, latitude,
        closest_bar['Cells']['geoData']['coordinates'][0],
        closest_bar['Cells']['geoData']['coordinates'][1]))
    return (closest_bar['Cells']['Name'], distance_to_closest_bar)


if __name__ == '__main__':
    filepath = sys.argv[1]

    bars_info = load_bars_data(filepath)
    biggest_bar = get_biggest_bar(bars_info)
    smallest_bar = get_smallest_bar(bars_info)
    print("The biggest bar is %s: %d seats." % biggest_bar)
    print("The smallest bar is %s: %d seats." % smallest_bar)

    current_longitude = float(input('Enter current longitude in decimal degrees (37.617778):\n'))
    current_latitude = float(input('Enter current latitude in decimal degrees (55.755833):\n'))
    closest_bar = get_closest_bar(bars_info, current_longitude, current_latitude)
    print("The closest bar is %s: %d metres." % closest_bar)
