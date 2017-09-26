import json
import os
def load_data():
    dirname = os.path.dirname(__file__)
    with open(os.path.join(dirname, 'data.json')) as fp:
        data = json.load(fp)

    area_list = [[area['AreaName'] for area in city['AreaList']] for city in data]
    city_list = [city['CityName'] for city in data]

    return city_list, area_list


CITY_LIST, AREA_LIST = load_data()

def split_address(address):
    target = {}

    for ix, city in enumerate(CITY_LIST):
        if city in address:
            target['city'] = city
            address.replace(city, '')
            for area in AREA_LIST[ix]:
                if area in address:
                    target['area'] = area
                    address.replace(area, '')
                    break

    target['road'] = address

    return target

