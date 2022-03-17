from flask import Flask
import xmltodict as xd
import json
import logging

app = Flask(__name__)

iss_epoch_data = {}
iss_sighting_data = {}

@app.route('/read_data', methods=['POST'])
def read_data_from_file_into_dict():
    """
    This route reads two XML data files and returns a statement that confirms that the data from both files have been read.
    """
    logging.info("Data is being read.")
    global iss_epoch_data
    global iss_sighting_data

    with open('ISS.OEM_J2K_EPH.xml' , 'r') as f:
        iss_epoch_data =  xd.parse(f.read())

    with open('XMLsightingData_citiesUSA07.xml' , 'r') as f:
        iss_sighting_data = xd.parse(f.read())

    return f'Data has been read from file\n'


@app.route('/help', methods=['GET'])
def help():
    """
    Outputs information on each route including the results from each
    """
    logging.info("Information on each route is being outputted on the screen for your reference.")
    describe = "ISS Sighting Location\n"
    describe += "/                                                      (GET) print this information\n"
    describe += "/read_data                                             (POST) reset data, load from file\n"
    describe += "Routes for Querying Positional and Velocity Data:\n\n"
    describe += "/epochs                                                (GET) lists all epochs in positional and velocity data\n"
    describe += "/epochs/<epoch>                                        (GET) lists all data associated with a specific epoch\n"
    describe += "Routes for Querying Sighting Data\n\n"
    describe += "/countries                                             (GET) lists all countries in sighting data\n"
    describe += "/countries/<country>                                   (GET) lists all data for a specific country\n"
    describe += "/countries/<country>/regions                           (GET) lists all regions in a specific country\n"
    describe += "/countries/<country>/regions/<regions>                 (GET) lists all data for a specific region\n"
    describe += "/countries/<country>/regions/<regions>/cities          (GET) lists all cities in a specific region\n"
    describe += "/countries/<country>/regions/<regions>/cities/<city>   (GET) lists all data for a specific city \n"
    return describe


# RETURNS ALL OF THE EPOCHS IN THE POSITIONAL DATA
@app.route('/EPOCH', methods=['GET'])
def get_all_epochs():
    """
    Iterates through a list of EPOCH dictionaries

    Returns:
    All of the EPOCHS in the positional data
    """
    logging.info("Querying route to obtain all EPOCHS...")
    EPOCH = ""
    for i in range(len(iss_epoch_data['ndm']['oem']['body']['segment']['data']['stateVector'])):
        EPOCH = EPOCH + iss_epoch_data['ndm']['oem']['body']['segment']['data']['stateVector'][i]['EPOCH'] + '\n'
    return EPOCH

# RETURNS ALL INFORMATION ABOUT A SPECIFIC EPOCH IN THE POSITIONAL DATA
@app.route('/<epoch>', methods=['GET'])
def get_epoch_data(epoch: str):
    """
    Iterates through all of the state vectors in the ISS EPOCH DATA dictionary. Once it finds the specific <epoch> value entered by the user, another iteration is carried to acquire all of the positional and velocity data information.

    Args:
    epoch (str): A string containing the specific EPOCH value

    Returns:
    epoch_dict (dictionary): All information about a specific EPOCH in the positional and velocity data.
    """
    logging.info("Querying route to obtain all information about EPOCH:/"+epoch) 
    for i in range(len(iss_epoch_data['ndm']['oem']['body']['segment']['data']['stateVector'])):
        if epoch == iss_epoch_data['ndm']['oem']['body']['segment']['data']['stateVector'][i]['EPOCH']:
            epoch_num = i
            break
    pos_vel_data = ['X', 'Y', 'Z', 'X_DOT', 'Y_DOT', 'Z_DOT']
    epoch_dict = {}
    for vals in pos_vel_data:
        epoch_dict[vals] = iss_epoch_data['ndm']['oem']['body']['segment']['data']['stateVector'][epoch_num][vals]
    return epoch_dict

# ALL COUNTRIES AND INFO FOR A SPECIFIC COUNTRY
@app.route('/countries',methods=['GET'])
def get_all_countries():
    """
    Iterates through all of the visible passes in the ISS Sighting Data Dictionary and obtains the 'country' key in each.

    Returns:
    COUNTRIES (dictionary): All of the countries in the Sighting Data 
    """
    logging.info("Querying route to obtain all countries...")
    COUNTRIES = {}
    for i in range(len(iss_sighting_data['visible_passes']['visible_pass'])):
        specific_country = iss_sighting_data['visible_passes']['visible_pass'][i]['country']
        if specific_country in COUNTRIES:
            COUNTRIES[specific_country] += 1
        else:
            COUNTRIES[specific_country] = 1
    return COUNTRIES
@app.route('/COUNTRY/<country>', methods=['GET'])
def get_country_data(country):
    """
    Iterates through all visible passes in the ISS Sighting Data dictionary and obtains the information for each value associated with the 'country' key supplied by the user.

    Args:
    country (str): A string countaining the specific country to acquire the data for.

    Returns:
    list_dicts (list): All information about a specific country
    """
    logging.info("Querying route to obtain all info on /"+country)
    list_dicts = []
    list_country_data = ['region', 'city', 'spacecraft', 'sighting_date','duration_minutes','max_elevation','enters','exits','utc_offset','utc_time', 'utc_date']
    for i in range(len(iss_sighting_data['visible_passes']['visible_pass'])):
        specific_country = iss_sighting_data['visible_passes']['visible_pass'][i]['country']
        if country == specific_country:
            country_dict = {}
            for j in list_country_data:
                country_dict[j] = iss_sighting_data['visible_passes']['visible_pass'][i][j]
            list_dicts.append(country_dict)
    return json.dumps(list_dicts, indent=2)

