import json, requests, os
FILE_PATH = os.path.dirname(os.path.abspath(__file__))
ENDPOINT = 'https://swapi.co/api'

PEOPLE_KEYS = ('url', 'name', 'height', 'mass', 'hair_color', 'skin_color', 'eye_color', 'birth_year', 'gender', 'homeworld', 'species')
PLANET_KEYS = ('url', 'name', 'rotation_period', 'orbital_period', 'diameter', 'climate', 'gravity', 'terrain', 'surface_water', 'population')
STARSHIP_KEYS = ('url', 'starship_class', 'name', 'model', 'manufacturer', 'length', 'width', 'max_atmosphering_speed', 'hyperdrive_rating', 'MGLT', 'crew', 'passengers', 'cargo_capacity', 'consumables', 'armament')
SPECIES_KEYS = ('url', 'name', 'classification', 'designation', 'average_height', 'skin_colors', 'hair_colors', 'eye_colors', 'average_lifespan', 'language')
VEHICLE_KEYS = ('url', 'vehicle_class', 'name', 'model', 'manufacturer', 'length', 'max_atmosphering_speed', 'crew', 'passengers', 'cargo_capacity', 'consumables', 'armament')
PLANET_HOTH_KEYS = ('url', 'name', 'system_position', 'natural_satellites', 'rotation_period', 'orbital_period', 'diameter', 'climate', 'gravity', 'terrain', 'surface_water', 'population', 'indigenous_life_forms')

def assign_crew(entity, crew):
    """Function assigns crew members to a starship

    Parameters:
    entity (dict): starship dictionary
    crew (dict): crew dictionary 

    Returns:
    entity (updated_dict)
    """
    entity.update(crew)
    return entity


def clean_data(entity):
    """Function converts dictionary string values to more appropriate types such as float,
    int, list, or, None. 

    Parameters:
    entity (dict): a dictionary

    Returns:
    float, int, list, or None
    """
    float_props = ('gravity', 'length', 'width', 'hyperdrive_rating')
    int_props = ('system_position', 'natural_satellites', 'rotation_period', 'orbital_period', 'diameter', 'surface_water', 'population', 'height', 'mass', 'average_height', 'average_lifespan', 'max_atmosphering_speed', 'MGLT', 'crew', 'passengers', 'cargo_capacity')
    list_props = ('climate', 'terrain', 'indigenous_life_forms', 'hair_color', 'hair_colors', 'skin_color', 'skin_colors', 'eye_colors', 'armament')
    dict_props = ('homeworld', 'species')
    cleaned = {}
    for key, value in entity.items():
        if key in PLANET_HOTH_KEYS or key in PEOPLE_KEYS or key in SPECIES_KEYS or key in VEHICLE_KEYS or key in STARSHIP_KEYS:
            if is_unknown(value) == True:
                cleaned[key] = None
            elif key in int_props:
                cleaned[key] = convert_string_to_int(value)
            elif key in float_props:
                cleaned[key] = convert_string_to_float(value)
            elif key in list_props:
                cleaned[key] = convert_string_to_list(value)
            elif key in dict_props:
                if key == 'homeworld':
                    homeworld_url = get_swapi_resource(value)
                    homeworld = filter_data(homeworld_url, PLANET_KEYS)
                    homeworld = clean_data(homeworld)
                    cleaned[key] = homeworld
                if key == 'species':
                    species_url = get_swapi_resource(value[0])
                    species_1 = filter_data(species_url, SPECIES_KEYS)
                    #print(species_1)
                    species_1 = clean_data(species_1)
                    species = []
                    species.append(species_1)
                    #print(species)
                    cleaned[key] = (species)
            else:
                cleaned[key] = value
    return cleaned
        
            




def combine_data(default_data, override_data):
    """Creates a shallow copy of the default dictionary and then updates the new
    copy with override data. Override values will replace default values when if
    the keys match.

    Parameters:
        default_data (dict): entity data that provides the default representation of the object.
        override_data (dict): entity data intended to override matching default values.

    Returns:
        dict: updated dictionary that contains override values.

    """

    combined_data = default_data.copy()  
    combined_data.update(override_data)  

    return combined_data



def convert_string_to_float(value):
    """This function converts a string to a float, otherwise returns the string

    Parameters:
    value (str): a string

    Returns:
    float: float conversion of string 
    or 
    value (str)"""

    try:
       new_value = value.split(' ')
       for item in new_value:
           try:
               return float(item)
           except ValueError:
               return value 
       

    except ValueError:
        return value 
    except AttributeError:
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
    try:
        converted_list = []
        value = value.split(delimiter)
        for item in value:
            converted_list.append(item.strip())
        return converted_list
    except AttributeError:
        return value


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
    """Issues an HTTP GET request to return a representation of a
    resource. An optional query string of key:value pairs may be
    provided as search terms. If a match is achieved the JSON object that
    is returned will include a list property named 'results' that
    contains the resource(s) matched by the search query.

    Parameters:
        url (str): a url that specifies the resource.
        params (dict): optional dictionary of query string args.

    Returns:
        dict: dictionary representation of the decoded JSON.
    """
    if params:
        response = requests.get(url, params=params).json()
    else:
        response = requests.get(url).json()
    return response


