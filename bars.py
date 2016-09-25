import sys
import json
import math


def load_data(filepath):
    data = ""
    with open(filepath, 'r', encoding="utf8") as file:
        data = file.read()
    return json.loads(data)


def get_biggest_bar(data):
    max_num_of_seats = data[0]['Cells']['SeatsCount']
    biggest_bar = data[0]['Cells']['Name']

    for bar in data:
        if bar['Cells']['SeatsCount'] > max_num_of_seats:
            max_num_of_seats = bar['Cells']['SeatsCount']
            biggest_bar = bar['Cells']['Name']

    return [biggest_bar, max_num_of_seats]


def get_smallest_bar(data):
    min_num_of_seats = data[0]['Cells']['SeatsCount']
    smallest_bar = data[0]['Cells']['Name']

    for bar in data:
        if bar['Cells']['SeatsCount'] < min_num_of_seats:
            min_num_of_seats = bar['Cells']['SeatsCount']
            smallest_bar = bar['Cells']['Name']

    return [smallest_bar, min_num_of_seats]


def distance(current_long, current_lat, bar_long, bar_lat):
    earth_radius = 6372795

    current_lat = current_lat * math.pi / 180.
    bar_lat = bar_lat * math.pi / 180.
    current_long = current_long * math.pi / 180.
    bar_long = bar_long * math.pi / 180.

    # косинусы и синусы широт и разницы долгот
    cl1 = math.cos(current_lat)
    cl2 = math.cos(bar_lat)
    sl1 = math.sin(current_lat)
    sl2 = math.sin(bar_lat)
    delta = bar_long - current_long
    cdelta = math.cos(delta)
    sdelta = math.sin(delta)

    # вычисления длины большого круга
    numerator = math.sqrt(math.pow(cl2 * sdelta, 2) + math.pow(cl1 * sl2 - sl1 * cl2 * cdelta, 2))
    denominator = sl1 * sl2 + cl1 * cl2 * cdelta
    angular_disparity = math.atan2(numerator, denominator)
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
    return closest_bar, min_distance


if __name__ == '__main__':
    bars_info = load_data('bar_list.json')
    bb = get_biggest_bar(bars_info)
    sb = get_smallest_bar(bars_info)
    print("The biggest bar is", bb[0] + ':', bb[1], "seats")
    print("The smallest bar is", sb[0] + ':', sb[1], "seats")

    # current_longitude = 37.617778
    # current_latitude = 55.755833
    current_longitude = float(input('Enter current longitude:'))
    current_latitude = float(input('Enter current latitude:'))
    cb = get_closest_bar(bars_info, current_longitude, current_latitude)
    print("The closest bar is", cb)
