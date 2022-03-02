import requests

# Own Functions
from functions import *

API_KEY = getAPIkey()
BASE_URL = "https://api.checkwx.com/"

# LOCATION WHERE STATION HISTORY SHOULD BE SAVED
SAVED_STATIONS = "station_history.json"
# LOAD SAVED STATIONS FROM JSON FILE AND PRINT TO CONSOLE IF THEY EXIST
stations = load_stations(SAVED_STATIONS)
if len(stations) > 0:
    print("Saved Stations:\nICAO  :  Station Name")
    for key, value in stations.items():
        print(key, " : ", value)
    print()

# GET AERODROME IDENTIFIER FROM USER
ICAO = input("Input ICAO: ").upper()

# GET AIRFIELD INFORMATION AND PRINT TO CONSOLE
inf_req = get_information(BASE_URL,API_KEY,ICAO)
try:
    inf_req.raise_for_status()
    info = inf_req.json()
    print_information(info)
    stations[ICAO] = name
    save_stations(SAVED_STATIONS, stations)
except requests.exceptions.HTTPError as e:
    print(e)

# GET METAR AND PRINT TO CONSOLE 
met_req = get_metar(BASE_URL,API_KEY,ICAO)
try:
    met_req.raise_for_status()
    met_response = met_req.json()
    if len(met_response["data"]) == 1:
        metar = met_response["data"][0]
        print_metar(metar)
    else:
        dtnow = datform()
        print(f"\nNo METAR data found: {dtnow}\n")
except requests.exceptions.HTTPError as e:
    print(e)

print("\n")
x = None
while x == None:
    x = input("Press Enter to exit: ")