def is_unknown(value):
    """Given a string (value), this function applies a case-insensitive truth value test for
    string values that equal 'unknown' or 'n/a'

    Parameters: 
    value (str): the value in a key, value set

    Returns:
    True or False (Boolean) 
    """
    #if 'unknown' in value.lower() or 'n/a' in value.lower():
    try:
        if value.lower().strip() == 'unknown' or value.lower().strip() == 'n/a':
            return True
        else:
            return False 
    except AttributeError:
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
    """Entry point to program. Performs the following operations:

    1. Reads swapi_planets-v1p0.json file, filters uninhabited planets, cleans data,
    and writes into a new json file
    2. Request additional info about Hoth, garrison commander, vehicles, starships from swapi.
    3. Combine default data with swapi data; override default values with swapi data (match on key).
    4. Filter traveler, planet, and vehicle entity data, removing unnecessary key-value pairs
    5. Create new dictionaries for evacuation plan (numbers, transports, crew), filter key-value pairs, clean data
    6. Write updated echo_base dict to the file system as a JSON document.

    Parameters:
        None

    Returns:
        None
    """

    uninhabited_planet_data = []
    #filepath = os.path.join(FILE_PATH, 'swapi_planets-v1p0.json')
    filepath = 'swapi_planets-v1p0.json'
    planets = read_json(filepath)
    for planet in planets: 
        for key, value in planet.items():
            if key == 'population':
                if is_unknown(value) == True:
                    filter_data(planet, PLANET_KEYS)
                    planet = clean_data(planet)
                    uninhabited_planet_data.append(planet)
    write_json('swapi_planets_uninhabited-v1p1.json', uninhabited_planet_data)

    #filepath2 = os.path.join(FILE_PATH, 'swapi_echo_base-v1p0.json')
    echo_base = read_json('swapi_echo_base-v1p0.json')
    swapi_hoth_url = f"{ENDPOINT}/planets/4/"
    swapi_hoth = get_swapi_resource(swapi_hoth_url)
    echo_base_hoth = echo_base['location']['planet']
    hoth = combine_data(swapi_hoth, echo_base_hoth)
    hoth = filter_data(hoth, PLANET_HOTH_KEYS)
    hoth = clean_data(hoth)
    echo_base['location']['planet'] = hoth

    echo_base_commander = echo_base['garrison']['commander']
    #print(echo_base_commander)
    echo_base_commander = clean_data(echo_base_commander)
    #print(echo_base_commander)
    echo_base['garrison']['commander'] = echo_base_commander
  

    visiting_starship_pilot = echo_base['visiting_starships']['freighters'][1]['pilot']
    visiting_starship_pilot = clean_data(visiting_starship_pilot)
    echo_base['visiting_starships']['freighters'][1]['pilot'] = visiting_starship_pilot
    
    swapi_vehicles_url = f"{ENDPOINT}/vehicles/"
    swapi_snowspeeder = get_swapi_resource(swapi_vehicles_url, {'search': 'snowspeeder'})['results'][0]
    #print(swapi_snowspeeder)
    echo_base_snowspeeder = echo_base['vehicle_assets']['snowspeeders'][0]['type']
    #print(echo_base_snowspeeder)
    snowspeeder = combine_data(echo_base_snowspeeder, swapi_snowspeeder)
    #print(snowspeeder)
    snowspeeder = filter_data(snowspeeder, VEHICLE_KEYS)
    #print(snowspeeder)
    snowspeeder = clean_data(snowspeeder)
    #print(snowspeeder)
    echo_base['vehicle_assets']['snowspeeders'][0]['type'] = snowspeeder

    
    swapi_starships_url = f"{ENDPOINT}/starships/"
    swapi_xwing = get_swapi_resource(swapi_starships_url, {'search': 'T-65 X-Wing'})['results'][0]
    echo_base_xwing = echo_base['starship_assets']['starfighters'][0]['type']
    xwing = combine_data(echo_base_xwing, swapi_xwing)
    xwing = filter_data(xwing, STARSHIP_KEYS)
    xwing = clean_data(xwing)
    echo_base['starship_assets']['starfighters'][0]['type'] = xwing

    #print(swapi_xwing)
    #print(echo_base_xwing)
    #print(xwing)
    swapi_gr = get_swapi_resource(swapi_starships_url, {'search': 'GR-75 medium transport'})['results'][0]
    echo_base_gr = echo_base['starship_assets']['transports'][0]['type']
    gr = combine_data(echo_base_gr, swapi_gr)
    gr = filter_data(gr, STARSHIP_KEYS)
    gr = clean_data(gr)
    echo_base['starship_assets']['transports'][0]['type'] = gr
    write_json('swapi_echo_base-v1p1.json', echo_base)

    swapi_falcon = get_swapi_resource(swapi_starships_url, {'search': 'Millennium Falcon'})['results'][0]
    echo_base_falcon = echo_base['visiting_starships']['freighters'][0]
    falcon = combine_data(echo_base_falcon, swapi_falcon)
    #print(falcon)
    falcon = filter_data(falcon, STARSHIP_KEYS)
    #print(falcon)
    falcon = clean_data(falcon)
    #print(falcon)
    echo_base['visiting_starships']['freighters'][0] = falcon


    swapi_people_url = f"{ENDPOINT}/people/"
    han = get_swapi_resource(swapi_people_url, {'search': 'han solo'})['results'][0]
    han = filter_data(han, PEOPLE_KEYS)
    han = clean_data(han)
    #print(han)
    swapi_people_url = f"{ENDPOINT}/people/"
    chewie = get_swapi_resource(swapi_people_url, {'search': 'chewbacca'})['results'][0]
    chewie = filter_data(chewie, PEOPLE_KEYS)
    chewie = clean_data(chewie)
    #print(chewie)
    falcon = assign_crew(falcon, {'pilot': han, 'copilot': chewie})
    #print(falcon)
    echo_base['visiting_starships']['freighters'][0] = falcon 


    evac_plan = echo_base['evacuation_plan']
    max_base_personnel = 0
    for key, value in echo_base['garrison']['personnel'].items():
        max_base_personnel += value
    #print(max_base_personnel)
    evac_plan['max_base_personnel'] = max_base_personnel
    max_available_transports = echo_base['starship_assets']['transports'][0]['num_available']
    evac_plan['max_available_transports'] = max_available_transports
    passenger_overload_multiplier = echo_base['starship_assets']['transports'][0]['type']['passengers'] * 3
    max_passenger_overload_capacity = max_available_transports * passenger_overload_multiplier
    evac_plan['max_passenger_overload_capacity'] = max_passenger_overload_capacity
    echo_base['evacuation_plan'] = evac_plan

    
    evac_transport = gr.copy()
    evac_transport['name'] = 'Bright Hope'
    evac_transport['passenger_manifest'] = []
    leia = get_swapi_resource(swapi_people_url, {'search': 'leia organa'})['results'][0]
    leia = filter_data(leia, PEOPLE_KEYS)
    leia = clean_data(leia)

    C3PO = get_swapi_resource(swapi_people_url, {'search': 'C-3PO'})['results'][0]
    C3PO = filter_data(C3PO, PEOPLE_KEYS)
    C3PO = clean_data(C3PO)
    #print(C3PO)
    evac_transport['passenger_manifest'].append(leia)
    evac_transport['passenger_manifest'].append(C3PO)

    evac_transport['escorts'] =[]
    luke_x_wing = xwing.copy()
    wedge_x_wing = xwing.copy()
    luke = get_swapi_resource(swapi_people_url, {'search': 'luke skywalker'})['results'][0]
    luke = filter_data(luke, PEOPLE_KEYS)
    luke = clean_data(luke)
    #print(luke)
    R2D2 = get_swapi_resource(swapi_people_url, {'search': 'R2-D2'})['results'][0]
    R2D2 = filter_data(R2D2, PEOPLE_KEYS)
    R2D2 = clean_data(R2D2)
    luke_x_wing = assign_crew(luke_x_wing, {'pilot' : luke, 'astromech_droid': R2D2})
    evac_transport['escorts'].append(luke_x_wing)

    wedge = get_swapi_resource(swapi_people_url, {'search': 'wedge antilles'})['results'][0]
    wedge = filter_data(wedge, PEOPLE_KEYS)
    wedge = clean_data(wedge)
    R5D4 = get_swapi_resource(swapi_people_url, {'search': 'R5-D4'})['results'][0]
    R5D4 = filter_data(R5D4, PEOPLE_KEYS)
    R5D4 = clean_data(R5D4)
    wedge_x_wing = assign_crew(wedge_x_wing, {'pilot': wedge, 'astromech_droid': R5D4})
    evac_transport['escorts'].append(wedge_x_wing)
    evac_plan['transport_assignments'].append(evac_transport)
    echo_base['evacuation_plan'] = evac_plan
    write_json('swapi_echo_base-v1p1.json', echo_base)   
if __name__ == '__main__':
    main()
