import sys
import json
import math  # for accurate_distance


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


def get_closest_bar(data, longitude, latitude):
    def distance(current_long, current_lat, bar_long, bar_lat, is_accurate=True):
        """
        simple_distance finds distance between two points in Cartesian coordinates
        it is not very accurate and it cannot give information about actual distance
        but it works properly if you want to find the closest bar in the city ;)

        accurate_distance uses modification of haversine formula witch can give very accurate distance in meters
        You can find more information here:
        http://gis-lab.info/qa/great-circles.html
        """

        def simple_distance(current_long, current_lat, bar_long, bar_lat):
            return ((bar_long - current_long) ** 2 + (bar_lat - current_lat) ** 2) ** 0.5

        def accurate_distance(current_long, current_lat, bar_long, bar_lat):
            earth_rad = 6372795

            lat1 = current_lat * math.pi / 180.
            lat2 = bar_lat * math.pi / 180.
            long1 = current_long * math.pi / 180.
            long2 = bar_long * math.pi / 180.

            # косинусы и синусы широт и разницы долгот
            cl1 = math.cos(lat1)
            cl2 = math.cos(lat2)
            sl1 = math.sin(lat1)
            sl2 = math.sin(lat2)
            delta = long2 - long1
            cdelta = math.cos(delta)
            sdelta = math.sin(delta)

            # вычисления длины большого круга
            y = math.sqrt(math.pow(cl2 * sdelta, 2) + math.pow(cl1 * sl2 - sl1 * cl2 * cdelta, 2))
            x = sl1 * sl2 + cl1 * cl2 * cdelta
            ad = math.atan2(y, x)
            distance = ad * earth_rad
            return distance

        if is_accurate:
            return accurate_distance(current_long, current_lat, bar_long, bar_lat)
        else:
            return simple_distance((current_long, current_lat, bar_long, bar_lat))

    bar_longitude, bar_latitude = data[0]['Cells']['geoData']['coordinates']
    min_distance = distance(longitude, latitude, bar_longitude, bar_latitude)
    closest_bar = data[0]['Cells']['Name']
    for bar in data:
        bar_longitude, bar_latitude = bar['Cells']['geoData']['coordinates']
        dist_to_bar = distance(longitude, latitude, bar_longitude, bar_latitude)
        if dist_to_bar < min_distance:
            min_distance = dist_to_bar
            closest_bar = bar['Cells']['Name']
    return closest_bar


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
