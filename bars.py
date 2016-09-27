import sys
import json
import math


def load_bars_data(filepath):
    with open(filepath, 'r', encoding="utf8") as input_file:
        data = json.load(input_file)
    return data


def get_biggest_bar(data):
    max_num_of_seats = data[0]['Cells']['SeatsCount']
    biggest_bar = data[0]['Cells']['Name']

    for bar in data:
        if bar['Cells']['SeatsCount'] > max_num_of_seats:
            max_num_of_seats = bar['Cells']['SeatsCount']
            biggest_bar = bar['Cells']['Name']

    return (biggest_bar, max_num_of_seats)


def get_smallest_bar(data):
    min_num_of_seats = data[0]['Cells']['SeatsCount']
    smallest_bar = data[0]['Cells']['Name']

    for bar in data:
        if bar['Cells']['SeatsCount'] < min_num_of_seats:
            min_num_of_seats = bar['Cells']['SeatsCount']
            smallest_bar = bar['Cells']['Name']

    return (smallest_bar, min_num_of_seats)


def distance(current_longitude, current_latitude, bar_longitude, bar_latitude):
    current_latitude = current_latitude * math.pi / 180.
    bar_latitude = bar_latitude * math.pi / 180.
    current_longitude = current_longitude * math.pi / 180.
    bar_longitude = bar_longitude * math.pi / 180.

    cosl1 = math.cos(current_latitude)
    cosl2 = math.cos(bar_latitude)
    sinl1 = math.sin(current_latitude)
    sinl2 = math.sin(bar_latitude)
    longitude_delta = bar_longitude - current_longitude
    cos_delta = math.cos(longitude_delta)
    sin_delta = math.sin(longitude_delta)

    numerator = math.sqrt(math.pow(cosl2 * sin_delta, 2) + math.pow(cosl1 * sinl2 - sinl1 * cosl2 * cos_delta, 2))
    denominator = sinl1 * sinl2 + cosl1 * cosl2 * cos_delta
    angular_disparity = math.atan2(numerator, denominator)
    earth_radius = 6372795
    distance = angular_disparity * earth_radius
    return distance


def get_closest_bar(data, longitude, latitude):
    bar_longitude, bar_latitude = data[0]['Cells']['geoData']['coordinates']
    min_distance = distance(longitude, latitude, bar_longitude, bar_latitude)
    closest_bar = data[0]['Cells']['Name']
    for bar in data:
        bar_longitude, bar_latitude = bar['Cells']['geoData']['coordinates']
        dist_to_bar = distance(longitude, latitude, bar_longitude, bar_latitude)
        if dist_to_bar < min_distance:
            min_distance = dist_to_bar
            closest_bar = bar['Cells']['Name']
    return (closest_bar, round(min_distance))


if __name__ == '__main__':
    filepath = sys.argv[1]
    bars_info = load_bars_data(filepath)
    biggest_bar = get_biggest_bar(bars_info)
    smallest_bar = get_smallest_bar(bars_info)
    print("The biggest bar is %s: %d seats." % biggest_bar)
    print("The smallest bar is %s: %d seats." % smallest_bar)

    current_longitude = float(input('Enter current longitude:\n'))
    current_latitude = float(input('Enter current latitude:\n'))
    closest_bar = get_closest_bar(bars_info, current_longitude, current_latitude)
    print("The closest bar is %s: %d metres." % closest_bar)
