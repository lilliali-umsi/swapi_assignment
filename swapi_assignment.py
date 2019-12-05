import json, requests, os
FILE_PATH = os.path.dirname(os.path.abspath(__file__))
ENDPOINT = 'https://swapi.co/api'

PEOPLE_KEYS = ('url', 'name', 'height', 'mass', 'hair_color', 'skin_color', 'eye_color', 'birth_year', 'gender', 'homeworld', 'species')
PLANET_KEYS = ('url', 'name', 'rotation_period', 'orbital_period', 'diameter', 'climate', 'gravity', 'terrain', 'surface_water', 'population')
STARSHIP_KEYS = ('url', 'starship_class', 'name', 'model', 'manufacturer', 'length', 'width', 'max_atmosphering_speed', 'hyperdrive_rating', 'MGLT', 'crew', 'passengers', 'cargo_capacity', 'consumables', 'armament')
SPECIES_KEYS = ('url', 'name', 'classification', 'designation', 'average_height', 'skin_colors', 'hair_colors', 'eye_colors', 'average_lifespan', 'language')
VEHICLE_KEYS = ('url', 'vehicle_class', 'name', 'model', 'manufacturer', 'length', 'max_atmosphering_speed', 'crew', 'passengers', 'cargo_capacity', 'consumables', 'armament')

def assign_crew(entity, crew):
    pass


def clean_data(entity):
    """Function converts dictionary string values to more appropriate types such as float,
    int, list, or, None. 

    Parameters:
    entity (dict): a dictionary

    Returns:
    float, int, list, or None
    """
    float_props = ('gravity', 'length', 'width', 'hyperdrive_rating')
    int_props = ('rotation_period', 'orbital_period', 'diameter', 'surface_water', 'population', 'height', 'mass', 'average_height', 'average_lifespan', 'max_atmosphering_speed', 'MGLT', 'crew', 'passengers', 'cargo_capacity')
    list_props = ('climate', 'terrain', 'hair_color', 'skin_color', 'eye_colors')
    dict_props = ('homeworld', 'species')
    cleaned = {}
    for key, value in entity.items():
        if key in PLANET_KEYS:
            if is_unknown(value) == True:
                cleaned[key] = None
            elif key in int_props:
                cleaned[key] = convert_string_to_int(value)
            elif key in float_props:
                cleaned[key] = convert_string_to_float(value)
            elif key in list_props:
                cleaned[key] = convert_string_to_list(value)
            else:
                cleaned[key] = value
    return cleaned
        
            




def combine_data(default_data, override_data):
    pass


def convert_string_to_float(value):
    """This function converts a string to a float, otherwise returns the string

    Parameters:
    value (str): a string

    Returns:
    float: float conversion of string 
    or 
    value (str)"""

    try:
        return float(value)
    except ValueError:
        return value 


def convert_string_to_int(value):
    """This function converts a string to an integer, otherwise returns the string

    Parameters:
    value (str): a string

    Returns:
    integer: integer conversion of string 
    or 
    value (str)"""
    try:
       return int(value)
    except ValueError:
        return value 


def convert_string_to_list(value, delimiter=','):
    """This function converts a string to a list

    Parameters:
    value (str): a string

    Returns:
    list: a list version of the string split by the delimiter"""

    return value.strip().split(delimiter)


def filter_data(data, filter_keys):
    """Returns a new dictionary based containing a filtered subset of key-value pairs
    sourced from a dictionary provided by the caller.

    Parameters:
        data (dict): source entity.
        filter_keys (tuple): sequence of keys used to select a subset of key-value pairs.

    Returns:
        dict: a new entity containing a subset of the source entity's key-value pairs.

    """
    record = {}
    for item in filter_keys:
        if item in data.keys():
            record[item] = data[item]
    return record 


def get_swapi_resource(url, params=None):
    pass


def is_unknown(value):
    """Given a string (value), this function applies a case-insensitive truth value test for
    string values that equal 'unknown' or 'n/a'

    Parameters: 
    value (str): the value in a key, value set

    Returns:
    True or False (Boolean) 
    """
    #if 'unknown' in value.lower() or 'n/a' in value.lower():
    if value.lower().strip() == 'unknown' or value.lower().strip() == 'n/a':
        return True
    else:
        return False 


def read_json(filepath):
    """Given a valid filepath, reads a JSON document and returns a dictionary.

    Parameters:
        filepath (str): path to file.

    Returns:
        dict: decoded JSON document expressed as a dictionary.
    """

    with open(filepath, 'r', encoding='utf-8') as file_obj:
        data = json.load(file_obj)

    return data


def write_json(filepath, data):
    """Given a valid filepath, write data to a JSON file.

    Parameters:
        filepath (str): the path to the file.
        data (dict): the data to be encoded as JSON and written to the file.

    Returns:
        None
    """

    with open(filepath, 'w', encoding='utf-8') as file_obj:
        json.dump(data, file_obj, ensure_ascii=False, indent=2)


def main():
    """a function that I will fill in soon
    Parameters: None
    Returns: None"""
    
    uninhabited_planet_data = []
    filepath = os.path.join(FILE_PATH, 'swapi_planets-v1p0.json')
    planets = read_json(filepath)
    for planet in planets: 
        for key, value in planet.items():
            if key == 'population':
                if is_unknown(value) == True:
                    filter_data(planet, PLANET_KEYS)
                    planet = clean_data(planet)
                    uninhabited_planet_data.append(planet)
    write_json('swapi_planets_uninhabited-v1p1.json', uninhabited_planet_data)
    


if __name__ == '__main__':
    main()