# ALL OF THE REGIONS AND INFO FOR A SPECIFIC COUNTRY
@app.route('/COUNTRY/<country>/regions',methods=['GET'])
def get_all_regions(country):
    """
    Iterates through all visible pases in the ISS Sighting Data Dictionary that includes the user input <country> and pulls all of the values tied to the 'region' key. It then stores each unique region as a key in a new dictionary called REGIONS.

    Args:
    country (str): A string containing the specific country to find the regions for.

    Returns:
    REGIONS (dictionary): dictionary containing all of the regions in a specific country
    """
    logging.info("Querying route to obtain list of all regions in /"+country)
    REGIONS = {}
    for i in range(len(iss_sighting_data['visible_passes']['visible_pass'])):
        specific_country = iss_sighting_data['visible_passes']['visible_pass'][i]['country']
        if country == specific_country:
            specific_region = iss_sighting_data['visible_passes']['visible_pass'][i]['region']
            if specific_region in REGIONS:
                REGIONS[specific_region] += 1
            else:
                REGIONS[specific_region] = 1
    return REGIONS
@app.route('/COUNTRY/<country>/regions/<regions>',methods=['GET'])
def get_region_data(country, regions):
    """
    Iterates through all of the visible passes in the ISS SIGHTING DATA Dictionary that includes the user input <country> and the user input <regions>. It obtains each piece of information associated with that region from the data dictionary.

    Args:
    country (str): A user input string that contains the country
    regions (str): A user input string that contains the region in the specific country

    Returns: list_dicts (list): contains all the information about a specific region
    """
    logging.info("Querying route to obtain all info about /"+regions)
    list_dicts = []
    list_region_data = ['city', 'spacecraft', 'sighting_date','duration_minutes','max_elevation','enters',\
'exits','utc_offset','utc_time', 'utc_date']
    for i in range(len(iss_sighting_data['visible_passes']['visible_pass'])):
        specific_country = iss_sighting_data['visible_passes']['visible_pass'][i]['country']
        if country == specific_country:
            specific_region = iss_sighting_data['visible_passes']['visible_pass'][i]['region']
            if regions == specific_region:
                region_dict = {}
                for j in list_region_data:
                    region_dict[j] = iss_sighting_data['visible_passes']['visible_pass'][i][j]
                list_dicts.append(region_dict)
    return json.dumps(list_dicts, indent=2)

# ALL OF THE CITY AND INFO FOR A SPECIFIC CITY
@app.route('/COUNTRY/<country>/regions/<regions>/cities',methods=['GET'])
def get_all_cities(country, regions):
    """
    Iterates through all visible passes in the ISS Sighting Data Dictionary that includes BOTH the user input <country> and <region> and puts all values associated with the 'city' key into a new dictionary called CITIES.

    Args:
    country (str): A user input string that contains the country
    regions (str): A user input string that contains the region in the specific\
 country

    Returns:
    CITIES (dictionary): A dictionary that contains all of the cities in a specific region in a specific country.
    """
    logging.info("Querying route to obtain all cities in /"+regions)
    CITIES = {}
    for i in range(len(iss_sighting_data['visible_passes']['visible_pass'])):
        specific_country = iss_sighting_data['visible_passes']['visible_pass'][i]['country']
        if country == specific_country:
            specific_region = iss_sighting_data['visible_passes']['visible_pass'][i]['region']
            if regions == specific_region:
                specific_cities = iss_sighting_data['visible_passes']['visible_pass'][i]['city']
                if specific_cities in CITIES:
                    CITIES[specific_cities] +=1
                else:
                    CITIES[specific_cities]=1
    return CITIES
@app.route('/COUNTRY/<country>/regions/<regions>/cities/<cities>',methods=['GET'])
def get_city_data(country, regions, cities):
    """
    Iterates through all visible passes in the ISS Sighting Data Dictionary that includes the user input <country>, <region>, and <city>. Stores the values associated with the 'city' key into a brand new list.

    Args:
    country (str): user input string that contains the specific country
    regions (str): user input string that contains the specific regions
    cities (str): user input string that contains the specific city

    Returns:
    list_dicts (list): All of the information that pertains to a specific city
    """
    logging.info("Querying route to obtain info about /"+cities)
    list_dicts = []
    list_city_data = ['spacecraft', 'sighting_date','duration_minutes','max_elevation','enters',\
'exits','utc_offset','utc_time', 'utc_date']
    for i in range(len(iss_sighting_data['visible_passes']['visible_pass'])):
        specific_country = iss_sighting_data['visible_passes']['visible_pass'][i]['country']
        if country == specific_country:
            specific_region = iss_sighting_data['visible_passes']['visible_pass'][i]['region']
            if regions == specific_region:
                specific_city = iss_sighting_data['visible_passes']['visible_pass'][i]['city']
                if cities == specific_city:
                    city_dict = {}
                    for j in list_city_data:
                        city_dict[j] = iss_sighting_data['visible_passes']['visible_pass'][i][j]
                    list_dicts.append(city_dict)
    return json.dumps(list_dicts, indent=2)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
